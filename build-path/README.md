# Build path

The teaching workspace behind the [departure board](..) — a stateful
workspace for Claude Code's `teach` skill ([.claude/skills/teach](.claude/skills/teach)),
so learning here can pick back up across sessions instead of starting from
zero each time.

To resume teaching, run Claude Code with **this directory** as the working
directory (or add it as an additional working directory) — the `teach`
skill's paths are relative to it.

| Path | Holds |
|---|---|
| [`MISSION.md`](MISSION.md) | Why this project exists — grounds every teaching decision |
| [`NOTES.md`](NOTES.md) | Working preferences for how lessons should be run |
| [`RESOURCES.md`](RESOURCES.md) | Curated, primary-source material (datasheets, docs, communities) |
| [`learning-records/`](learning-records) | What's already been learned — the ADR equivalent for teaching |
| [`lessons/`](lessons) | Self-contained HTML lessons, one tightly-scoped concept each |
| [`reference/`](reference) | Compressed, look-up-friendly cheat sheets distilled from lessons |
| [`assets/`](assets) | Shared stylesheet/components lessons are built from |
| [`workbooks/`](workbooks) | The build output of each lesson (firmware, scripts, etc.) — `workbooks/lesson-0005-departure-board/` is the original copy of what now lives at the repo root's `firmware/` |

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
