#!/usr/bin/env python3
"""C5a-01: correct the `supersedes` field of the C5a-01 line for F-016, written by c5_f016_supersede.py as
'F-016 (C3c)'; the check requires an id the file carries, 'F-016'. Changes that one field of that one line and nothing
else; the script that wrote it is fixed to write 'F-016'.

    python3 out/_analysis/c5_f016_fix.py
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = os.path.join(ROOT, "out", "findings.jsonl")
rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
hit = [r for r in rows if r["id"] == "F-016" and r.get("leg") == "C5a-01" and r.get("supersedes") == "F-016 (C3c)"]
if len(hit) != 1:
    sys.exit("the line to fix was not found once")
hit[0]["supersedes"] = "F-016"
with open(path, "w", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
print("fixed; %d lines" % len(rows))
