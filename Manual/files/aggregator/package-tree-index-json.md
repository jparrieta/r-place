# `package/tree_index.json`

Coordinate to item for every room, with the forest's header counts.

## What it holds

One key per room. Under it, `counts` (`threads_given`, `threads_with_codes`, `items`, `coded`, `bridge`, `removed`, `dropped`, `orphans`, `na_stretches`, `coverage_of_coded_items`, `threads_total_in_window`) and `index`: thread id, then coordinate, then the item (`item_id`, `parent_id`, `author`, `created_utc`, `dt_parent_sec`, `dt_thread_sec`, `state`, `code_ids`, `labels`, `sequence`, `coverage`, `meta`).

## Who writes it, and when

`build_store.py` at stage 00, merging each room's `forest/tree_index.json` from the coders' input.

## Why it exists

`build_store.py` describes it as "coordinate -> item, per room, with the header counts". It supplies the `created_utc` that forest nodes lack, and its counts become the `forest` field and `threads_total` in `rooms.jsonl`. A1 recomputes the forest header totals over `trees/` and compares them with the store's figures.

## Where

[package/tree_index.json](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/tree_index.json).

Checked against: tools/build_store.py, stages/STAGE-A1-reading-room-notes.md, package/tree_index.json.
