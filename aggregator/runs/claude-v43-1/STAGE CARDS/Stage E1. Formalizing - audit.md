# Stage E1. Formalizing: audit

The audit: the run as only the logs can tell it, then the analyst's own account.

Analyst: `claude-opus-5-5`, effort medium. Readers: `@preset/cheap`, through the gateway, 1 per packet.

## What you type, in order

Every line is typed in Terminal, in the run folder. A leg opens Claude with its first message already sent; when the analyst has closed the leg and stopped, quit Claude (`/exit`) and type the close line. A leg id is the stage, the step letter and a count where the step repeats.

- Before E1 opens: `python3 check_quotes.py` in the handler's folder (the yard's path in paths.json) writes `run/DROPS/E1/quote-check-E1.json`, which the stage reads
- **E1a scripts**: `bash CONTROL/harness/step.sh E1a`, then `bash CONTROL/harness/close.sh E1a`
- **E1b audit section**: `bash CONTROL/harness/step.sh E1b-01`, then `bash CONTROL/harness/close.sh E1b-01`  (legs E1b-01, E1b-02, ... as many as the work needs)
- **E1c reconstruction build**: `bash CONTROL/harness/step.sh E1c`, then `bash CONTROL/harness/close.sh E1c`
- `bash CONTROL/harness/dispatch.sh E1` (the reconstruction readers)
- **E1d reconstruction check**: `bash CONTROL/harness/step.sh E1d`, then `bash CONTROL/harness/close.sh E1d`
- **E1e experience**: `bash CONTROL/harness/step.sh E1e`, then `bash CONTROL/harness/close.sh E1e`

## Pausing

To stop cleanly (the subscription week ending, or any reason): `bash CONTROL/harness/pause.sh`. The analyst stops at its next safe stop and closes with `done.sh E1 --pause`; quit Claude and run the close line as usual. `close.sh` prints the leg to resume with (the same id with `-p2`); it picks up from the head and the diary. To stop at once instead: quit Claude, then `close.sh <leg> --force`.

A close that refuses says why; tell the handler. A stage is finished when `close.sh` prints `stage E1 finished`.

## If you want to read

`00_GIVE-THE-AGENT/out/handback-E1.md` when the stage finishes; `out/_head.md` at any time.

## The one rule

Inside a leg, say nothing to the analyst beyond what the harness sends; questions it has go into its files, and the handler answers them there. Talk freely in an interview: it is a fork and never a leg.
