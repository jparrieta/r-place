# `tools/done.sh`

The leg's one exit.

## What it holds

`done.sh NN [--cut <name> | --cut interview | --pause]`. In order: for a pause, it requires a `pause` diary line for this leg; for an interview cut, it requires the step to have an interview point, the brief `out/interview/<leg>.md`, and at a stage's end `handback-NN.md`; the close-check (`validate.py NN`, skipped on a pause), with its report in `out/_closes/`; `links.py`; the head's ceiling (refused above 3,200 words); `gen_views.py`; the leg's line in `RUN.json`; the brief filed under leg, stage, step and minute; a `.closed` marker. Any failure leaves the leg open.

## Who writes it, and when

Shipped in the analyst's `tools/`; the analyst runs it at the end of each leg.

## Why it exists

STANDING §2: "The exit is `done.sh NN`", and "A leg that fails the close-check is not closed." The snap and the probe run after it in `close.sh`, outside the session.

## Where

[tools/done.sh](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/done.sh).

Checked against: tools/done.sh, STANDING-INSTRUCTIONS.md §2, CLAUDE.md, harness/close.sh.
