#!/usr/bin/env bash
# Copy firmware/ onto the Pico's filesystem over USB and soft-reset it.
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v mpremote >/dev/null 2>&1; then
  echo "mpremote not found. Install it with: pip install mpremote" >&2
  exit 1
fi

if [ ! -f firmware/config.py ]; then
  echo "firmware/config.py not found — copying firmware/config.example.py as a starting point."
  cp firmware/config.example.py firmware/config.py
fi

echo "Creating device directories..."
mpremote mkdir :lib >/dev/null 2>&1 || true
mpremote mkdir :lib/fonts >/dev/null 2>&1 || true

echo "Copying firmware to device..."
while IFS= read -r -d '' file; do
  rel="${file#firmware/}"
  echo "  $rel"
  mpremote cp "$file" ":$rel"
done < <(find firmware -type f -print0)

echo "Soft-resetting device..."
mpremote reset

echo "Done. Watch serial output with: mpremote"
