#!/usr/bin/env bash
# close.sh LEG [--files-only] [--force]      (or close.sh NN LEG ...; LEG is the leg id, e.g. B1b-03)
#   Handler only, after the analyst has closed the leg with tools/done.sh and you have quit Claude.
#   In order: confirms the launch; runs the recall probe as a fresh headless turn of the leg's own
#   session and scores it; runs the trusted close-check; audits the model that served against
#   CONTROL/arm.json; then publishes the leg's checkpoint (the analyst's whole folder, its private
#   runtime, the transcript verified by id, the cost, the ancestry), built in a temporary directory
#   under a lock, verified, then published atomically, COMMITTED written last.
#   A leg closed at `--cut packets-out` prints the dispatch command next. A leg after which the
#   analyst wrote handback-NN.md, with a clean validation, finishes the stage.
#   --files-only   save the filesystem without an agent (diagnostic); never unlocks the next stage.
#   --force        close although the analyst did not close the leg; recorded under "forced".
# Ported from v37's done.sh (_v37-source/harness/done.sh): labels are NN.LEG, every leg is its
# own session, the probe and the model audit are new.
set -euo pipefail
ARGS=("$@")
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
read_leg "$@"; shift "$LEGARGS"
FILES_ONLY=0; FORCE=0
for a in "$@"; do case "$a" in --files-only) FILES_ONLY=1;; --force) FORCE=1;; esac; done
RUN="$(harness_run_dir)"
AG="$RUN/00_GIVE-THE-AGENT"; C="$RUN/CONTROL"
LABEL="$NN.$LEG"
STAGE="$(stage_file_of "$RUN" "$NN")"
[ -n "$STAGE" ] || { echo "no such stage in DROPS/ORDER.tsv: $NN" >&2; exit 1; }
D="$C/snapshots/$LABEL"
[ -f "$D/COMMITTED" ] && { echo "REFUSING: $D is committed. A leg is checkpointed once." >&2; exit 1; }
if [ "${AGGREGATOR_LOCK_RUN:-}" != "$RUN" ]; then
  exec python3 "$C/harness/protocol_guard.py" locked "$RUN" bash "$0" "${ARGS[@]}"
fi
if [ -e "$D" ]; then
  mkdir -p "$C/snapshots/_failed"
  mv "$D" "$C/snapshots/_failed/$LABEL-$(date -u +%Y%m%dT%H%M%SZ)"
  echo "  note: an uncommitted $LABEL directory was moved to snapshots/_failed/" >&2
fi

# ---- preconditions ------------------------------------------------------------------------
MISSING=""
grep -q "	handed	$NN	" "$C/handover-events.log" 2>/dev/null || MISSING="$MISSING not-handed"
[ -f "$AG/out/_closes/$NN-$LEG.closed" ] || MISSING="$MISSING analyst-did-not-close"
CUT=""; [ -f "$AG/out/_closes/$NN-$LEG.closed" ] && CUT="$(tail -1 "$AG/out/_closes/$NN-$LEG.closed" | awk '{print $2}')"
# a leg the analyst paused at a safe stop closes without the stage's close-check: its work is half
# done by design; the checkpoint is published and marked paused, and the stage goes on at the next leg
PAUSED=0; if [ "$CUT" = pause ]; then PAUSED=1; FORCE=1; fi
if [ -n "$MISSING" ] && [ "$FORCE" -eq 0 ]; then
  echo "REFUSING: $LABEL is not closable:$MISSING. The analyst closes the leg with" >&2
  echo "          bash tools/done.sh $NN; relaunch the leg (legs.py open, or step.sh $LEG by hand), or pass --force." >&2
  exit 1
fi

# ---- the session, by id -------------------------------------------------------------------
if ! python3 "$C/harness/protocol_guard.py" confirm "$RUN"; then
  [ "$FILES_ONLY" -eq 1 ] || { echo "REFUSING: the launch for this run is unconfirmed (above). Pass --files-only for a filesystem-only save." >&2; exit 1; }
