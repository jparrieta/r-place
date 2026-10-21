#!/usr/bin/env python3
"""D3a-47, read-only: the G1b draws of an arrow's instantiate packets and the class each drawn line was given in its
joined spec file. Reads each draw file for the drawn ids, in the lines the draw script prints as '<id> instantiate',
and prints the classes by draw. A general form of d3_a19_draw_outcomes.py. Writes nothing.

  python3 out/_analysis/d3_draw_outcomes.py --spec out/_analysis/d3_rulings/A20-inst-spec.txt \
      --draws out/_analysis/d3_draw_A20_447.txt out/_analysis/d3_draw_A20_547.txt
"""
import argparse
import re
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("--draws", nargs="+", required=True)
a = ap.parse_args()
spec = {}
for l in open(a.spec, encoding="utf-8"):
    if l.strip():
        i, c, _ = l.split("|", 2)
        spec[i] = c
LINE = re.compile(r"^(\S+-\d{3})\s+instantiate\b")
for f in a.draws:
    ids = [m.group(1) for m in (LINE.match(l) for l in open(f, encoding="utf-8")) if m]
    got = Counter(spec[i] for i in ids)
    print("%s: %d drawn; %s" % (f, len(ids), dict(sorted(got.items()))))
    print("  " + ", ".join("%s %s" % (i, spec[i]) for i in ids))
