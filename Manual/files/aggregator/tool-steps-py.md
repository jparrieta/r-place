# `tools/steps.py`

Parses stage and leg ids against `steps.tsv`.

## What it holds

Commands: `check <leg>` (one line: stage, kind, interview, round, label; or exit 1); `stages`; `steps <stage>`; `label <leg>` (for example `B1b-03_coding-third-order-scheme_getting-lost`); `name <stage>`; `first <stage> <kind>`. A leg id is the stage, the step letter, and a count where the step repeats: `B1a`, `B1b-03`, `B2a-r1`, `D1a-02`, and `-p2` for a leg continued after a pause.

## Who writes it, and when

Shipped in the analyst's `tools/`. `build.sh` copies it with `steps.tsv` into `CONTROL/harness/`, where `lib.sh` uses it; `done.sh` uses it to check an interview cut.

## Why it exists

STANDING §2: "The harness names the leg in your first message and in `.leg`; every snap, probe and checkpoint carries that name." READ-ME-FIRST: a leg id that does not name a step of its stage is refused.

## Where

[tools/steps.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/steps.py).

Checked against: tools/steps.py, harness/lib.sh, tools/done.sh, STANDING-INSTRUCTIONS.md §2, harness/READ-ME-FIRST.md.
