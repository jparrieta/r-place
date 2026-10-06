# `package/store/relations.jsonl`

The mention graph: every room another room's coder recorded.

## What it holds

One line per (room, other) pair: `sub`, `other`, `other_in_frame`, `direction` (`names`), `label` (the pair's most frequent coder relation, ties broken toward the stronger tie), `labels` (all counted), `n`, `pointer_ids`, `code_ids`, `moved`, `reciprocal`, `adjacent`. Off-platform pointers are counted per room in lines with `other` null. `adjacent` is null unless an adjacency file was given.

## Who writes it, and when

`relations.py` at stage 00, from the store's `pointers.jsonl` and `rooms.jsonl`.

## Why it exists

Contract §5: the analyst may "read relations, count them", but "never merge rooms, never name a coalition before the material does, and never receive a list of which rooms belong together." `gen_views.py` writes `_views/relations.tsv` from it.

## Where

[package/store/relations.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/relations.jsonl).

Checked against: tools/relations.py, tools/gen_views.py, CONTRACT-aggregator.md §5.
