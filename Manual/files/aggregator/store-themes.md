# `package/store/themes.jsonl`

Every second-order theme of every room, with its concepts.

## What it holds

`sub`, `theme_id`, `second_order`, `theme_note`, `n_codes` (after retraction), `n_codes_coder`, `code_ids`, `items`, `threads`, `first_hour`, `last_hour`, `regrouped_from`.

## Who writes it, and when

`build_store.py` at stage 00, from every room's `themes.jsonl`.

## Why it exists

It is the unit the scheme is built from: at B1 "the second-order themes are read room by room" (contract §6). `counts.py`'s `assignment_items_expected` is every second-order theme of the analysed set, "what stage B3's batches must cover". `mem.py theme` and `mem.py themes` serve it.

## Where

[package/store/themes.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/themes.jsonl).

Checked against: tools/build_store.py, tools/counts.py, tools/mem.py, CONTRACT-aggregator.md §6.
