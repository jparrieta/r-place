#!/usr/bin/env python3
"""D3a-48: check every single-quoted segment in notes-D3.md's D3a-48 section and in G53's readings (segments as
d3_trunc_check.py finds them, so those that close before a colon are read too) against the quotes cite.py printed in
P06's quote files and cites files, and list those found in none, with whether P06's element record holds them.
Writes nothing.

  python3 out/_analysis/d3_p06_notes_quote_check.py
"""
import glob
import json
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
sec = notes.split("## D3a-48: P06")[1]
readings = notes.split("- **G53's readings (D3a-48).**")[1].split("## Where the mass is")[0]
el = next(json.loads(l) for l in open("out/model/elements.jsonl", encoding="utf-8") if l.strip()
          and json.loads(l)["id"] == "P06")
fields = [json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v for v in el.values()]
QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]')
quotes = []
for f in glob.glob("out/_analysis/d3_wq_P06_*.txt") + glob.glob("out/_analysis/d3_absent_cites_P06*.txt"):
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m:
            quotes.append(m.group(1))
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
for name, text in (("D3a-48 section", sec), ("G53's readings", readings)):
    segs = SEG.findall(text)
    miss = [s for s in segs if not any(s in q for q in quotes)]
    print("%s: segments %d; found in a room quote %d; not found %d" % (name, len(segs), len(segs) - len(miss), len(miss)))
    for s in miss:
        print("  %s | in P06's record: %s" % (s, any(s in t for t in fields)))
