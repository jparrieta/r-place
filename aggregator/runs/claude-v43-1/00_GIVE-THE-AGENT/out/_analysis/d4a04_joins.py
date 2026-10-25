#!/usr/bin/env python3
"""D4a-04: can the 25 top-level branches be joined into parents the stage allows? Read-only; prints only.
(1) The handler's facts, checked: the elements and dimensions of the 25 (dimension from the key's node lifted to its
dimension, and the element's own dimension field), and the Jaccard distances between their member sets (median,
minimum, the closest pairs), with average linkage on that distance: the first merge height and the groups at 0.95.
(2) Every pair or set of top-level branches that could nest under one parent under stage_D4.py's inheritance rule
(same op, same target, the parent's node the children's common lift): for each element-and-op with two or more
top-level branches, the deepest common node (fourth order, dimension or bare target), the parent key, its rooms in
that level's matrix, and how many of them are in none of the children.
(3) For the families named at D4a-02 that span elements or ops: whether any key is common to their branches.

    python3 out/_analysis/d4a04_joins.py
"""
import collections, itertools, json, os, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
V = os.path.join(OUT, "_views")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


B = [b for b in jl(os.path.join(OUT, "branches.jsonl")) if not b["parent"]]
els = {e["id"]: e for e in jl(os.path.join(OUT, "model", "elements.jsonl"))}
t3_t4 = {m: r["id"] for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl")) for m in r.get("members") or []}
t4_d = {m: r["id"] for r in jl(os.path.join(OUT, "dimensions.jsonl")) for m in r.get("members") or []}


def lift(node):
    """(T4, D) for a node at level 3 or 4."""
    if node.startswith("T3-"):
        t4 = t3_t4.get(node)
        return t4, t4_d.get(t4)
    return node, t4_d.get(node)


print("== (1) the 25 top-level branches: %d" % len(B))
dim_by_key = collections.Counter()
for b in B:
    op, el, node = b["keys"][0].split(":")
    t4, d = lift(node)
    dim_by_key[d] += 1
    print("%s %s | element %s (element's dimension field %s) | node %s -> %s -> %s | %d members" % (
        b["id"], b["keys"][0], el, els[el].get("dimension"), node, t4, d, len(b["members"])))
print("elements: %d; by the key's lifted dimension: %s" % (len({b['keys'][0].split(':')[1] for b in B}),
                                                          dict(sorted(dim_by_key.items()))))
ids = [b["id"] for b in B]
M = {b["id"]: set(b["members"]) for b in B}
D = {}
for x, y in itertools.combinations(ids, 2):
    D[(x, y)] = D[(y, x)] = 1 - len(M[x] & M[y]) / len(M[x] | M[y])
vals = sorted(D[(x, y)] for x, y in itertools.combinations(ids, 2))
print("Jaccard distance over %d pairs: median %.3f, minimum %.3f; the five closest pairs: %s" % (
    len(vals), statistics.median(vals), vals[0], "; ".join("%s-%s %.3f" % (x, y, D[(x, y)]) for x, y in sorted(
        itertools.combinations(ids, 2), key=lambda p: D[p])[:5])))
clusters = {i: {i} for i in ids}
merges = []
while len(clusters) > 1:
    keys = list(clusters)
    best = None
    for a_, b_ in itertools.combinations(keys, 2):
        d = statistics.mean(D[(x, y)] for x in clusters[a_] for y in clusters[b_])
        if best is None or d < best[0]:
            best = (d, a_, b_)
    d, a_, b_ = best
    merges.append((d, sorted(clusters[a_]), sorted(clusters[b_])))
    clusters[a_] = clusters[a_] | clusters.pop(b_)
    if d > 0.95 and not any(m[0] > 0.95 for m in merges[:-1]):
        pass
print("average linkage: first merge at %.3f (%s with %s)" % (merges[0][0], merges[0][1], merges[0][2]))
groups = {i: {i} for i in ids}
for d, a_, b_ in merges:
    if d > 0.95:
        break
    ga = next(k for k, v in groups.items() if a_[0] in v)
    gb = next(k for k, v in groups.items() if b_[0] in v)
    groups[ga] |= groups.pop(gb)
mixed = []
for g in groups.values():
    elems = sorted({next(b for b in B if b["id"] == i)["keys"][0].split(":")[1] for i in g})
    mixed.append((sorted(g), elems))
print("groups at 0.95: %d; %s" % (len(mixed), "; ".join("%s (%s)" % ("+".join(g), ",".join(e)) for g, e in mixed if len(g) > 1)))
print("\n== (2) branches that could nest under one parent (same element and op)")


def matrix(level):
    with open(os.path.join(V, "rooms-x-adaptations.%s.all.tsv" % level), encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")[1:]
        held = collections.defaultdict(set)
        for line in f:
            p = line.rstrip("\n").split("\t")
            for k, v in zip(head, p[1:]):
                if v == "1":
                    held[k].add(p[0])
    return held


H4, HD, HT = matrix("4"), matrix("dim"), matrix("target")
byeo = collections.defaultdict(list)
for b in B:
    op, el, node = b["keys"][0].split(":")
    byeo[(el, op)].append(b)
for (el, op), bs in sorted(byeo.items()):
    if len(bs) < 2:
        continue
    lifts = [lift(b["keys"][0].split(":")[2]) for b in bs]
    t4s = {t for t, d in lifts}
    ds = {d for t, d in lifts}
    if len(t4s) == 1:
        level, key, held = "fourth", "%s:%s:%s" % (op, el, t4s.pop()), H4
    elif len(ds) == 1:
        level, key, held = "dimension", "%s:%s:%s" % (op, el, ds.pop()), HD
    else:
        level, key, held = "bare target", "%s:%s:*" % (op, el), HT
    rooms = held.get(key, set())
    inchild = set().union(*[set(b["members"]) for b in bs])
    print("%s %s: %s; their deepest common node is at the %s: %s, held by %d rooms, %d of them in none of the "
          "children" % (el, op, ", ".join("%s (%s)" % (b["id"], b["keys"][0]) for b in bs), level, key, len(rooms),
                        len(rooms - inchild)))
print("\n== (3) families that span ops or elements: common keys")
FAM = {"P05's clause and the marking": ["F07", "F26", "F27", "F32"], "the shared instruction": ["F08", "F15", "F33"],
       "carrying on": ["F11", "F23", "F25"], "the chat": ["F16", "F29", "F30"], "machine hands": ["F08", "F24"],
       "the frame": ["F01", "F21"], "help": ["F22", "F28"]}
for name, fs in FAM.items():
    ks = [set(next(b for b in B if b["id"] == f)["keys"]) for f in fs]
    common = set.intersection(*ks)
    both = set.intersection(*[M[f] for f in fs])
    print("%s (%s): common keys %s; rooms in all of them %d" % (name, ", ".join(fs), sorted(common) or "none", len(both)))
