# `package/store/items.jsonl`

Every item of every coded thread, without its text.

## What it holds

`sub`, `thread_id`, `item_id`, `coord`, `parent_id`, `author`, `created_utc`, `hour`, `state` (coded, bridge, removed, dropped), `codes`, `dt_parent_sec`, `dt_thread_sec`, `collapsed_n`, `coverage`, `depth`, `meta` (`score`, `distinguished`, `stickied`, `edited`, `link_flair_text`, `author_flair_text`, `retrieved_on`).

## Who writes it, and when

`build_store.py` at stage 00, from the forest.

## Why it exists

The dictionary says: "no body: the record's text stays with the record"; the only words the store carries are the coded passages. It also warns that the score and `stickied` "are snapshots taken at retrieval, weeks after the event: lower bounds with no timing. `distinguished` is reliable."

## Where

[package/store/items.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/items.jsonl).

Checked against: tools/build_store.py.
