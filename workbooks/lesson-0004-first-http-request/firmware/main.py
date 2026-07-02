import time
import network
import urequests

import config

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


def describe(status):
    return STATUS_NAMES.get(status, str(status))


print("Powering up the CYW43439 and its Wi-Fi firmware...")
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
    time.sleep(5)

if wlan.status() != 3:
    raise RuntimeError(f"network connection failed: {describe(wlan.status())}")

ip, subnet, gateway, dns = wlan.ifconfig()
print(f"connected — ip = {ip}")

# httpbin.org/json — small, stable, no-auth JSON test endpoint.
# date.jsontest.com (the guide's own §3.8.2 example) no longer resolves.
url = "http://httpbin.org/json"
print(f"GET {url}")
response = urequests.get(url)
try:
    print(f"status = {response.status_code}")
    body = response.json()
    print(f"slideshow title = {body['slideshow']['title']}")
finally:
    response.close()
