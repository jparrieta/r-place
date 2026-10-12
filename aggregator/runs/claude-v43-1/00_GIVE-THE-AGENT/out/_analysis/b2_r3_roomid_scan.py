#!/usr/bin/env python3
"""B2a-r3-p2: scan round 3's packet files for room code or room theme ids (J, 12:15 Berlin: fleet.py refuses a
packet with codes_by_item if any room id appears in its text, headings included). Two patterns: the strict one
(c or t and digits, as the room writes them: c0006, t01) and the builder's looser one. Prints each hit with its
line number and the line whole. Reads only; writes nothing."""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, "out", "_packets-B2", "round-3")
STRICT = re.compile(r"\b(?:c\d{4}|t\d{2})\b")
LOOSE = re.compile(r"(?<![A-Za-z0-9])[ct]\d{2,4}(?![0-9])", re.I)

for p in sorted(glob.glob(os.path.join(D, "*.md"))):
    n_s = n_l = 0
    for i, ln in enumerate(open(p, encoding="utf-8"), 1):
        s, l = STRICT.findall(ln), LOOSE.findall(ln)
        n_s += len(s); n_l += len(l)
        if l:
            print("%s:%d %s | %s" % (os.path.basename(p), i, ",".join(l), ln.rstrip("\n")))
    print("== %s strict %d loose %d" % (os.path.basename(p), n_s, n_l))
