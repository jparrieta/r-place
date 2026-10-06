# Stage B2. Coding: pilot

The pilot: fresh readers test the scheme; the scheme is frozen.

Analyst: `claude-opus-5-5`, effort medium. Readers: `@preset/cheap`, through the gateway, 3 per packet.

## What you type, in order

Every line is typed in Terminal, in the run folder. A leg opens Claude with its first message already sent; when the analyst has closed the leg and stopped, quit Claude (`/exit`) and type the close line. A leg id is the stage, the step letter and a count where the step repeats.

- **B2a build round**: `bash CONTROL/harness/step.sh B2a-r1`, then `bash CONTROL/harness/close.sh B2a-r1`  (legs B2a-r1, B2a-r2, ... one per pilot round)
- `bash CONTROL/harness/dispatch.sh B2 --round K` (the readers of round K; your Keychain; the analyst is not running)
- **B2b check round**: `bash CONTROL/harness/step.sh B2b-r1`, then `bash CONTROL/harness/close.sh B2b-r1`  (legs B2b-r1, B2b-r2, ... one per pilot round)
- **B2c gold and stability build**: `bash CONTROL/harness/step.sh B2c`, then `bash CONTROL/harness/close.sh B2c`
- `bash CONTROL/harness/dispatch.sh B2 --round gold`, then `--round stab-1` and `--round stab-2` (the gold and stability readers on the frozen scheme)
- **B2d gold and stability check**: `bash CONTROL/harness/step.sh B2d`, then `bash CONTROL/harness/close.sh B2d`

## Pausing

To stop cleanly (the subscription week ending, or any reason): `bash CONTROL/harness/pause.sh`. The analyst stops at its next safe stop and closes with `done.sh B2 --pause`; quit Claude and run the close line as usual. `close.sh` prints the leg to resume with (the same id with `-p2`); it picks up from the head and the diary. To stop at once instead: quit Claude, then `close.sh <leg> --force`.

A close that refuses says why; tell the handler. A stage is finished when `close.sh` prints `stage B2 finished`.

## If you want to read

`00_GIVE-THE-AGENT/out/handback-B2.md` when the stage finishes; `out/_head.md` at any time.

## The one rule

Inside a leg, say nothing to the analyst beyond what the harness sends; questions it has go into its files, and the handler answers them there. Talk freely in an interview: it is a fork and never a leg.