fi
python3 "$C/harness/protocol_guard.py" preclose "$RUN" "$LABEL" "$FORCE" "$FILES_ONLY"
# ---- the snap and the recall probe, handler-side, after the leg is shown closed -------------
if [ "$FILES_ONLY" -eq 0 ]; then
  SNAPLABEL="${CUT:+cut-$CUT-}$LEG-$(date -u +%Y%m%dT%H%M%SZ)"
  ( cd "$AG" && python3 -I "$C/harness/validation_tools/snap.py" "$NN" "$SNAPLABEL" --out out >/dev/null ) \
    || echo "  snap: failed (see above); the checkpoint below still records the files" >&2
  ( cd "$AG" && python3 -I "$C/harness/validation_tools/probe.py" "$NN" --leg "$LEG" --root . --out out --ask >/dev/null ) \
    || echo "  probe: no questions written" >&2
  if [ -f "$AG/out/_probe/$NN-$LEG.questions.md" ]; then
    if python3 "$C/harness/protocol_guard.py" probe "$RUN" "$LABEL" "$AG/out/_probe/$NN-$LEG.questions.md" "$AG/out/_probe/$NN-$LEG.answers.md"; then
      ( cd "$AG" && python3 -I "$C/harness/validation_tools/probe.py" "$NN" --leg "$LEG" --root . --out out --score ) || echo "  probe: misses written to out/_probe/notes.jsonl" >&2
    else
      echo "  probe: the headless turn failed; no answers scored" >&2
    fi
  fi
fi
SESSION="$(session_of "$RUN" "$LABEL")"
[ "$FILES_ONLY" -eq 0 ] || SESSION=""
T=""
if [ "$FILES_ONLY" -eq 0 ]; then
  if [ -z "$SESSION" ]; then
    echo "REFUSING: no confirmed session for $LABEL in CONTROL/sessions.json. step.sh records one" >&2
    echo "          at launch; if this leg ran in a session step.sh did not open, there is no" >&2
    echo "          agent to checkpoint. Pass --files-only for a filesystem-only save, marked as such." >&2
    exit 1
  fi
  T="$(transcript_of "$RUN" "$SESSION")"
  [ -f "$T" ] || { echo "REFUSING: the recorded session $SESSION has no transcript at $T" >&2; exit 1; }
fi

# ---- the transcript, verified ---------------------------------------------------------------
TSHA=""; TLINES=0; TBOUNDARY_OK=false
if [ -n "$T" ]; then
  VER="$(python3 - "$T" <<'PY'
import json, sys, hashlib
p = sys.argv[1]
n = bad = 0; last_assistant = None; ended = None
h = hashlib.sha256()
with open(p, "rb") as f:
    for i, raw in enumerate(f, 1):
        h.update(raw); n = i
        line = raw.decode("utf-8", "replace").strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except ValueError:
            bad += 1; continue
        if d.get("type") == "assistant":
            last_assistant = i
        ended = d.get("type")
print(json.dumps({"lines": n, "unparseable": bad, "last_assistant_line": last_assistant,
                  "last_type": ended, "sha256": h.hexdigest()}))
PY
)"
  TLINES="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["lines"])' "$VER")"
  TSHA="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["sha256"])' "$VER")"
  BAD="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["unparseable"])' "$VER")"
  LA="$(python3 -c 'import json,sys;d=json.loads(sys.argv[1]);print(d["last_assistant_line"] or 0)' "$VER")"
  if [ "$BAD" != "0" ]; then
    echo "REFUSING: transcript $SESSION has $BAD unparseable line(s); a checkpoint does not publish a transcript it cannot read." >&2; exit 1
  fi
  if [ "$LA" = "0" ]; then
    echo "REFUSING: transcript $SESSION carries no assistant turn; the session never answered." >&2; exit 1
  fi
  TBOUNDARY_OK="$(json_get "$C/close-status-$LABEL.json" completed_turn)"
fi

# ---- the close-time additions, before the boundary ----------------------------------------
if [ -n "$T" ]; then
  mkdir -p "$AG/out/_transcripts"
  cp "$T" "$AG/out/_transcripts/leg-$LABEL-$SESSION.jsonl"
  python3 - "$AG/out/_transcripts/INDEX.md" "$LABEL" "$SESSION" "$TLINES" "$(NOW)" <<'PYINDEX'
from pathlib import Path
import sys
p, nn, sid, lines, closed = sys.argv[1:]
p = Path(p)
old = p.read_text().splitlines() if p.exists() else ['# sessions, one line per leg close', '', '| leg | session | file | lines | closed |', '|---|---|---|---|---|']
old = [r for r in old if not r.startswith('| ' + nn + ' |')]
old.append('| %s | %s | leg-%s-%s.jsonl | %s | %s |' % (nn, sid, nn, sid, lines, closed))
p.write_text('\n'.join(old) + '\n')
PYINDEX
fi

