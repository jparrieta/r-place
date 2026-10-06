# `AGENT.md`

The analyst's first page: who it is, what the folder holds, and what one session may do.

## What it holds

Three parts. **What is here** lists the root documents (the contract, METHOD.md, STANDING-INSTRUCTIONS.md, then FLEET.md and SCHEMA-adaptations.md when their stages come), `stages/`, `package/` and `trees/` (read-only, with the canvas in `package/` from the start), `tools/`, and `out/`, whose `_probe/` and `_transcripts/` are the harness's. **State** says the stages completed are the files in `stages/` with their outputs in `out/`, and that every leg starts from the startup packet: the head, the stage file, the last five diary entries and `validate.py --open NN`. **This session** says: one leg, then `done.sh`; do not begin the next leg or stage, and do not summarise it.

## Who writes it, and when

Written with the instrument. `build.sh` copies it into `00_GIVE-THE-AGENT/` before stage A1. The first message `step.sh` writes for every leg begins "Read AGENT.md."

## Why it exists

It fixes the one-leg-per-session shape that STANDING-INSTRUCTIONS §2 describes and closes the world: "There is nothing outside this directory." It tells the analyst to read the contract once, whole, at A1 and by section afterwards (`mem.py contract --section <n>`), and says the analyst has not seen any later stage "and must not guess it".

## Where

[AGENT.md](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/AGENT.md) in the analyst's folder; source [aggregator/instrument/AGENT.md](../../../aggregator/instrument/AGENT.md).

Checked against: AGENT.md, harness/build.sh, harness/step.sh.
