import time
import gc

import network
import urequests
from machine import Pin, SPI

import config
from lib.ili9341 import Display, color565

# CYW43 wireless-chip link status codes.
# Source: "Connecting to the Internet with Raspberry Pi Pico W-series"
# (Raspberry Pi Ltd), section 3.6.1.
STATUS_NAMES = {
    0: "down",
    1: "joined, no ip yet",
    2: "joined, waiting for ip",
    3: "connected",
    -1: "failed",
    -2: "no ap found",
    -3: "wrong password",
}

BLACK = color565(0, 0, 0)
NAVY = color565(0, 0, 128)
WHITE = color565(255, 255, 255)
YELLOW = color565(255, 255, 0)
AMBER = color565(255, 180, 0)
RED = color565(255, 60, 60)

POLL_SECONDS = 60
ROW_HEIGHT = 24
MAX_ROWS = 6

# RTT.io access tokens are valid ~20 minutes (see /api/get_access_token).
# The Pico has no synced wall clock to compare against the server's
# validUntil timestamp, so refresh on a conservative relative timer
# instead of an absolute one.
ACCESS_TOKEN_LIFETIME_MS = 15 * 60 * 1000

_access_token = None
_access_token_fetched_at = None


def describe(status):
    return STATUS_NAMES.get(status, str(status))


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print(f"Joining '{config.WIFI_SSID}'...")
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

    max_wait = 10
    while max_wait > 0:
        status = wlan.status()
        if status < 0 or status >= 3:
            break
        max_wait -= 1
        print(f"waiting for connection... ({describe(status)})")
        time.sleep(2)

    if wlan.status() != 3:
        raise RuntimeError(f"network connection failed: {describe(wlan.status())}")

    ip, subnet, gateway, dns = wlan.ifconfig()
    print(f"connected — ip = {ip}")
    return wlan


def reconnect_if_dropped(wlan):
    status = wlan.status()
    if status < 0 or status == 0:
        print(f"link dropped ({describe(status)}) — reconnecting")
        wlan.disconnect()
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)


def hhmm(iso_datetime):
    """RTT.io timestamps are ISO 8601, e.g. "2026-07-02T18:32:00Z".
    MicroPython has no datetime.fromisoformat — slice the substring by hand.
    """
    if not iso_datetime:
        return "--:--"
    return iso_datetime[11:16]


def normalize_service(service):
    """Flatten one RTT.io service — deeply-nested camelCase JSON, straight
    off the wire — into the flat snake_case shape this board renders.

    Source field -> board field, each one a step down the nesting:
      temporalData.departure.scheduleAdvertised -> scheduled
      temporalData.departure.realtimeActual/realtimeForecast -> estimated
      temporalData.departure.isCancelled -> is_cancelled
      locationMetadata.platform.actual/planned -> platform
      destination[].location.description -> destination_name
      scheduleMetadata.operator.name -> operator_name
    """
    departure = service.get("temporalData", {}).get("departure") or {}
    scheduled = departure.get("scheduleAdvertised")
    estimated = (
        departure.get("realtimeActual")
        or departure.get("realtimeForecast")
        or scheduled
    )

    platform_block = service.get("locationMetadata", {}).get("platform") or {}
    # Real boards say "TBC" rather than leaving it blank — RTT.io only
    # reports a platform once it's confirmed, which for anything more
    # than a few minutes out is often "not yet".
    platform = platform_block.get("actual") or platform_block.get("planned") or "TBC"

    destinations = service.get("destination") or []
    destination_name = " & ".join(
        d["location"]["description"] for d in destinations
    ) or "unknown"

    operator_name = service.get("scheduleMetadata", {}).get("operator", {}).get("name", "?")

    return {
        "scheduled": hhmm(scheduled),
        "estimated": hhmm(estimated),
        "is_cancelled": bool(departure.get("isCancelled")),
        "platform": platform,
        "destination_name": destination_name,
        "operator_name": operator_name,
    }


