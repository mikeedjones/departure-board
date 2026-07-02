# Departure Board

A Raspberry Pi Pico 2 W (RP2350) driving a small ILI9341 SPI TFT screen as a
train/transit departure board — eventually pulling live departure data over
Wi-Fi.

The board is the excuse, not the point. This repo exists to build real,
transferable embedded systems fluency along the way: reading datasheets,
understanding what a driver library is doing at the protocol level, and
writing networked MicroPython applications on the RP2040/2350 — not just
ending up with a working gadget. See [MISSION.md](MISSION.md) for the full
rationale and constraints.

## A teaching workspace, not just a codebase

This repo doubles as a stateful teaching workspace for Claude Code's `teach`
skill ([.claude/skills/teach](.claude/skills/teach)), so learning here can
pick back up across sessions instead of starting from zero each time.

| Path | Holds |
|---|---|
| [`MISSION.md`](MISSION.md) | Why this project exists — grounds every teaching decision |
| [`NOTES.md`](NOTES.md) | Working preferences for how lessons should be run |
| [`RESOURCES.md`](RESOURCES.md) | Curated, primary-source material (datasheets, docs, communities) |
| [`learning-records/`](learning-records) | What's already been learned — the ADR equivalent for teaching |
| [`lessons/`](lessons) | Self-contained HTML lessons, one tightly-scoped concept each |
| [`reference/`](reference) | Compressed, look-up-friendly cheat sheets distilled from lessons |
| [`assets/`](assets) | Shared stylesheet/components lessons are built from |
| [`workbook/`](workbook) | The actual build output of each lesson (firmware, scripts, etc.) |

## Working style

Per [NOTES.md](NOTES.md): lessons are interleaved with build sessions — one
short lesson tied to whatever was just built, not a separate course track —
and prefer primary-source datasheets (e.g. the ILI9341 datasheet itself) over
secondhand summaries.

## Scope

Already fluent in electronics fundamentals and general programming (physics
PhD, prior Arduino/C, professional Python), so this deliberately skips
breadboarding/Ohm's-law-level content and general Python syntax. It also
skips the C/Pico-SDK path — MicroPython was the deliberate choice here, with
C kept only as a point of contrast. Full constraints in
[MISSION.md](MISSION.md).
