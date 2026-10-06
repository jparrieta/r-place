# `harness/pause.sh`

Asks the analyst to stop at its next safe stop.

## What it holds

`pause.sh [--clear]` writes `00_GIVE-THE-AGENT/.pause` with the time and logs `pause-requested` in `handover-events.log`; `--clear` removes the request.

## Who writes it, and when

The handler, when the subscription week is running out or the run must stop cleanly.

## Why it exists

STANDING §2: at every safe stop the analyst checks `ls .pause`; if it is there it logs its working hypothesis and the next room or item (`--kind pause`), updates the head, and closes with `done.sh NN --pause`. "A pause is never a judgement on the work." `close.sh` then prints the resume leg (the same id with `-p2`); `step.sh` clears `.pause` at every new leg.

## Where

[harness/pause.sh](../../../aggregator/runs/claude-v43-1/CONTROL/harness/pause.sh).

Checked against: harness/pause.sh, STANDING-INSTRUCTIONS.md §2, tools/done.sh, harness/close.sh, harness/step.sh.
