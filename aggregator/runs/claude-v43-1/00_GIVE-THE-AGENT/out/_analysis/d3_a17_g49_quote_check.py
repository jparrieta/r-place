#!/usr/bin/env python3
"""D3a-44: check every single-quoted segment in G49 (notes-D3.md, segments as d3_trunc_check.py finds them, so those
that close before a colon are read too) against A17's arrow record (model/arrows.jsonl), and list those found in no
field. Writes nothing.

  python3 out/_analysis/d3_a17_g49_quote_check.py
"""
import json
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
g49 = notes.split("- **G49 (logged at D3a-44")[1].split("## Where the mass is")[0].split("- **G49's readings")[0]
arrow = next(json.loads(l) for l in open("out/model/arrows.jsonl", encoding="utf-8") if json.loads(l)["id"] == "A17")
src = [json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v for v in arrow.values()]
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
segs = SEG.findall(g49)
miss = [s for s in segs if not any(s in t for t in src)]
print("G49: segments %d; found in A17's record %d; not found %d" % (len(segs), len(segs) - len(miss), len(miss)))
for s in miss:
    print("  " + s)
