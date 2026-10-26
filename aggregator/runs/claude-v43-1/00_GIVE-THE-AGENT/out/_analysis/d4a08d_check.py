#!/usr/bin/env python3
"""D4a-08: check the written room-forms tree files against each other and against room-forms-D4a08c.jsonl.
Reads only the files in out/. Prints a short report.

    python3 out/_analysis/d4a08d_check.py
"""
import collections, json, os, sys
import numpy as np
from scipy.cluster.hierarchy import fcluster, is_valid_linkage, is_monotonic

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.setrecursionlimit(20000)


def rows(p):
    lines = open(os.path.join(OUT, p), encoding="utf-8").read().splitlines()
    cols = lines[0].split("\t")
    return [dict(zip(cols, l.split("\t"))) for l in lines[1:]]


R = rows("room-forms-tree-rooms.tsv")
L = rows("room-forms-tree-linkage.tsv")
print("rooms rows", len(R), "unique", len({r["room"] for r in R}), "linkage rows", len(L))
print("roles", dict(collections.Counter(r["role"] for r in R)))
# the six forms against D4a-08c
d8c = {s: f["id"] for f in map(json.loads, open(os.path.join(OUT, "room-forms-D4a08c.jsonl"), encoding="utf-8")) for s in f["members"]}
print("form differs from D4a-08c:", sum(1 for r in R if d8c[r["room"]] != r["form"] or r["k6"] != r["form"]))
# nesting: each label at k + 1 equals or extends the label at k, below six
bad = 0
for r in R:
    for k in range(6, 30):
        x, y = r["k%d" % k], r["k%d" % (k + 1)]
        if not (y == x or y.startswith(x + ".")):
            bad += 1
print("labels not nested below six:", bad)
print("groups per k:", {k: len({r["k%d" % k] for r in R}) for k in (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, 30)})
# the full linkage: valid, monotone, and its cuts by height equal the table's labels
Z = np.array([[float(x["a"]), float(x["b"]), float(x["height"]), float(x["rooms"])] for x in L])
print("valid", bool(is_valid_linkage(Z)), "monotone", bool(is_monotonic(Z)), "root rooms", int(Z[-1, 3]))
ward_h = sorted(float(x["height"]) for x in L if x["kind"] == "ward")
mism = []
for k in range(2, 31):
    t = (ward_h[-k] + ward_h[-(k - 1)]) / 2
    lab = fcluster(Z, t, criterion="distance")
    a = collections.defaultdict(set)
    b = collections.defaultdict(set)
    for r in R:
        a[lab[int(r["leaf_id"])]].add(r["room"])
        b[r["k%d" % k]].add(r["room"])
    if sorted(map(sorted, a.values())) != sorted(map(sorted, b.values())):
        mism.append((k, len(a), len(b)))
print("cuts of the full linkage by height that differ from the table:", mism)
# the Newick: every room once, and every leaf at the root's height from the root
s = open(os.path.join(OUT, "room-forms-tree.nwk"), encoding="utf-8").read().strip()
pos = 0


def parse():
    global pos
    kids = []
    if s[pos] == "(":
        pos += 1
        kids.append(parse())
        while s[pos] == ",":
            pos += 1
            kids.append(parse())
        assert s[pos] == ")"
        pos += 1
    j = pos
    while s[pos] not in ":,);":
        pos += 1
    name = s[j:pos]
    bl = 0.0
    if s[pos] == ":":
        pos += 1
        j = pos
        while s[pos] not in ",);":
            pos += 1
        bl = float(s[j:pos])
    return (name, bl, kids)


tree = parse()
assert s[pos] == ";"
depth = []
names = []


def walk(nd, acc):
    name, bl, kids = nd
    if not kids:
        names.append(name)
        depth.append(acc + bl)
    for c in kids:
        walk(c, acc + bl)


walk(tree, 0.0)
rootH = float(L[-1]["height"])
print("newick leaves", len(names), "unique", len(set(names)), "equal to the rooms", set(names) == {r["room"] for r in R})
print("leaf depth from root: min %.6f max %.6f, root height %.6f" % (min(depth), max(depth), rootH))
print("negative branch lengths:", s.count(":-"))
