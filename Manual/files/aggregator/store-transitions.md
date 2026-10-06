# `package/store/transitions.jsonl`

The transitions ledger: every coded turn that answers a coded turn.

## What it holds

`id` (`<thread_id>:<from_coord>><to_coord>`), `sub`, `thread_id`, `from_item`, `to_item`, `from_coord`, `to_coord`, `from_codes`, `to_codes`, `from_case_themes`, `to_case_themes` (second-order ids), `from_author`, `to_author`, `same_author`, `interval_s`, `hops` (1 for a direct reply, more when uncoded turns lie between), `from_hour`, `limit`.

## Who writes it, and when

`transitions.py` at stage 00, from `package/forest.jsonl` and the store's `codes.jsonl`.

## Why it exists

Contract §2: an arrow's instance may be "a transition in a forest, two coded turns in one thread in order". The id is readable off `trees/<sub>.md`, so a D2 labeler can cite a transition without the store. `mem.py after` and `mem.py pairs` read it; the limit rides on every line: "a reply is a reply".

## Where

[package/store/transitions.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/transitions.jsonl).

Checked against: tools/transitions.py, tools/mem.py, CONTRACT-aggregator.md §2.
