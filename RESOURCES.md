# Embedded Systems / Pico 2 W Resources

## Knowledge

- [Raspberry Pi Pico 2 W Datasheet](https://pip.raspberrypi.com/documents/RP-008304-DS-pico-2-w-datasheet.pdf)
  Official datasheet for the exact board in this kit — RP2350 core/memory specs, the Infineon CYW43439 wireless chip and its SPI link to the RP2350, full pinout. Use for: hardware-level questions about the board itself, before Wi-Fi code is written.
- [MicroPython docs: Quick reference for the RP2](https://docs.micropython.org/en/latest/rp2/quickref.html)
  Official reference for `machine.SPI`, `machine.Pin`, `network.WLAN`, PIO, and everything else the RP2040/RP2350 port exposes. Use for: exact API signatures when writing device code.
- [Raspberry Pi: Raspberry Pi Pico-series Python SDK (PDF)](https://pip.raspberrypi.com/documents/RP-008355-DS)
  Official Raspberry Pi Foundation guide to MicroPython on Pico boards, command line + Thonny workflows. Use for: toolchain/workflow questions (flashing, mpremote/Thonny, filesystem layout).
- [Raspberry Pi: Connecting to the Internet with Raspberry Pi Pico W (PDF)](https://pip.raspberrypi.com/documents/RP-008257-DS)
  Official guide to Wi-Fi (and Bluetooth) on the Pico W family, MicroPython and C. Ch.3 (§3.1-3.4) covers W-series-specific basics ahead of any networking: flashing the UF2, connecting over USB (Thonny/minicom/mpremote), and the on-board LED being wired to the wireless chip's `WL_GPIO0` rather than the RP2350. §3.6 "Connecting to a wireless network" is the primary source for lesson 3 — `network.WLAN(STA_IF)`, the connect/poll sequence, and the CYW43 link-status codes table. §3.8 "Making HTTP requests" is the primary source for lesson 4 — raw sockets (§3.8.1), `urequests` (§3.8.2, including the required `response.close()`), and the reconnect-on-failure pattern (§3.8.3). Note: the guide's own §3.8.2 example endpoint, `date.jsontest.com`, no longer resolves (dead as of 2026) — verify example URLs before trusting them. Use for: Wi-Fi bring-up and HTTP/JSON work now, HTTP servers (§3.9) later.
- [ILI9341 datasheet (ILI Technology Corp, v1.11)](https://cdn-shop.adafruit.com/datasheets/ILI9341.pdf)
  Primary source for the display controller actually in use. Use for: understanding what the vendored driver (`firmware/lib/ili9341.py`) is doing register-by-register — section 7.1.8 "Serial Interface" (p.33) covers the 3-line vs 4-line SPI framing directly.
- [Wikipedia: Serial Peripheral Interface](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface)
  Base protocol reference (CS/SCLK/MOSI/MISO, clock polarity/phase, 3-wire vs 4-wire variants). Use for: general SPI vocabulary before diving into a chip-specific datasheet.
- [rdagger/micropython-ili9341](https://github.com/rdagger/micropython-ili9341) (MIT)
  Source of the vendored driver at `workbooks/lesson-0002-command-or-data/firmware/lib/ili9341.py`. Use for: what a given driver method actually does before reaching for the datasheet — cross-check the two together.
- [Realtime Trains (RTT.io) API specification](https://github.com/realtimetrains/api-specification)
  Authoritative OpenAPI spec for the live departure data this board actually polls (lesson 5) — UK National Rail departures as plain JSON. Covers the refresh-token/access-token exchange (`/api/get_access_token`), the `/rtt/location` departures-summary endpoint, and the `/rtt/service` per-stop-detail endpoint. Note: the key issued from api-portal.rtt.io is a long-life *refresh* token, not directly usable as a Bearer token — confirmed by testing directly against the API with `curl` before writing any device code.
- [chrisys/train-departure-display](https://github.com/chrisys/train-departure-display)
  Reference implementation this project's departure-parsing structure (parse-at-the-edge into a flat dict, dedupe/sort) is adapted from — it targets National Rail's OpenLDBWS SOAP/XML API rather than RTT.io's JSON, since MicroPython has no XML parser in its standard library. Use for: the overall shape of a departure-board data pipeline, not a literal port.

## Wisdom (Communities)

- [MicroPython Forum](https://forum.micropython.org/)
  Official community, maintainers are active participants. Use for: MicroPython-specific bugs, port quirks, driver troubleshooting.
- [r/embedded](https://reddit.com/r/embedded)
  General embedded systems discussion, reasonably high signal. Use for: architecture-level questions, career/industry context, second opinions on approach.

## Gaps

- Reconnect logic in lesson 5's workbook is a flat 60-second retry on any exception, not the backoff-with-cap pattern real long-running deployments would want — fine for a desk device, worth revisiting if this ever runs somewhere less reliable than home Wi-Fi.
- No NTP sync yet, so the board has no real wall-clock time — token-expiry tracking uses a relative `ticks_ms()` timer instead of comparing against the server's `validUntil`. Fine for now; would matter if a future lesson needs an actual displayed clock.
- RTT.io platform data is inconsistently populated per station (confirmed via `/rtt/service` for Wandsworth Town, see `reference/departure-board-api.html`) — the user is planning to add their own platform-inference logic on top of the API's gaps.
