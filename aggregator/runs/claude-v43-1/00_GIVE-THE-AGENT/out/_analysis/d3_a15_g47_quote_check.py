#!/usr/bin/env python3
"""D3a-42: check every single-quoted segment in G47 (notes-D3.md, segments as d3_spec_quotes.py finds them) against
A15's arrow record (model/arrows.jsonl) and the D3a-02 section of notes-D3.md, and list those found in neither.
Writes nothing.

  python3 out/_analysis/d3_a15_g47_quote_check.py
"""
import json
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
g47 = notes.split("- **G47 (logged at D3a-42")[1].split("## Where the mass is")[0].split("- **G47's readings")[0]
d3a02 = notes.split("## D3a-02: P01")[1].split("## D3a-03")[0]
arrow = next(json.loads(l) for l in open("out/model/arrows.jsonl", encoding="utf-8") if json.loads(l)["id"] == "A15")
src = [str(v) for v in arrow.values()] + [d3a02]
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
segs = SEG.findall(g47)
miss = [s for s in segs if not any(s in t for t in src)]
print("G47: segments %d; found in A15's record or the D3a-02 section %d; not found %d" % (
    len(segs), len(segs) - len(miss), len(miss)))
for s in miss:
    print("  " + s)
