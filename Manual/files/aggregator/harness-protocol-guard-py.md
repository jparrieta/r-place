# `harness/protocol_guard.py`

The handler-side guards: settings, launch, probe, close and checkpoint.

## What it holds

Operations: `settings` (renders `.claude/settings.json` per stage, adding denies for folders beside the run, `INPUT/`, any `.git`, some home folders, and before E1 `out/_probe` and `out/_transcripts`; sets transcript retention to 36,500 days); `prepare`, `confirm`, `launch` (a fresh session id per leg, or a fork from a cut); `preclose` (the trusted validator, run isolated); `probe` (a headless forked turn, tools disallowed); `capture` (the analyst's folder whole, and of the run's Claude folder only `projects/run/`, the run's own sessions), `cost` (a leg's turns, tokens and the models that served, from its transcript; at a forked leg's first close it skips the parent's messages, which the fork copied with their ids, so the model audit reads the leg's own replies; v43.2, 6 October 2026), `verify-checkpoint`, `verify-tree`, `advance`, `arm`, and `locked` (one lock per run).

## Who writes it, and when

`step.sh`, `launch.sh`, `close.sh` and `acceptance.sh` call it; never the analyst.

## Why it exists

An ordinary leg forks the last close's session (`step.sh`); only the run's first leg, or one opened with `--fresh`, is fresh. The E1 wall is held "by the permission rules and by the sandbox, not only by the stage file". It never runs analyst-writable code with the handler's access.

## Where

[harness/protocol_guard.py](../../../aggregator/runs/claude-v43-1/CONTROL/harness/protocol_guard.py).

Checked against: harness/protocol_guard.py, harness/step.sh, harness/close.sh.
