#!/usr/bin/env python3
"""D3a-53: check every single-quoted segment in notes-D3.md's D3a-53 section, in G57 and in G57's readings
(segments as d3_trunc_check.py finds them, so those that close before a colon are read too) against the quotes
cite.py printed in P19's quote files and cites files, and list those found in none, with whether P19's element record
holds them. Writes nothing. A copy of d3_k04_notes_quote_check.py for P19.

  python3 out/_analysis/d3_p19_notes_quote_check.py
"""
import glob
import json
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
sec = notes.split("## D3a-53: P19, the host and its guests")[1]
g57 = notes.split("- **G57 (logged at D3a-53, before any of P19's lines was read or ruled).**")[1].split(
    "- **G57's readings (D3a-53).**")[0]
readings = notes.split("- **G57's readings (D3a-53).**")[1].split("## Where the mass is")[0]
el = next(json.loads(l) for l in open("out/model/elements.jsonl", encoding="utf-8") if l.strip()
          and json.loads(l)["id"] == "P19")
fields = [json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v for v in el.values()]
QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]')
quotes = []
for f in glob.glob("out/_analysis/d3_wq_P19_*.txt") + glob.glob("out/_analysis/d3_absent_cites_P19*.txt"):
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m:
            quotes.append(m.group(1))
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
for name, text in (("D3a-53 section", sec), ("G57", g57), ("G57's readings", readings)):
    segs = SEG.findall(text)
    miss = [s for s in segs if not any(s in q for q in quotes)]
    print("%s: segments %d; found in a room quote %d; not found %d" % (name, len(segs), len(segs) - len(miss), len(miss)))
    for s in miss:
        print("  not in a room quote: %r; in P19's element record: %s" % (s, any(s in f for f in fields)))
