#!/usr/bin/env python3
"""D3a-47: check every single-quoted segment in G52 (notes-D3.md, segments as d3_trunc_check.py finds them, so those
that close before a colon are read too) against A20's arrow record (model/arrows.jsonl) and F-010's latest line
(findings.jsonl), and list those found in neither, with the source each found segment came from. Writes nothing.

  python3 out/_analysis/d3_a20_g52_quote_check.py
"""
import json
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
g52 = notes.split("- **G52 (logged at D3a-47")[1].split("## Where the mass is")[0].split("- **G52's readings")[0]
arrow = next(json.loads(l) for l in open("out/model/arrows.jsonl", encoding="utf-8") if json.loads(l)["id"] == "A20")
f010 = [json.loads(l) for l in open("out/findings.jsonl", encoding="utf-8") if l.strip() and json.loads(l)["id"] == "F-010"][-1]


def fields(r):
    return [json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v for v in r.values()]


src = {"A20": fields(arrow), "F-010": fields(f010)}
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
segs = SEG.findall(g52)
miss = 0
for s in segs:
    where = [k for k, v in src.items() if any(s in t for t in v)]
    miss += not where
    print("  %s | %s" % (",".join(where) or "NOT FOUND", s))
print("G52: segments %d; found %d; not found %d" % (len(segs), len(segs) - miss, miss))
