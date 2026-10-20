#!/usr/bin/env python3
"""D3a-41: check every single-quoted segment in G46 (notes-D3.md, segments as d3_spec_quotes.py finds them) against
A14's arrow record (model/arrows.jsonl) and F-020's statement (findings.jsonl), and list those found in neither.
Writes nothing.

  python3 out/_analysis/d3_a14_g46_quote_check.py
"""
import json
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
g46 = notes.split("- **G46 (logged at D3a-41")[1].split("## Where the mass is")[0]
arrow = next(json.loads(l) for l in open("out/model/arrows.jsonl", encoding="utf-8") if json.loads(l)["id"] == "A14")
f020 = next(json.loads(l) for l in open("out/findings.jsonl", encoding="utf-8") if json.loads(l)["id"] == "F-020")
src = [str(v) for v in arrow.values()] + [f020["statement"], f020["bound"]]
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
segs = SEG.findall(g46)
miss = [s for s in segs if not any(s in t for t in src)]
print("G46: segments %d; found in A14's record or F-020 %d; not found %d" % (len(segs), len(segs) - len(miss), len(miss)))
for s in miss:
    print("  " + s)
