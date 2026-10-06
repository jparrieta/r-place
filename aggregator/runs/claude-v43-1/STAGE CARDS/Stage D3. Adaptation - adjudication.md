# Stage D3. Adaptation: adjudication

Adjudication by element, the model frozen and re-read.

Analyst: `claude-opus-5-5`, effort xhigh. No readers.

## What you type, in order

Every line is typed in Terminal, in the run folder. A leg opens Claude with its first message already sent; when the analyst has closed the leg and stopped, quit Claude (`/exit`) and type the close line. A leg id is the stage, the step letter and a count where the step repeats.

- **D3a element group**: `bash CONTROL/harness/step.sh D3a-01`, then `bash CONTROL/harness/close.sh D3a-01`  (legs D3a-01, D3a-02, ... as many as the work needs)
- Only if the analyst built a re-check (a D3a leg closed at packets-out): `bash CONTROL/harness/dispatch.sh D3` prints the re-check brief for Codex and sends the re-check's verdict packets; wait for `DROPS/D/recheck/DONE` and `out/_fleet_raw/D3v/DONE`; step.sh then runs ingest.py D --recheck
- **D3b recheck**: `bash CONTROL/harness/step.sh D3b`, then `bash CONTROL/harness/close.sh D3b`
- **D3c freeze and re-read**: `bash CONTROL/harness/step.sh D3c`, then `bash CONTROL/harness/close.sh D3c`  *Interview point: the stage's last leg of this step closes at it.*

## Interview point

A leg marked above closes with `--cut interview` and leaves a brief named after the leg, the stage, the step and the minute, in `00_GIVE-THE-AGENT/out/interview/`. After that leg's close, talk with the analyst in a fork run in a copy of its folder as the leg closed (you may add material; nothing reaches the run): `bash CONTROL/harness/interview.sh` (the last interview point) or `bash CONTROL/harness/interview.sh <leg>`. To answer later, write the reply file interview.sh names; the next leg reads it. The run goes on with the next `step.sh` whether or not you interview.

## Pausing

To stop cleanly (the subscription week ending, or any reason): `bash CONTROL/harness/pause.sh`. The analyst stops at its next safe stop and closes with `done.sh D3 --pause`; quit Claude and run the close line as usual. `close.sh` prints the leg to resume with (the same id with `-p2`); it picks up from the head and the diary. To stop at once instead: quit Claude, then `close.sh <leg> --force`.

A close that refuses says why; tell the handler. A stage is finished when `close.sh` prints `stage D3 finished`.

## If you want to read

`00_GIVE-THE-AGENT/out/handback-D3.md` when the stage finishes; `out/_head.md` at any time.

## The one rule

Inside a leg, say nothing to the analyst beyond what the harness sends; questions it has go into its files, and the handler answers them there. Talk freely in an interview: it is a fork and never a leg.
