#!/usr/bin/env python3
"""C2, pass 3, read-only: the rooms whose pre-event brief is empty (the harness's "empty brief": no posts or comments
in the week before the canvas), over the analysed rooms, through `mem.py brief <sub>` (one logged read per room).
Declared in notes-C2.md (pass 3) before the count: a room with an empty brief may have been founded by the canvas.
Writes out/_analysis/c2_empty_brief-p3.json (refuses to overwrite) and prints the count with items_in_window per room.

    python3 out/_analysis/c2_empty_brief.py
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(OUT, "_analysis", "c2_empty_brief-p3.json")
if os.path.exists(DEST):
    sys.exit("c2_empty_brief-p3.json exists; not overwritten")


def mem(*args):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py")] + list(args), cwd=ROOT,
                       capture_output=True, text=True)
    return p.stdout


size = {}
txt = mem("facts", "--field", "items_in_window", "--json", "--limit", "10000")
for l in txt.splitlines():
    if l.startswith("{"):
        r = json.loads(l)
        size[r["sub"]] = r.get("items_in_window")
if len(size) != 705:
    sys.exit("expected 705 rooms from facts, got %d" % len(size))
empty = []
for s in sorted(size):
    b = mem("brief", s, "--limit", "40")
    if "Harness-generated empty brief" in b:
        empty.append(s)
json.dump({"rule": "pre-event brief is the harness's empty brief (no posts or comments in the pre-week archive)",
           "rooms": len(size), "empty": empty}, open(DEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rooms with an empty pre-event brief: %d of %d" % (len(empty), len(size)))
print(", ".join("%s (%s)" % (s, size[s]) for s in empty))
