from machine import Pin, SPI

import config
from lib.ili9341 import Display, color565

print("Backlight on...")
backlight = Pin(config.PIN_BL, Pin.OUT)
backlight.on()

print("Bringing up SPI0 and the ILI9341...")

spi = SPI(
    config.SPI_ID,
    baudrate=config.SPI_BAUDRATE,
    sck=Pin(config.PIN_SCK),
    mosi=Pin(config.PIN_MOSI),
)
display = Display(
    spi,
    cs=Pin(config.PIN_CS),
    dc=Pin(config.PIN_DC),
    rst=Pin(config.PIN_RST),
    width=config.DISPLAY_WIDTH,
    height=config.DISPLAY_HEIGHT,
)

print("Clearing to navy...")
display.clear(color565(0, 0, 128))

display.draw_text8x8(60, 150, "Departure Board", color565(255, 255, 255))

print("Done — if the screen is navy with white text, SPI is talking to the panel.")
