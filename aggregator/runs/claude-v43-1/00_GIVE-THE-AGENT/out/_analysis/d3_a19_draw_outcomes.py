#!/usr/bin/env python3
"""D3a-46, read-only: the G1b draw of A19's instantiate packet and the class each drawn line was given in
A19-inst-spec.txt. Reads the draw file (d3_draw_A19_487.txt) for the drawn ids, in the lines the draw script prints as
'<id> instantiate ...'. Writes nothing.

  python3 out/_analysis/d3_a19_draw_outcomes.py
"""
import re
from collections import Counter

spec = {}
for l in open("out/_analysis/d3_rulings/A19-inst-spec.txt", encoding="utf-8"):
    if l.strip():
        i, c, _ = l.split("|", 2)
        spec[i] = c
LINE = re.compile(r"^(\S+-\d{3})\s+instantiate\b")
f = "out/_analysis/d3_draw_A19_487.txt"
ids = [m.group(1) for m in (LINE.match(l) for l in open(f, encoding="utf-8")) if m]
got = Counter(spec[i] for i in ids)
print("%s: %d drawn; %s" % (f, len(ids), dict(sorted(got.items()))))
print("  " + ", ".join("%s %s" % (i, spec[i]) for i in ids))
