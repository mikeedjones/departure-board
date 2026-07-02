"""Pin and display configuration.

Copy this file to config.py (gitignored) and edit if your wiring differs.
Pin numbers are Pico GP numbers, not physical pin positions.
"""

# SPI0 bus
SPI_ID = 0
SPI_BAUDRATE = 20_000_000  # driver author benchmarks up to 40MHz; start lower
SPI_SCK = 18
SPI_MOSI = 19

# Display control pins
DISPLAY_CS = 17
DISPLAY_DC = 20
DISPLAY_RST = 21

# Panel geometry
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 320
