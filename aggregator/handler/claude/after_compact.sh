#!/usr/bin/env bash
# after_compact.sh: the SessionStart hook (matcher "compact") after a compaction of the analyst's
# context. It lives in CONTROL/harness, where the analyst cannot edit it, and prints a short
# instruction: hook output over about 10,000 characters is cut to a preview, so the head and the
# stage file are named for the analyst to Read, never pasted.
AG="$(cd "$(dirname "$0")/../.." && pwd -P)/00_GIVE-THE-AGENT"
NN="$(cat "$AG/.stage" 2>/dev/null)"; LEG="$(cat "$AG/.leg" 2>/dev/null)"
F="$(cat "$AG/.stagefile" 2>/dev/null)"   # step.sh writes it from DROPS/ORDER.tsv
if [ -z "$F" ] || [ ! -f "$AG/$F" ]; then
  F="$(cd "$AG" && ls stages/STAGE-"$NN"-*.md 2>/dev/null)"
  [ "$(printf '%s\n' "$F" | grep -c .)" -eq 1 ] || F=""      # ambiguous or none: name no file rather than a wrong one
fi
# the gate: pretool_guard.py refuses every other call until the head, the stage file and the diary are read
printf '{"t": "%s", "stage": "%s", "leg": "%s", "done": [], "refused": 0}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$NN" "$LEG" > "$(dirname "$0")/../.compact-gate.json"
cat <<MSG
Your context was compacted during stage ${NN:-?}, leg ${LEG:-?}. Before any other step (the harness refuses
other calls until these are done):
1. Read out/_head.md in full.
2. Read ${F:-your stage file under stages/} in full.
3. Run: python3 tools/mem.py diary --last 5
4. Reconcile the head with the diary, then log it: python3 tools/mem.py log "compacted; head reconciled" --kind note
Then continue the leg where the diary says you stopped.
MSG
# stages A1 and B1: the next room comes from the files, never from the summary of the compacted context
if [ "$NN" = "A1" ] || [ "$NN" = "B1" ]; then
  NEXT="$(cd "$AG" && python3 tools/mem.py next --stage "$NN" 2>&1 | head -2)"
  [ -n "$NEXT" ] && printf '\nThe reading order is on disk, not in your summary. From python3 tools/mem.py next --stage %s:\n%s\nRead that room next, whatever the summary says.\n' "$NN" "$NEXT"
fi
