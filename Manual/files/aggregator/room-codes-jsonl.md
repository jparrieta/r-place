# `package/<room>/codes.jsonl`

The coder's first-order concepts for one room, as written.

## What it holds

One JSON line per concept: `passage_id`, `code_id` (c0001 and on), `batch`, `first_order` (the coder's label), `theme_id` (its second-order theme), `thread_id`, `item_id`, `item_kind` (post or comment), `author`, `created_utc`, `exchange_id`, `discovered_at`, `minted_in_stage`, `start`, `end`, `text` (the participant's words), `note`, and on some lines `minted_after_n_codes` and `corpus_position`. A withdrawn concept carries `retracted` true, with a `retracted_reason` in the lines seen.

## Who writes it, and when

The coder. `build_store.py` copies it whole and builds the store's `codes.jsonl` from it, moving retracted lines to `_retracted.jsonl`.

## Why it exists

Rule 3: an exemplar is the participant's words, "never labels and never a coder's note"; `cite.py` quotes only `text`. A1 checks the store's concept counts against this file in each room folder. At D1 it goes into every labeler's task folder.

## Where

Example: [package/armenia/codes.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/armenia/codes.jsonl).

Checked against: tools/build_store.py, tools/cite.py, CONTRACT-aggregator.md rule 3, stages/STAGE-A1-reading-room-notes.md, tools/handoff.py, package/armenia/codes.jsonl.
