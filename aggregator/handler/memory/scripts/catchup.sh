#!/bin/bash
# one catch-up tick: the usual tick, then restart the list from the next block if the handler halted it after a close
cd $HOME/mnt/Jail/r-place; RUN=claude-v43-1; R=aggregator/runs/$RUN; P=aggregator/handler/claude-adapter/legs.py
$HOME/tick.sh ${1:-50}
ST="$(python3 $P status $RUN | sed -n '4p')"
if echo "$ST" | grep -q "list: completed\|list: stopped"; then
  if echo "$ST" | grep -q "Stage A1 finished at A1.A1b-"; then
    N=$(echo "$ST" | grep -o 'next: A1b-[0-9]*' | grep -o '[0-9]*$')
    if [ -n "$N" ] && [ "$N" -le 48 ]; then
      if [ -f $HOME/catchup.pause ]; then echo "PAUSED by J: not restarting; next is A1b-$N"
        L=$(grep "closed A1.A1b-" $R/CONTROL/legs/events.log | tail -1 | cut -c1-120)
        grep -q "paused before A1b-$N" aggregator/handler/memory/diary.md || echo "- $(date -u +%Y-%m-%d\ %H:%M) $L; paused before A1b-$N (J)." >> aggregator/handler/memory/diary.md
        exit 0; fi
      echo "RESTART from A1b-$N"; timeout 100 python3 $P run $RUN A1b-$N..A1b-48 | head -2
      L=$(grep "closed A1.A1b-" $R/CONTROL/legs/events.log | tail -1 | cut -c1-120)
      echo "- $(date -u +%Y-%m-%d\ %H:%M) $L; restarted at A1b-$N." >> aggregator/handler/memory/diary.md
    fi
  else echo "STOPPED (not a catch-up halt): $ST"; fi
fi
