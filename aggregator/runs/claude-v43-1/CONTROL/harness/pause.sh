#!/usr/bin/env bash
# pause.sh [--clear]   Ask the analyst to stop at its next safe stop.
#   Writes 00_GIVE-THE-AGENT/.pause. At every safe stop the stage file names, the analyst checks
#   for it; when it is there, the analyst logs where to pick up and closes the leg with
#   `done.sh NN --pause`. Then quit Claude and run close.sh as usual: the checkpoint is published
#   as paused and the next leg (step.sh <leg>-p2, which close.sh prints) picks up from the head and the diary.
#   Use it when the subscription week is running out, or whenever you need the run to stop cleanly.
#   If you must stop at once, quit Claude, then close.sh LEG --force; the diary still holds
#   everything the analyst logged.
set -eu
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
RUN="$(harness_run_dir)"; AG="$RUN/00_GIVE-THE-AGENT"
if [ "${1:-}" = "--clear" ]; then rm -f "$AG/.pause"; echo "pause request cleared"; exit 0; fi
printf 'pause requested %s\n' "$(NOW)" > "$AG/.pause"
printf '%s\tpause-requested\n' "$(NOW)" >> "$RUN/CONTROL/handover-events.log"
echo "Pause requested. The analyst stops at its next safe stop and closes with done.sh --pause."
