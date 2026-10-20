#!/usr/bin/env python3
"""D3a-46: check every single-quoted segment in G51 (notes-D3.md, segments as d3_trunc_check.py finds them, so those
that close before a colon are read too) against A19's arrow record (model/arrows.jsonl) and F-008's latest line
(findings.jsonl), and list those found in neither, with the source each found segment came from. Writes nothing.

  python3 out/_analysis/d3_a19_g51_quote_check.py
"""
import json
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
g51 = notes.split("- **G51 (logged at D3a-46")[1].split("## Where the mass is")[0].split("- **G51's readings")[0]
arrow = next(json.loads(l) for l in open("out/model/arrows.jsonl", encoding="utf-8") if json.loads(l)["id"] == "A19")
f008 = [json.loads(l) for l in open("out/findings.jsonl", encoding="utf-8") if l.strip() and json.loads(l)["id"] == "F-008"][-1]


def fields(r):
    return [json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v for v in r.values()]


src = {"A19": fields(arrow), "F-008": fields(f008)}
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
segs = SEG.findall(g51)
miss = 0
for s in segs:
    where = [k for k, v in src.items() if any(s in t for t in v)]
    miss += not where
    print("  %s | %s" % (",".join(where) or "NOT FOUND", s))
print("G51: segments %d; found %d; not found %d" % (len(segs), len(segs) - miss, miss))
