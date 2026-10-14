#!/usr/bin/env python3
"""C2c, read-only: the reviewer's partition of the third-order themes against the analyst's fourth-order tier
(fourth/fourth.jsonl), to read how determined the tier is (stage C2 section 6). Counts, for the 197 third-order themes:
pairs grouped together in both partitions, in one only, the Rand and adjusted Rand indices; per reviewer group, the
fourth-order theme it overlaps most, the overlap and the Jaccard; the fourth-order themes the reviewer keeps whole
(every member in one group, nothing added); and the themes that leave their fourth-order theme's majority group.
The analyst's two unpicked themes and the reviewer's unplaced themes each count as singletons.

    python3 out/_analysis/c2c_partition_compare.py
"""
import collections, itertools, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
S = dict((r["id"], r) for r in (json.loads(l) for l in open(os.path.join(OUT, "scheme_v2.jsonl"), encoding="utf-8")))
T4 = [json.loads(l) for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"), encoding="utf-8")]
D = [json.loads(l) for l in open(os.path.join(OUT, "dimensions.jsonl"), encoding="utf-8")]
R = json.loads(open(os.path.join(OUT, "_fleet_raw", "C2", "C2-reviewer", "r1.jsonl"), encoding="utf-8").readline())
mine = {}
names = {}
dim_of = {}
for d in D:
    for t in d["members"]:
        dim_of[t] = d["id"]
for r in T4:
    names[r["id"]] = r["name"]
    for m in r["members"]:
        mine[m] = r["id"]
theirs = {}
for i, g in enumerate(R["partition"]):
    for m in g["members"]:
        theirs[m] = "G%02d" % (i + 1)
all_t3 = sorted(S)
for t in all_t3:
    mine.setdefault(t, "unpicked:" + t)
    theirs.setdefault(t, "unplaced:" + t)
dup = [m for m, n in collections.Counter(m for g in R["partition"] for m in g["members"]).items() if n > 1]
missing = [t for t in all_t3 if theirs[t].startswith("unplaced") and t not in [u["id"] for u in R["unplaced"]]]
print("third-order themes %d; reviewer groups %d; placed twice %s; missing from the return %s" % (
    len(all_t3), len(R["partition"]), dup or "none", missing or "none"))
a = b = c = d_ = 0
for x, y in itertools.combinations(all_t3, 2):
    m, t = mine[x] == mine[y], theirs[x] == theirs[y]
    a += m and t
    b += m and not t
    c += t and not m
    d_ += not m and not t
n = a + b + c + d_
rand = (a + d_) / n
sm, st = a + b, a + c
exp = sm * st / n
ari = (a - exp) / ((sm + st) / 2 - exp)
print("pairs together in both %d; in mine only %d; in the reviewer's only %d; Rand %.3f; adjusted Rand %.3f" % (a, b, c, rand, ari))
mine_groups = collections.defaultdict(set)
for t, g in mine.items():
    mine_groups[g].add(t)
print("\nper reviewer group: the fourth-order theme it overlaps most (overlap of group size; Jaccard), and its dimensions")
whole = []
for i, g in enumerate(R["partition"]):
    gs = set(g["members"])
    best = max((k for k in mine_groups if not k.startswith("unpicked")), key=lambda k: (len(gs & mine_groups[k]), -len(mine_groups[k])))
    j = len(gs & mine_groups[best]) / len(gs | mine_groups[best])
    dims = sorted(set(dim_of.get(mine[m], "none") for m in gs if not mine[m].startswith("unpicked")))
    src = collections.Counter(mine[m] for m in gs)
    print("  G%02d %-32s %2d: %s %s (%d of %d; J %.2f); from %s; dimensions %s" % (
        i + 1, g["label"][:32], len(gs), best, names[best], len(gs & mine_groups[best]), len(gs), j,
        ", ".join("%s x%d" % (k, v) for k, v in src.most_common()), ", ".join(dims)))
    if mine_groups[best] == gs:
        whole.append(best)
print("\nfourth-order themes the reviewer keeps exactly: %d (%s)" % (len(whole), ", ".join("%s %s" % (k, names[k]) for k in whole)))
moved = []
for k, ms in sorted(mine_groups.items()):
    if k.startswith("unpicked"):
        continue
    maj = collections.Counter(theirs[m] for m in ms).most_common(1)[0][0]
    moved += [(m, k, theirs[m]) for m in ms if theirs[m] != maj]
print("third-order themes outside their fourth-order theme's majority group in the reviewer's partition: %d of %d" % (
    len(moved), len(all_t3)))
print("\n".join("  %s %s: %s %s -> %s" % (m, S[m]["name"], k, names[k], theirs[m]) for m, k, _ in moved))
