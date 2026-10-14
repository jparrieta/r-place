#!/usr/bin/env python3
"""C2 section 4, read-only: the transition mass between dimensions, for model.md's apparatus, and the third-order themes the
model does not use.

The transitions are the generated view _views/transitions.tsv (coded turn answering coded turn, at the second-order
level); each end is lifted to the dimensions of its placement (third-order theme, then fourth-order theme, then
dimension). A second-order theme placed on two or more third-order themes is a double (rule 0); it lifts to each of
its dimensions. Per dimension: in-mass (transitions into it from another dimension), out-mass (out of it into
another), internal mass (inside it), with the doubles and without them (any transition touching a double dropped).
Counts are of transitions with the rooms beside them (rule 4). Also: the third-order themes no element of
model/elements.jsonl uses, directly or through its fourth-order theme.

    python3 out/_analysis/c2_dim_mass.py
"""
import collections, json, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jl(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


t4 = jl(os.path.join("fourth", "fourth.jsonl"))
owner = dict((m, r["id"]) for r in t4 for m in r["members"])
dims = jl("dimensions.jsonl")
dim_of = dict((m, d["id"]) for d in dims for m in d["members"])
place = {}
for r in jl("assignments_final.jsonl"):
    place[(r["sub"], r["theme_id"])] = r.get("third_order") or []


def ds(sub, tid):
    return sorted(set(dim_of[owner[t]] for t in place.get((sub, tid), []) if t in owner))


mass = dict((k, collections.Counter()) for k in ("in", "out", "int", "in_nd", "out_nd", "int_nd"))
rooms = dict((k, collections.defaultdict(set)) for k in mass)
pairmass = collections.Counter()
n = nd = 0
with open(os.path.join(OUT, "_views", "transitions.tsv"), encoding="utf-8") as f:
    for line in f:
        if line.startswith("#") or line.startswith("room\t"):
            continue
        sub, a, b, _ = line.rstrip("\n").split("\t")
        da, db = ds(sub, a), ds(sub, b)
        if not da or not db:
            continue
        n += 1
        double = len(place.get((sub, a), [])) > 1 or len(place.get((sub, b), [])) > 1
        nd += not double
        for x in da:
            for y in db:
                pairmass[(x, y)] += 1
                if x == y:
                    mass["int"][x] += 1
                    rooms["int"][x].add(sub)
                    if not double:
                        mass["int_nd"][x] += 1
                        rooms["int_nd"][x].add(sub)
                else:
                    mass["out"][x] += 1
                    rooms["out"][x].add(sub)
                    mass["in"][y] += 1
                    rooms["in"][y].add(sub)
                    if not double:
                        mass["out_nd"][x] += 1
                        rooms["out_nd"][x].add(sub)
                        mass["in_nd"][y] += 1
                        rooms["in_nd"][y].add(sub)
print("transitions with both ends placed in a dimension: %d; with no double at either end: %d" % (n, nd))
print("| dimension | in (rooms) | out (rooms) | internal (rooms) | in, no doubles | out, no doubles | internal, no doubles |")
print("|---|---|---|---|---|---|---|")
for d in dims:
    i = d["id"]
    print("| %s %s | %d (%d) | %d (%d) | %d (%d) | %d (%d) | %d (%d) | %d (%d) |" % (
        i, d["label"], mass["in"][i], len(rooms["in"][i]), mass["out"][i], len(rooms["out"][i]), mass["int"][i],
        len(rooms["int"][i]), mass["in_nd"][i], len(rooms["in_nd"][i]), mass["out_nd"][i], len(rooms["out_nd"][i]),
        mass["int_nd"][i], len(rooms["int_nd"][i])))
print("largest cross-dimension masses: " + "; ".join("%s->%s %d" % (x, y, k) for (x, y), k in pairmass.most_common(40) if x != y))
els = jl(os.path.join("model", "elements.jsonl"))
used_t = set()
for e in els:
    for t in (e["tier"] if isinstance(e["tier"], list) else [e["tier"]]):
        used_t.add(t)
scheme = jl("scheme_v2.jsonl")
unused = [t["id"] for t in scheme if t["id"] not in used_t and owner.get(t["id"]) not in used_t]
print("third-order themes the model does not use: %d of %d" % (len(unused), len(scheme)))
by4 = collections.defaultdict(list)
for t in unused:
    by4[owner.get(t, "unpicked")].append(t)
print("; ".join("%s: %d" % (k, len(v)) for k, v in sorted(by4.items())))
