#!/usr/bin/env bash
# build.sh RUN_DIR [--instrument DIR] [--input DIR] [--input-root DIR] [--rebuild-store]
#   --input-root: the shared input (default aggregator/input): coders/, canvas/, raw/ (restructure 2026-10-02)
#   Lay out a v43 run (the Claude platform) from the instrument and the coder documents. Refuses a run that has begun
#   (CONTROL/sessions.json names a session). Writes:
#     00_GIVE-THE-AGENT/   the analyst's world: the standing documents, tools/ (without fleet.py,
#                          which is the handler's), package/ and trees/ (the store, built if absent
#                          or with --rebuild-store), stages/ (empty: one stage file arrives per
#                          stage), out/ (empty tree), shelves/
#     DROPS/ORDER.tsv, DROPS/NN/   what step.sh delivers at each stage's first leg
#     CONTROL/harness/     this harness, with validation_tools/ (the trusted copies close.sh and
#                          dispatch.sh run: validate.py, vlib.py, checks/, probe.py, fleet.py)
#     CONTROL/arm.json, RUN.json, settings.template.json, sessions.json
#     STAGE CARDS/, READ-ME-FIRST.md
#   The instrument's fingerprint (sha256 over its manifest) goes into CONTROL/RUN.json.
set -euo pipefail
RUN="${1:?run directory}"; shift
HERE="$(cd "$(dirname "$0")" && pwd -P)"
INS="$(cd "$HERE/../../instrument" && pwd -P)"; INPUT=""; REBUILD=0; IN="$HERE/../../input"
while [ $# -gt 0 ]; do
  case "$1" in --instrument) INS="$2"; shift 2;; --input) INPUT="$2"; shift 2;; --input-root) IN="$2"; shift 2;; --rebuild-store) REBUILD=1; shift;;
    *) echo "unknown option: $1" >&2; exit 1;; esac
