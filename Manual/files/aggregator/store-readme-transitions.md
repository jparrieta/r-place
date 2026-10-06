# `package/store/_README-transitions.md`

The transitions ledger's dictionary entry, with its counts.

## What it holds

A section headed "The transitions ledger (`transitions.jsonl`)": lines, threads and rooms; how many are direct replies (`hops` 1) and how many reach the nearest coded ancestor through uncoded turns; how many are the same author answering themselves; the median interval; that `from_case_themes` and `to_case_themes` carry second-order theme ids; the verbs that read it (`mem.py after`, `mem.py pairs`). It ends with the limit.

## Who writes it, and when

`transitions.py` at stage 00; `build_store.py --readme-only` folds it into `README-store.md`.

## Why it exists

`transitions.py`: "The limit is on every line and it is the whole ledger's meaning: a reply is a reply." An interval is elapsed time, "never the speed of a decision."

## Where

[package/store/_README-transitions.md](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/_README-transitions.md).

Checked against: tools/transitions.py, tools/build_store.py.
