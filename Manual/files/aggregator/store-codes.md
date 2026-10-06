# `package/store/codes.jsonl`

Every first-order concept of every room, joined.

## What it holds

`sub`, `code_id`, `theme_id`, `second_order`, `first_order`, `text` (the participant's words), `start`, `end`, `item_id`, `thread_id`, `item_kind`, `author`, `created_utc`, `hour`, `coord`, `state` (coded or unjoined), `batch`, `discovered_at`, `minted_in_stage`, `exchange_id`, `note`, `passage_id`. Retracted concepts are absent here; the coder's own `codes.jsonl` in the room's run keeps each one, marked `retracted: true`, with its reason in emit's journal. No third-order or higher field is stored; `mem.py` overlays those from `out/` at query time.

## Who writes it, and when

`build_store.py` at stage 00, from every room's `codes.jsonl` joined to the forest.

## Why it exists

`cite.py` quotes only from `text`, `start` and `end` (rule 3). STANDING §1 describes each concept "with its second-order theme, item, thread, author, hour since open, forest coordinate, the participant's words with offsets". Contract §5: no raw count of concepts "may be reported across communities as a property of the communities."

## Where

[package/store/codes.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/codes.jsonl).

Checked against: tools/build_store.py, tools/cite.py, tools/mem.py, STANDING-INSTRUCTIONS.md §1, CONTRACT-aggregator.md §5.
