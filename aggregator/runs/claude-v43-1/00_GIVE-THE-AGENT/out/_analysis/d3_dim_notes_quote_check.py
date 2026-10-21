#!/usr/bin/env python3
"""D3a-54: check every single-quoted segment in notes-D3.md's D3a-54 section, in G58 and in G58's readings (segments
as d3_trunc_check.py finds them) against the quotes cite.py printed in the dimension windows' quote files, and list
those found in none, with whether the dimension records (dimensions.jsonl) or the stage's own notes hold them.
Writes nothing. A copy of d3_p19_notes_quote_check.py for the dimension lines.

  python3 out/_analysis/d3_dim_notes_quote_check.py
"""
import glob
import json
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
sec = notes.split("## D3a-54: the dimension lines")[1]
g58 = notes.split("- **G58 (logged at D3a-54, before any dimension line was read or ruled).**")[1].split(
    "- **G58's readings (D3a-54).**")[0]
readings = notes.split("- **G58's readings (D3a-54).**")[1].split("## Where the mass is")[0]
dims = [json.dumps(json.loads(l), ensure_ascii=False) for l in open("out/dimensions.jsonl", encoding="utf-8")
        if l.strip()]
QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]')
quotes = []
for f in glob.glob("out/_analysis/d3_wq_D0*_[alrs]00[1-9]_0*.txt") + glob.glob("out/_analysis/d3_wq_D0*_l00[134]_0*.txt"):
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m:
            quotes.append(m.group(1))
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
for name, text in (("D3a-54 section", sec), ("G58", g58), ("G58's readings", readings)):
    segs = SEG.findall(text)
    miss = [s for s in segs if not any(s in q for q in quotes)]
    print("%s: segments %d; found in a room quote %d; not found %d" % (name, len(segs), len(segs) - len(miss), len(miss)))
    for s in miss:
        print("  not in a room quote: %r; in a dimension record: %s" % (s, any(s in d for d in dims)))
