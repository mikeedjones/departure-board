# Departure Board

A Raspberry Pi Pico 2 W powered train/transit departure board with a small
SPI TFT screen. This repo covers the whole thing end-to-end: device firmware,
wiring, and (later) pulling live departure data over Wi-Fi.

This first pass just gets the hardware and toolchain working — flashing
MicroPython, wiring the screen, and rendering a "hello world" — before any
real departure data is involved.

## Hardware

- Raspberry Pi Pico 2 W (RP2350)
- 240×320 4-wire SPI TFT display, ILI9341-class controller (CS, SCK, MOSI, DC,
  RST, no MISO/SDO — the panel is write-only)
- Breadboard + jumper wires (or your own wiring)

### Wiring

| Display pin | Pico pin | Notes |
|---|---|---|
| VCC | 3V3 | |
| GND | GND | |
| CS | GP17 | SPI0 chip select |
| RESET | GP21 | |
| DC (RS) | GP20 | Data/command |
| SDI (MOSI) | GP19 | SPI0 TX |
| SCK | GP18 | SPI0 SCK |
| LED (backlight) | 3V3 | tied high directly; no dimming for now |

If your board is wired to different GPIOs, edit `firmware/config.py` (see
below) rather than rewiring.

## Firmware setup

1. **Flash MicroPython.** Download the `.uf2` for your board specifically
   from [micropython.org/download/RPI_PICO2_W](https://micropython.org/download/RPI_PICO2_W/)
   — the Pico 2 W (RP2350) needs the `RPI_PICO2_W` build, not the older Pico
   W's `RPI_PICO_W` build. Hold **BOOTSEL** while plugging the Pico into USB,
   it'll mount as a USB drive, then copy the `.uf2` onto it — it reboots into
   MicroPython automatically.

2. **Install mpremote** (used to copy files onto the device and talk to its
   REPL):

   ```sh
   pip install mpremote
   ```

3. **Wire the display** per the table above.

4. **Configure pins (first time only).** `scripts/deploy.sh` will copy
   `firmware/config.example.py` to `firmware/config.py` automatically if it
   doesn't exist yet. Edit `firmware/config.py` first if your wiring differs
   from the table above — it's gitignored, so local tweaks won't get
   committed.

5. **Deploy:**

   ```sh
   scripts/deploy.sh
   ```

   This copies everything in `firmware/` onto the Pico's filesystem and
   soft-resets it.

6. **Check the result.** You should see "Departure Board" / "Pico 2 W is
   alive" plus a test rectangle render on the screen. To see print output or
   tracebacks, open a REPL:

   ```sh
   mpremote
   ```

   (Ctrl-] to exit.)

## Repo layout

```
firmware/
  boot.py             # runs on every power-up
  main.py             # hello-world display test
  config.example.py   # pin config template — copy to config.py to customize
  lib/
    ili9341.py           # vendored driver (rdagger/micropython-ili9341, MIT)
    xglcd_font.py        # font rendering support
    LICENSE-ili9341.txt  # license for the two vendored files above
    fonts/
      Unispace12x24.c   # bundled font
scripts/
  deploy.sh           # copies firmware/ to the device and resets it
```

## Troubleshooting

- **Nothing on screen / `OSError` from SPI calls:** double check CS/DC/RST
  wiring and that the display's backlight (LED) pin is powered — a lot of
  "not working" cases are actually just a dark backlight.
- **Screen shows static/garbage:** try lowering `SPI_BAUDRATE` in
  `firmware/config.py`, especially over long breadboard jumpers.
- **`config.py not found` error:** run `scripts/deploy.sh` at least once —
  it creates `firmware/config.py` from the example automatically.
