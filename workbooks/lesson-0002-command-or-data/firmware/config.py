"""Pin assignments and SPI settings for the ILI9341 wiring.

See lessons/0002-command-or-data.html for what each pin does and why
these particular GPIOs were picked.
"""

SPI_ID = 0
SPI_BAUDRATE = 20_000_000  # faster and the ILI9341 misbehaves — see datasheet timing specs

PIN_SCK = 18
PIN_MOSI = 19
PIN_CS = 17
PIN_DC = 20
PIN_RST = 21
PIN_BL = 22

DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 320
