# Mission: Embedded systems fluency, via the Pico 2 W departure board

## Why
The departure board is a vehicle, not the point: the goal is real, transferable embedded systems skill — reading datasheets, understanding what a driver library is actually doing at the protocol level, and building networked microcontroller applications — rather than just a working gadget. This builds on an existing base of electronics fundamentals (PhD in experimental physics, comfortable with breadboards/instrumentation) and prior Arduino/C experience, now extending into the MicroPython/Python embedded ecosystem and Wi-Fi-connected microcontrollers specifically.

## Success looks like
- Can explain what's happening at the protocol level (SPI, later Wi-Fi/HTTP) when driving a peripheral, not just call a library function
- Comfortable reading an unfamiliar MicroPython driver against its chip's datasheet and adapting it (pins, timing, commands) without hand-holding
- Can build a Wi-Fi + HTTP MicroPython application from scratch on RP2040/2350 (auth, JSON parsing, error handling, reconnect logic)
- Can articulate the concrete tradeoffs between MicroPython and the Arduino/C environment already known (performance, memory, iteration speed, ecosystem)

## Constraints
- Skip electronics fundamentals entirely (breadboards, wiring, multimeters, Ohm's law) — already fluent
- Skip general programming instruction — already a competent programmer (Arduino/C, plus general technical background from a physics PhD, professional level python experience)
- Prefers lessons **interleaved** with build sessions — one short lesson tied to whatever was just built, not a separate course track run in parallel

## Out of scope
- Basic electronics/circuit theory
- General Python syntax
- The C/Pico-SDK path — MicroPython was deliberately chosen for this project; C is a reference point for contrast, not a track to learn in parallel
