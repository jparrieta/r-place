#!/usr/bin/env python3
"""B2b-r1: test F-001's grain bound across rooms and within rooms (the PI's correction, 2026-10-11).

Across rooms: Spearman correlation between a room's mean concepts per placed second-order theme and the
share of its placed themes on one kind (rooms with at least 5 placed themes).
Within rooms: for each room, Spearman correlation between a theme's concepts and its number of kinds;
the mean of those correlations, and the pooled share of single-kind themes by concept band after
subtracting each room's own single share (a within-room comparison).
Reads scheme_current.jsonl (the B1 working grouping) and the store; writes nothing.
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
            j += 1
        for k in range(i, j + 1):
            r[o[k]] = (i + j) / 2.0
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = rank(x), rank(y)
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else float("nan")


themes = jl(os.path.join(ROOT, "package", "store", "themes.jsonl"))
lab2id = {(t["sub"], t["second_order"]): t["theme_id"] for t in themes}
nc = collections.Counter()
for c in jl(os.path.join(ROOT, "package", "store", "codes.jsonl")):
    if c.get("theme_id"):
        nc[(c["sub"], c["theme_id"])] += 1
kinds = collections.defaultdict(set)
for r in jl(os.path.join(ROOT, "out", "scheme", "scheme_current.jsonl")):
    for m in r["members"]:
        kinds[(m["sub"], lab2id.get((m["sub"], m["second_order"]), m["second_order"]))].add(r["theme"])
by_room = collections.defaultdict(list)
for k, v in kinds.items():
    by_room[k[0]].append((nc.get(k, 0), len(v)))
rooms = [r for r, v in by_room.items() if len(v) >= 5]
g = [sum(c for c, _ in by_room[r]) / len(by_room[r]) for r in rooms]
s = [sum(1 for _, k in by_room[r] if k == 1) / len(by_room[r]) for r in rooms]
print("across rooms (%d rooms with 5+ placed themes): Spearman(mean concepts per theme, single share) = %.3f" % (len(rooms), spearman(g, s)))
within = []
for r in rooms:
    xs = [c for c, _ in by_room[r]]
    ys = [k for _, k in by_room[r]]
    if len(set(xs)) > 1 and len(set(ys)) > 1:
        within.append(spearman(xs, ys))
print("within rooms (%d rooms with variation): mean Spearman(theme concepts, kinds) = %.3f; positive in %d" % (
    len(within), sum(within) / len(within), sum(1 for w in within if w > 0)))
bands = collections.defaultdict(list)
for r in rooms:
    base = sum(1 for _, k in by_room[r] if k == 1) / len(by_room[r])
    for c, k in by_room[r]:
        b = "1-5" if c <= 5 else "6-10" if c <= 10 else "11-20" if c <= 20 else "21-40" if c <= 40 else "41+"
        bands[b].append((1 if k == 1 else 0) - base)
print("single share relative to the theme's own room, by concept band:")
for b in ("1-5", "6-10", "11-20", "21-40", "41+"):
    v = bands[b]
    print("  %s: %d themes, %+.3f" % (b, len(v), sum(v) / len(v)))
