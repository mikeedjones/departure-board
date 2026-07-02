# Embedded Systems / Pico 2 W Resources

## Knowledge

- [Raspberry Pi Pico 2 W Datasheet](https://pip.raspberrypi.com/documents/RP-008304-DS-pico-2-w-datasheet.pdf)
  Official datasheet for the exact board in this kit — RP2350 core/memory specs, the Infineon CYW43439 wireless chip and its SPI link to the RP2350, full pinout. Use for: hardware-level questions about the board itself, before Wi-Fi code is written.
- [MicroPython docs: Quick reference for the RP2](https://docs.micropython.org/en/latest/rp2/quickref.html)
  Official reference for `machine.SPI`, `machine.Pin`, `network.WLAN`, PIO, and everything else the RP2040/RP2350 port exposes. Use for: exact API signatures when writing device code.
- [Raspberry Pi: Raspberry Pi Pico-series Python SDK (PDF)](https://pip.raspberrypi.com/documents/RP-008355-DS)
  Official Raspberry Pi Foundation guide to MicroPython on Pico boards, command line + Thonny workflows. Use for: toolchain/workflow questions (flashing, mpremote/Thonny, filesystem layout).
- [Raspberry Pi: Connecting to the Internet with Raspberry Pi Pico W (PDF)](https://pip.raspberrypi.com/documents/RP-008257-DS)
  Official guide to Wi-Fi (and Bluetooth) on the Pico W family, MicroPython and C. Ch.3 (§3.1-3.4) also covers W-series-specific basics ahead of any networking: flashing the UF2, connecting over USB (Thonny/minicom/mpremote), and the on-board LED being wired to the wireless chip's `WL_GPIO0` rather than the RP2350. Use for: initial flash/REPL setup now, Wi-Fi/HTTP work later.
- [ILI9341 datasheet (ILI Technology Corp, v1.11)](https://cdn-shop.adafruit.com/datasheets/ILI9341.pdf)
  Primary source for the display controller actually in use. Use for: understanding what the vendored driver (`firmware/lib/ili9341.py`) is doing register-by-register — section 7.1.8 "Serial Interface" (p.33) covers the 3-line vs 4-line SPI framing directly.
- [Wikipedia: Serial Peripheral Interface](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface)
  Base protocol reference (CS/SCLK/MOSI/MISO, clock polarity/phase, 3-wire vs 4-wire variants). Use for: general SPI vocabulary before diving into a chip-specific datasheet.

## Wisdom (Communities)

- [MicroPython Forum](https://forum.micropython.org/)
  Official community, maintainers are active participants. Use for: MicroPython-specific bugs, port quirks, driver troubleshooting.
- [r/embedded](https://reddit.com/r/embedded)
  General embedded systems discussion, reasonably high signal. Use for: architecture-level questions, career/industry context, second opinions on approach.

## Gaps

- No curated resource yet for Wi-Fi reconnect/error-handling patterns in MicroPython specifically — likely needed once the departure-data fetch work starts.
