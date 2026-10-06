# `package/store/threads.jsonl`

Every coded thread, its shape and the coder's disposition in one line.

## What it holds

`sub`, `thread_id`, `title`, `opener`, `opened_hour`, `last_hour`, `n_items`, `n_coded`, `n_dropped`, `n_authors`, `depth`, `first_code_hour`, `last_code_hour`, `codes`, `themes`, `read`, `verdict`, `reason`, `batch`, `op_score`, `op_stickied`, `op_distinguished`, `op_flair`, `retrieved_on`.

## Who writes it, and when

`build_store.py` at stage 00, from the forest joined with the coder's `threads.jsonl`.

## Why it exists

A1 uses it for one of the two clocks of ending: `onset_last_code_hour` against "the last `last_hour` over the room's threads in `threads.jsonl`", reporting how many rooms have each null.

## Where

[package/store/threads.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/threads.jsonl).

Checked against: tools/build_store.py, stages/STAGE-A1-reading-room-notes.md.
