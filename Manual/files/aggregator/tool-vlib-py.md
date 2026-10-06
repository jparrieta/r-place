# `tools/vlib.py`

The shared library of the close-checks.

## What it holds

Helpers that `validate.py` and every `tools/checks/stage_*.py` import: error and warning collectors (E, W), and readers such as `jsonl`, `text` and `need`. Errors and warnings are folded by shape at the end, so a per-line check over thousands of lines prints one line per shape with a count and the first instance.

## Who writes it, and when

Shipped in the analyst's `tools/`; `build.sh` also puts a trusted copy in `CONTROL/harness/validation_tools/`.

## Why it exists

Its docstring: "what every close-check shares." The folding keeps a close report readable when one defect repeats over a whole ledger. Beyond this, its purpose is not stated in the sources.

## Where

[tools/vlib.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/vlib.py).

Checked against: tools/vlib.py, tools/checks/stage_A1.py, harness/build.sh.
