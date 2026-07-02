# Departure Board

A Raspberry Pi Pico 2 W (RP2350) driving an ILI9341 SPI TFT screen as a live
UK rail departure board, polling [RTT.io (Realtime Trains)](https://api-portal.rtt.io)
for departures from a station of your choice.

## Parts list

No specific vendor/SKU is pinned down here — any part matching the spec
below works. Wiring is write-only SPI (no MISO connection to the display).

| Part | Notes |
|---|---|
| Raspberry Pi Pico 2 W | RP2350 + CYW43439 Wi-Fi. A plain "Pico 2" (no W) won't work — no wireless. |
| ILI9341 TFT display breakout, 240×320, SPI | Needs CS, DC (aka RS), RST, and a backlight (LED/BL) pin broken out separately from the SPI bus. |
| 8 jumper wires | 3V3, GND, SCK, MOSI, CS, DC, RST, backlight |
| USB cable (micro-USB) | Flashes MicroPython and powers the board |

## Wiring

Pin numbers are Pico GPIO ("GP") numbers, matching `firmware/config.example.py`.

| Display pin | Pico GPIO |
|---|---|
| VCC | 3V3 |
| GND | GND |
| SCK (CLK) | GP18 |
| MOSI (SDI) | GP19 |
| CS | GP17 |
| DC (RS) | GP20 |
| RST | GP21 |
| LED (backlight) | GP22 |

SPI bus 0, 20 MHz.

## Setup, end to end

1. **Flash MicroPython.** Hold BOOTSEL while plugging the Pico 2 W into USB,
   then drag the latest Pico 2 W UF2 from [micropython.org](https://micropython.org/download/)
   onto the `RPI-RP2` drive that appears.
2. **Install tooling.** `uv sync` (installs `mpremote`, pinned in
   `pyproject.toml`).
3. **Wire the display** per the table above.
4. **Get an RTT.io refresh token** from [api-portal.rtt.io](https://api-portal.rtt.io)
   — it's a long-life refresh token, not a Bearer token; `firmware/main.py`
   exchanges it for a short-life access token on your behalf.
5. **Configure the device.** Copy `firmware/config.example.py` to
   `firmware/config.py` (gitignored — stays local and on-device only) and
   fill in your Wi-Fi credentials, the RTT.io refresh token, and your
   station's three-letter National Rail CRS code (e.g. `PAD` for London
   Paddington).
6. **Deploy.** `scripts/deploy.sh` — copies `firmware/` onto the device over
   USB and soft-resets it.
7. **Watch it run.** `mpremote` attaches to the device's serial output.

## How this was built

This board was built lesson-by-lesson as a way to learn embedded systems
fundamentals — SPI, MicroPython, Wi-Fi, HTTP — rather than just to end up
with a working gadget. That whole teaching history — lessons, learning
records, and the build workbook for each step — lives in
[`build-path/`](build-path).
