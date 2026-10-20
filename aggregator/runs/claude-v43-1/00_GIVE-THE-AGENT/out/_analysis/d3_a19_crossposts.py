#!/usr/bin/env python3
"""D3a-46, read-only: list quote texts that cite.py printed for more than one room across A19's window quote files and
cites files (d3_wq_A19_*.txt, d3_cites_A19_*.txt), with each room, code and author, to find cross-posted messages
whose writer may not be the room's member (G50 reading 108). Texts shorter than 25 characters are skipped. Writes
nothing.

  python3 out/_analysis/d3_a19_crossposts.py
"""
import glob
import re
from collections import defaultdict

QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]\s+item \S+\s+thread \S+\s+h\+[\d.]+\s+(\S+)')
seen = defaultdict(set)
for f in sorted(glob.glob("out/_analysis/d3_wq_A19_*.txt") + glob.glob("out/_analysis/d3_cites_A19_*.txt")):
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m and len(m.group(1)) >= 25:
            seen[m.group(1)].add((m.group(2), m.group(3), m.group(4)))
n = 0
for text, where in sorted(seen.items()):
    rooms = {w[0] for w in where}
    if len(rooms) > 1:
        n += 1
        print("%s\n   %s" % (text[:160], "; ".join("%s/%s by %s" % w for w in sorted(where))))
print("texts in more than one room:", n)
