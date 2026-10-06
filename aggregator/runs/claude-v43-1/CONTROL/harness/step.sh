#!/usr/bin/env bash
# step.sh LEG [--prepare] [--from-cut LABEL] [--fresh] [--force-order] [--api-ok]
# step.sh NN LEG ...  (the same; the stage is also read from the leg id)
#   Handler only. Open one leg: deliver the stage on its first leg, write the leg's startup
#   message, prepare a fresh session and launch the analyst in 00_GIVE-THE-AGENT/.
#   A leg id is the stage, the step letter and a count where the step repeats: A1a, B1b-03,
#   B2a-r1; a leg continued after a pause adds -p2 (tools/steps.tsv lists every step).
#   A check step (kind "check" in steps.tsv) refuses to open until the dispatch has left DONE
#   (dispatch.sh), and its message tells the analyst one thing, that the readers left their files.
#   Every ordinary leg continues the conversation of the last committed close (v40): it forks that
#   checkpoint's session, in the same folder. The first leg of a run, and a leg relaunched under the
#   label it already has, do not.
#   --from-cut LABEL   open this leg as a fork of the checkpoint of LABEL (a cut); LABEL must be the last close.
#   --fresh            open a fresh session instead of continuing; logged in RUN.json as a departure.
#   --prepare          print the launch command instead of running it.
#   --force-order      open a stage whose previous stage is not finished; logged as a departure.
#   --reopen           open a leg the analyst already closed (out/_closes/NN-LEG.closed); logged as a departure.
set -euo pipefail
ARGS=("$@")
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
RUN="$(harness_run_dir)"; C="$RUN/CONTROL"; AG="$RUN/00_GIVE-THE-AGENT"
refuse_in_vault "$RUN"
if [ "${AGGREGATOR_LOCK_RUN:-}" != "$RUN" ]; then
  exec python3 "$C/harness/protocol_guard.py" locked "$RUN" bash "$0" "${ARGS[@]}"
fi
read_leg "$@"; shift "$LEGARGS"
PREPARE=0; APIOK=0; FORCE=0; FROM=""; FRESH=0; REOPEN=0
while [ $# -gt 0 ]; do
  case "$1" in
    --prepare) PREPARE=1; shift;; --api-ok) APIOK=1; shift;; --force-order) FORCE=1; shift;;
    --from-cut) FROM="${2:?label}"; shift 2;;
    --fresh) FRESH=1; shift;;
    --reopen) REOPEN=1; shift;;
    *) echo "unknown option: $1" >&2; exit 1;;
  esac
done
LABEL="$NN.$LEG"
# a leg the analyst has closed is not opened again: the next step is close.sh, or the next leg (J, 2026-10-03)
if [ -f "$AG/out/_closes/$NN-$LEG.closed" ]; then
  if [ "$REOPEN" -eq 0 ]; then
    echo "REFUSING: leg $LEG is already closed (out/_closes/$NN-$LEG.closed). Run close.sh $LEG if you have not, then open the next leg. To open it again on purpose: step.sh $LEG --reopen" >&2; exit 1
  fi
  touch "$C/handover-events.log"
  printf '%s\treopened\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$LABEL" "already closed by done.sh" >> "$C/handover-events.log"
fi
STAGE="$(stage_file_of "$RUN" "$NN")"
[ -n "$STAGE" ] || { echo "stage $NN is not in DROPS/ORDER.tsv" >&2; exit 1; }
python3 "$C/harness/protocol_guard.py" arm "$RUN" "$LABEL" >/dev/null
if [ -n "${ANTHROPIC_API_KEY:-}" ] && [ "$APIOK" -eq 0 ]; then
  echo "ANTHROPIC_API_KEY is set; the analyst runs on the subscription. Unset it, or pass --api-ok for a declared API run." >&2; exit 1
fi
if [ -n "${ANTHROPIC_BASE_URL:-}" ] || [ -n "${ANTHROPIC_AUTH_TOKEN:-}" ]; then
  echo "ANTHROPIC_BASE_URL or ANTHROPIC_AUTH_TOKEN is set: this shell routes to a gateway. The analyst never runs on the gateway; open a clean terminal." >&2; exit 1
fi
python3 "$C/harness/protocol_guard.py" settings "$RUN" "$NN"
if ! python3 "$C/harness/protocol_guard.py" confirm "$RUN"; then
  [ "$(json_get "$C/pending_launch.json" label)" = "$LABEL" ] || { echo "Another leg's launch is still pending." >&2; exit 1; }
