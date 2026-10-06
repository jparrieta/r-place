# Stage D5. Forming: branch accounts

The branch accounts.

Analyst: `claude-opus-5-5`, effort xhigh. No readers.

## What you type, in order

Every line is typed in Terminal, in the run folder. A leg opens Claude with its first message already sent; when the analyst has closed the leg and stopped, quit Claude (`/exit`) and type the close line. A leg id is the stage, the step letter and a count where the step repeats.

- **D5a branch**: `bash CONTROL/harness/step.sh D5a-01`, then `bash CONTROL/harness/close.sh D5a-01`  (legs D5a-01, D5a-02, ... as many as the work needs)
- **D5b waterfall and survival**: `bash CONTROL/harness/step.sh D5b`, then `bash CONTROL/harness/close.sh D5b`

## Pausing

To stop cleanly (the subscription week ending, or any reason): `bash CONTROL/harness/pause.sh`. The analyst stops at its next safe stop and closes with `done.sh D5 --pause`; quit Claude and run the close line as usual. `close.sh` prints the leg to resume with (the same id with `-p2`); it picks up from the head and the diary. To stop at once instead: quit Claude, then `close.sh <leg> --force`.

A close that refuses says why; tell the handler. A stage is finished when `close.sh` prints `stage D5 finished`.

## If you want to read

`00_GIVE-THE-AGENT/out/handback-D5.md` when the stage finishes; `out/_head.md` at any time.

## The one rule

Inside a leg, say nothing to the analyst beyond what the harness sends; questions it has go into its files, and the handler answers them there. Talk freely in an interview: it is a fork and never a leg.
