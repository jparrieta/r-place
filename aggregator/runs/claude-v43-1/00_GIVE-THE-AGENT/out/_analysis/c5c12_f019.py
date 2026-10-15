#!/usr/bin/env python3
"""C5c-12: F-019 quoted anarcho_capitalism/c0077 with its spelling corrected ('Building'); the record has 'Buildling'.
Appends a superseding F-019 line with the quote as the record has it, status unchanged, the bound noting the correction.
Refuses if F-019 already has a line from this leg.

    python3 out/_analysis/c5c12_f019.py
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(ROOT, "out", "findings.jsonl")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
rows = [json.loads(l) for l in open(F, encoding="utf-8") if l.strip()]
f = [r for r in rows if r["id"] == "F-019"]
if any(r.get("leg") == LEG for r in f):
    sys.exit("F-019 already has a line from this leg")
r = dict(f[-1])
old = "'Building ancap flag somewhere else would be a good idea'"
if old not in r["statement"]:
    sys.exit("the misquote is not in F-019's statement")
r["statement"] = r["statement"].replace(old, "'Buildling ancap flag somewhere else would be a good idea'")
r["bound"] = r["bound"] + " At C5c-12 a quote was restored to the record's spelling ('Buildling'); nothing else changed."
r.update({"leg": LEG, "supersedes": "F-019", "t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
with open(F, "a", encoding="utf-8") as fh:
    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print("F-019 superseded with the quote as recorded; findings.jsonl now %d lines" % (len(rows) + 1))