fi
touch "$C/handover-events.log"
# ---- the order: a stage opens only when the previous one finished --------------------------
if [ "$NN" = E2 ] && [ "$LEGSTEP" = a ]; then
  for f in proposal.md design-note.md; do
    [ -s "$RUN/DROPS/E2/handling/$f" ] || { echo "stage E2 needs $RUN/DROPS/E2/handling/$f (the study's proposal as it stands now; the instrument's design note)" >&2; exit 1; }
  done
fi
FIRST=0
grep -q "	handed	$NN	" "$C/handover-events.log" || FIRST=1
if [ "$FIRST" -eq 1 ]; then
  PREV="$(prev_stage "$RUN" "$NN")"
  if [ -n "$PREV" ] && [ ! -f "$C/stage-state/$PREV/FINISHED" ]; then
    if [ "$FORCE" -eq 0 ]; then
      echo "Stage $PREV is not finished (no CONTROL/stage-state/$PREV/FINISHED: its last leg closed with handback-$PREV.md and a clean validation)." >&2; exit 1
    fi
    printf '%s\tforced-order\t%s\t%s unfinished\n' "$(NOW)" "$NN" "$PREV" >> "$C/handover-events.log"
  fi
  # deliver the stage: its file, its shelf, anything else the drop holds
  [ -d "$RUN/DROPS/$NN" ] || { echo "no DROPS/$NN to deliver" >&2; exit 1; }
  cp -R "$RUN/DROPS/$NN"/. "$AG"/
  printf '%s\thanded\t%s\t%s\n' "$(NOW)" "$NN" "$STAGE" >> "$C/handover-events.log"
