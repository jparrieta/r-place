# `harness/publish.sh`

Regenerates the Manual and commits the run to git.

## What it holds

`publish.sh LABEL [KIND]`, KIND one of close, interview, pause, finished (`close.sh` passes `interview-point` at an interview cut). It runs `gen_manual.py`, then, if the run sits in a git repository, `git add -A`, commits "<kind> <label>", tags an interview point with its leg and a finished stage with `stage-<ST>`, and pushes when a remote is set.

## Who writes it, and when

`close.sh` and `interview.sh` call it; never typed by hand.

## Why it exists

Its header: a failed push "is reported and never fails the close". The repository's `.gitignore` decides what is committed. It keeps the run's Claude folder, `CONTROL/.cc`, out; each checkpoint's `agent.tar.gz` holds only the run's own sessions from it (`projects/run/`), so no account data is committed ([the handlers](../../6-the-handlers.md)).

## Where

[harness/publish.sh](../../../aggregator/runs/claude-v43-1/CONTROL/harness/publish.sh).

Checked against: harness/publish.sh, harness/close.sh, harness/interview.sh.
