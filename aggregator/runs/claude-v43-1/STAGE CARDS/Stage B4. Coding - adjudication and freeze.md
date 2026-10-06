# Stage B4. Coding: adjudication and freeze

Adjudication, the blind sample and the codebook frozen.

Analyst: `claude-opus-5-5`, effort xhigh. Readers: `@preset/cheap`, through the gateway, 2 per packet.

## What you type, in order

Every line is typed in Terminal, in the run folder. A leg opens Claude with its first message already sent; when the analyst has closed the leg and stopped, quit Claude (`/exit`) and type the close line. A leg id is the stage, the step letter and a count where the step repeats.

- **B4a adjudicate packet**: `bash CONTROL/harness/step.sh B4a-01`, then `bash CONTROL/harness/close.sh B4a-01`  (legs B4a-01, B4a-02, ... as many as the work needs)
- **B4b sample build**: `bash CONTROL/harness/step.sh B4b`, then `bash CONTROL/harness/close.sh B4b`
- `bash CONTROL/harness/dispatch.sh B4` (the blind sample's readers)
- **B4c check and final placements**: `bash CONTROL/harness/step.sh B4c`, then `bash CONTROL/harness/close.sh B4c`  *Interview point: the stage's last leg of this step closes at it.*

## Interview point

A leg marked above closes with `--cut interview` and leaves a brief named after the leg, the stage, the step and the minute, in `00_GIVE-THE-AGENT/out/interview/`. After that leg's close, talk with the analyst in a fork run in a copy of its folder as the leg closed (you may add material; nothing reaches the run): `bash CONTROL/harness/interview.sh` (the last interview point) or `bash CONTROL/harness/interview.sh <leg>`. To answer later, write the reply file interview.sh names; the next leg reads it. The run goes on with the next `step.sh` whether or not you interview.

## Pausing

To stop cleanly (the subscription week ending, or any reason): `bash CONTROL/harness/pause.sh`. The analyst stops at its next safe stop and closes with `done.sh B4 --pause`; quit Claude and run the close line as usual. `close.sh` prints the leg to resume with (the same id with `-p2`); it picks up from the head and the diary. To stop at once instead: quit Claude, then `close.sh <leg> --force`.

A close that refuses says why; tell the handler. A stage is finished when `close.sh` prints `stage B4 finished`.

## If you want to read

`00_GIVE-THE-AGENT/out/handback-B4.md` when the stage finishes; `out/_head.md` at any time.

## The one rule

Inside a leg, say nothing to the analyst beyond what the harness sends; questions it has go into its files, and the handler answers them there. Talk freely in an interview: it is a fork and never a leg.
