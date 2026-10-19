#!/usr/bin/env python3
"""A06's order test (D3a-33, G38): the census of my rulings, by room, beside C2's count and F-005.

Each ruled line gets the class it was ruled under:
  instantiate (A06-inst-spec.txt): O order; M order named in words; BOUND bound; J one act holding both ends (joint);
    JM joint, with the mechanism named in later words (joint, counted apart); NP not P14's act; ONE one end; OTHER
    machine hands first shown after hour 73; P-G6 NONPORTABLE (other);
  restrict (A06-restrict-spec.txt): S-O order; S-M order named in words; S-BOUND bound; S-HELD held by another
    statement; EL evidence limit; P-G6 other;
  add-condition (A06-adds.jsonl): bound where the reason names A06's own bound, else held;
  absent (A06-absent.jsonl): a reject is the order (named in words where its reason says so), an accept with kind
    none is a limit.
Every class is checked against the decision and kind written in the rulings file. A room is counted in each class its
lines show, then once by priority: order, bound, joint, held, np, one, el, other, limit. An episode is the order or the
bound.

  python3 out/_analysis/d3_a06_census.py
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
for f in ("A06-inst.jsonl", "A06-restrict.jsonl", "A06-adds.jsonl", "A06-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
print("lines ruled in A06's files:", len(ruled))

EXPECT = {"O": ("accept", None), "M": ("accept", None), "BOUND": ("reject", None), "J": ("reject", None),
          "JM": ("reject", None), "NP": ("reject", None), "ONE": ("reject", None), "OTHER": ("reject", None),
          "P-G6": ("particular", None), "S-O": ("accept", "specification"), "S-M": ("accept", "specification"),
          "S-BOUND": ("accept", "specification"), "S-HELD": ("accept", "specification"), "EL": ("accept", "none")}
CLASS = {"O": "order", "M": "order", "BOUND": "bound", "J": "joint", "JM": "joint", "NP": "np", "ONE": "one",
         "OTHER": "other", "P-G6": "other", "S-O": "order", "S-M": "order", "S-BOUND": "bound", "S-HELD": "held",
         "EL": "el"}

line_class, words, jm = {}, set(), set()
for name in ("A06-inst-spec.txt", "A06-restrict-spec.txt"):
    for i, c in spec(name).items():
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d, (i, c, ruled[i]["decision"])
        if k:
            assert ruled[i].get("kind") == k, (i, c, ruled[i].get("kind"))
        line_class[i] = CLASS[c]
        if c in ("M", "S-M"):
            words.add(i)
        if c == "JM":
            jm.add(i)
for r in load("A06-adds.jsonl"):
    assert r["decision"] == "accept" and r["kind"] == "specification", r["adaptation"]
    line_class[r["adaptation"]] = "bound" if "A06's own bound" in r["reason"] else "held"
for r in load("A06-absent.jsonl"):
    i = r["adaptation"]
    if r["decision"] == "reject":
        line_class[i] = "order"
        if "in the members' words" in r["reason"]:
            words.add(i)
    else:
        assert r["decision"] == "accept" and r["kind"] == "none", i
        line_class[i] = "limit"
assert set(line_class) == set(ruled), set(ruled) ^ set(line_class)

print("lines by class:", dict(Counter(line_class.values())))
print("lines showing the order named in words:", len(words), "; joint lines with the mechanism named later:", len(jm))
by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A06 line:", len(by_room))
PRI = ("order", "bound", "joint", "held", "np", "one", "el", "other", "limit")
for c in PRI:
    print("  rooms showing %-6s %d" % (c, sum(1 for s in by_room.values() if c in s)))
first = Counter(next(c for c in PRI if c in s) for s in by_room.values())
print("rooms once, by priority:", {c: first[c] for c in PRI})
order = {r for r, s in by_room.items() if "order" in s}
bound = {r for r, s in by_room.items() if "bound" in s}
episode = order | bound
print("rooms in both the order and the bound:", len(order & bound))
print("rooms with an episode (order or bound):", len(episode))
print("  order: %d, share %.3f" % (len(order), len(order) / len(episode)))
print("  bound only: %d, share %.3f" % (len(bound - order), len(bound - order) / len(episode)))
named = {room(i) for i in words}
print("rooms where the order is named in words: %d (%.3f of the episode rooms; %.3f of the order rooms)" % (
    len(named), len(named) / len(episode), len(named) / len(order)))
apart = {r for r, s in by_room.items() if "joint" in s and not s & {"order", "bound"}}
print("rooms with only one act holding both ends, no order or bound: %d" % len(apart))
print("  with them in the denominator, the order holds in %d of %d (%.3f)" % (
    len(order), len(episode | apart), len(order) / len(episode | apart)))
print("C2's count: both 203, holds 160, share 0.788 (null mean 0.603, p95 0.655); F-005: the reverse order in 41 of 203")
