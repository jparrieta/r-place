#!/bin/bash
# Written by the handler on J's word (27 Oct 23:24 Berlin): the E1 fleet dispatch, run in J's Terminal.
cd "$HOME/Jail/r-place/aggregator/runs/claude-v43-1--C4-field" || exit 1
bash CONTROL/harness/dispatch.sh E1 2>&1 | tee "$HOME/Jail/r-place/aggregator/handler/memory/analysis/dispatch-E1-$(date -u +%Y%m%dT%H%MZ).log"
echo; echo "dispatch finished (exit ${PIPESTATUS[0]}). You can close this window."
