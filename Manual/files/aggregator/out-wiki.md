# `out/_wiki/`

Generated pages, one per room and one per model element.

## What it holds

`rooms/<sub>.md` (the room's column) and `model/<id>.md` (an element: its statement, evidence, and the adaptations touching it). STANDING §2 also names pages per theme and form, with a ceiling of 800 words a page.

## Who writes it, and when

`gen_views.py`, run by `done.sh` at every close. Never edited. Read with `mem.py wiki [page]`, which says so when the analyst's working files changed since the page was written.

## Why it exists

Rule 15, as for the views. At D1 `handoff.py` appends the wiki pages of the elements a room's themes were placed under to that room's `MODEL.md`, so a labeler reads the same page the analyst does.

## Where

[out/_wiki/](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/_wiki/).

Checked against: tools/gen_views.py, tools/mem.py, tools/handoff.py, STANDING-INSTRUCTIONS.md §2, CONTRACT-aggregator.md rule 15.