done
mkdir -p "$RUN"; RUN="$(cd "$RUN" && pwd -P)"
case "$RUN" in */Obsidian/*) echo "REFUSING: a run is never built inside the vault" >&2; exit 1;; esac
if [ -f "$RUN/CONTROL/sessions.json" ] && python3 -c 'import json,sys;sys.exit(0 if json.load(open(sys.argv[1])) else 1)' "$RUN/CONTROL/sessions.json"; then
  echo "REFUSING: $RUN has begun (CONTROL/sessions.json names a session). A run is built once." >&2; exit 1
fi
AG="$RUN/00_GIVE-THE-AGENT"; C="$RUN/CONTROL"
mkdir -p "$AG/tools" "$AG/stages" "$AG/out" "$AG/shelves" "$RUN/DROPS" "$C/harness/validation_tools" "$RUN/STAGE CARDS"
# ---- the analyst's world ----------------------------------------------------------------------
python3 "$HERE/gen_platform.py" --check >/dev/null || { echo "the platform files are stale: run python3 aggregator/handler/claude/gen_platform.py" >&2; exit 1; }
for f in AGENT.md CLAUDE.md PLATFORM-claude.md CONTRACT-aggregator.md METHOD.md STANDING-INSTRUCTIONS.md FLEET.md HOW-TO-RUN.md PRIOR-template.md WRITING.md; do
  cp "$INS/$f" "$AG/$f"
done
# copies overwrite in place (a connected folder may refuse to delete, so no tar unlink)
copytree() { python3 - "$1" "$2" "$3" <<'PY'
import os, shutil, sys
src, dst, excl = sys.argv[1], sys.argv[2], set(filter(None, sys.argv[3].split(",")))
for d, dirs, files in os.walk(src):
    dirs[:] = [x for x in dirs if x not in excl and x != "__pycache__"]
    rel = os.path.relpath(d, src)
    os.makedirs(os.path.join(dst, rel), exist_ok=True)
    for f in files:
        if f in excl or f.endswith(".pyc"):
            continue
        shutil.copyfile(os.path.join(d, f), os.path.join(dst, rel, f))
        shutil.copymode(os.path.join(d, f), os.path.join(dst, rel, f))
PY
}
copytree "$INS/tools" "$AG/tools" "tests,fleet.py,rerender_forests.sh,version_log.py,stages_full.py,index_md.py,build_store.py,build_neighbours.py,build_shelves.py,TOOLS-STATUS.md,HOW-TO-RUN.md"
if [ "$REBUILD" -eq 1 ] || [ ! -f "$AG/package/store/rooms.jsonl" ]; then
  [ -n "$INPUT" ] || { echo "the store is absent; pass --input aggregator/input/coders to build it" >&2; exit 1; }
  python3 "$INS/tools/build_store.py" --input "$INPUT" --root "$AG"
  python3 "$INS/tools/transitions.py" --root "$AG"
  python3 "$INS/tools/relations.py" --root "$AG"
  python3 "$INS/tools/build_store.py" --root "$AG" --readme-only
fi
# ---- the canvas (contract §2, §4, rule 7): outcome fields, pixel series, artworks; joined here ------
CV="$IN/canvas"
if [ -f "$CV/case_facts_outcome.jsonl" ]; then
  for f in case_facts_outcome.jsonl pixels.csv DATA-manifest-canvas.md artworks.jsonl; do
    [ -f "$CV/$f" ] || { echo "input/canvas/$f is absent; the canvas joins whole or not at all" >&2; exit 1; }
  done
  mkdir -p "$AG/package/canvas"
  cp "$CV/case_facts_outcome.jsonl" "$CV/pixels.csv" "$CV/DATA-manifest-canvas.md" "$AG/package/"
  cp "$CV/artworks.jsonl" "$AG/package/canvas/"
  ( cd "$AG" && python3 "$INS/tools/build_store.py" --root . --join-canvas package/case_facts_outcome.jsonl )
  if [ -f "$CV/atlas_2017.json" ]; then
    ( cd "$AG" && python3 "$INS/tools/build_neighbours.py" --root . --atlas "$CV/atlas_2017.json" \
      && python3 "$INS/tools/build_store.py" --root . --readme-only >/dev/null )
  else
    echo "no input/canvas/atlas_2017.json: package/store/neighbours.jsonl holds no canvas neighbours; mem.py neighbours will say so" >&2
  fi
else
  echo "no input/canvas/: the canvas is not joined; stage A1 will report it" >&2
fi
for d in _analysis _questions _views _wiki rooms diary model fourth _closes; do mkdir -p "$AG/out/$d"; done
# ---- the drops ------------------------------------------------------------------------------------
printf 'stage\tfile\n' > "$RUN/DROPS/ORDER.tsv"
# a stage file the instrument no longer holds is moved aside, never served beside the current one
# (review 2026-09-29: a renamed C4 file stayed in DROPS/C4 and the hooks picked it)
for old in "$RUN"/DROPS/*/stages/STAGE-*.md; do
  [ -e "$old" ] || continue
  [ -f "$INS/stages/$(basename "$old")" ] && continue
  sd="$RUN/DROPS/_superseded/$(date -u +%Y%m%dT%H%M%SZ)/$(basename "$(dirname "$(dirname "$old")")")"
  mkdir -p "$sd"; mv "$old" "$sd/"; echo "moved aside a stage file the instrument no longer holds: $old" >&2
done
for f in "$INS/stages"/STAGE-*.md; do   # a glob, sorted, safe for a path with spaces (v41)
  b="$(basename "$f")"; nn="$(echo "$b" | sed -E 's/^STAGE-([A-E][1-6])-.*/\1/')"
  mkdir -p "$RUN/DROPS/$nn/stages"; cp "$f" "$RUN/DROPS/$nn/stages/$b"
  printf '%s\tstages/%s\n' "$nn" "$b" >> "$RUN/DROPS/ORDER.tsv"
  [ -d "$INS/shelves/$nn" ] && { mkdir -p "$RUN/DROPS/$nn/shelves"; cp -R "$INS/shelves/$nn"/. "$RUN/DROPS/$nn/shelves/"; }
