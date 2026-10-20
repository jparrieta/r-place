#!/usr/bin/env python3
"""D3a-43: check every single-quoted segment in G48 (notes-D3.md, segments as d3_spec_quotes.py finds them) against
A16's arrow record (model/arrows.jsonl), and list those found in no field. Writes nothing.

  python3 out/_analysis/d3_a16_g48_quote_check.py
"""
import json
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
g48 = notes.split("- **G48 (logged at D3a-43")[1].split("## Where the mass is")[0].split("- **G48's readings")[0]
arrow = next(json.loads(l) for l in open("out/model/arrows.jsonl", encoding="utf-8") if json.loads(l)["id"] == "A16")
src = [json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v for v in arrow.values()]
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
segs = SEG.findall(g48)
miss = [s for s in segs if not any(s in t for t in src)]
print("G48: segments %d; found in A16's record %d; not found %d" % (len(segs), len(segs) - len(miss), len(miss)))
for s in miss:
    print("  " + s)
