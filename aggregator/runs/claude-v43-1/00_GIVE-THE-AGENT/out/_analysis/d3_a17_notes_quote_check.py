#!/usr/bin/env python3
"""D3a-44: check every single-quoted segment in notes-D3.md's D3a-44 section and in G49's readings (segments as
d3_trunc_check.py finds them, so those that close before a colon are read too) against the quotes cite.py printed in
A17's quote files and cites files, and list those found in none, with whether A17's arrow record holds them. Writes
nothing.

  python3 out/_analysis/d3_a17_notes_quote_check.py
"""
import glob
import json
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
sec = notes.split("## D3a-44: A17")[1]
readings = notes.split("- **G49's readings (D3a-44).**")[1].split("## Where the mass is")[0]
arrow = next(json.loads(l) for l in open("out/model/arrows.jsonl", encoding="utf-8") if json.loads(l)["id"] == "A17")
fields = [json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v for v in arrow.values()]
QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]')
quotes = []
for f in glob.glob("out/_analysis/d3_wq_A17_*.txt") + glob.glob("out/_analysis/d3_cites_A17_*.txt"):
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m:
            quotes.append(m.group(1))
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
for name, text in (("D3a-44 section", sec), ("G49's readings", readings)):
    segs = SEG.findall(text)
    miss = [s for s in segs if not any(s in q for q in quotes)]
    print("%s: segments %d; found in a room quote %d; not found %d" % (name, len(segs), len(segs) - len(miss), len(miss)))
    for s in miss:
        print("  %s | in A17's record: %s" % (s, any(s in t for t in fields)))
