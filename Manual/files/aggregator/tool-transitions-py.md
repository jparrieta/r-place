# `tools/transitions.py`

Stage 00's builder of the transitions ledger.

## What it holds

It reads `package/forest.jsonl` and the store's `codes.jsonl` and writes `transitions.jsonl`: one line for every coded turn that answers a coded turn, directly or through uncoded turns the forest kept, with the interval and the hop count. It also writes `_README-transitions.md`. It knows nothing of themes above the second order; `mem.py` lifts the pairs through the analyst's tier files at query time.

## Who writes it, and when

Handler side at build: `build.sh` runs it after `build_store.py`. It is also shipped in the analyst's `tools/`.

## Why it exists

Its limit, on every line: "a reply is a reply". The ledger "does not show that the first caused the second, and an interval is elapsed time, never the speed of a decision." STANDING §1: "No relation you write may rest on adjacency alone."

## Where

[tools/transitions.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/transitions.py).

Checked against: tools/transitions.py, harness/build.sh, STANDING-INSTRUCTIONS.md §1.
