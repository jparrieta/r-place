#!/usr/bin/env python3
"""D4a-06: confirm that the files J named are unchanged since the D4a-05 close snap: branches.jsonl,
crosslinks.jsonl, tree-D4.md, every forms/ file, room-forms-D4a05.*, and the D5 files. Read-only.

    python3 out/_analysis/d4a06_unchanged.py
"""
import glob, hashlib, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
snap = sorted(glob.glob(os.path.join(OUT, "_snap", "D4-cut-close-D4a-05-*.sha256")))[-1]
rec = {}
for ln in open(snap, encoding="utf-8"):
    if ln.startswith("#"):
        continue
    parts = ln.rstrip("\n").split(None, 3)
    if len(parts) == 4:
        rec[parts[3]] = parts[0]
names = ["branches.jsonl", "crosslinks.jsonl", "tree-D4.md", "branches-D5.jsonl", "survival-D5.md", "waterfall-D5.md",
         "handback-D5.md", "notes-D5.md", "room-forms-D4a05.md", "room-forms-D4a05.jsonl", "room-forms-D4a05.tsv"]
names += sorted(os.path.relpath(p, OUT) for p in glob.glob(os.path.join(OUT, "forms", "*")))
same = changed = missing = 0
for n in names:
    cur = hashlib.sha256(open(os.path.join(OUT, n), "rb").read()).hexdigest()
    if n not in rec:
        missing += 1
        print("not in snap:", n)
    elif rec[n] == cur:
        same += 1
    else:
        changed += 1
        print("CHANGED:", n)
print("snap", os.path.basename(snap), "files compared", len(names), "unchanged", same, "changed", changed, "not in snap", missing)
