# `package/store/_README-relations.md`

The mention graph's dictionary entry, with its counts.

## What it holds

A section headed "The mention graph (`relations.jsonl`)": the number of (room, other) pairs and of rooms, how many name a room of this study, how many are reciprocated, the counts of each label (the pair's most frequent), the off-platform lines with `other` null, and whether `adjacent` was filled. It ends with the limit.

## Who writes it, and when

`relations.py` at stage 00; `build_store.py --readme-only` folds it into `README-store.md`.

## Why it exists

`relations.py`: "The limit. A pointer is a mention the coder read and recorded. It is not the whole of a room's dealings with another."

## Where

[package/store/_README-relations.md](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/_README-relations.md).

Checked against: tools/relations.py, tools/build_store.py.
