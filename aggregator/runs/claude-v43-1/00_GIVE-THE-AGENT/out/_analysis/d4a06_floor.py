#!/usr/bin/env python3
"""D4a-06: the distribution of selected changes per room (placed lines), and of the fourth-order themes they
reach, so that the floor on thin rooms is chosen before any clustering. Read-only; prints counts.

    python3 out/_analysis/d4a06_floor.py
"""
import collections, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import adaptation_ledger as al  # noqa: E402

CHANGE = {"add-step", "add-condition", "link", "restrict", "contradict"}
L = [r for r in al.shared_lines(OUT) if r.get("op") in CHANGE and len(r.get("lift") or []) >= 4]
n = collections.Counter(r["sub"] for r in L)
t4 = collections.defaultdict(set)
for r in L:
    if r["lift"][2]:
        t4[r["sub"]].add(r["lift"][2])
dist = collections.Counter(n.values())
print("rooms with changes", len(n))
print("changes per room:", sorted(dist.items()))
for f in (3, 4, 5, 6, 8):
    below = [s for s in n if n[s] < f]
    print("floor %d: below %d rooms (%.1f%%); their fourth-order themes reached, median %s" % (
        f, len(below), 100 * len(below) / len(n), sorted(len(t4[s]) for s in below)[len(below) // 2] if below else None))
print("fourth-order themes reached, by number of changes:",
      {k: sorted(len(t4[s]) for s in n if n[s] == k)[len([s for s in n if n[s] == k]) // 2] for k in sorted(dist) if k <= 8})
