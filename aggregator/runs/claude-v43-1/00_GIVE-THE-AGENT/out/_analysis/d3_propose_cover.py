#!/usr/bin/env python3
"""D3a-55: check the propose spec files against the propose packets: for each packet given, the ids it holds that no
spec file rules (held for a later node or missed), and spec ids that no packet given holds (typed wrong or from
another packet); then the classes counted over all spec files given, and any id ruled twice. Writes nothing.

  python3 out/_analysis/d3_propose_cover.py --packets out/_analysis/d3_pk_propose_0000.txt \
      --specs out/_analysis/d3_rulings/propose-spec-0000.txt
"""
import argparse
import re
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("--packets", nargs="+", required=True)
ap.add_argument("--specs", nargs="+", required=True)
a = ap.parse_args()
pk = {}
for f in a.packets:
    for m in re.finditer(r"^== (\S+)  propose", open(f, encoding="utf-8").read(), re.M):
        pk[m.group(1)] = f
rows = []
for f in a.specs:
    for l in open(f, encoding="utf-8"):
        if l.strip():
            p = l.rstrip("\n").split("|")
            rows.append((p[0], p[1], f))
ids = Counter(r[0] for r in rows)
print("packet ids: %d; spec rows: %d" % (len(pk), len(rows)))
print("ruled twice: %s" % (sorted(i for i, n in ids.items() if n > 1) or "none"))
print("in a packet, not ruled: %s" % (sorted(i for i in pk if i not in ids) or "none"))
print("ruled, in no packet given: %s" % (sorted(i for i in ids if i not in pk) or "none"))
print("classes: %s" % dict(sorted(Counter(r[1] for r in rows).items())))
bad = [r for r in rows if not re.match(r"^(C-[A-Z]+|H-[A-Z]\d\d|OUT|PART|P-G6|NOT|PEND)$", r[1])]
print("rows with an unknown class: %s" % ([(r[0], r[1]) for r in bad] or "none"))
