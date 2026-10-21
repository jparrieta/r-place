#!/usr/bin/env python3
"""D3a-52: check every single-quoted segment in notes-D3.md's D3a-52 section, in G56a and in G56's readings
(segments as d3_trunc_check.py finds them, so those that close before a colon are read too) against the quotes
cite.py printed in K04's quote files and cites files, and list those found in none, with whether K04's element record
holds them. Writes nothing. A copy of d3_r02_notes_quote_check.py for K04.

  python3 out/_analysis/d3_k04_notes_quote_check.py
"""
import glob
import json
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
sec = notes.split("## D3a-52: K04, the body carried in and the colour faith")[1]
g56a = notes.split("- **G56a (amendment, 21 October 2026, D3a-52;")[1].split("- **G56's readings (D3a-52).**")[0]
readings = notes.split("- **G56's readings (D3a-52).**")[1].split("## Where the mass is")[0]
el = next(json.loads(l) for l in open("out/model/elements.jsonl", encoding="utf-8") if l.strip()
          and json.loads(l)["id"] == "K04")
fields = [json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v for v in el.values()]
QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]')
quotes = []
for f in glob.glob("out/_analysis/d3_wq_K04_*.txt") + glob.glob("out/_analysis/d3_absent_cites_K04*.txt"):
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m:
            quotes.append(m.group(1))
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
for name, text in (("D3a-52 section", sec), ("G56a", g56a), ("G56's readings", readings)):
    segs = SEG.findall(text)
    miss = [s for s in segs if not any(s in q for q in quotes)]
    print("%s: segments %d; found in a room quote %d; not found %d" % (name, len(segs), len(segs) - len(miss), len(miss)))
    for s in miss:
        print("  not in a room quote: %r; in K04's element record: %s" % (s, any(s in f for f in fields)))