# ---- build the checkpoint in a temporary directory ----------------------------------------
TMP="$C/snapshots/.tmp-$LABEL-$$"
rm -rf "$TMP"; mkdir -p "$TMP"
# Capture only the aggregator tree and its private persisted runtime.
python3 "$C/harness/protocol_guard.py" capture "$RUN" "$TMP" "$SESSION" "$TSHA"
cp "$C/validation-$LABEL.txt" "$TMP/validation-report.txt"
cp "$C/close-status-$LABEL.json" "$TMP/validation.json"
# 3. the instrument and the run's declarations as they stood (an absent optional file expands to nothing, by design)
# shellcheck disable=SC2046
( cd "$RUN" && tar -czf "$TMP/instrument.tar.gz" DROPS CONTROL/harness CONTROL/RUN.json CONTROL/arm.json \
    $( [ -f CONTROL/settings.template.json ] && echo CONTROL/settings.template.json ) \
    $( [ -f CONTROL/sessions.json ] && echo CONTROL/sessions.json ) \
    $( [ -f CONTROL/active_blocks.json ] && echo CONTROL/active_blocks.json ) \
    $( [ -f CONTROL/handover-events.log ] && echo CONTROL/handover-events.log ) )
# 4. the cost of this step, fork-aware: lines already counted at an earlier boundary of the same session are
#    skipped by count; a fork's first session skips its parent's messages by their ids (protocol_guard cost)
PREV_LINES=0; INHERIT=""
PREV=""; [ -f "$C/snapshots/INDEX.tsv" ] && PREV="$(tail -1 "$C/snapshots/INDEX.tsv" | cut -f1)"; [ "$PREV" = label ] && PREV=""
if [ -n "$SESSION" ]; then
  if [ -f "$C/snapshots/INDEX.tsv" ]; then
    PREV_LINES=$(awk -F'\t' -v s="$SESSION" '$4==s{n=$8} END{print n+0}' "$C/snapshots/INDEX.tsv")
  fi
  if [ "$PREV_LINES" -eq 0 ] && [ "$(json_get "$C/RUN.json" lineage.child_session)" = "$SESSION" ]; then
    INHERIT="$(json_get "$C/RUN.json" lineage.resumed_session)"
  fi
fi
python3 "$C/harness/protocol_guard.py" cost "$T" "$PREV_LINES" "$C/.cc/projects/run" "$SESSION" "$TMP/cost.json" "$INHERIT"
TIN=$(python3 -c 'import json,sys;d=json.load(open(sys.argv[1]))["main"];print(d["input_tokens"]+d["cache_creation_input_tokens"]+d["cache_read_input_tokens"])' "$TMP/cost.json")
TOUT=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["main"]["output_tokens"])' "$TMP/cost.json")
# the model audit: what served, from the transcript, against CONTROL/arm.json
if [ -n "$SESSION" ]; then
  WANT="$(python3 "$C/harness/protocol_guard.py" arm "$RUN" "$LABEL")"
  if ! python3 - "$TMP/cost.json" "$WANT" <<'PYAUDIT'
import json, sys
c, want = json.load(open(sys.argv[1])), sys.argv[2]
served = sorted(set(c["main"]["models"]) | {m for s in c.get("subagents", {}).values() for m in s.get("models", {})})
bad = [m for m in served if m != want and not m.startswith(want) and m != "<synthetic>"]
print("  model audit: arm %s, served %s (analyst and helpers)" % (want, ", ".join(served) or "none"))
sys.exit(1 if bad else 0)
PYAUDIT
  then
    echo "REFUSING: the leg's transcript names a model the arm does not ($WANT). Nothing published." >&2
    [ "$FORCE" -eq 1 ] || { rm -rf "$TMP"; exit 1; }
  fi
