#!/usr/bin/env python3
"""A09's order test (D3a-36, G41): the census of my rulings, by room, beside C2's count.

Each ruled line gets the class it was ruled under (the rules were logged before this script ran):
  instantiate (A09-inst-spec.txt, with A09-rerule.jsonl's two re-rulings replacing the first classes): O order;
    M order named in words; J joint; ONE one end; BOUND bound; P-G6 other;
  restrict (A09-restrict-spec.txt): S-O order; S-M order named in words; S-BOUND bound; S-CF carry first; S-HELD
    held; EL evidence limit;
  add-condition (A09-adds.jsonl): carry first or the bound where the reason names it; else held;
  absent (A09-absent.jsonl): a reject is the order; a particular is other; an accept with kind none is a limit.
Every class is checked against the decision and kind written in the rulings files. A room is counted in each class
its lines show, then once by priority: order, bound, carry first, joint, held, one, el, other, limit. An episode is
the order or the bound.

  python3 out/_analysis/d3_a09_census.py
"""
import json
import re
from collections import Counter

R = "out/_analysis/d3_rulings/"


def load(name):
    return [json.loads(l) for l in open(R + name) if l.strip()]


def room(aid):
    return aid.rsplit("-", 1)[0]


def spec(name):
    out = {}
    for l in open(R + name):
        if l.strip():
            p = l.rstrip("\n").split("|")
            out[p[0]] = (p[1], p[2])
    return out


ruled = {}
for f in ("A09-inst.jsonl", "A09-restrict.jsonl", "A09-adds.jsonl", "A09-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
print("lines ruled in A09's files:", len(ruled))
# the re-rulings replace the first rulings; their classes, as A09-rerule.jsonl's reasons state them
RERULE = {"pitt-039": "O", "DestinyTheGame-052": "J"}
rr = load("A09-rerule.jsonl")
assert sorted(r["adaptation"] for r in rr) == sorted(RERULE), [r["adaptation"] for r in rr]
for r in rr:
    ruled[r["adaptation"]] = r

EXPECT = {"O": ("accept", None), "M": ("accept", None), "J": ("reject", None), "ONE": ("reject", None),
          "BOUND": ("reject", None), "P-G6": ("particular", None),
          "S-O": ("accept", "specification"), "S-M": ("accept", "specification"),
          "S-BOUND": ("accept", "specification"), "S-CF": ("accept", "specification"),
          "S-HELD": ("accept", "specification"), "EL": ("accept", "none")}
CLASS = {"O": "order", "M": "order", "J": "joint", "ONE": "one", "BOUND": "bound", "P-G6": "other",
         "S-O": "order", "S-M": "order", "S-BOUND": "bound", "S-CF": "carryfirst", "S-HELD": "held", "EL": "el"}

line_class, words, early_cf = {}, set(), {}
for name in ("A09-inst-spec.txt", "A09-restrict-spec.txt"):
    for i, (c, ev) in spec(name).items():
        c = RERULE.get(i, c)
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d, (i, c, ruled[i]["decision"])
        if k:
            assert ruled[i].get("kind") == k, (i, c, ruled[i].get("kind"))
        line_class[i] = CLASS[c]
        if c in ("M", "S-M"):
            words.add(i)
        if c == "S-CF":
            early_cf[i] = float(re.search(r"h\+(\d+\.\d+)", ev).group(1))
for r in load("A09-adds.jsonl"):
    i, k = r["adaptation"], r.get("kind")
    assert r["decision"] == "accept" and k == "specification", i
    line_class[i] = ("carryfirst" if "counted in the census as carry first" in r["reason"] else
                     "bound" if "counted in the census as the bound" in r["reason"] else "held")
    if line_class[i] == "carryfirst":
        early_cf[i] = float(re.search(r"h\+(\d+\.\d+)", r["reason"]).group(1))
for r in load("A09-absent.jsonl"):
    i = r["adaptation"]
    if r["decision"] == "reject":
        line_class[i] = "order"
    elif r["decision"] == "particular":
        line_class[i] = "other"
    else:
        assert r["decision"] == "accept" and r["kind"] == "none", i
        line_class[i] = "limit"
assert set(line_class) == set(ruled), set(ruled) ^ set(line_class)

print("lines by class:", dict(Counter(line_class.values())))
print("lines showing the mechanism in words:", len(words))
by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A09 line:", len(by_room))
PRI = ("order", "bound", "carryfirst", "joint", "held", "one", "el", "other", "limit")
for c in PRI:
    print("  rooms showing %-11s %d" % (c, sum(1 for s in by_room.values() if c in s)))
first = Counter(next(c for c in PRI if c in s) for s in by_room.values())
print("rooms once, by priority:", {c: first[c] for c in PRI})
order = {r for r, s in by_room.items() if "order" in s}
bound = {r for r, s in by_room.items() if "bound" in s}
cf = {r for r, s in by_room.items() if "carryfirst" in s}
episode = order | bound
print("rooms in both the order and the bound: %d: %s" % (len(order & bound), " ".join(sorted(order & bound))))
print("rooms in both the order and carry first: %d: %s" % (len(order & cf), " ".join(sorted(order & cf))))
print("rooms with an episode (order or bound):", len(episode))
print("  order: %d, share %.3f" % (len(order), len(order) / len(episode)))
print("  bound only: %d, share %.3f: %s" % (len(bound - order), len(bound - order) / len(episode),
                                            " ".join(sorted(bound - order))))
cf_only = cf - episode
print("rooms with carry first and no order or bound: %d: %s" % (len(cf_only), " ".join(sorted(cf_only))))
print("  with them in the denominator, the order holds in %d of %d (%.3f)" % (
    len(order), len(episode | cf_only), len(order) / len(episode | cf_only)))
named = {room(i) for i in words}
print("rooms where the mechanism is named in words: %d (%.3f of the order rooms)" % (len(named), len(named) / len(order)))
joint = {r for r, s in by_room.items() if "joint" in s and not s & {"order", "bound", "carryfirst"}}
print("rooms with one act holding both ends and no order, bound or carry first: %d: %s" % (
    len(joint), " ".join(sorted(joint))))
wide = episode | cf_only | joint
print("  with those rooms too in the denominator, the order holds in %d of %d (%.3f)" % (
    len(order), len(wide), len(order) / len(wide)))
e61 = sorted(i for i, h in early_cf.items() if h < 61)
print("carry-first lines whose act comes before hour 61 (D3a-20's forms): %d: %s" % (len(e61), " ".join(e61)))
print("C2's count: both 145, holds 113, share 0.779 (null mean 0.563, p95 0.628)")
