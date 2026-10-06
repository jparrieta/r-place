#!/usr/bin/env bash
# lib.sh, v38: shared by step.sh, close.sh, dispatch.sh and build.sh. Sourced, never run.
# macOS bash 3.2: no mapfile, no associative arrays, no ${var,,}. JSON goes through python3.
if command -v shasum >/dev/null 2>&1; then SHA="shasum -a 256"; else SHA="sha256sum"; fi
NOW() { date -u +%Y-%m-%dT%H:%M:%SZ; }

# the run directory is the parent of CONTROL/harness/
harness_run_dir() { cd "$(dirname "${BASH_SOURCE[1]}")/../.." && pwd -P; }

# the stages and their steps live in steps.tsv beside the harness (a copy of tools/steps.tsv)
STEPS_PY() { local h; h="$(dirname "${BASH_SOURCE[0]}")"; if [ -f "$h/steps.py" ]; then python3 "$h/steps.py" "$@"; elif [ -f "$h/../tools/steps.py" ]; then python3 "$h/../tools/steps.py" "$@"; elif [ -f "$h/../aggregator/tools/steps.py" ]; then python3 "$h/../aggregator/tools/steps.py" "$@"; else python3 "$h/../../instrument/tools/steps.py" "$@"; fi; }
# norm_stage X -> A1, B1 ... E2 (case does not matter)
norm_stage() {
  local x; x="$(printf '%s' "$1" | tr '[:lower:]' '[:upper:]')"
  if STEPS_PY stages | grep -x "$x" >/dev/null; then echo "$x"; else echo "not a stage: $1 (stages: $(STEPS_PY stages | tr '\n' ' '))" >&2; return 1; fi
}
# read_leg LEG ... | NN LEG ... : sets NN, LEG, LEGKIND, LEGINTERVIEW, LEGROUND, LEGSTEP, LEGLABEL, LEGARGS
read_leg() {
  local first="${1:?leg id, e.g. B1b-03}" out
  if [ -n "${2:-}" ] && [ "${2#-}" = "$2" ] && norm_stage "$first" >/dev/null 2>&1; then
    NN="$(norm_stage "$first")"; LEG="$2"; LEGARGS=2
  else
    LEG="$first"; NN=""; LEGARGS=1
  fi
  out="$(STEPS_PY check "$LEG" ${NN:+--stage "$NN"})" || return 1
  NN="$(printf '%s' "$out" | cut -f1)"; LEGKIND="$(printf '%s' "$out" | cut -f2)"
  LEGINTERVIEW="$(printf '%s' "$out" | cut -f3)"; LEGROUND="$(printf '%s' "$out" | cut -f4)"
  LEGLABEL="$(printf '%s' "$out" | cut -f5)"; LEGSTEP="$(printf '%s' "$LEG" | cut -c3)"
}
check_leg() { STEPS_PY check "$1" >/dev/null; }

# the stage file of a stage, from DROPS/ORDER.tsv (stage<TAB>file)
stage_file_of() { awk -F'\t' -v s="$2" '$1==s{print $2}' "$1/DROPS/ORDER.tsv"; }
prev_stage() { awk -F'\t' -v s="$2" 'NR>1{if($1==s){print p; exit} p=$1}' "$1/DROPS/ORDER.tsv"; }

json_get() { python3 - "$1" "$2" <<'PY'
import json, sys
p, key = sys.argv[1:]
try:
    d = json.load(open(p))
except Exception:
    print(""); sys.exit(0)
for k in key.split("."):
    d = d.get(k) if isinstance(d, dict) else None
    if d is None:
        print(""); sys.exit(0)
print(d if not isinstance(d, (dict, list)) else json.dumps(d))
PY
}

# the fleet stages, the check legs they gate, and where their returns land
is_fleet_stage() { case "$1" in B2|B3|B4|C2|C5|D2|D3|E1) return 0;; *) return 1;; esac; }
raw_dir_of() { case "$1" in D2) echo "out/_fleet_raw/D2v";; *) echo "out/_fleet_raw/$1";; esac; }

transcript_of() { echo "$1/CONTROL/.cc/projects/run/$2.jsonl"; }

refuse_in_vault() {
  case "$1" in */Obsidian/*)
    echo "REFUSING: the run stands inside the vault ($1). Move it out first." >&2; exit 1;; esac
}

session_of() { python3 - "$1" "$2" <<'PY'
import json, os, sys
run, lab = sys.argv[1:]
sp = os.path.join(run, "CONTROL", "sessions.json")
S = json.load(open(sp)) if os.path.exists(sp) else {}
print((S.get(lab) or {}).get("session_id") or "")
PY
}

# set_aside_dir RUN: where a script's set-aside files go (J, 2026-10-06: nothing set aside stays in a repository or a
# run; it goes to Jail/_to_delete/ under the path it came from). A run at <repository>/aggregator/runs/<run> sends them
# to <repository>/../_to_delete/<repository>/aggregator/runs/<run>/; a run anywhere else (the harness tests) keeps them
# in its own _to_delete/.
set_aside_dir() {
  local run="$1" top
  case "$run" in
    */aggregator/runs/*) top="${run%/aggregator/runs/*}"
      printf '%s/_to_delete/%s%s\n' "$(dirname "$top")" "$(basename "$top")" "${run#"$top"}";;
    *) printf '%s/_to_delete\n' "$run";;
  esac
}
