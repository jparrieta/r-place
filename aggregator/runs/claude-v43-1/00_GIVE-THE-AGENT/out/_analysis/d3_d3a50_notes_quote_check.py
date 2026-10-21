#!/usr/bin/env python3
"""D3a-50: check every single-quoted segment in notes-D3.md's D3a-50 section (segments as d3_trunc_check.py finds
them) against the quotes cite.py printed in d3_p06p05_stop_cites.txt and in P06's quote and cites files, and list the
segments found in none. Writes nothing. A copy of d3_r02_notes_quote_check.py for this section.

  python3 out/_analysis/d3_d3a50_notes_quote_check.py
"""
import glob
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
sec = notes.split("## D3a-50: P06's order test against P05")[1]
QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]')
quotes = []
files = (["out/_analysis/d3_p06p05_stop_cites.txt"] + glob.glob("out/_analysis/d3_wq_P06_*.txt")
         + glob.glob("out/_analysis/d3_absent_cites_P06*.txt"))
for f in files:
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m:
            quotes.append(m.group(1))
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
segs = SEG.findall(sec)
miss = [s for s in segs if not any(s in q for q in quotes)]
print("D3a-50 section: segments %d; found in a room quote %d; not found %d" % (len(segs), len(segs) - len(miss),
                                                                              len(miss)))
for s in miss:
    print("  not in a room quote: %r" % s)
