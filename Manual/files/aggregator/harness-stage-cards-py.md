# `harness/stage_cards.py`

Writes `STAGE CARDS/`, one card per stage for the person running it.

## What it holds

Each card: what the stage is for (one line per stage in the script), the lines to type in order for every leg and dispatch, where an interview point falls and how to talk at it, pausing, and the rule to say nothing to the analyst inside a leg. Generated from `steps.tsv`, the script's notes, `arm.json` and `DROPS/ORDER.tsv`.

## Who writes it, and when

`build.sh`, once, at build.

## Why it exists

Its docstring: "never edited by hand". Contract §4: "the operator's stage cards launch them one at a time."

## Where

[harness/stage_cards.py](../../../aggregator/runs/claude-v43-1/CONTROL/harness/stage_cards.py).

Checked against: harness/stage_cards.py, harness/build.sh, CONTRACT-aggregator.md §4.
