#!/usr/bin/env python3
"""A07's order test (D3a-34, G39): the census of my rulings, by room, beside C2's count.

Each ruled line gets the class it was ruled under (the rules were logged before this script ran):
  instantiate (A07-inst-spec.txt): O order; M order named in words; J one act holding both ends (joint); ONE one end;
    BOUND2 bound; OTHER and P-G6 other; the three BOUND lines take the class of their re-ruling
    (A07-rerule-reading1.jsonl), an early marking;
  restrict (A07-restrict-spec-105.txt): S-O order; S-M order named in words; S-BOUND bound; S-HELD an early marking
    where its evidence names an early marking or credit, else held; EL evidence limit; FAM the family;
  add-condition, add-step and contradict (A07-adds.jsonl): bound where the reason names A07's own bound; the order
    where it restates A07's connection with the order shown; the family for an elaboration; el for kind none; other
    for the particular; else held;
  absent (A07-absent.jsonl): a reject is the order (named in words where its reason says a plain report); the
    specification is one end; an accept with kind none is a limit.
Every class is checked against the decision and kind written in the rulings files. A room is counted in each class
its lines show, then once by priority: order, bound, joint, early, family, held, one, el, other, limit. An episode is
the order or the bound.

  python3 out/_analysis/d3_a07_census.py
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
            out[p[0]] = (p[1], p[2])
    return out


ruled = {}
for f in ("A07-inst.jsonl", "A07-restrict.jsonl", "A07-adds.jsonl", "A07-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
rerule = {r["adaptation"]: r for r in load("A07-rerule-reading1.jsonl")}
for i, r in rerule.items():
    assert i in ruled and r["decision"] == ruled[i]["decision"] == "reject", i
    ruled[i] = r
print("lines ruled in A07's files:", len(ruled), "; re-ruled under corrected reading 1:", len(rerule))

EXPECT = {"O": ("accept", None), "M": ("accept", None), "J": ("reject", None), "ONE": ("reject", None),
          "BOUND": ("reject", None), "BOUND2": ("reject", None), "FAM": ("reject", None), "OTHER": ("reject", None),
          "P-G6": ("particular", None), "S-O": ("accept", "specification"), "S-M": ("accept", "specification"),
          "S-BOUND": ("accept", "specification"), "S-HELD": ("accept", "specification"), "EL": ("accept", "none")}
CLASS = {"O": "order", "M": "order", "J": "joint", "ONE": "one", "BOUND2": "bound", "OTHER": "other",
         "P-G6": "other", "S-O": "order", "S-M": "order", "S-BOUND": "bound", "EL": "el"}

line_class, words = {}, set()
for name in ("A07-inst-spec.txt", "A07-restrict-spec-105.txt"):
    for i, (c, ev) in spec(name).items():
        if c == "FAM" and name.startswith("A07-restrict"):
            assert ruled[i]["decision"] == "accept" and ruled[i].get("kind") == "elaboration" and ruled[i].get("pair"), i
            line_class[i] = "family"
            continue
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d, (i, c, ruled[i]["decision"])
        if k:
            assert ruled[i].get("kind") == k, (i, c, ruled[i].get("kind"))
        if c == "BOUND":
            assert i in rerule and "an early marking" in ruled[i]["reason"], i
            line_class[i] = "early"
        elif c == "FAM":
            line_class[i] = "family"
        elif c == "S-HELD":
            line_class[i] = "early" if ("early marking" in ev or "early credit" in ev) else "held"
        else:
            line_class[i] = CLASS[c]
        if c in ("M", "S-M"):
            words.add(i)
for r in load("A07-adds.jsonl"):
    i, k = r["adaptation"], r.get("kind")
    if r["decision"] == "particular":
        line_class[i] = "other"
    elif k == "elaboration":
        assert r["decision"] == "accept" and r.get("pair"), i
        line_class[i] = "family"
    elif k == "none":
        assert r["decision"] == "accept", i
        line_class[i] = "el"
    else:
        assert r["decision"] == "accept" and k == "specification", i
        if "A07's own bound" in r["reason"]:
            line_class[i] = "bound"
        elif "restates A07's connection" in r["reason"]:
            line_class[i] = "order"
        else:
            line_class[i] = "held"
for r in load("A07-absent.jsonl"):
    i = r["adaptation"]
    if r["decision"] == "reject":
        line_class[i] = "order"
        if "a plain report" in r["reason"]:
            words.add(i)
    elif r.get("kind") == "specification":
        assert r["decision"] == "accept", i
        line_class[i] = "one"
    else:
        assert r["decision"] == "accept" and r["kind"] == "none", i
        line_class[i] = "limit"
assert set(line_class) == set(ruled), set(ruled) ^ set(line_class)

print("lines by class:", dict(Counter(line_class.values())))
print("lines showing the order with a plain report answered by a marking (the mechanism in words):", len(words))
by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A07 line:", len(by_room))
PRI = ("order", "bound", "joint", "early", "family", "held", "one", "el", "other", "limit")
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
print("rooms where a plain report is answered by a marking: %d (%.3f of the episode rooms; %.3f of the order rooms)" % (
    len(named), len(named) / len(episode), len(named) / len(order)))
joint = {r for r, s in by_room.items() if "joint" in s and not s & {"order", "bound"}}
early = {r for r, s in by_room.items() if "early" in s and not s & {"order", "bound", "joint"}}
print("rooms with one act holding both ends and no order or bound: %d" % len(joint))
print("rooms with an early marking and no order, bound or joint act: %d: %s" % (len(early), " ".join(sorted(early))))
wide = episode | joint | early
print("  with those rooms in the denominator, the order holds in %d of %d (%.3f)" % (
    len(order), len(wide), len(order) / len(wide)))
fam = {r for r, s in by_room.items() if "family" in s}
print("rooms showing the family (an attempt ended before the close, marked): %d: %s" % (len(fam), " ".join(sorted(fam))))
print("C2's count: both 182, holds 139, share 0.764 (null mean 0.378, p95 0.434)")
