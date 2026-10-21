#!/usr/bin/env python3
"""D3a-57: run `handoff.py D --recheck <rooms>` with the affected rooms read from out/recheck-scope.json, so
that no room name is typed. Refuses if handoff-D/recheck/tasks already exists (a handoff is written once per
version) or if the model hash differs from the version MODEL-D3.md names.

    python3 out/_analysis/d3_recheck_handoff.py
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib  # noqa: E402

scope = json.load(open(os.path.join(OUT, "recheck-scope.json"), encoding="utf-8"))
rooms = scope["affected_rooms"]
if os.path.exists(os.path.join(OUT, "handoff-D", "recheck", "tasks")):
    sys.exit("refused: handoff-D/recheck/tasks exists")
named = re.search(r"Model version: ([0-9a-f]{64})", open(os.path.join(OUT, "MODEL-D3.md"), encoding="utf-8").read())
mh = vlib.model_hash(OUT)
if not named or named.group(1) != mh:
    sys.exit("refused: MODEL-D3.md names %s, the model hashes to %s" % (named.group(1) if named else None, mh))
print("rooms %d; model %s" % (len(rooms), mh))
r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "handoff.py"), "D", "--recheck", ",".join(rooms),
                    "--root", ROOT], cwd=ROOT)
sys.exit(r.returncode)
