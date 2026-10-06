# `package/store/pointers.jsonl`

Every pointer every coder wrote, in one file.

## What it holds

Each room's pointer lines as written (see the per-room page), with `sub` added.

## Who writes it, and when

`build_store.py` at stage 00.

## Why it exists

It is the input to the mention graph: `relations.py` reads it to write `relations.jsonl`. `links.py` lets a room that the rooms named resolve as an id. The dictionary: "`relations.py` builds the mention graph from it." A pointer with `relation` null "was named in the case account and carries no relation label."

## Where

[package/store/pointers.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/pointers.jsonl).

Checked against: tools/build_store.py, tools/relations.py, tools/links.py.
