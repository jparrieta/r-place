# `harness/build.sh`

Lays out a run from the instrument and the coders' documents, once.

## What it holds

It writes `00_GIVE-THE-AGENT/` (the eight root documents, `tools/` less the handler's and the build scripts, `package/` and `trees/` with the store built by `build_store.py`, `transitions.py` and `relations.py`, the canvas joined when `INPUT/canvas/` is whole, neighbours when the atlas is there, and empty `stages/`, `shelves/`, `out/`); `DROPS/ORDER.tsv` and `DROPS/NN/` (each stage file and shelf, SCHEMA and the handoff templates at D1, the design note at E2); `CONTROL/harness/` with `validation_tools/`; `arm.json`, `RUN.json` (with the instrument's fingerprint), `sessions.json`; `STAGE CARDS/`; the Manual; `READ-ME-FIRST.md`.

## Who writes it, and when

The handler, once, before stage A1: `build.sh <run folder> --input <run folder>/INPUT/coders`. On a fresh run `--input` is required, since the store is built from it; the canvas is joined only if `<run folder>/INPUT/canvas/` is already in place, so copy `INPUT/` in first. It refuses a folder inside an Obsidian vault and a run that has begun. Build outside a git clone: the run's first close commits and pushes whatever repository it sits in ([the front page](../../README.md#start-a-run-of-your-own)).

## Why it exists

It refuses a run that has begun ("A run is built once") and a run inside the vault. The trusted copies in `validation_tools/` are what `close.sh` and `dispatch.sh` run.

## Where

[harness/build.sh](../../../aggregator/handler/claude/build.sh); source [aggregator/handler/claude/build.sh](../../../aggregator/handler/claude/build.sh).

Checked against: harness/build.sh.
