from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)

print("MicroPython is running on the Pico 2 W.")

for _ in range(5):
    led.toggle()
    sleep(0.25)

led.off()
print("Done — if the LED blinked five times, the interpreter is alive.")
