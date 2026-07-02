# Lesson 1 complete: flash-vs-deploy model, and the CYW43439 LED quirk

Flashed MicroPython, got a working `mpremote` REPL, and confirmed the LED-toggle win condition on real hardware. Demonstrated the flash-vs-deploy distinction (interpreter flashed once, `.py` files deployed per change) and that `Pin("LED")` on the Pico 2 W routes through the CYW43439 wireless chip, not the RP2350 — safe to build straight on both going forward without re-explaining. The LED quirk also foreshadows the eventual Wi-Fi lesson, since it's the same chip.
