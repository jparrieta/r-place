#!/usr/bin/env python3
"""Check that a spec file ('id|CLASS|evidence') covers the ids of one or more packet files exactly once each,
and count its classes. Writes nothing.

  python3 out/_analysis/d3_spec_cover.py --spec out/_analysis/d3_rulings/A04-inst-spec.txt \
      out/_analysis/d3_pk_A04_inst_000.txt out/_analysis/d3_pk_A04_inst_100.txt
"""
import argparse
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("packets", nargs="+")
a = ap.parse_args()

pk = []
for f in a.packets:
    pk += [l.split()[1] for l in open(f) if l.startswith("== ")]
rows = [l.rstrip("\n") for l in open(a.spec) if l.strip()]
bad = [r[:50] for r in rows if r.count("|") != 2]
sp = [r.split("|")[0] for r in rows]
print("packet ids %d (distinct %d); spec rows %d (distinct %d)" % (len(pk), len(set(pk)), len(sp), len(set(sp))))
print("in one and not the other:", sorted(set(pk) ^ set(sp)))
print("rows without exactly two bars:", bad)
print("classes:", dict(Counter(r.split("|")[1] for r in rows if r.count("|") == 2)))
