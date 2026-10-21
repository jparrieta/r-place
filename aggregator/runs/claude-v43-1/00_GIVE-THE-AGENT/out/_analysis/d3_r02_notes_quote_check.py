#!/usr/bin/env python3
"""D3a-49: check every single-quoted segment in notes-D3.md's D3a-49 section and in G54's readings (segments as
d3_trunc_check.py finds them, so those that close before a colon are read too) against the quotes cite.py printed in
R02's quote files and cites files, and list those found in none, with whether R02's element record holds them.
Writes nothing. A copy of d3_p06_notes_quote_check.py for R02.

  python3 out/_analysis/d3_r02_notes_quote_check.py
"""
import glob
import json
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
sec = notes.split("## D3a-49: P06's status ruled again; R02, the envoy")[1]
readings = notes.split("- **G54's readings (D3a-49).**")[1].split("## Where the mass is")[0]
el = next(json.loads(l) for l in open("out/model/elements.jsonl", encoding="utf-8") if l.strip()
          and json.loads(l)["id"] == "R02")
fields = [json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v for v in el.values()]
QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]')
quotes = []
for f in glob.glob("out/_analysis/d3_wq_R02_*.txt") + glob.glob("out/_analysis/d3_absent_cites_R02*.txt"):
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m:
            quotes.append(m.group(1))
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
for name, text in (("D3a-49 section", sec), ("G54's readings", readings)):
    segs = SEG.findall(text)
    miss = [s for s in segs if not any(s in q for q in quotes)]
    print("%s: segments %d; found in a room quote %d; not found %d" % (name, len(segs), len(segs) - len(miss), len(miss)))
    for s in miss:
        print("  not in a room quote: %r; in R02's element record: %s" % (s, any(s in f for f in fields)))
