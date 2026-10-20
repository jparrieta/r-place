#!/usr/bin/env python3
"""D3a-46, read-only: list writers whose posts cite.py printed in more than one room across A19's window quote files
and cites files (d3_wq_A19_*.txt, d3_cites_A19_*.txt), with each room and code, so that a line resting on a writer who
posts in several rooms can be read again under G50's reading 108 (a cross-posted message whose writer's side the
words do not show is not the room's). Deleted authors are skipped. Writes nothing.

  python3 out/_analysis/d3_a19_crossauthors.py
"""
import glob
import re
from collections import defaultdict

QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]\s+item \S+\s+thread \S+\s+h\+([\d.]+)\s+(\S+)')
by = defaultdict(set)
for f in sorted(glob.glob("out/_analysis/d3_wq_A19_*.txt") + glob.glob("out/_analysis/d3_cites_A19_*.txt")):
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m and m.group(5) != "[deleted]":
            by[m.group(5)].add((m.group(2), m.group(3), m.group(4)))
n = 0
for a, where in sorted(by.items()):
    rooms = sorted({w[0] for w in where})
    if len(rooms) > 1:
        n += 1
        print("%s: %s" % (a, "; ".join("%s/%s h+%s" % w for w in sorted(where))))
print("writers in more than one room:", n)
