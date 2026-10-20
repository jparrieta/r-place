#!/usr/bin/env python3
"""D3a-46, read-only: for every REJ or PART row of a rows file ('id|CLASS|evidence'), name the writer of each concept
the row cites, from A19's window quote files and cites files (as d3_a19_crossauthors.py reads them), and flag a writer
whose posts in those files sit in more than one room, so that no REJ rests unread on a cross-poster (G50 reading 108,
G51 reading 103). Writes nothing.

  python3 out/_analysis/d3_a19_rej_crosscheck.py --rows out/_analysis/d3_rulings/A19-absent-rows.txt
"""
import argparse
import glob
import re
from collections import defaultdict

ap = argparse.ArgumentParser()
ap.add_argument("--rows", required=True)
a = ap.parse_args()

QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]\s+item \S+\s+thread \S+\s+h\+([\d.]+)\s+(\S+)')
author = {}
rooms_of = defaultdict(set)
for f in sorted(glob.glob("out/_analysis/d3_wq_A19_*.txt") + glob.glob("out/_analysis/d3_cites_A19_*.txt")):
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m:
            author[(m.group(2), m.group(3))] = m.group(5)
            if m.group(5) != "[deleted]":
                rooms_of[m.group(5)].add(m.group(2))

flagged, rows, unknown = 0, 0, 0
for l in open(a.rows, encoding="utf-8"):
    l = l.strip()
    if not l:
        continue
    aid, cls, ev = l.split("|", 2)
    rows += 1
    room = aid.rsplit("-", 1)[0]
    codes = sorted(set(re.findall(r"\bc\d{4}\b", ev)))
    parts = []
    for c in codes:
        w = author.get((room, c))
        if w is None:
            unknown += 1
            parts.append("%s ?" % c)
            continue
        other = sorted(rooms_of.get(w, set()) - {room})
        if other:
            flagged += 1
            parts.append("%s %s ALSO IN %s" % (c, w, ",".join(other)))
        else:
            parts.append("%s %s" % (c, w))
    print("%s %s: %s" % (aid, cls, "; ".join(parts)))
print("rows: %d; cited concepts by a writer also in another room: %d; cited concepts with no writer in the files: %d"
      % (rows, flagged, unknown))