done
# stage D4's activity table, cut to the frame by build_canvas.py into input/canvas/D4/
[ -d "$CV/D4" ] && { mkdir -p "$RUN/DROPS/D4/data"; cp "$CV/D4"/* "$RUN/DROPS/D4/data/"; }
cp "$INS/SCHEMA-adaptations.md" "$RUN/DROPS/D1/SCHEMA-adaptations.md"
mkdir -p "$RUN/DROPS/D1/handoff"; cp "$INS/handoff"/*.md "$RUN/DROPS/D1/handoff/"
# stage E2, the feedback: the design note now, the proposal from the principal investigator later
mkdir -p "$RUN/DROPS/E2/handling"
for dn in "$HERE/../DESIGN-NOTE-v38.md" "$INS/DESIGN-NOTE-v38.md"; do
  [ -f "$dn" ] && { cp "$dn" "$RUN/DROPS/E2/handling/design-note.md"; break; }
done
printf '%s\n' "Stage E2 reads this folder as handling/. Put the study's proposal, as it stands when stage E1 ends, here as proposal.md." \
  "design-note.md is the instrument's design note, copied at build; replace it if the design changed. step.sh refuses E2 without both." > "$RUN/DROPS/E2/handling/README.txt"
# ---- the handler's ----------------------------------------------------------------------------
for f in lib.sh step.sh launch.sh close.sh dispatch.sh protocol_guard.py stage_cards.py acceptance.sh acceptance_v41.sh after_compact.sh pretool_guard.py pause.sh interview.sh gen_manual.py publish.sh; do
  [ -f "$HERE/$f" ] && cp "$HERE/$f" "$C/harness/$f"
done
cp "$INS/tools/steps.py" "$INS/tools/steps.tsv" "$C/harness/"
# every module the checks import, directly or through another (audit 2026-09-29c: B1 and D closes crashed)
for f in validate.py vlib.py probe.py fleet.py links.py snap.py steps.py steps.tsv saturation.py dreturn.py handoff.py ingest.py distance.py counts.py adaptation_ledger.py adaptation_tree.py chunk_compare.py; do cp "$INS/tools/$f" "$C/harness/validation_tools/$f"; done
copytree "$INS/tools/checks" "$C/harness/validation_tools/checks" ""
cp "$HERE/arm.claude.json" "$C/arm.json"   # v41: the Claude platform's schedule; the Codex runtime reads arm.codex.json
printf 'claude\n' > "$C/PLATFORM"
cp "$HERE/settings.template.json" "$C/settings.template.json"
[ -f "$C/sessions.json" ] || echo '{}' > "$C/sessions.json"
[ -f "$C/active_blocks.json" ] || echo '{}' > "$C/active_blocks.json"
touch "$C/handover-events.log"
FP="$( { (cd "$INS" && find AGENT.md CLAUDE.md PLATFORM-claude.md CONTRACT-aggregator.md METHOD.md STANDING-INSTRUCTIONS.md FLEET.md SCHEMA-adaptations.md WRITING.md stages tools handoff -type f ! -path '*__pycache__*' | LC_ALL=C sort | xargs shasum -a 256); (cd "$HERE" && find . -type f ! -path '*__pycache__*' ! -path './tests/bin/*' | LC_ALL=C sort | xargs shasum -a 256); } | shasum -a 256 | cut -c1-16)"
python3 - "$C/RUN.json" "$FP" <<'PY'
import json, os, sys, datetime
p, fp = sys.argv[1:]
r = json.load(open(p)) if os.path.exists(p) else {}
r.update({"instrument_version": "v43", "fingerprint": fp, "built_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
r.setdefault("lineage", {})
json.dump(r, open(p, "w"), indent=2)
PY
python3 "$HERE/stage_cards.py" "$RUN"
python3 "$C/harness/gen_manual.py" "$RUN" || true
cp "$HERE/READ-ME-FIRST.md" "$RUN/READ-ME-FIRST.md"
echo "built $RUN: instrument v43 (claude) fingerprint $FP; $(($(wc -l < "$RUN/DROPS/ORDER.tsv") - 1)) stages in DROPS/ORDER.tsv"
echo "Before the first leg: run the acceptance test,  bash \"$C/harness/acceptance.sh\""
