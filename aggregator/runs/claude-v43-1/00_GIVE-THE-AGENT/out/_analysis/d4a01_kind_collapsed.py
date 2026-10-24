#!/usr/bin/env python3
"""D4a-01, J after the D3c interview: "do not rely on the kind of add-condition, add-step and restrict lines (kappa
0.08); run the distance once with kind collapsed for those ops as a sensitivity check." The distance is
tools/distance.py's, on the same shared lines (adaptation_ledger.shared_lines) and prior.md's weights and grades,
with one change: every add-condition, add-step and restrict line takes one kind, 'collapsed', in place of its
adjudicated kind. In the grade this makes two different ops among the three agree at the same-kind grade (0.5), and
any of them against an op of another kind at 0; in the per-kind split the three ops leave the specification,
elaboration and correction views. Nothing in _views/ is touched. Writes, under --dir: distance-collapsed.tsv,
tree-likeness-collapsed.json; and prints the comparison with _views/distance.tsv: the Pearson and Spearman
correlations over room pairs, the mean absolute difference, the delta score under the same seed, and the adjusted
Rand index between the two average-linkage trees cut at 2, 3, 5, 8 and 12 clusters. Also the per-kind line counts
before and after. Never overwrites.

    python3 out/_analysis/d4a01_kind_collapsed.py --dir out/_analysis/d4a01_kind_collapsed
"""
import argparse, collections, itertools, json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import distance  # noqa: E402
from adaptation_ledger import shared_lines  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--dir", required=True)
ap.add_argument("--quartets", type=int, default=20000)
ap.add_argument("--seed", type=int, default=0)
a = ap.parse_args()
if os.path.exists(a.dir):
    raise SystemExit("refusing to overwrite %s" % a.dir)
COLLAPSE = {"add-condition", "add-step", "restrict"}
w, g = distance.read_prior(os.path.join(OUT, "prior.md"))
keep = shared_lines(OUT)
before = collections.Counter((l["op"], l["kind"]) for l in keep if l["op"] in COLLAPSE)
for l in keep:
    if l["op"] in COLLAPSE:
        l["kind"] = "collapsed"
hdr = open(os.path.join(OUT, "_views", "distance.tsv"), encoding="utf-8").readline().rstrip("\n").split("\t")[1:]
rooms = hdr
by_room = collections.defaultdict(list)
for l in keep:
    by_room[l["sub"]].append(l)
n = len(rooms)
D = [[0.0] * n for _ in range(n)]
for i, j in itertools.combinations(range(n), 2):
    li, lj = by_room[rooms[i]], by_room[rooms[j]]
    if not li and not lj:
        d = 0.0
    elif not li or not lj:
        d = 0.5
    else:
        S = distance.similarity(li, lj, w, g)
        d = (1.0 - max(-1.0, min(1.0, S))) / 2.0
    D[i][j] = D[j][i] = d
os.makedirs(a.dir)
distance.write_tsv(os.path.join(a.dir, "distance-collapsed.tsv"),
                   [[rooms[i]] + ["%.17g" % D[i][j] for j in range(n)] for i in range(n)], ["room"] + rooms)
D0 = []
with open(os.path.join(OUT, "_views", "distance.tsv"), encoding="utf-8") as f:
    f.readline()
    for line in f:
        D0.append([float(x) for x in line.rstrip("\n").split("\t")[1:]])
x = [D0[i][j] for i, j in itertools.combinations(range(n), 2)]
y = [D[i][j] for i, j in itertools.combinations(range(n), 2)]


def pearson(u, v):
    mu, mv = sum(u) / len(u), sum(v) / len(v)
    su = math.sqrt(sum((p - mu) ** 2 for p in u))
    sv = math.sqrt(sum((q - mv) ** 2 for q in v))
    return sum((p - mu) * (q - mv) for p, q in zip(u, v)) / (su * sv)


def ranks(u):
    order = sorted(range(len(u)), key=lambda k: u[k])
    r = [0.0] * len(u)
    k = 0
    while k < len(order):
        m = k
        while m + 1 < len(order) and u[order[m + 1]] == u[order[k]]:
            m += 1
        for t in range(k, m + 1):
            r[order[t]] = (k + m) / 2.0
        k = m + 1
    return r


def ari(p, q):
    labs = list(zip(p, q))
    nij = collections.Counter(labs)
    ai = collections.Counter(p)
    bj = collections.Counter(q)
    c2 = lambda z: z * (z - 1) / 2.0
    sij = sum(c2(v) for v in nij.values())
    sa, sb = sum(c2(v) for v in ai.values()), sum(c2(v) for v in bj.values())
    exp = sa * sb / c2(len(p))
    mx = (sa + sb) / 2.0
    return (sij - exp) / (mx - exp) if mx != exp else 1.0


def labels(merges, k):
    groups = distance.cut(rooms, merges, k)
    lab = {}
    for gi, gr in enumerate(groups):
        for r in gr:
            lab[r] = gi
    return [lab[r] for r in rooms]


m0 = distance.upgma(rooms, D0)
m1 = distance.upgma(rooms, D)
res = {"collapsed_ops": sorted(COLLAPSE), "weights": w, "grades": g, "rooms": n, "lines_used": len(keep),
       "lines_by_op_and_adjudicated_kind_before": {"%s/%s" % k: v for k, v in sorted(before.items())},
       "delta_score_collapsed": distance.delta_score(rooms, D, a.quartets, a.seed),
       "delta_score_carried": json.load(open(os.path.join(OUT, "_views", "tree-likeness.json")))["delta_score"],
       "pearson": pearson(x, y), "spearman": pearson(ranks(x), ranks(y)),
       "mean_abs_diff": sum(abs(p - q) for p, q in zip(x, y)) / len(x),
       "pairs_changed": sum(1 for p, q in zip(x, y) if abs(p - q) > 1e-12), "pairs": len(x),
       "ari_upgma": {str(k): ari(labels(m0, k), labels(m1, k)) for k in (2, 3, 5, 8, 12)}}
json.dump(res, open(os.path.join(a.dir, "tree-likeness-collapsed.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
