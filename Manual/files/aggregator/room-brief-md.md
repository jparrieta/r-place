# `package/<room>/brief.md`

The coder's account of the room's pre-event week.

## What it holds

Prose sections. In the armenia example: Evidence base, Vernacular, Who talks, Recurring formats, Register, Jokes with a history, Moderation and its visible traces, The week's shape, What I could not tell, Data problems. Quoted words carry their item ids in backticks.

## Who writes it, and when

The coder, one sealed reader per room, before the run. `build_store.py` copies it whole into `package/<sub>/` at stage 00; `rooms.jsonl` records `brief` true or false and `_build.json` counts the briefs present.

## Why it exists

`mem.py brief <sub>` serves it as "the room's pre-event week". A1 reads it with `case.md` after the forest and the concepts, and checks that every room folder holds the same six files. At D1 each labeler's task folder includes it, described in the task as "what was known of the room before the event".

## Where

Example: [package/armenia/brief.md](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/armenia/brief.md).

Checked against: tools/build_store.py, tools/mem.py, stages/STAGE-A1-reading-room-notes.md, handoff/TASK-template.md, package/armenia/brief.md.
