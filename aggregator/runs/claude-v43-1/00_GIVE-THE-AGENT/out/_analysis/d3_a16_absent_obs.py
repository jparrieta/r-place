#!/usr/bin/env python3
"""D3a-43: list A16's absent lines that need a named ruling (observed-absent or not-needed, and NONPORTABLE), read from
the four absent packets, with each line's observation. Writes nothing.

  python3 out/_analysis/d3_a16_absent_obs.py
"""
import re

P = ["out/_analysis/d3_pk_A16_absent_%03d.txt" % o for o in (0, 100, 200, 300)]
n, need = 0, []
for p in P:
    for blk in open(p, encoding="utf-8").read().split("\n== ")[1:]:
        n += 1
        head = blk.split("\n", 1)[0]
        aid = head.split()[0]
        obs = re.search(r"observation: (\S+)", blk)
        o = obs.group(1) if obs else "?"
        np = "NONPORTABLE" in head
        if o in ("observed-absent", "not-needed") or np:
            need.append((aid, o, "NONPORTABLE" if np else ""))
print("absent lines read:", n)
for x in need:
    print(" ".join(x).strip())
