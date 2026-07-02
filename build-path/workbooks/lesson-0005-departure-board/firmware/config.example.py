"""Device configuration for the departure board.

Never committed — see .gitignore's `firmware/config.py` rule. Fill in
every value below before deploying. They stay on the device's
filesystem only, in plain text — there is no secrets manager or
keychain on a microcontroller. See lessons/0005-departure-board.html
for why that matters here.
"""

# --- Wi-Fi (lesson 3) ---
WIFI_SSID = "your-network-name"
WIFI_PASSWORD = "your-password"

# --- Display wiring (lesson 2) ---
SPI_ID = 0
SPI_BAUDRATE = 20_000_000
PIN_SCK = 18
PIN_MOSI = 19
PIN_CS = 17
PIN_DC = 20
PIN_RST = 21
PIN_BL = 22
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 320

# --- RTT.io (Realtime Trains) API (lesson 5) ---
# From https://api-portal.rtt.io. This is a long-life REFRESH token, not
# an access token — it can't be used against /rtt/location directly.
# main.py exchanges it at /api/get_access_token for a short-life
# (~20 min) access token and refreshes that on a timer.
RTT_IO_REFRESH_TOKEN = "your-refresh-token"
RTT_IO_HOST = "data.rtt.io"

# CRS codes (three-letter National Rail station codes). STATION_CRS is
# the board's own departure station; DEST_CRS filters to services
# calling at that one destination. Leave DEST_CRS = "" to show every
# departure from STATION_CRS regardless of where it's going.
STATION_CRS = "PAD"
DEST_CRS = ""
