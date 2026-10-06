# `harness/launch.sh`

Starts the analyst's Claude session for a prepared leg.

## What it holds

Six lines: it runs `protocol_guard.py launch` under the run's lock. The launch starts `claude` in `00_GIVE-THE-AGENT/` with the session id `step.sh` prepared, `--model` and `--effort` from `arm.json`, `--strict-mcp-config`, and the leg's first message; the config folder is `CONTROL/.cc`, helpers run on the leg's model, and auto memory is off.

## Who writes it, and when

`step.sh`, always; never typed by hand.

## Why it exists

Its comment: "The analyst sees only 00_GIVE-THE-AGENT/." `protocol_guard.py` sets `CLAUDE_CODE_DISABLE_AUTO_MEMORY` with the note "no Claude auto-memory: what carries between legs is the forked conversation and the folder".

## Where

[harness/launch.sh](../../../aggregator/runs/claude-v43-1/CONTROL/harness/launch.sh).

Checked against: harness/launch.sh, harness/protocol_guard.py, harness/step.sh.
