#!/usr/bin/env python3
"""B2: the gate defects (out/_analysis/b2_gates_r1_before.txt, from `mem.py gates`) whose pair touches a set of themes.

Usage: python3 out/_analysis/b2_defects_touching.py T3-005,T3-021,... [--file F]
Prints the one-way discriminators and the must_not_show defects with at least one side in the set.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ids = set(sys.argv[1].split(","))
f = sys.argv[sys.argv.index("--file") + 1] if "--file" in sys.argv else os.path.join(ROOT, "out", "_analysis", "b2_gates_r1_before.txt")
one = re.compile(r"^\s+(T3-\d+) has one against (T3-\d+); (T3-\d+) none against")
mns = re.compile(r"^\s+(T3-\d+) -> (T3-\d+)$")
a, b = [], []
for line in open(f, encoding="utf-8"):
    m = one.match(line)
    if m and (m.group(1) in ids or m.group(2) in ids):
        a.append((m.group(1), m.group(2)))
    m = mns.match(line)
    if m and (m.group(1) in ids or m.group(2) in ids):
        b.append((m.group(1), m.group(2)))
print("one-way, touching the set: %d" % len(a))
for x, y in a:
    print("  %s has, %s lacks" % (x, y))
print("must_not_show with no discriminator, touching the set: %d" % len(b))
for x, y in b:
    print("  %s -> %s" % (x, y))
