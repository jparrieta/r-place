#!/usr/bin/env python3
"""D4a-05: confirm that the files J named are unchanged since the D5b close snap: branches.jsonl,
crosslinks.jsonl, tree-D4.md, every forms/ file, the D5 survival, waterfall and handback files, and
branches-D5.jsonl. Compares each file's sha256 now with its line in the snap. Read-only.

    python3 out/_analysis/d4a05_unchanged.py
"""
import glob, hashlib, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
snaps = sorted(glob.glob(os.path.join(OUT, "_snap", "D5-cut-close-D5b-*.sha256")))
snap = snaps[-1]
rec = {}
for ln in open(snap, encoding="utf-8"):
    if ln.startswith("#"):
        continue
    parts = ln.rstrip("\n").split(None, 3)  # sha256, size, time, path
    if len(parts) == 4:
        rec[parts[3]] = parts[0]
names = ["branches.jsonl", "crosslinks.jsonl", "tree-D4.md", "branches-D5.jsonl", "survival-D5.md",
         "waterfall-D5.md", "handback-D5.md", "notes-D5.md"]
names += sorted(os.path.relpath(p, OUT) for p in glob.glob(os.path.join(OUT, "forms", "*")))
same = changed = missing = 0
for n in names:
    key = next((k for k in rec if k == n or k.endswith("/" + n) or k == "out/" + n), None)
    cur = hashlib.sha256(open(os.path.join(OUT, n), "rb").read()).hexdigest()
    if key is None:
        missing += 1
        print("not in snap:", n)
    elif rec[key] == cur:
        same += 1
    else:
        changed += 1
        print("CHANGED:", n)
print("snap", os.path.basename(snap), "files compared", len(names), "unchanged", same, "changed", changed, "not in snap", missing)
