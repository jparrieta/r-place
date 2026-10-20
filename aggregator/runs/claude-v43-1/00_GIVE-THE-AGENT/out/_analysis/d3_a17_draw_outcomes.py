#!/usr/bin/env python3
"""D3a-44, read-only: the G1b draws of A17's instantiate packets and the class each drawn line was given in
A17-inst-spec.txt. Reads the two draw files (d3_draw_A17_432.txt, d3_draw_A17_532.txt) for the drawn ids, in the
lines the draw script prints as '<id> instantiate ...'. Writes nothing.

  python3 out/_analysis/d3_a17_draw_outcomes.py
"""
import re
from collections import Counter

spec = {}
for l in open("out/_analysis/d3_rulings/A17-inst-spec.txt", encoding="utf-8"):
    if l.strip():
        i, c, _ = l.split("|", 2)
        spec[i] = c
LINE = re.compile(r"^(\S+-\d{3})\s+instantiate\b")
total = Counter()
for f in ("out/_analysis/d3_draw_A17_432.txt", "out/_analysis/d3_draw_A17_532.txt"):
    ids = [m.group(1) for m in (LINE.match(l) for l in open(f, encoding="utf-8")) if m]
    got = Counter(spec[i] for i in ids)
    total.update(got)
    print("%s: %d drawn; %s" % (f, len(ids), dict(sorted(got.items()))))
    print("  " + ", ".join("%s %s" % (i, spec[i]) for i in ids))
print("both packets: %d drawn; %s" % (sum(total.values()), dict(sorted(total.items()))))
