# `tools/relations.py`

Stage 00's builder of the mention graph.

## What it holds

It reads the store's `pointers.jsonl` and `rooms.jsonl` and writes `relations.jsonl`, one line per (room, other) pair a room's coder recorded, and `_README-relations.md`. `other` is the pointer's normalised form without `r/`, matched to the frame case-insensitively. Off-platform pointers go in lines with `other` null. `--adjacency FILE` fills `adjacent` from a file built outside the analyst's reach.

## Who writes it, and when

Handler side at build: `build.sh` runs it after `build_store.py` and `transitions.py`. It is also shipped in the analyst's `tools/`.

## Why it exists

Contract §5: other rooms "are data, never units". Its limit: a pointer "is not the whole of a room's dealings with another: a room that coordinated off the record, or whose coder read other threads, has relations this file does not hold."

## Where

[tools/relations.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/relations.py).

Checked against: tools/relations.py, harness/build.sh, CONTRACT-aggregator.md §5.
