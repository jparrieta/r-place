# `stages/`

The stage files, handed to the analyst one stage at a time.

## What it holds

Eighteen files, from `STAGE-A1-reading-room-notes.md` to `STAGE-E2-formalizing-feedback.md`. Each opens with a header: model and effort, legs, steps, safe stops, the startup packet, reads allowed and forbidden, outputs. Numbered sections follow, then the moments to log and the final message in one of rule 17's two forms. A1's file, for example, gives the fixed form of a room note. The folder is empty at the start.

## Who writes it, and when

`build.sh` copies each file into `DROPS/<stage>/stages/` and lists it in `DROPS/ORDER.tsv`. `step.sh` copies the drop into the analyst's folder at the stage's first leg, and refuses to open a stage whose previous stage has not finished unless forced (logged as `forced-order` in `handover-events.log`).

## Why it exists

Contract §4: "You are handed one stage at a time, and the stage's whole file at its first leg." AGENT.md: the analyst has not seen any later stage "and must not guess it". `validate.py --open` reads the header to check that every declared input exists.

## Where

[stages/](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/stages/) in the analyst's folder; sources in [aggregator/instrument/stages/](../../../aggregator/instrument/stages/).

Checked against: harness/build.sh, harness/step.sh, CONTRACT-aggregator.md §4, AGENT.md, tools/validate.py, stages/STAGE-A1-reading-room-notes.md.
