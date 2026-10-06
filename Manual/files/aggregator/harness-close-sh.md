# `harness/close.sh`

Closes a leg after the analyst has run `done.sh` and quit.

## What it holds

`close.sh LEG [--files-only] [--force]`. In order: confirms the launch; runs the trusted close-check; takes the snap; runs the recall probe in a fork and scores it; copies the transcript to `out/_transcripts/`; builds the checkpoint in a temporary folder (the analyst's folder, the run's own sessions from its Claude folder and nothing else of it, the transcript, `cost.json`, `checkpoint.json` with ancestry and validation, a manifest), audits the model that served against `arm.json` (counted by `protocol_guard.py cost`, a forked leg's own messages only), verifies, and publishes atomically with `COMMITTED` last. Then it prints the next step: the dispatch after `packets-out`, the interview command, or the resume leg after a pause, and marks a stage finished when `handback-NN.md` exists and validation is clean. Last it calls `publish.sh`.

## Who writes it, and when

The handler, once per leg, by hand or through the leg handler (`legs.py close`).

## Why it exists

"A leg is checkpointed once." A pause closes without the stage's close-check.

## Where

[harness/close.sh](../../../aggregator/runs/claude-v43-1/CONTROL/harness/close.sh).

Checked against: harness/close.sh, harness/protocol_guard.py, harness/READ-ME-FIRST.md.
