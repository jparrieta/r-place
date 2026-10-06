# `trees/<room>.md`

The rendered forest of one room: its coded threads as reply trees.

## What it holds

A header with counts (threads given and with a code, threads in the window, items coded, bridge, removed and dropped, orphans, uncoded stretches, the mean share of text under a code) and a key to the notation. Then one block per coded thread: id, title, hour opened, counts. Each item sits on a line with its Dewey coordinate, author and flair, time since its parent, score at retrieval, and its chunks in text order (a code id, or `na` for a passage passed over), then the labels. Runs of uncoded items are collapsed with a count.

## Who writes it, and when

The coders' forest renderer, one per room; `build_store.py` copies it to `trees/` at stage 00.

## Why it exists

STANDING §1: "each coded thread as its reply tree, coded turns hung on it, gaps kept, dropped items counted in the header." A1 reads every room whole through it (`mem.py forest`). The header warns that scores and sticky flags are "snapshots weeks after the event, not facts about the week."

## Where

Example: [trees/armenia.md](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/trees/armenia.md).

Checked against: STANDING-INSTRUCTIONS.md §1, tools/build_store.py, tools/transitions.py, stages/STAGE-A1-reading-room-notes.md, trees/armenia.md.
