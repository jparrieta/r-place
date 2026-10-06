# `tools/validate.py`

The close-check of every leg and the open-check of every launch.

## What it holds

Four modes: `validate.py NN` (the close-check, run by `done.sh`); `--open NN` (at the open: every input the stage file's header declares is found, the startup counts from `counts.py` are printed, and `links.py` runs over the head and the questions); `--links`; `--self-test [--summary]` (every check fires on its own planted defect). It exits 1 on any ERROR; warnings never fail a leg. One handler per stage lives in `tools/checks/stage_NN.py`.

## Who writes it, and when

Shipped in the analyst's `tools/`. The harness keeps a trusted copy in `CONTROL/harness/validation_tools/`, which `close.sh` runs so that analyst-writable code is never run with the handler's access.

## Why it exists

Its docstring: it "checks a run, not the instrument", and "a clean report is not evidence about the analysis." A check keyed on the analysed set refuses when `rooms.jsonl` or `dropped.jsonl` is absent, since "an empty frame passes every membership test". A1 runs the self-test once and pastes it into `notes-A1.md`.

## Where

[tools/validate.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/validate.py).

Checked against: tools/validate.py, harness/build.sh, harness/protocol_guard.py, stages/STAGE-A1-reading-room-notes.md.
