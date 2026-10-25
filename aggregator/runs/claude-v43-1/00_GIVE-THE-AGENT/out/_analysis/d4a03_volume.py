#!/usr/bin/env python3
"""D4a-03, stage D4 section 5 (tier and size checks): branch and cluster memberships against the rooms' volume. The
volume fields are the comparison's own per-room counts (chunk-share-D4.result.json, case_information): concepts
(unique concept ids) and placed fourth-tier themes. For each branch (branches.jsonl) and cluster
(chunk-share-D4.jsonl): the median concepts and the percentile of that median against a permutation null (random
groups of the same size from the 705 rooms, --perms draws, --seed); for the clusters, the share of variance in log
concepts the labels explain (eta squared) with its permutation percentile; and two cross-tables by concept-count
quartile: clusters by quartile, and rooms in a branch or in none by quartile. Read-only; prints only.

    python3 out/_analysis/d4a03_volume.py [--perms 2000 --seed 0]
"""
import argparse, collections, json, math, os, random, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--perms", type=int, default=2000)
ap.add_argument("--seed", type=int, default=0)
a = ap.parse_args()
r = json.load(open(os.path.join(OUT, "chunk-share-D4.result.json"), encoding="utf-8"))
conc = {c["sub"]: c["concepts"] for c in r["case_information"]}
themes = {c["sub"]: c["placed_themes"] for c in r["case_information"]}
rooms = sorted(conc)
rng = random.Random(a.seed)
vals = [conc[s] for s in rooms]
q = statistics.quantiles(vals, n=4)


def quart(v):
    return 1 if v <= q[0] else 2 if v <= q[1] else 3 if v <= q[2] else 4


def pct(members):
    med = statistics.median(conc[s] for s in members)
    n = len(members)
    null = [statistics.median(rng.sample(vals, n)) for _ in range(a.perms)]
    return med, 100.0 * sum(1 for x in null if x < med) / len(null) + 50.0 * sum(1 for x in null if x == med) / len(null)


print("rooms %d; concepts per room: median %d, quartile cuts %s; placed themes median %d" % (
    len(rooms), statistics.median(vals), [round(x) for x in q], statistics.median(themes.values())))
B = [json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8") if l.strip()]
C = [json.loads(l) for l in open(os.path.join(OUT, "chunk-share-D4.jsonl"), encoding="utf-8") if l.strip()]
print("\n== branches: median concepts and its percentile against random groups of the same size")
hi = lo = 0
for b in B:
    med, p = pct(b["members"])
    hi += p >= 95
    lo += p <= 5
    print("%s (%d): median %d, percentile %.1f" % (b["id"], len(b["members"]), med, p))
print("branches at the 95th percentile or above: %d of %d; at the 5th or below: %d" % (hi, len(B), lo))
print("\n== clusters")
for c in C:
    med, p = pct(c["members"])
    print("%s (%d): median %d, percentile %.1f" % (c["code"], len(c["members"]), med, p))
lab = {s: c["code"] for c in C for s in c["members"]}
y = [math.log(conc[s]) for s in rooms]
L = [lab[s] for s in rooms]


def eta2(labels):
    mu = statistics.mean(y)
    tot = sum((v - mu) ** 2 for v in y)
    g = collections.defaultdict(list)
    for v, l in zip(y, labels):
        g[l].append(v)
    return sum(len(v) * (statistics.mean(v) - mu) ** 2 for v in g.values()) / tot


e = eta2(L)
null = []
for _ in range(a.perms):
    LL = L[:]
    rng.shuffle(LL)
    null.append(eta2(LL))
print("eta squared of log concepts by cluster: %.3f; permutation percentile %.1f (null max %.3f)" % (
    e, 100.0 * sum(1 for x in null if x < e) / len(null), max(null)))
print("\n== cross-table: clusters by concept-count quartile (1 smallest)")
ct = collections.Counter((lab[s], quart(conc[s])) for s in rooms)
for c in C:
    print("%s: %s" % (c["code"], "  ".join("Q%d %d" % (k, ct[(c['code'], k)]) for k in (1, 2, 3, 4))))
inb = set(m for b in B for m in b["members"])
ct2 = collections.Counter(("in a branch" if s in inb else "in no branch", quart(conc[s])) for s in rooms)
print("\n== cross-table: branch membership by concept-count quartile")
for g in ("in a branch", "in no branch"):
    print("%s: %s" % (g, "  ".join("Q%d %d" % (k, ct2[(g, k)]) for k in (1, 2, 3, 4))))
