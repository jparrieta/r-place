# `tools/probe.py`

The recall probe: five questions at every close, and their score.

## What it holds

`--ask` writes `_probe/NN-L.questions.md` with five questions: the method question in one sentence; the open distinctions by slug; the last three rooms opened; the element or theme changed and why; the next comparison. `--score` reads `NN-L.answers.md` and marks each question right, wrong, missing or not applicable: the goal against three of four key words; the slugs against the open question files; the rooms against the last `room` reads; the change against an id from this leg's history lines (the id, not the reason); the next comparison against the last `next:` the leg wrote in the diary. A question with nothing on record to check is not applicable and never counts as recall; the score is the right answers over the questions that could be checked, or none (review of 29 September 2026). It writes `NN-L.json`, and each miss to `_probe/notes.jsonl`. The probe forks the closing session with its tools refused: it measures what the leg recalls unaided, not how well the next leg rebuilds the argument from the files.

## Who writes it, and when

Shipped in the analyst's `tools/`; `close.sh` runs the trusted copy after the leg closes.

## Why it exists

STANDING §2: the probe "measures whether the goal survived the leg". A miss the head or the diary answers is a note, not a defect.

## Where

[tools/probe.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/probe.py).

Checked against: tools/probe.py, harness/close.sh, harness/protocol_guard.py, STANDING-INSTRUCTIONS.md §2.