fi
# the leg's tokens into the analyst's RUN.json, on the leg's line
python3 - "$AG/RUN.json" "$NN" "$LEG" "$TMP/cost.json" <<'PYTOK'
import json, os, sys
p, nn, leg, cp = sys.argv[1:]
r = json.load(open(p)) if os.path.exists(p) else {}
c = json.load(open(cp))["main"]
for e in reversed(r.get("legs", [])):
    if e.get("stage") == nn and e.get("leg") == leg:
        e["tokens"] = {k: c[k] for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")}
        break
json.dump(r, open(p, "w"), indent=1)
PYTOK

# 5. checkpoint.json: identity, ancestry, versions, validation
NOUT=$(find "$AG/out" -type f | wc -l | tr -d ' ')
FSFP=$($SHA "$TMP/fs.sha256" | cut -d' ' -f1)
PARENT_CKPT=""; [ -n "$PREV" ] && [ -f "$C/snapshots/$PREV/COMMITTED" ] && PARENT_CKPT="$(json_get "$C/snapshots/$PREV/checkpoint.json" checkpoint_id)"
CKPT_ID="$(python3 -c 'import hashlib,sys;print(hashlib.sha256(("|".join(sys.argv[1:])).encode()).hexdigest()[:16])' "$(json_get "$C/arm.json" "$NN")" "$(json_get "$C/RUN.json" fingerprint)" "$LABEL" "$FSFP" "$TSHA")"
HANDED=$(grep -q "	handed	$NN	" "$C/handover-events.log" 2>/dev/null && echo true || echo false)
python3 - "$TMP/checkpoint.json" "$CKPT_ID" "$LABEL" "$NN" "$STAGE" "$FILES_ONLY" "$C/RUN.json" "$C/sessions.json" \
  "$PARENT_CKPT" "$PREV" "$SESSION" "$TSHA" "$TLINES" "$TBOUNDARY_OK" "${T#$RUN/}" "$NOUT" "$FSFP" "$HANDED" \
  "$AG/out/notes-$NN.md" "$AG/out/handback-$NN.md" "$FORCE" "${MISSING# }" "$TIN" "$TOUT" <<'PY'
import json, sys, os, datetime
(out, ckpt, label, nn, stage, files_only, runp, sessp, parent_ckpt, prev, session, tsha, tlines,
 tbok, tpath, nout, fsfp, handed, notes, handback, force, missing, tin, tout) = sys.argv[1:]
r = json.load(open(runp))
S = json.load(open(sessp)) if os.path.exists(sessp) else {}
rec = S.get(label) or {}
vr = ""
if os.path.exists(notes):
    vr = open(notes, encoding="utf-8", errors="replace").read()
json.dump({
  "checkpoint_id": ckpt, "label": label, "stage": nn, "stage_file": stage,
  "kind": "files-only" if files_only == "1" else "agent-and-files",
  "run": {k: r.get(k) for k in ("instrument_version", "fingerprint")},
  "arm": json.load(open(os.path.join(os.path.dirname(runp), "arm.json"))).get(nn),
  "lineage": r.get("lineage"),
  "parent_checkpoint": parent_ckpt or None, "parent_label": prev or None,
  "session": {"session_id": session or None, "mode": rec.get("mode") or "none",
              "transcript_sha256": tsha or None, "boundary_line": int(tlines or 0),
              "boundary_verified": tbok.lower() == "true", "transcript_path_at_close": tpath or None},
  "cli_version": rec.get("cli_version"),
  "fs": {"files_in_out": int(nout), "manifest_sha256": fsfp},
  "subject": "aggregator", "filesystem_root": "00_GIVE-THE-AGENT",
  "handler_conversation_included": False,
  "validation": {**json.load(open(os.path.join(os.path.dirname(out), "validation.json"))), "handed": handed == "true", "notes_present": os.path.exists(notes),
                 "handback_present": os.path.exists(handback),
                 "validate_report_in_notes": "errors" in vr},
  "forced": (missing or "no reason recorded") if force == "1" else None,
  "cost": {"tokens_in": int(tin), "tokens_out": int(tout)},
  "published_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}, open(out, "w"), indent=2)
PY
# 6. the manifest binding everything, then verify from the artifacts before publishing
( cd "$TMP" && find . -type f ! -name MANIFEST.sha256 -print0 | sort -z | xargs -0 -n50 $SHA | sed 's|\./||' > MANIFEST.sha256 )
( cd "$TMP" && $SHA -c --quiet MANIFEST.sha256 ) || { echo "checkpoint manifest failed to verify; nothing published" >&2; exit 1; }
tar -tzf "$TMP/fs.tar.gz" >/dev/null || { echo "fs.tar.gz unreadable; nothing published" >&2; exit 1; }
[ -f "$TMP/agent.tar.gz" ] && { tar -tzf "$TMP/agent.tar.gz" >/dev/null || { echo "agent.tar.gz unreadable; nothing published" >&2; exit 1; }; }
python3 "$C/harness/protocol_guard.py" verify-checkpoint "$TMP"

# ---- publish atomically ---------------------------------------------------------------------
sync 2>/dev/null || true
mv "$TMP" "$D"
printf '%s\n' "$CKPT_ID" > "$D/COMMITTED"
[ -f "$C/snapshots/INDEX.tsv" ] || printf 'label\tstage_file\tclosed_utc\tsession_id\tout_files\tfs_manifest_sha256\ttokens_in\ttranscript_lines\ttokens_out\tkind\tcheckpoint_id\n' > "$C/snapshots/INDEX.tsv"
printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$LABEL" "$STAGE" "$(NOW)" "${SESSION:--}" "$NOUT" "$FSFP" "$TIN" "$TLINES" "$TOUT" \
  "$([ "$FILES_ONLY" -eq 1 ] && echo files-only || echo agent-and-files)" "$CKPT_ID" >> "$C/snapshots/INDEX.tsv"
printf '%s\tclosed\t%s\t%s\n' "$(NOW)" "$LABEL" "$STAGE" >> "$C/handover-events.log"

echo "checkpoint $LABEL  ($CKPT_ID)"
echo "  stage        $STAGE"
echo "  kind         $([ "$FILES_ONLY" -eq 1 ] && echo files-only || echo agent-and-files)"
echo "  session      ${SESSION:-NONE}  lines $TLINES"
echo "  out files    $NOUT   fs manifest $FSFP"
echo "  tokens       in $TIN, out $TOUT (cost.json; subagents apart)"
[ -n "$MISSING" ] && echo "  FORCED with:$MISSING"
case "$CUT" in interview)
  BRIEF=""; for b in "$AG"/out/interview/"$LEG"_*.md; do case "$b" in *-reply.md) ;; *) [ -f "$b" ] && BRIEF="$b";; esac; done   # the last brief, by name
  echo "  INTERVIEW POINT ($LEGLABEL). Talk with the analyst in an interview, a fork in a copy of its folder:"
  echo "    legs.py interview $(basename "$RUN") $LEG \"...\"   (by hand: bash CONTROL/harness/interview.sh $LEG)"
  echo "  (its brief: ${BRIEF#$RUN/}). The run goes on with its next leg either way.";;
