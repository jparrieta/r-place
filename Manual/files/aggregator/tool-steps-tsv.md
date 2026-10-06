# `tools/steps.tsv`

Every stage and step of the run, one per line.

## What it holds

Columns: `stage`, `stage_name`, `step`, `step_name`, `kind` (work, build, check, recheck), `repeat` (no, yes, round, optional), `interview` (`-`, `end`, `mid`). 45 steps from A1a (checks and screen) to E2b (next instrument). Twelve carry an interview point: A1c, B1e, B4c, C1a, C2c (mid), C3c, C4a, C5d, D3c, D4a, D6b, E2b.

## Who writes it, and when

Written with the instrument. Shipped in the analyst's `tools/`; copied into `CONTROL/harness/` by `build.sh`; read by `steps.py`, `stage_cards.py` and `gen_manual.py`.

## Why it exists

Contract §4: "`tools/steps.tsv` lists every step; the stage file says what each does and where it stops." `done.sh` refuses `--cut interview` at a step whose row has no interview point, and `step.sh` refuses a check step until the dispatch has left `DONE`.

## Where

[tools/steps.tsv](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/steps.tsv).

Checked against: tools/steps.tsv, tools/steps.py, tools/done.sh, harness/step.sh, CONTRACT-aggregator.md §4.
