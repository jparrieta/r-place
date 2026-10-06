# `package/<room>/threads.jsonl`

The coder's disposition of every thread it looked at.

## What it holds

One line per thread disposed: `thread_id`, `read` (full or triaged), `verdict` (coded or out_of_scope in the lines seen), `reason`, `excluded_quote`, `recorded` (singly or bulk), `batch`.

## Who writes it, and when

The coder. `build_store.py` copies it, reads `read`, `verdict`, `reason` and `batch` into the store's `threads.jsonl`, and counts `threads_disposed`, `threads_read_in_full`, `threads_triaged` and `threads_out_of_scope` per room in `rooms.jsonl`.

## Why it exists

It records what the one reader chose to code. STANDING §1: "one reader per room decided what in each record was worth coding, and you hold what it kept." A1's screen reads it for any room the coder's own documents give reason to doubt.

## Where

Example: [package/armenia/threads.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/armenia/threads.jsonl).

Checked against: tools/build_store.py, STANDING-INSTRUCTIONS.md §1, stages/STAGE-A1-reading-room-notes.md, package/armenia/threads.jsonl.
