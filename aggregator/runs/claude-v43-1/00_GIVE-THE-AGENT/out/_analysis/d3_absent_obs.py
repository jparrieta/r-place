#!/usr/bin/env python3
"""D3a-47, read-only: a general form of d3_a19_absent_obs.py. Lists an element's absent lines that need a named ruling
(observed-absent or not-needed, and NONPORTABLE), read from its absent packets, with each line's observation, and
counts the lines by observation. Writes nothing.

  python3 out/_analysis/d3_absent_obs.py --packets out/_analysis/d3_pk_A20_absent_000.txt ...
"""
import argparse
import re
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("--packets", nargs="+", required=True)
a = ap.parse_args()
n, need, by = 0, [], Counter()
for p in a.packets:
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
