#!/usr/bin/env python3
"""D3a-42: count the classes in one or more spec files ('id|class|evidence'), and list the ids of the classes named
with --list. Writes nothing.

  python3 out/_analysis/d3_spec_classes.py --spec out/_analysis/d3_rulings/A15-inst-spec.txt [--list J BOUND]
"""
import argparse
import collections

ap = argparse.ArgumentParser()
ap.add_argument("--spec", nargs="+", required=True)
ap.add_argument("--list", nargs="*", default=[])
a = ap.parse_args()
n = collections.Counter()
ids = collections.defaultdict(list)
for f in a.spec:
    for l in open(f, encoding="utf-8"):
        if l.strip():
            i, c = l.split("|")[:2]
            n[c] += 1
            ids[c].append(i)
print("rows %d: %s" % (sum(n.values()), ", ".join("%s %d" % kv for kv in sorted(n.items()))))
for c in a.list:
    print("%s: %s" % (c, " ".join(ids[c])))
