# `package/store/_unjoined.jsonl`

Concepts whose item the forest does not hold.

## What it holds

One line per such concept: `sub`, `code_id`, `item_id`, `thread_id`, and `why` ("the forest holds no such item").

## Who writes it, and when

`build_store.py` at stage 00. The concept stays in the store's `codes.jsonl` with `state` `unjoined` and a null `coord`.

## Why it exists

The build keeps a concept whose item is missing instead of dropping it; when the forest lacks a coded thread, "its codes are kept and listed as unjoined". A1 recomputes the count "against `codes.jsonl` and `items.jsonl`" and says whether it agrees with `README-store.md`.

## Where

[package/store/_unjoined.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/_unjoined.jsonl).

Checked against: tools/build_store.py, stages/STAGE-A1-reading-room-notes.md.
