#!/usr/bin/env python3
"""A03's order test (D3a-30, G35): the census of my rulings, by room, beside C2's count.

Each ruled line gets the class it was ruled under:
  instantiate (A03-inst-spec.txt): O order; BOUND upkeep before the line's report; J a first report that is itself
    damage or repair, counted apart; ONE one end; OTHER another canvas or after hour 73; P-G6 NONPORTABLE (other);
  restrict (A03-restrict-spec.txt): S-O order; S-BOUND bound; S-HELD held by another statement; EL evidence limit;
  add-condition and add-step (A03-adds.jsonl): order where the reason names A03's own order, else held;
  absent (A03-absent-v2.jsonl): a reject is the order, a particular is other, an accept is an evidence limit.
Every class is checked against the decision and kind written to the ledger. A room is counted in each class its lines
show, then once by priority: order, bound, joint, held, one, el, other, limit. An episode is the order or the bound.

  python3 out/_analysis/d3_a03_census.py
"""
import json
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
            out[p[0]] = p[1]
    return out


ruled = {}
for f in ("A03-inst.jsonl", "A03-restrict.jsonl", "A03-adds.jsonl", "A03-absent-v2.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r

EXPECT = {"O": ("accept", "specification"), "BOUND": ("reject", None), "J": ("reject", None),
          "ONE": ("reject", None), "OTHER": ("reject", None), "P-G6": ("particular", None),
          "S-O": ("accept", "specification"), "S-BOUND": ("accept", "specification"),
          "S-HELD": ("accept", "specification"), "EL": ("accept", "none")}
CLASS = {"O": "order", "BOUND": "bound", "J": "joint", "ONE": "one", "OTHER": "other", "P-G6": "other",
         "S-O": "order", "S-BOUND": "bound", "S-HELD": "held", "EL": "el"}

line_class = {}
for name in ("A03-inst-spec.txt", "A03-restrict-spec.txt"):
    for i, c in spec(name).items():
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d, (i, c, ruled[i]["decision"])
        if k:
            assert ruled[i].get("kind") == k, (i, c, ruled[i].get("kind"))
        line_class[i] = CLASS[c]
for r in load("A03-adds.jsonl"):
    assert r["decision"] == "accept" and r["kind"] == "specification", r["adaptation"]
    line_class[r["adaptation"]] = "order" if "A03's own order" in r["reason"] else "held"
for r in load("A03-absent-v2.jsonl"):
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
by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A03 line:", len(by_room))
for c in ("order", "bound", "joint", "held", "one", "el", "other", "limit"):
    print("  rooms showing %-6s %d" % (c, sum(1 for s in by_room.values() if c in s)))
PRI = ("order", "bound", "joint", "held", "one", "el", "other", "limit")
first = Counter(next(c for c in PRI if c in s) for s in by_room.values())
print("rooms once, by priority:", {c: first[c] for c in PRI})
order = {r for r, s in by_room.items() if "order" in s}
bound = {r for r, s in by_room.items() if "bound" in s}
episode = order | bound
print("rooms in both the order and the bound:", len(order & bound))
print("rooms with an episode (order or bound):", len(episode))
print("  order: %d, share %.3f" % (len(order), len(order) / len(episode)))
print("  bound only: %d" % len(bound - order))
print("  joint only (no order or bound line): %d" % sum(1 for s in by_room.values() if "joint" in s and not s & {"order", "bound"}))
print("C2's count: both 190, holds 148, share 0.779 (null mean 0.340, p95 0.389)")
