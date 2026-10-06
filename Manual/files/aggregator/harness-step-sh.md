# `harness/step.sh`

Opens one leg: delivers the stage, writes the first message, and launches the analyst continuing the last close's conversation (a fork of its session; fresh only for the run's first leg or with `--fresh`).

## What it holds

`step.sh LEG [--prepare] [--fresh] [--from-cut LABEL] [--force-order] [--reopen] [--api-ok]`. `--fresh` opens a fresh session and `--reopen` a leg the analyst already closed, each logged as a departure. It checks the leg id and the arm; refuses an API key or a gateway route in the shell; renders the settings; at a stage's first leg copies `DROPS/NN/` into the analyst's folder, refusing if the previous stage is unfinished unless forced; holds a check leg until the dispatch has left `DONE`; clears `.pause`; writes `.stage` and `.leg`; writes the first message (the reading order, and lines for a failed last close, an interview reply, the readers' files); records the session; calls `launch.sh`. With `--prepare` it stops before the launch: the leg handler (`legs.py`) then runs the turn headless. At stage E2a it copies every interview listed in `CONTROL/interviews.tsv` into the analyst's `handling/interviews/`.

## Who writes it, and when

The handler, once per leg.

## Why it exists

Since v40 (2026-10-02) every ordinary leg forks the last committed close's session, as the OpenAI copy does; `--fresh` opens a fresh session and is logged in RUN.json as a departure. With `--from-cut` the leg opens as a fork of a named cut's checkpoint, and only from the last close: once a later leg has closed, the live folder is no longer the cut's, and that state is talked to through `interview.sh`, in a copy of its own. `step.sh` also writes `.stagefile`, the one stage file `DROPS/ORDER.tsv` names, which `validate.py` and the compaction hook read.

## Where

[harness/step.sh](../../../aggregator/runs/claude-v43-1/CONTROL/harness/step.sh).

Checked against: harness/step.sh, harness/lib.sh, harness/protocol_guard.py, harness/READ-ME-FIRST.md.