fi
# ---- stage E2's first leg: the proposal, the design note, the interviews and the harness log ---
HANDLINGLINE=""
if [ "$NN" = E2 ] && [ "$LEGSTEP" = a ]; then
  H="$AG/handling"
  for f in proposal.md design-note.md; do
    [ -s "$H/$f" ] || { echo "stage E2 needs $RUN/DROPS/E2/handling/$f (the study's proposal as it stands now; the instrument's design note)" >&2; exit 1; }
  done
  mkdir -p "$H/interviews" "$H/harness-log/first-messages"; cp "$RUN/DROPS/E2/handling/"*.md "$H/"
  if [ -f "$C/interviews.tsv" ]; then
    cp "$C/interviews.tsv" "$H/interviews/"
    cut -f4 "$C/interviews.tsv" | while read -r fk; do
      f="$(ls "$C"/.cc/projects/*/"$fk".jsonl 2>/dev/null | head -1 || true)"
      if [ -n "$f" ]; then cp "$f" "$H/interviews/"; fi   # an interview with no transcript is not an error
    done
  fi
  for f in handover-events.log RUN.json; do [ -f "$C/$f" ] && cp "$C/$f" "$H/harness-log/"; done
  for d in "$C"/stage-state/*/; do [ -f "$d/PAUSES" ] && cp "$d/PAUSES" "$H/harness-log/PAUSES-$(basename "$d")"; done
  for f in "$C"/prompts/*.txt; do [ -f "$f" ] && cp "$f" "$H/harness-log/first-messages/"; done
  HANDLINGLINE="handling/ holds the proposal, the design note, the interview transcripts and the harness log."
fi
# ---- a check leg waits for the dispatch ------------------------------------------------------
CHECKLINE=""
case "$LEGKIND" in check)
  is_fleet_stage "$NN" || { echo "stage $NN has no dispatch, so it has no check step" >&2; exit 1; }
  RAW="$(raw_dir_of "$NN")"
  if [ "$NN" = B2 ] && [ -n "$LEGROUND" ] && [ "$LEGROUND" != - ]; then   # B2b-rK reads round-K
    RAW="$RAW/round-$LEGROUND"
  elif [ "$NN" = B2 ]; then                        # B2d reads the gold round and the two stability rounds
    for K in gold stab-1 stab-2; do
      [ -f "$AG/$RAW/round-$K/DONE" ] || { echo "the dispatch has not finished: no $RAW/round-$K/DONE. Run dispatch.sh B2 --round $K first." >&2; exit 1; }
    done
    RAW="$RAW/round-gold, round-stab-1 and round-stab-2"
  fi
  case "$RAW" in *round-gold,*) ;; *) [ -f "$AG/$RAW/DONE" ] || { echo "the dispatch has not finished: no $RAW/DONE. Run dispatch.sh $NN first." >&2; exit 1; };; esac
  if [ "$NN" = D2 ]; then
    [ -f "$AG/DROPS/D/DONE" ] || { echo "the labelers have not finished: no DROPS/D/DONE in the analyst's folder." >&2; exit 1; }
    if [ ! -f "$AG/out/adaptations.jsonl" ] || [ "$AG/DROPS/D/DONE" -nt "$AG/out/adaptations.jsonl" ]; then   # once per return
      (cd "$AG" && python3 tools/ingest.py D) || echo "ingest.py D rejected some rooms; they are in DROPS/D/UNRETURNED.tsv and the report is out/ingest-D.md"
      (cd "$AG" && python3 tools/gen_views.py D2 >/dev/null) || echo "gen_views.py D2 failed; the analyst's close will say why"
    fi
    CHECKLINE="The labelers left their files in DROPS/D/ and the verdict readers left theirs in $RAW/; ingest.py D compiled the ledger and the verdicts."
  else
    CHECKLINE="The readers left their files in $RAW/."
  fi;;
recheck)
  [ -f "$AG/DROPS/D/recheck/DONE" ] || { echo "the re-check has not returned: no DROPS/D/recheck/DONE in the analyst's folder." >&2; exit 1; }
  [ -f "$AG/out/_fleet_raw/D3v/DONE" ] || { echo "the re-check's verdicts have not returned: no out/_fleet_raw/D3v/DONE. Run dispatch.sh D3 first." >&2; exit 1; }
  if [ ! -f "$AG/out/adaptations-recheck.jsonl" ] || [ "$AG/DROPS/D/recheck/DONE" -nt "$AG/out/adaptations-recheck.jsonl" ]; then
    (cd "$AG" && python3 tools/ingest.py D --recheck) || echo "ingest.py D --recheck rejected some rooms; see out/ingest-D-recheck.md"
  fi
  CHECKLINE="The labelers' re-check returns are in DROPS/D/recheck/ and the verdicts in out/_fleet_raw/D3v/; ingest.py D --recheck compiled them.";;
esac
# ---- a leg relaunched after a failed close is told where the report is ----------------------
FAILLINE=""
LASTFAIL="$(ls -t "$AG/out/_closes/$NN-"*.validate.txt 2>/dev/null | head -1 || true)"
if [ -n "$LASTFAIL" ] && [ ! -f "$AG/out/_closes/$NN-$LEG.closed" ] && grep -q "^ERROR" "$LASTFAIL" 2>/dev/null; then
  FAILLINE="Your last close of stage $NN failed; the report is out/_closes/$(basename "$LASTFAIL")."
fi
# ---- a reply the principal investigator left after an interview, newer than the last close ---
REPLYLINE=""
LASTCLOSE="$(ls -t "$AG"/out/_closes/*.closed 2>/dev/null | head -1 || true)"
for f in "$AG"/out/interview/*-reply.md; do
  [ -f "$f" ] || continue
  if [ -z "$LASTCLOSE" ] || [ "$f" -nt "$LASTCLOSE" ]; then REPLYLINE="$REPLYLINE out/interview/$(basename "$f")"; fi
done
[ -n "$REPLYLINE" ] && REPLYLINE="The principal investigator left a reply after an interview: read$REPLYLINE before your first write, and answer it in your files under rule 13."
# ---- answers to the analyst's questions (mem.py ask): each named in the first message of the first leg opened
# after it, and again if that leg is opened again (v43.2: an answer written while a leg was open, before its done.sh,
# was newer than no close and never named). CONTROL/answers-named.tsv: id, the leg whose first message named it.
ANSWERLINE=""; NAMED="$C/answers-named.tsv"; NEWNAMED=""
for f in "$AG"/out/_answers/*.md; do
  [ -f "$f" ] || continue
  id="$(basename "$f" .md)"
  prev="$( [ -f "$NAMED" ] && awk -F'\t' -v i="$id" '$1==i{l=$2} END{print l}' "$NAMED" || true)"
  if [ -z "$prev" ] || [ "$prev" = "$LABEL" ]; then ANSWERLINE="$ANSWERLINE $id"; [ -z "$prev" ] && NEWNAMED="$NEWNAMED $id"; fi
done
[ -n "$ANSWERLINE" ] && ANSWERLINE="The principal investigator answered your questions$ANSWERLINE: read them with python3 tools/mem.py asks <id> before your first write, and revisit the work that rested on your assumption."
rm -f "$AG/.pause"   # a new leg starts with no pause request; pause.sh asks again
printf '%s\n' "$NN" > "$AG/.stage"; printf '%s\n' "$LEG" > "$AG/.leg"
printf '%s\n' "$STAGE" > "$AG/.stagefile"   # the one stage file, from DROPS/ORDER.tsv, for the checks and the hooks
# a compaction gate left by an earlier leg does not bind this one (pretool_guard.py)
[ -f "$RUN/CONTROL/.compact-gate.json" ] && mv "$RUN/CONTROL/.compact-gate.json" "$RUN/CONTROL/.compact-gate.$(date -u +%Y%m%dT%H%M%SZ).stale.json"
cat > "$C/next_prompt.txt" <<MSG
Stage $NN, leg $LEG. This leg continues the last close's conversation, in the same folder, unless it is the run's first. Orient before you write: read AGENT.md, then, in this order and nothing else by default: out/_head.md; $STAGE; the output of \`python3 tools/mem.py diary --last 5\`; the output of \`python3 tools/validate.py --open $NN\`.${CHECKLINE:+ $CHECKLINE}${FAILLINE:+ $FAILLINE}${REPLYLINE:+ $REPLYLINE}${ANSWERLINE:+ $ANSWERLINE}${HANDLINGLINE:+ $HANDLINGLINE} Do this leg's work as the stage file says, writing as you work with \`python3 tools/mem.py log\`, and close the leg with \`bash tools/done.sh $NN\` (or \`--cut <move>\` where the stage file says). Then stop.
MSG
mkdir -p "$C/prompts"; cp "$C/next_prompt.txt" "$C/prompts/$NN.$LEG.txt"
for id in $NEWNAMED; do printf '%s\t%s\n' "$id" "$LABEL" >> "$C/answers-named.tsv"; done
# ---- continuity (v40): an ordinary leg forks the last committed close's session ---------------
if [ -z "$FROM" ] && [ "$FRESH" -eq 0 ] && [ -z "$(session_of "$RUN" "$LABEL")" ] && [ ! -f "$C/pending_launch.json" ]; then
  AUTO="$(awk -F'\t' 'NR>1 && $1!="label" && $10=="agent-and-files"{l=$1} END{print l}' "$C/snapshots/INDEX.tsv" 2>/dev/null || true)"
  if [ -n "$AUTO" ] && [ -f "$C/snapshots/$AUTO/COMMITTED" ] && [ -n "$(session_of "$RUN" "$AUTO")" ]; then
    FROM="$AUTO"; echo "Continuing from the last close, $FROM (its conversation and this folder)."
  fi
fi
if [ "$FRESH" -eq 1 ]; then
  python3 - "$C/RUN.json" "$LABEL" <<'PY'
import json, os, sys, datetime
p, lab = sys.argv[1:]
r = json.load(open(p)) if os.path.exists(p) else {}
r.setdefault("departures", []).append({"leg": lab, "what": "opened fresh, not continuing the last close (--fresh)",
                                       "utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
json.dump(r, open(p, "w"), indent=2)
PY
fi
# ---- a leg from a cut forks that cut's session -----------------------------------------------
if [ -n "$FROM" ]; then
  PSID="$(session_of "$RUN" "$FROM")"
  [ -n "$PSID" ] || { echo "no session recorded for $FROM" >&2; exit 1; }
  [ -f "$C/snapshots/$FROM/COMMITTED" ] || { echo "$FROM has no committed checkpoint to fork from" >&2; exit 1; }
  # the live folder is the cut's only while no later leg has closed: a leg never reuses a folder that has
  # moved on (J, 2026-09-29); an earlier state is talked to through interview.sh, in a copy of its own
  LASTCK="$(awk -F'\t' 'NR>1 && $1!="label"{l=$1} END{print l}' "$C/snapshots/INDEX.tsv" 2>/dev/null)"
  [ "$LASTCK" = "$FROM" ] || { echo "REFUSING: $FROM is not the last close (the last is ${LASTCK:-none}); the folder has moved on since. Talk to that state with interview.sh $FROM." >&2; exit 1; }
  python3 - "$C/RUN.json" "$PSID" <<'PY'
import json, os, sys
p, sid = sys.argv[1:]
r = json.load(open(p)) if os.path.exists(p) else {}
r.setdefault("lineage", {})["resume_session"] = sid
json.dump(r, open(p, "w"), indent=2)
PY
fi
CLI_VERSION="$(claude --version 2>/dev/null | head -1 || echo unknown)"
python3 "$C/harness/protocol_guard.py" prepare "$RUN" "$LABEL" "$CLI_VERSION"
json_get "$C/pending_launch.json" requested_session_id > "$AG/.session"
TOKEN="$(json_get "$C/pending_launch.json" launch_id)"
CMD=(bash "$C/harness/launch.sh" "$LABEL" "$TOKEN"); [ "$APIOK" -eq 0 ] || CMD+=(--api-ok)
echo "Stage $NN, leg $LEG, model $(python3 "$C/harness/protocol_guard.py" arm "$RUN" "$LABEL")."
echo "Claude opens with the leg's first message already sent. When the analyst has closed the leg"
echo "and stopped, quit Claude (/exit) and run:  bash \"$C/harness/close.sh\" $NN $LEG"
if [ "$PREPARE" -eq 1 ]; then printf 'Prepared: '; printf '%q ' "${CMD[@]}"; printf '\n'; exit 0; fi
"${CMD[@]}"
