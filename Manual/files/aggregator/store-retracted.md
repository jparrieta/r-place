# `package/store/_retracted.jsonl`

Every concept its coder withdrew, listed and kept out of the store.

## What it holds

One line per retracted concept: the line as the coder wrote it, with `sub` added.

## Who writes it, and when

`build_store.py` at stage 00, which drops these lines from the store's `codes.jsonl`.

## Why it exists

Contract §5: "Retracted concepts (the coder's own withdrawals) are not in the store." The list keeps them visible: A1 confirms the dropped count "against `_retracted.jsonl` and against the coder's `codes.jsonl` in each room folder". At D2, `ingest.py` refuses a labeler's line that cites a retracted concept.

## Where

[package/store/_retracted.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/_retracted.jsonl).

Checked against: tools/build_store.py, CONTRACT-aggregator.md §5, stages/STAGE-A1-reading-room-notes.md, tools/ingest.py.
