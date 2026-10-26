#!/usr/bin/env python3
"""D5, room-form accounts: the split below one form, by the rule logged at D5a-36. Walks the form's groups in the
tree (room-forms-tree-rooms.tsv addresses, room-forms-tree-linkage.tsv cuts), on the defining rooms. A split reads as a
split when both parts hold 10 defining rooms or more and each part has a fourth-order change column (node or link)
at 1.5 times the parent's defining share or more, held by a third of the part or more and by fewer in the other part.
The walk descends only into parts whose own split reads. Prints JSON.

    python3 out/_analysis/d5f_split.py --form A > out/_analysis/d5a36_split.json
"""
import argparse, collections, json, os, sys

ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
ap.add_argument("--start", default="", help="begin the walk at this group instead of the form (description beyond the walk, D5a-37)")
a = ap.parse_args()
sys.argv = [sys.argv[0]]
AN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402

OUT = E.OUT


def tsv(p):
    lines = open(os.path.join(OUT, p), encoding="utf-8").read().splitlines()
    cols = lines[0].split("\t")
    return [dict(zip(cols, l.split("\t"))) for l in lines[1:]]


R = [r for r in tsv("room-forms-tree-rooms.tsv") if r["form"] == a.form]
K = {r["label"]: r for r in tsv("room-forms-tree-linkage.tsv") if r["label"]}
addr = {r["room"]: r["address"].split("/")[0] for r in R}
role = {r["room"]: r["role"] for r in R}
names4 = {r["id"]: r.get("name") for r in E.jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
cols = E.CCOLS["T4"]
S = E.shares(E.MCD["T4"])
P = E.MCD["T4"] > 0


def lab(c):
    return " > ".join(names4.get(x) or x for x in c.split(">"))


def under(label, defining=True):
    return [s for s, x in addr.items() if (x == label or x.startswith(label + ".")) and (not defining or role[s] == "defining")]


def leans(part, other, parent):
    ip, io, ipa = [E.IDX[s] for s in part], [E.IDX[s] for s in other], [E.IDX[s] for s in parent]
    sp, pp, po, spa = S[ip].mean(axis=0), P[ip].mean(axis=0), P[io].mean(axis=0), S[ipa].mean(axis=0)
    out = [{"col": c, "name": lab(c), "ratio_to_parent": round(float(sp[j] / spa[j]), 2), "presence": round(float(pp[j]), 3),
            "presence_other": round(float(po[j]), 3)}
           for j, c in enumerate(cols) if spa[j] > 0 and sp[j] / spa[j] >= 1.5 and pp[j] >= 1 / 3 and po[j] < pp[j]]
    return sorted(out, key=lambda r: -r["presence"])


walk, queue = [], [a.start or a.form]
while queue:
    g = queue.pop(0)
    c1, c2 = g + ".1", g + ".2"
    if c1 not in K or c2 not in K:
        continue
    par, p1, p2 = under(g), under(c1), under(c2)
    l1 = leans(p1, p2, par) if len(p1) >= 2 and len(p2) >= 2 else []
    l2 = leans(p2, p1, par) if len(p1) >= 2 and len(p2) >= 2 else []
    reads = len(p1) >= 10 and len(p2) >= 10 and bool(l1) and bool(l2)
    walk.append({"group": g, "splits_at_k": int(K[g]["k_to"]) + 1, "parts": {c1: {"defining": len(p1), "all": len(under(c1, False)), "leans": l1[:5]},
                                                                           c2: {"defining": len(p2), "all": len(under(c2, False)), "leans": l2[:5]}},
                 "reads_as_split": reads})
    if reads:
        queue += [c1, c2]
print(json.dumps({"form": a.form, "walk": walk}, ensure_ascii=False))
