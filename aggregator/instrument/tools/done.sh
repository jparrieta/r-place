#!/usr/bin/env bash
# done.sh NN [--cut <name> | --cut interview | --pause] : the leg's one exit (STANDING-INSTRUCTIONS §2).
# --pause closes the leg at a safe stop without the close-check (the stage's work is half done by
# design); the head and the diary carry where to pick up, and the next leg continues from them.
# Runs, in order: the close-check; links; the head's ceiling; gen_views; the leg record; and
# marks the leg closed. Exits non-zero, and does not close the leg, when a check fails. The snap
# and the recall probe run afterwards in the harness's close.sh, outside your session.
set -u
STAGE="$(printf '%s' "${1:?stage}" | tr '[:lower:]' '[:upper:]')"; shift || true
CUT=""; PAUSE=0
if [ "${1:-}" = "--cut" ]; then CUT="${2:?cut name}"; fi
if [ "${1:-}" = "--pause" ]; then PAUSE=1; CUT="pause"; fi
ROOT="${ROOT:-.}"; OUT="${OUT:-$ROOT/out}"; TOOLS="$(cd "$(dirname "$0")" && pwd)"
LEG="$(cat "$ROOT/.leg" 2>/dev/null || echo "$STAGE-leg")"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$OUT/_closes"
echo "done.sh $STAGE leg=$LEG cut=${CUT:-none} $STAMP"

# 1. close-check (validate.py NN), if the validator exists; a failure leaves the leg open.
#    A pause skips it: the leg stops at a safe stop, not at the end of its work.
if [ "$PAUSE" -eq 1 ]; then
  # the pause line of THIS leg: where to pick up (the working hypothesis and the next room or item)
  if ! python3 -c '
import glob, json, sys
out, stage, leg = sys.argv[1:4]
for p in glob.glob("%s/diary/%s-*.jsonl" % (out, stage)):
    for l in open(p, encoding="utf-8"):
        try:
            r = json.loads(l)
        except ValueError:
            continue
        if r.get("kind") == "pause" and r.get("leg") == leg:
            sys.exit(0)
sys.exit(1)
' "$OUT" "$STAGE" "$LEG"
  then
    echo "no pause line for leg $LEG. Log where to pick up first: mem.py log \"<working hypothesis>; next: <room or item>\" --kind pause; then done.sh $STAGE --pause again. The leg stays open."
    exit 1
  fi
fi
# 0b. an interview point (--cut interview) is a step the stage marks for one (tools/steps.tsv). It
#     needs its brief, out/interview/<leg>.md; at a stage's end, the handback too. The brief is then
#     filed under the leg, the stage, the step and the minute: <leg>_<stage>_<step>_<YYYY-MM-DDTHH-MM>.md
case "$CUT" in
  interview)
    INFO="$(python3 "$TOOLS/steps.py" check "$LEG" --stage "$STAGE")" || { echo "the leg id $LEG does not parse; the leg stays open"; exit 1; }
    IV="$(printf '%s' "$INFO" | cut -f3)"; LBL="$(printf '%s' "$INFO" | cut -f5)"
    [ "$IV" = end ] || [ "$IV" = mid ] || { echo "leg $LEG's step has no interview point (tools/steps.tsv); close without --cut interview"; exit 1; }
    [ -s "$OUT/interview/$LEG.md" ] || { echo "an interview point needs its brief at out/interview/$LEG.md (under 800 words); the leg stays open"; exit 1; }
    if [ "$IV" = end ] && [ ! -s "$OUT/handback-$STAGE.md" ]; then
      echo "this interview point ends stage $STAGE: write out/handback-$STAGE.md first; the leg stays open"; exit 1
    fi ;;
  interview-*) echo "the interview cut is --cut interview (the brief is out/interview/$LEG.md)"; exit 1;;
esac
if [ "$PAUSE" -eq 0 ] && [ -f "$TOOLS/validate.py" ]; then
  if ! python3 "$TOOLS/validate.py" "$STAGE" "$ROOT" "$OUT" > "$OUT/_closes/$STAGE-$LEG-$STAMP.validate.txt" 2>&1; then
    echo "close-check FAILED; the leg stays open. Report: $OUT/_closes/$STAGE-$LEG-$STAMP.validate.txt"
    tail -20 "$OUT/_closes/$STAGE-$LEG-$STAMP.validate.txt"
    exit 1
  fi
fi
# 1b. links: every id in the head, the questions and the views resolves
python3 "$TOOLS/links.py" --root "$ROOT" --out "$OUT" || { [ "$PAUSE" -eq 1 ] && echo "note: unresolved links, carried to the next leg" || { echo "unresolved links; the leg stays open"; exit 1; }; }
# 1c. the head's ceiling
if [ -f "$OUT/_head.md" ]; then
  W=$(wc -w < "$OUT/_head.md"); if [ "$W" -gt 3200 ]; then echo "_head.md is $W words (ceiling 3,000); the leg stays open"; exit 1; fi
fi
# 2. views
python3 "$TOOLS/gen_views.py" "$STAGE" --root "$ROOT" --out "$OUT" || [ "$PAUSE" -eq 1 ] || exit 1
# 4. tokens: the harness leaves the leg's totals in .tokens.json; recorded into RUN.json
if ! python3 -c '
import json, os, sys
root, out, stage, leg, stamp, cut = sys.argv[1:7]
p = os.path.join(root, "RUN.json"); run = json.load(open(p)) if os.path.exists(p) else {}
tok = os.path.join(root, ".tokens.json"); t = json.load(open(tok)) if os.path.exists(tok) else {}
run.setdefault("legs", []).append({"stage": stage, "leg": leg, "closed_utc": stamp, "cut": cut or None,
                                   "tokens": t, "session": open(os.path.join(root, ".session")).read().strip() if os.path.exists(os.path.join(root, ".session")) else None})
json.dump(run, open(p, "w"), indent=1)
' "$ROOT" "$OUT" "$STAGE" "$LEG" "$STAMP" "$CUT"; then
  echo "leg record FAILED; the leg stays open"
  exit 1
fi
# 5. file the interview brief under the leg, the stage, the step and the minute (local time)
if [ "$CUT" = interview ]; then
  mv "$OUT/interview/$LEG.md" "$OUT/interview/${LBL}_$(date +%Y-%m-%dT%H-%M).md"
fi
# 5b. the model frozen: at the last step of C5, D3 and D6 the model's hash is recorded (vlib.model_hash);
#     stage D1 serves only this version, and a later change without an amendment is a defect
case "$LEG" in D1*)                    # prior.md §7 and §8 sealed at D1's close (stage D1)
  [ "$PAUSE" -eq 0 ] && [ -f "$OUT/prior.md" ] && python3 -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$OUT/prior.md" > "$OUT/_closes/prior-D1.sha256";;
esac
case "$LEG" in C5d*|D3c*|D6b*)
  if [ -z "$CUT" ] || [ "$CUT" = interview ]; then
    python3 -c 'import sys; sys.path.insert(0, sys.argv[1]); import vlib; h = vlib.model_hash(sys.argv[2]); print(h or "")' "$TOOLS" "$OUT" > "$OUT/_closes/model-$STAGE.sha256"
    echo "model frozen at $LEG: $(cat "$OUT/_closes/model-$STAGE.sha256")"
  fi;;
esac
# 6. mark closed
echo "$STAMP ${CUT:-close}" >> "$OUT/_closes/$STAGE-$LEG.closed"
echo "leg $LEG closed${CUT:+ at cut $CUT}. Stop now; the harness takes the snap and runs the probe."
