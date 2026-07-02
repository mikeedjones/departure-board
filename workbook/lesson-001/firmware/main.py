"""Hello-world display test.

Proves the full chain works: MicroPython flashed -> code deployed -> SPI
wired correctly -> ILI9341 driver talks to the panel. No train data yet.
"""
from machine import Pin, SPI
from ili9341 import Display, color565
from xglcd_font import XglcdFont

try:
    import config
except ImportError:
    raise ImportError(
        "config.py not found on the device. Copy firmware/config.example.py "
        "to firmware/config.py (edit pins if your wiring differs), then "
        "redeploy with scripts/deploy.sh."
    )

spi = SPI(
    config.SPI_ID,
    baudrate=config.SPI_BAUDRATE,
    sck=Pin(config.SPI_SCK),
    mosi=Pin(config.SPI_MOSI),
)

display = Display(
    spi,
    cs=Pin(config.DISPLAY_CS),
    dc=Pin(config.DISPLAY_DC),
    rst=Pin(config.DISPLAY_RST),
    width=config.DISPLAY_WIDTH,
    height=config.DISPLAY_HEIGHT,
)

font = XglcdFont('lib/fonts/Unispace12x24.c', 12, 24)

display.clear()
display.draw_text(10, 10, 'Departure Board', font, color565(0, 255, 128))
display.draw_text(10, 40, 'Pico 2 W is alive', font, color565(255, 255, 255))
display.draw_rectangle(10, 80, 220, 40, color565(255, 128, 0))
display.fill_rectangle(20, 90, 60, 20, color565(0, 128, 255))

print('Rendered hello-world screen. If you can see it, wiring + driver are good.')
