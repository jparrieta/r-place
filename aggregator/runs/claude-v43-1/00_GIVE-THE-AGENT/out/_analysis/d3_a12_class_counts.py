#!/usr/bin/env python3
"""D3a-39: count the classes in A12's spec files ('id|CLASS|evidence'), the re-rulings beside them, and print the
first rows of a class if asked (--show CLASS --file NAME --n N). Writes nothing.

  python3 out/_analysis/d3_a12_class_counts.py
  python3 out/_analysis/d3_a12_class_counts.py --show T-R --file A12-inst-spec.txt --n 3
"""
import argparse
from collections import Counter

R = "out/_analysis/d3_rulings/"
FILES = ("A12-inst-spec.txt", "A12-restrict-spec.txt", "A12-addc-spec.txt", "A12-adds-spec.txt",
         "A12-absent-rows.txt", "A12-rerule-spec.txt")
ap = argparse.ArgumentParser()
ap.add_argument("--show")
ap.add_argument("--file")
ap.add_argument("--n", type=int, default=3)
a = ap.parse_args()


def rows(name):
    return [l.rstrip("\n").split("|", 2) for l in open(R + name, encoding="utf-8") if l.strip()]


if a.show:
    for p in [p for p in rows(a.file) if p[1] == a.show][:a.n]:
        print("|".join(p))
else:
    for name in FILES:
        c = Counter(p[1] for p in rows(name))
        print(name, sum(c.values()), dict(sorted(c.items())))
