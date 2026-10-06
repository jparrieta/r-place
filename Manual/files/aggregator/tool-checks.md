# `tools/checks/`

One close-check per stage, and the self-test that proves each one fires.

## What it holds

`stage_A1.py` to `stage_E2.py`, eighteen handlers pinned by name, and `selftest.py`. Each handler checks the shape of its stage's files: existence, parse, ids that resolve, counts that reconcile. Each module lists `PLANTED` cases, a minimal passing fixture plus one defect, and `selftest.py` runs each in a fresh temporary folder with its own small store and reports whether the planted defect fired.

## Who writes it, and when

Written with the instrument. Shipped in the analyst's `tools/`; `build.sh` copies a trusted set to `CONTROL/harness/validation_tools/checks/`.

## Why it exists

`validate.py`: "Each handler is written from the stage file's Outputs block and its Close section"; "A stage with no handler closes unvalidated and the report says so." `selftest.py`: "A check that does not fire on its own planted defect is a defect in the package." Each handler says it "cannot check whether a judgement is right."

## Where

[tools/checks/](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/checks/).

Checked against: tools/checks/selftest.py, tools/checks/stage_A1.py, tools/validate.py, harness/build.sh.
