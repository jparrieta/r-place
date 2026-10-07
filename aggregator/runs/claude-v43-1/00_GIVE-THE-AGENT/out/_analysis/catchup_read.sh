#!/bin/bash
# Stage A1 catch-up pass (J's ruling 1): one room's case.md and brief.md, each served whole through mem.py.
# usage: bash out/_analysis/catchup_read.sh <sub> case|brief|check
#   case   logs the room as opened for the pass, then prints case.md whole (--limit above any total)
#   brief  prints brief.md whole
#   check  prints the read log's last entries for the two calls: lines served against the file's total
# One file per call: each is under 30 KB (out/_analysis/catchup-A1.tsv gives the bytes), so the output is
# shown whole. No head, cut or limit below the total.
S="$1"; P="$2"; M="python3 -W ignore tools/mem.py"
case "$P" in
  case)
    $M log "catch-up opened $S (case.md and brief.md, read whole)" --kind opened --ids "$S" --stage A1 >/dev/null 2>&1
    $M case "$S" --stage A1 --limit 100000 2>&1 ;;
  brief)
    $M brief "$S" --stage A1 --limit 100000 2>&1 ;;
  check)
    grep -E "\"verb\": \"(case|brief)\", \"args\": \[\"$S\"\]" out/_mem_reads-A1.jsonl | tail -2 | \
      python3 -c "import sys,json
for l in sys.stdin:
    r=json.loads(l); print(r['verb'], r['args'][0], 'served', r['lines'], 'of', r['total'], 'WHOLE' if r['lines']==r['total'] else 'NOT WHOLE')" ;;
esac