def get_access_token(force=False):
    """Exchange the long-life refresh token for a short-life access token.
    Cached for ACCESS_TOKEN_LIFETIME_MS; pass force=True after a 401.
    """
    global _access_token, _access_token_fetched_at
    now = time.ticks_ms()
    if (
        not force
        and _access_token is not None
        and time.ticks_diff(now, _access_token_fetched_at) < ACCESS_TOKEN_LIFETIME_MS
    ):
        return _access_token

    url = f"https://{config.RTT_IO_HOST}/api/get_access_token"
    headers = {"Authorization": "Bearer " + config.RTT_IO_REFRESH_TOKEN}
    response = urequests.get(url, headers=headers)
    try:
        if response.status_code != 200:
            raise RuntimeError(f"token exchange returned {response.status_code}")
        body = response.json()
    finally:
        response.close()

    _access_token = body["token"]
    _access_token_fetched_at = now
    return _access_token


def query_departures(access_token):
    """Returns (departures, status_code). 401 means the caller should
    force a token refresh and retry; 204 means no services, not an error.
    """
    dest_filter = f"&filterTo=gb-nr:{config.DEST_CRS}" if config.DEST_CRS else ""
    url = (
        f"https://{config.RTT_IO_HOST}/rtt/location"
        f"?code=gb-nr:{config.STATION_CRS}{dest_filter}"
    )
    headers = {"Authorization": "Bearer " + access_token}

    response = urequests.get(url, headers=headers)
    try:
        status = response.status_code
        if status == 200:
            body = response.json()
            services = body.get("services") or []
            return [normalize_service(s) for s in services], status
        return [], status
    finally:
        response.close()


def fetch_departures():
    departures, status = query_departures(get_access_token())
    if status == 401:
        departures, status = query_departures(get_access_token(force=True))
    if status not in (200, 204):
        raise RuntimeError(f"RTT.io returned {status}")
    return departures


def render(display, departures, error=None):
    display.clear(BLACK)
    display.draw_text8x8(8, 6, f"{config.STATION_CRS} departures", YELLOW)

    if error:
        display.draw_text8x8(8, 40, "poll failed:", RED)
        display.draw_text8x8(8, 56, str(error)[:26], RED)
        return

    if not departures:
        display.draw_text8x8(8, 40, "no services found", WHITE)
        return

    y = 32
    for dep in departures[:MAX_ROWS]:
        colour = RED if dep["is_cancelled"] else WHITE
        line = f"{dep['scheduled']} {dep['destination_name'][:15]:<15} P {dep['platform']}"
        display.draw_text8x8(8, y, line, colour)

        if dep["is_cancelled"]:
            display.draw_text8x8(16, y + 10, "cancelled", RED)
        elif dep["estimated"] != dep["scheduled"]:
            display.draw_text8x8(16, y + 10, f"exp {dep['estimated']}", AMBER)

        y += ROW_HEIGHT


def build_display():
    backlight = Pin(config.PIN_BL, Pin.OUT)
    backlight.on()

    spi = SPI(
        config.SPI_ID,
        baudrate=config.SPI_BAUDRATE,
        sck=Pin(config.PIN_SCK),
        mosi=Pin(config.PIN_MOSI),
    )
    return Display(
        spi,
        cs=Pin(config.PIN_CS),
        dc=Pin(config.PIN_DC),
        rst=Pin(config.PIN_RST),
        width=config.DISPLAY_WIDTH,
        height=config.DISPLAY_HEIGHT,
    )


def main():
    display = build_display()
    display.clear(BLACK)
    display.draw_text8x8(8, 8, "Connecting...", WHITE)

    wlan = connect_wifi()

    while True:
        try:
            departures = fetch_departures()
            render(display, departures)
        except Exception as e:
            print("poll failed:", e)
            render(display, [], error=e)
            reconnect_if_dropped(wlan)

        # No pip, no persistent HTTP session, no OS-managed heap on this
        # board — urequests opens a fresh socket every call, and the
        # 520 KB of SRAM this shares with everything else means a forced
        # collect after each poll is worth the cycles it costs.
        gc.collect()
        time.sleep(POLL_SECONDS)


main()
