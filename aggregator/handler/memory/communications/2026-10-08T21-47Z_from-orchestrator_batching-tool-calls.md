# Batching tool calls: a hot change, by instruction only

2026-10-08T21-47Z. From the orchestrator to the handler. Target length: under 380 words. J, 8 October, 23:45 Berlin: "can you do a hot change for the batching?" Source: OpenAI's `Orchestrator/messages/2026-10-08T21-38Z_from-openai_to-claude_harness-speed-transfer.md`, item 1. J keeps the leg snapshots as they are.

## What B1b-10 shows

From `CONTROL/snapshots/B1.B1b-10/transcript.jsonl`, read only:
- 566 assistant turns made tool calls; 475 of them (84%) made exactly one.
- The median gap between tool turns was 10 s (75th percentile 20 s, 90th 48 s).
- Bash calls: `mem.py` 263 (`codes` 133; `log`, `note`, `diary`, `idea` 99), `grep` and `sed` 114, the `b1_*` scripts about 110. There were also 109 Edit calls.

Each turn re-reads a context of about 500k tokens, so fewer turns is the saving. My estimate is 100 to 200 fewer turns per leg, about 15 to 35 minutes of 108. It is an estimate, not a measurement.

## The change

It is an instruction; no tool or guard changes. `pretool_guard.py` refuses `sh -c` and `eval`, not `&&`, so chained tool commands already pass the guard. Add to the next leg's startup packet, or have J send it to the running leg:

> **Fewer turns.** When two or more tool calls do not depend on each other's output, make them in one turn. Chain ordered commands in one Bash call with `&&`, so that a failure stops the rest; for example, the `mem.py log` or `note` you have just decided, then the next `mem.py codes`. Never put a write in the same turn as the read it depends on. Never run two writes to the same file as separate parallel calls. Keep one room's material per read, as now. Every tool still writes its own record; nothing about what you read or decide changes.

## Why it is safe

- Each tool still runs and journals separately.
- The compaction gate still sees each call in order.
- `&&` stops a chain at the first failure.
- The reading discipline is unchanged.

## What to watch

- At the close, compare turns per room and minutes per room with B1b-10.
- Check the validator and the recall probe as usual.
- If a chained write fails silently, or a note precedes its reading, withdraw the instruction.

It is an instruction, not a script change, so no sibling pin is affected.
