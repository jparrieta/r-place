#!/usr/bin/env python3
"""D3a-45: list A18's absent lines that need a named ruling (observed-absent or not-needed, and NONPORTABLE), read from
the five absent packets, with each line's observation, and count the lines by observation. Writes nothing.

  python3 out/_analysis/d3_a18_absent_obs.py
"""
import re
from collections import Counter

P = ["out/_analysis/d3_pk_A18_absent_%03d.txt" % o for o in (0, 100, 200, 300, 400)]
n, need, by = 0, [], Counter()
for p in P:
    for blk in open(p, encoding="utf-8").read().split("\n== ")[1:]:
        n += 1
        head = blk.split("\n", 1)[0]
        aid = head.split()[0]
        obs = re.search(r"observation: (\S+)", blk)
        o = obs.group(1) if obs else "?"
        by[o] += 1
        np = "NONPORTABLE" in head
        if o in ("observed-absent", "not-needed") or np:
            need.append((aid, o, "NONPORTABLE" if np else ""))
print("absent lines read:", n, "; by observation:", dict(sorted(by.items())))
for x in need:
    print(" ".join(x).strip())
