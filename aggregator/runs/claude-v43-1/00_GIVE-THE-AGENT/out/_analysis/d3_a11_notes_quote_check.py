#!/usr/bin/env python3
"""D3a-38: check every single-quoted segment in notes-D3.md's D3a-38 section (segments as d3_spec_quotes.py finds
them) against the quotes cite.py printed in A11's quote files, and list those found in none, with whether the G43
paragraph (A11's fields as quoted there) holds them. Writes nothing.

  python3 out/_analysis/d3_a11_notes_quote_check.py
"""
import glob
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
sec = notes.split("## D3a-38: A11")[1]
g43 = notes.split("- **G43 (logged at D3a-38")[1].split("- **G43's readings")[0]
QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]')
quotes = []
for f in glob.glob("out/_analysis/d3_wq_A11_*.txt") + glob.glob("out/_analysis/d3_absent_cites_A11_*.txt") + \
        glob.glob("out/_analysis/d3_cites_A11_*.txt"):
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m:
            quotes.append(m.group(1))
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
segs = SEG.findall(sec)
miss = [s for s in segs if not any(s in q for q in quotes)]
print("segments: %d; found in a room quote: %d; not found: %d" % (len(segs), len(segs) - len(miss), len(miss)))
for s in miss:
    print("  %s | in G43's paragraph: %s" % (s, s in g43))
