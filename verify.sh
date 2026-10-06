#!/usr/bin/env bash
# verify.sh: every check that needs no account, from the repository root.
#   bash verify.sh          (about two minutes; give an agent's shell a longer timeout)
# Prints PASS, WARN or FAIL per check and exits 1 if any check fails. Writes nothing in the repository:
# the harness test builds a scratch run in a temporary directory, which this script removes.
set -uo pipefail
cd "$(dirname "$0")" || exit 1
AG=aggregator; RUN=$AG/runs/claude-v43-1; IN=$AG/input; A=$RUN/00_GIVE-THE-AGENT
fails=0
check() {  # check "name" command...
  local name="$1"; shift
  if out="$("$@" 2>&1)"; then echo "PASS  $name"; else
    echo "FAIL  $name"; { echo "$out" | grep -E "^(FAIL|Traceback|Error)" || echo "$out" | tail -5; } | head -12 | sed 's/^/      /'
    fails=$((fails+1)); fi
  left="$(echo "$out" | sed -n 's/.*run left in \([^)]*\)).*/\1/p' | tail -1)"
  [ -n "$left" ] && [ -d "$left" ] && case "$left" in /tmp/*|/var/*|/private/*|*/tmp/*) rm -rf "$left";; esac
}
# a case statement inside $( ) breaks macOS's bash 3.2, so the reasons come from a function (v41)
why() { if [ "$1" = zstd ]; then echo 'the room archives cannot be opened'; elif [ "$1" = codex ]; then echo 'the yard cannot code'; else echo 'the aggregator cannot run'; fi; }
for tool in zstd codex claude; do
  command -v "$tool" >/dev/null 2>&1 || echo "WARN  $tool is not installed: $(why "$tool")"
done
export PYTHONDONTWRITEBYTECODE=1
check "the close-checks each catch their planted defect" python3 $AG/instrument/tools/validate.py --self-test --summary
check "the analyst's verbs" python3 $AG/instrument/tools/tests/test_verbs.py
check "the harness (build, checkpoint, talk command)" bash $AG/handler/claude/tests/run.sh "$A"
check "every data and handler script parses" python3 - <<'PY'
import glob, subprocess, sys
bad = []
for p in glob.glob("data/**/*.py", recursive=True) + glob.glob("aggregator/handler/*.py") + glob.glob("aggregator/handler/codex/**/*.py", recursive=True) + glob.glob("coder/handler/tools/*.py"):
    try: compile(open(p, encoding="utf-8").read(), p, "exec")
    except SyntaxError as e: bad.append("%s: %s" % (p, e))
for p in glob.glob("data/**/*.sh", recursive=True) + ["verify.sh"]:
    if subprocess.run(["bash", "-n", p]).returncode: bad.append(p)
print("\n".join(bad)); sys.exit(1 if bad else 0)
PY
check "no full path in the aggregator or its handler (the corpus in package/ and trees/ is Reddit text, not paths)" python3 - <<'PY'
import os, re, sys
pat = re.compile(r'''(^|[\s"'(=`])(/Users/|/home/|/sessions/|/mnt/|/private/|/root/|/tmp/|/var/folders/|~/mnt/|~/Jail/|[A-Z]:\\)''')
A = "aggregator"; R = A + "/runs/"
skip = (A + "/input", A + "/handler/_work")
rskip = ("/CONTROL/.cc", "/00_GIVE-THE-AGENT/out/_views", "/CONTROL/snapshots", "/00_GIVE-THE-AGENT/out/_transcripts", "/_to_delete", "/interview-workspaces", "/00_GIVE-THE-AGENT/package", "/00_GIVE-THE-AGENT/trees", "/CONTROL/legs", "/interviews")
bad = []
for root, dirs, files in os.walk(A):
    dirs[:] = [d for d in dirs if not os.path.join(root, d).startswith(skip) and d not in ("__pycache__", ".git")
               and not (os.path.join(root, d).startswith(R) and os.path.join(root, d).endswith(rskip))]
    for f in files:
        p = os.path.join(root, f)
        if p.startswith(R) and p.endswith("/00_GIVE-THE-AGENT/.claude/settings.json"): continue   # rendered per machine at each step, gitignored (HANDLER.md, Paths)
        try: lines = open(p, encoding="utf-8").read().splitlines()
        except (UnicodeDecodeError, OSError): continue
        # a sandbox rule that denies the system's temporary folders names them on purpose (the Codex runtime)
        bad += ["%s:%d" % (p, i) for i, l in enumerate(lines, 1) if pat.search(l) and "'deny'" not in l]
print("\n".join(bad[:10])); sys.exit(1 if bad else 0)
PY
check "the v38 frame: every room has its nine files, and the store holds exactly the frame" python3 - "$RUN" "$IN" <<'PY'
import csv, json, os, sys
R = sys.argv[1]; C = sys.argv[2] + "/coders"
rooms = [r["sub"] for r in csv.DictReader(open(C + "/ROOMS.tsv"), delimiter="\t")]
need = ["brief.md", "case.md", "codes.jsonl", "themes.jsonl", "threads.jsonl", "pointers.jsonl", "window.json",
        "forest/forest.jsonl", "forest/tree_index.json"]
miss = ["%s/%s" % (s, f) for s in rooms for f in need if not os.path.exists("%s/rooms/%s/%s" % (C, s, f))]
store = {json.loads(l)["sub"] for l in open(R + "/00_GIVE-THE-AGENT/package/store/rooms.jsonl")}
print("%d rooms; missing files %d %s; store differs %s" % (len(rooms), len(miss), miss[:5], sorted(store ^ set(rooms))[:5]))
sys.exit(1 if miss or store != set(rooms) else 0)
PY
check "the canvas and the D4 table cover the frame and nothing else" python3 - "$RUN" "$IN" <<'PY'
import csv, sys
R = sys.argv[1]; I = sys.argv[2]
rooms = {r["sub"] for r in csv.DictReader(open(I + "/coders/ROOMS.tsv"), delimiter="\t")}
px = {r["sub"] for r in csv.DictReader(open(I + "/canvas/pixels.csv"))}
act = {r["sub"] for r in csv.DictReader(open(R + "/DROPS/D4/data/activity-week-before.csv"))}
bad = sorted(px - rooms) + sorted(rooms ^ act)
print("pixels.csv rooms %d, activity rows %d, mismatches %s" % (len(px), len(act), bad[:5])); sys.exit(1 if bad else 0)
PY
# the frame against the census: a known open item is a warning, not a failure
python3 - "$IN" <<'PY'
import csv, sys
I = sys.argv[1]
rooms = {r["sub"] for r in csv.DictReader(open(I + "/coders/ROOMS.tsv"), delimiter="\t")}
pop = {r["sub"] for r in csv.DictReader(open("coder/census/MASTER-census.csv")) if r["handable"] == "1"}
out = sorted(rooms - pop)
print(("WARN  the frame holds %d rooms outside the census population: %s (an open item for the handler)" % (len(out), ", ".join(out)))
      if out else "PASS  every frame room is in the census population")
PY
echo; [ "$fails" -eq 0 ] && echo "all checks passed" || { echo "$fails check(s) failed"; exit 1; }
