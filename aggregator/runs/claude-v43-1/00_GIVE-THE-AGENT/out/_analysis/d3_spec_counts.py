#!/usr/bin/env python3
"""D3a-47, read-only: count the rows of a spec file ('id|CLASS|evidence') by class and the rows of a tag file
('id|TAG,TAG') by tag, and list the order rows (O-A, O-H, S-O-A, S-O-H) that carry no tag row, so that every count
logged comes from a script. Writes nothing.

  python3 out/_analysis/d3_spec_counts.py --spec out/_analysis/d3_rulings/A20-restrict-spec-2.txt \
      --tags out/_analysis/d3_rulings/A20-tags-r2.txt
"""
import argparse
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("--tags", default="")
a = ap.parse_args()
spec = [l.rstrip("\n").split("|", 2) for l in open(a.spec, encoding="utf-8") if l.strip()]
c = Counter(r[1] for r in spec)
print("%s: %d rows; %s" % (a.spec, len(spec), dict(sorted(c.items()))))
if a.tags:
    tags = [l.strip().split("|") for l in open(a.tags, encoding="utf-8") if l.strip()]
    t = Counter(x for r in tags for x in r[1].split(","))
    print("%s: %d rows; %s" % (a.tags, len(tags), dict(sorted(t.items()))))
    tagged = {r[0] for r in tags}
    order = [r[0] for r in spec if r[1] in ("O-A", "O-H", "S-O-A", "S-O-H", "REJ")]
    print("order rows: %d; without a tag row: %s" % (len(order), [i for i in order if i not in tagged] or "none"))
    extra = [i for i in tagged if i not in {r[0] for r in spec}]
    print("tag rows for ids not in the spec: %s" % (extra or "none"))
