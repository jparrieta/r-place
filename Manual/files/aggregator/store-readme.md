# `package/store/README-store.md`

The store's dictionary: what each file is, and what none of them is.

## What it holds

The clock (hour 0 is 1490976000 UTC, 2017-03-31 16:00; placement stopped at hour 73; the window ends at 97; negative hours are the pre-event week); the limit on every row with a parent, "a reply is a reply: posted after, not caused by"; a table of files with what one line is and its keys, counts filled from `_build.json`; what the record holds (the threads the codes point at, every item of each, but no text); and what is not here: no canvas field outside `rooms.jsonl`, no third-order theme or higher, no item body, no interpretation. The three `_README-*.md` files are appended.

## Who writes it, and when

`build_store.py` (its `write_readme`) at stage 00, again after the canvas join, and with `--readme-only` once the transitions, relations and neighbours files exist.

## Why it exists

STANDING §1: "the dictionary. Read it at stage A1." It is in A1's first-leg packet, and A1 recomputes the build figures it prints.

## Where

[package/store/README-store.md](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/README-store.md).

Checked against: tools/build_store.py, harness/build.sh, STANDING-INSTRUCTIONS.md §1, stages/STAGE-A1-reading-room-notes.md.
