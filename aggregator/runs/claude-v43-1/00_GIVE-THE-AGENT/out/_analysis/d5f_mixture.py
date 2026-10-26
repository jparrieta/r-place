#!/usr/bin/env python3
"""D5, room-form accounts: do a form's signature patterns stand apart inside it (the rule logged at D5a-37)? For each
signature column (room-forms-D4a08c.jsonl), the defining members holding it; pairwise and three-way overlaps against
independence at those presences; the elements anchored at each signature theme; and how each set falls into the parts
of the tree below the form (first split, and the first split of each part). Prints JSON.

    python3 out/_analysis/d5f_mixture.py --form B > out/_analysis/d5a37_mixture.json
"""
import argparse, itertools, json, os, sys

ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
a = ap.parse_args()
sys.argv = [sys.argv[0]]
AN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402
import d4a07_features as F  # noqa: E402

form = E.FORMS[a.form]
DEFS = [s for s in form["members"] if s in E.IDX]
n = len(DEFS)
cols = E.CCOLS["T4"]
held = E.MCD["T4"] > 0
sig = [x["name"] for x in form["change_signature_T4"]]
names4 = {r["id"]: r.get("name") for r in E.jl(os.path.join(E.OUT, "fourth", "fourth.jsonl"))}
byname = {v: k for k, v in names4.items()}
sets = {}
for nm in sig:
    c = byname.get(nm, nm)
    j = cols.index(c)
    sets[nm] = {s for s in DEFS if held[E.IDX[s], j]}
pairs = []
for x, y in itertools.combinations(sig, 2):
    both = len(sets[x] & sets[y])
    exp = len(sets[x]) * len(sets[y]) / n
    pairs.append({"a": x, "b": y, "both": both, "expected_if_independent": round(exp, 1),
                  "jaccard": round(both / len(sets[x] | sets[y]), 3)})
allthree = set.intersection(*sets.values()) if len(sets) == 3 else set()
exp3 = 1.0
for s_ in sets.values():
    exp3 *= len(s_) / n
anchored = {nm: sorted(e for e in F.ELEM if byname.get(nm) in F.t4s(e)) for nm in sig}
none_ = [s for s in DEFS if not any(s in v for v in sets.values())]
tl = open(os.path.join(E.OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8").read().splitlines()
hd = tl[0].split("\t")
addr = {}
for line in tl[1:]:
    c = dict(zip(hd, line.split("\t")))
    addr[c["room"]] = c["address"].split("/")[0]


def part(s, depth):
    p = addr[s].split(".")
    return ".".join(p[:depth + 1]) if len(p) > depth else addr[s]


dist = {}
for depth in (1, 2):
    dist[str(depth)] = {nm: {} for nm in sig}
    for nm in sig:
        for s in sets[nm]:
            k = part(s, depth)
            dist[str(depth)][nm][k] = dist[str(depth)][nm].get(k, 0) + 1
    dist[str(depth)]["all defining"] = {}
    for s in DEFS:
        k = part(s, depth)
        dist[str(depth)]["all defining"][k] = dist[str(depth)]["all defining"].get(k, 0) + 1
print(json.dumps({"form": a.form, "n_def": n, "holders": {k: len(v) for k, v in sets.items()}, "pairs": pairs,
                  "all_three": len(allthree), "all_three_expected": round(exp3 * n, 1), "in_none": len(none_),
                  "only_one": {nm: len(sets[nm] - set().union(*(sets[o] for o in sig if o != nm))) for nm in sig},
                  "anchored_elements": anchored, "by_part": dist}, ensure_ascii=False))
