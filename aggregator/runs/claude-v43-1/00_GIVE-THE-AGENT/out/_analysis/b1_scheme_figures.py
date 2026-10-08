"""Scheme-wide figures for a close: themes, placed second-order themes, placements, size
distribution, one-room themes, multiple placements. Reads out/scheme/scheme_current.jsonl only.

usage: python3 out/_analysis/b1_scheme_figures.py
"""
import json
from collections import Counter

rows = [json.loads(l) for l in open("out/scheme/scheme_current.jsonl") if l.strip()]
placed = set()
placements = 0
sizes = []
mp = Counter()
for r in rows:
    keys = [m["sub"] + ":" + m["second_order"] for m in r["members"]]
    placed |= set(keys)
    placements += len(keys)
    mp.update(keys)
    sizes.append((len(set(keys)), r["theme"], r["label"], len(set(m["sub"] for m in r["members"]))))
sizes.sort(reverse=True)
print("themes %d, placed second-order themes %d, placements %d" % (len(rows), len(placed), placements))
print("largest:")
for n, t, l, k in sizes[:8]:
    print("  %s %s: %d second-order themes in %d rooms (%.1f%%)" % (t, l, n, k, 100.0 * n / len(placed)))
dist = Counter(n for n, _, _, _ in sizes)
print("size distribution (members: themes):", ", ".join("%d: %d" % (n, dist[n]) for n in sorted(dist) if n <= 8))
print("one room only: %d" % sum(1 for x in sizes if x[3] == 1))
print("multiply placed: %d (twice %d, three times %d, over three %d)" % (
    sum(1 for v in mp.values() if v > 1), sum(1 for v in mp.values() if v == 2),
    sum(1 for v in mp.values() if v == 3), sum(1 for v in mp.values() if v > 3)))