esac
if [ "$PAUSED" -eq 1 ]; then
  mkdir -p "$C/stage-state/$NN"; printf '%s\t%s\tpaused\n' "$(NOW)" "$LABEL" >> "$C/stage-state/$NN/PAUSES"
  case "$LEG" in *-p[0-9]*) NEXTLEG="${LEG%-p*}-p$(( ${LEG##*-p} + 1 ))";; *) NEXTLEG="$LEG-p2";; esac
  echo "  paused at a safe stop. Resume when you are ready: legs.py run $(basename "$RUN") $LEG (it continues as $NEXTLEG;"
  echo "  by hand: bash CONTROL/harness/step.sh $NEXTLEG)"
  echo "  (the analyst picks up from the head and the diary)"
fi
echo "  at           $D"
# ---- the analyst's questions for the principal investigator (mem.py ask, v43): every open one, here --
QOPEN="$(python3 - "$AG/out" <<'PY'
import json, os, sys
o = sys.argv[1]; p = os.path.join(o, "asks.jsonl")
rows = [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []
for r in rows:
    if not os.path.exists(os.path.join(o, "_answers", "%s.md" % r.get("id"))):
        print("%s (%s): %s | meanwhile: %s" % (r.get("id"), r.get("leg"), r.get("question"), r.get("assumption")))
PY
)"
if [ -n "$QOPEN" ]; then
  echo "  QUESTIONS    the analyst asked, not yet answered (answer in out/_answers/<id>.md):"
  printf '%s\n' "$QOPEN" | sed 's/^/               /'
fi
if [ "$CUT" = packets-out ]; then
  DNN="$NN"; [ "$NN" = D1 ] && DNN=D2   # D1's packets go out with D2's dispatch (the labelers and the verdict fleet)
  echo "  next         the dispatch, outside the analyst, in your own Terminal:  bash \"$C/harness/dispatch.sh\" $DNN"
fi
if [ -f "$AG/out/handback-$NN.md" ] && [ "$(json_get "$D/checkpoint.json" validation.complete)" = True ] && [ "$FILES_ONLY" -eq 0 ] && [ "$FORCE" -eq 0 ]; then
  mkdir -p "$C/stage-state/$NN"; printf '%s\t%s\n' "$(NOW)" "$LABEL" > "$C/stage-state/$NN/FINISHED"
  echo "  stage $NN    finished (handback-$NN.md written, validation clean)"
fi
# ---- the Manual and the repository: every close is committed (and pushed where a remote is set) --
PKIND=close
[ "$CUT" = interview ] && PKIND=interview-point
[ "$PAUSED" -eq 1 ] && PKIND=pause
[ -f "$C/stage-state/$NN/FINISHED" ] && grep -q "	$LABEL$" "$C/stage-state/$NN/FINISHED" && PKIND=finished
bash "$C/harness/publish.sh" "$LABEL" "$PKIND" || true
