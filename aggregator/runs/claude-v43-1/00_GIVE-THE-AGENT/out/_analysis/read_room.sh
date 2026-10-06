#!/bin/bash
# Stage A1 section 4, one room read in the stage file's order, every read through mem.py (logged).
# part 1: log opened; room --no-canvas; when.
# part f: the forest, from line OFF (default 11), LIM lines (default 220).
# part c: the concepts with their words, from line OFF, LIM lines.
# part 2: the coder's account, from line OFF; at OFF 0 also the brief's first page and the canvas, last.
# usage: bash out/_analysis/read_room.sh <sub> 1|f|c|2 [OFF] [LIM]
S="$1"; P="$2"; M="python3 -W ignore tools/mem.py"
case "$P" in
  1)
    $M log "opened $S" --kind opened --ids "$S" --stage A1 >/dev/null 2>&1
    $M room "$S" --size --stage A1 2>&1 | head -1
    $M room "$S" --no-canvas --stage A1 --limit 3000 2>&1 | grep -v "^note: no placements" | grep -v -E "^  [0-9a-z]{6} +h " | cut -c1-150
    $M when "$S" --stage A1 2>&1 | sed -n '2p;5p' ;;
  f)
    $M forest "$S" --stage A1 --offset "${3:-11}" --limit "${4:-220}" 2>&1 | cut -c1-260 ;;
  c)
    $M codes --sub "$S" --stage A1 --offset "${3:-0}" --limit "${4:-90}" 2>&1 | grep -v "^note: no placements" | cut -c1-6,28-46,66-330 ;;
  2)
    $M case "$S" --stage A1 --offset "${3:-0}" --limit "${4:-120}" 2>&1
    if [ "${3:-0}" = "0" ]; then
      $M brief "$S" --stage A1 --limit 10 2>&1 | cut -c1-300
      $M canvas "$S" --stage A1 --limit 200 2>&1
    fi ;;
esac
