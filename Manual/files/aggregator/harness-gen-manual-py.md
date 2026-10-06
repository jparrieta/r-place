# `harness/gen_manual.py`

Writes the run's Manual, a set of Markdown pages GitHub renders.

## What it holds

`Manual/README.md` (the run at a glance, how to start a run, how to talk to any leg) and `Manual/stages/<ST>.md` per stage (what the stage produces and its model, from the contract's stage table; its card, its stage file, its handback; and every leg closed: when, how it closed, its brief, its transcript, the command that reopens it as a read-only fork, its interviews). The Manual's other pages are written in `Manual/` itself; this script writes only the front page and the stage pages. It reads `CONTROL/arm.json` for each leg's model and effort (the stage's entry, then the leg's override, as the launch reads them), the contract's stage table, `CONTROL/snapshots/INDEX.tsv`, `CONTROL/interviews.tsv`, `steps.tsv`, `out/_closes/*.closed`, `out/_transcripts/`, `out/interview/` and `out/handback-*.md`.

## Who writes it, and when

`build.sh` once, then `publish.sh` at every close and interview.

## Why it exists

Its docstring: "Regenerated at every close and every interview ... never edited by hand." The Manual sits at the repository root beside `Instrument/`.

## Where

[harness/gen_manual.py](../../../aggregator/runs/claude-v43-1/CONTROL/harness/gen_manual.py).

Checked against: harness/gen_manual.py, harness/publish.sh, harness/build.sh.
