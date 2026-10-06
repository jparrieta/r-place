# `package/<room>/pointers.jsonl`

Every mention of another place that the coder recorded in the room.

## What it holds

`pointer_id`, `batch`, `raw` (as written), `normalised` (for example r/place), `kind` (subreddit or off_platform), `relation` (values seen: mentioned-only, negotiated, asked-help-from, attacked, gave-help-to, attacked-by, allied, destroyed-carelessly), `moved` (no, partial, yes), `what_still_returns`, `what_you_cannot_see`, `thread_id`, `item_id`, `start`, `end`, `text`, `code_ids`, `minted_in_stage`, `note`, `corpus_position`.

## Who writes it, and when

The coder. `build_store.py` copies it, adds `sub`, writes the store's `pointers.jsonl`, and counts `n_subreddits_named` and `n_off_platform` in `rooms.jsonl`. `relations.py` builds the mention graph from it.

## Why it exists

Contract §5: "Other rooms are data, never units", and `n_off_platform` "is a count of mentions, never a share of the doing"; every verdict at the return carries it. `relations.py`: "A pointer is a mention the coder read and recorded."

## Where

Example: [package/armenia/pointers.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/armenia/pointers.jsonl).

Checked against: tools/build_store.py, tools/relations.py, CONTRACT-aggregator.md §5, package/armenia/pointers.jsonl.
