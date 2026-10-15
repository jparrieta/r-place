#!/usr/bin/env python3
"""C5c-10, rule 14: F-018 (Stigmergy's recut) is touched by the rename of T4-007 to Direct information sharing. Appends a
superseding F-018 line: the statement takes the theme's new name, the bound adds why the old name was dropped, status
bounded. Refuses if a C5c-10 F-018 line exists.

    python3 out/_analysis/c5c10_f018.py
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(ROOT, "out", "findings.jsonl")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
rows = [json.loads(l) for l in open(F, encoding="utf-8") if l.strip()]
f18 = [r for r in rows if r["id"] == "F-018"]
if any(r.get("leg") == LEG for r in f18):
    sys.exit("F-018 already has a line from this leg")
r = dict(f18[-1])
old = "and Stigmergy holds building and reporting alone."
if old not in r["statement"]:
    sys.exit("the statement's last clause is not as expected")
r["statement"] = r["statement"].replace(old, "and the theme holds building and reporting alone; since C5c-10 it is "
                                              "named Direct information sharing (T4-007).")
r["bound"] = r["bound"] + (" At C5c-10 the recut stands and the theme was renamed: its records are members' posts of the "
                           "work's state, which Okhuysen and Bechky (2009, p. 474) call direct information sharing; "
                           "the name Stigmergy claimed the placing that would answer the posts, which the record does "
                           "not hold (serial-C5/finding-4-stigmergy-aligned.md).")
r.update({"stage": "C5", "leg": LEG, "status": "bounded", "supersedes": "F-018",
          "t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
r["literature"] = list(r.get("literature") or []) + ["Okhuysen and Bechky 2009", "Moffett et al. 2021"]
with open(F, "a", encoding="utf-8") as f:
    f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("F-018 superseded; findings.jsonl now %d lines" % (len(rows) + 1))
