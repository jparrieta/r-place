#!/usr/bin/env bash
# dispatch.sh NN [--round K] [--only B001,B002] [--dry-run] [--recheck]
#   The dispatch leg of a fleet stage. Run it yourself in a Terminal on your Mac (the OpenRouter
#   key is read from your Keychain), never inside a Claude session, after the analyst closed the
#   build leg with --cut packets-out and close.sh checkpointed it. It runs the trusted copy of
#   fleet.py over the packets the analyst built, with the readers CONTROL/arm.json names, and
#   leaves the returns and DONE in the analyst's out/_fleet_raw/. It reads nothing else of the
#   analyst's and analyses nothing. Then open the stage's check step (dispatch prints its id).
#   At D2 it also prints what the adaptation handler runs in Codex; with --recheck at D3, the
#   re-check.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
RUN="$(harness_run_dir)"; C="$RUN/CONTROL"; AG="$RUN/00_GIVE-THE-AGENT"
NN="$(norm_stage "${1:?stage}")"; shift
ROUND=""; ONLY=""; DRY=""; RECHECK=0
while [ $# -gt 0 ]; do
  case "$1" in
    --round) ROUND="${2:?k}"; shift 2;; --only) ONLY="${2:?batches}"; shift 2;;
    --dry-run) DRY="--dry-run"; shift;; --recheck) RECHECK=1; shift;;
    *) echo "unknown option: $1" >&2; exit 1;;
  esac
done
if [ -f "$C/active_launch.json" ]; then
  echo "REFUSING: an analyst launch is active ($(json_get "$C/active_launch.json" label)). The dispatch runs with the analyst stopped." >&2; exit 1
fi
if [ "$NN" = D3 ]; then                 # the re-check: the labelers in Codex, and the verdict fleet on its rooms
  echo "The re-check (stage D3): give the adaptation handler in Codex the brief"
  echo "  $AG/out/handoff-D/recheck/HANDLER.md"
  echo "Returns go to $AG/DROPS/D/recheck/<sub>/; the handler writes DROPS/D/recheck/DONE."
  mkdir -p "$AG/DROPS/D/recheck"
  [ "$RECHECK" -eq 1 ] && exit 0      # --recheck prints the brief only
fi
R="$(json_get "$C/arm.json" "$( [ "$NN" = D3 ] && echo D2 || echo "$NN" ).readers")"
[ -n "$R" ] || { echo "stage $NN has no readers in CONTROL/arm.json; nothing to dispatch" >&2; exit 1; }
getr() { python3 -c 'import json,sys;d=json.loads(sys.argv[1]);v=d.get(sys.argv[2]);print("" if v is None else v)' "$R" "$1"; }
ROUTE="$(getr route)"; MODEL="$(getr model)"; N="$(getr n)"; SHARED="$(getr shared)"; ALLOW="$(getr allow_anthropic)"
case "$NN" in
  B2) [ -n "$ROUND" ] || { echo "B2 needs --round K" >&2; exit 1; }
      PK="out/_packets-B2/round-$ROUND"; RET="out/RETURN-B2.md"; RAW="out/_fleet_raw/B2/round-$ROUND";;
  D2) PK="out/verdict-D"; RET="out/verdict-D/RETURN-D2v.md"; RAW="out/_fleet_raw/D2v";;
  D3) PK="out/verdict-D/recheck"; RET="out/verdict-D/recheck/RETURN-D2v.md"; RAW="out/_fleet_raw/D3v";;
  *) PK="out/_packets-$NN"; RET="out/RETURN-$NN.md"; RAW="out/_fleet_raw/$NN";;
esac
[ -d "$AG/$PK" ] || { echo "no packets at $PK: the build leg did not finish" >&2; exit 1; }
[ -f "$AG/$RET" ] || { echo "no return specification at $RET" >&2; exit 1; }
[ -f "$AG/$RAW/DONE" ] && [ -z "$ONLY" ] && { echo "REFUSING: $RAW/DONE exists; this dispatch ran. Rebuilt packets go out with --only <names> into the same folder (new reader ids, a PARTIAL record)." >&2; exit 1; }
if [ "$NN" = D2 ]; then
  echo "The labelers (stage D2): give the adaptation handler in Codex the brief"
  echo "  $AG/out/handoff-D/HANDLER.md"
  echo "Returns go to $AG/DROPS/D/<sub>/; the handler writes DROPS/D/DONE. The check leg waits for both."
  mkdir -p "$AG/DROPS/D"
fi
CMD=(python3 -I "$C/harness/validation_tools/fleet.py" "$NN" --packets "$PK" --return "$RET" --raw "$RAW"
     --readers "$N" --model "$MODEL" --route "${ROUTE:-gateway}" --shared "$SHARED")
[ "$ALLOW" = True ] && CMD+=(--allow-anthropic)
[ -n "$ONLY" ] && CMD+=(--only "$ONLY")
[ -n "$DRY" ] && CMD+=("$DRY")
# the cli readers use the analyst runtime's login (CONTROL/.cc) from their own scratch folder, so their
# sessions sit in a project of their own and never in the analyst's
if [ "$ROUTE" = cli ]; then CMD+=(--cli-config "$C/.cc" --cli-cwd "$C/readers-cwd/$NN"); fi
printf '%s\tdispatch%s\t%s\t%s %s x%s\n' "$(NOW)" "${DRY:+-dry-run}" "$NN" "$ROUTE" "$MODEL" "$N" >> "$C/handover-events.log"
set +e
( cd "$AG" && "${CMD[@]}" )
RC=$?
set -e
[ -n "$DRY" ] || printf '%s\tdispatched\t%s\trc=%s\n' "$(NOW)" "$NN" "$RC" >> "$C/handover-events.log"
case "$NN:$ROUND" in
  B2:gold|B2:stab-*) CHK="B2d";;                                   # the gold and stability rounds: one check leg
  B2:*) CHK="$(STEPS_PY first B2 check)-r$ROUND";;
  D3:*) CHK="$(STEPS_PY first D3 recheck || echo D3b)";;          # the re-check's step
  *) CHK="$(STEPS_PY first "$NN" check || true)";;
esac
[ -z "$DRY" ] && echo "Next: the check leg:  legs.py run $(basename "$RUN") $CHK   (by hand: bash \"$C/harness/step.sh\" $CHK)"
exit $RC
