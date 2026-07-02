# Teaching notes

- Background: PhD in experimental physics, prior Arduino/C experience, comfortable with breadboards and general electronics. Do not re-teach electronics fundamentals or general programming. Professional python developer experience, but not yet fluent in MicroPython or the RP2040 ecosystem.
- Pacing preference: interleaved — a short lesson after each chunk of build work, tied directly to what was just built, not a separate curriculum track.
- Useful framing: primary-source datasheets land well — verified the ILI9341 datasheet directly for lesson 1 rather than relying on secondhand summaries, and it produced a sharper lesson. Keep pulling from chip datasheets over blog posts where possible.
- Workflow preference: when integrating a new third-party HTTP API, debug auth/schema/status-code questions with `curl` on the dev machine first — user explicitly redirected away from iterating via `mpremote run` on the Pico for this. A USB deploy + Wi-Fi join is a slow, noisy way to debug something that has nothing to do with the board. Reserve on-device runs for confirming the thing that's actually specific to the hardware (display rendering, real Wi-Fi timing).
