#!/usr/bin/env python3
"""D3a-40: check every single-quoted segment in notes-D3.md's D3a-40 section and in G45's readings (segments as
d3_spec_quotes.py finds them) against the quotes cite.py printed in A13's quote files, and list those found in none,
with whether the G45 paragraph (A13's fields as quoted there) holds them. Writes nothing.

  python3 out/_analysis/d3_a13_notes_quote_check.py
"""
import glob
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
sec = notes.split("## D3a-40: A13")[1]
readings = notes.split("- **G45's readings (D3a-40).**")[1].split("## Where the mass is")[0]
g45 = notes.split("- **G45 (logged at D3a-40")[1].split("- **G45's readings")[0]
QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]')
quotes = []
for f in glob.glob("out/_analysis/d3_wq_A13_*.txt") + glob.glob("out/_analysis/d3_cites_A13_*.txt"):
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m:
            quotes.append(m.group(1))
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
for name, text in (("D3a-40 section", sec), ("G45's readings", readings)):
    segs = SEG.findall(text)
    miss = [s for s in segs if not any(s in q for q in quotes)]
    print("%s: segments %d; found in a room quote %d; not found %d" % (name, len(segs), len(segs) - len(miss), len(miss)))
    for s in miss:
        print("  %s | in G45's paragraph: %s" % (s, s in g45))
