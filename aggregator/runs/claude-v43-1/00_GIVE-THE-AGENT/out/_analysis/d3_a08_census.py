#!/usr/bin/env python3
"""A08's order test (D3a-35, G40): the census of my rulings, by room, beside C2's count.

Each ruled line gets the class it was ruled under (the rules were logged before this script ran):
  instantiate (A08-inst-spec.txt): O order; M order named in words; J joint; JM joint with a record asked for or
    given later (joint); ONE one end; OTHER and P-G6 other;
  restrict (A08-restrict-spec.txt): S-O order; S-M order named in words; S-BOUND bound; S-RF record first; S-HELD an
    early record where its evidence names an early record, an attempt where it names A07's bound, else held; EL
    evidence limit; FAM the family; P-G6 other;
  add-condition and add-step (A08-adds.jsonl): the order where the reason names A08's own mechanism; an early record
    where it names one; else held; kind none is el;
  absent (A08-absent.jsonl): a reject is the order; a particular is other; an accept with kind none is a limit.
Every class is checked against the decision and kind written in the rulings files. A room is counted in each class
its lines show, then once by priority: order, bound, record first, joint, attempt, early, family, held, one, el,
other, limit. An episode is the order or the bound.

  python3 out/_analysis/d3_a08_census.py
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
for f in ("A08-inst.jsonl", "A08-restrict.jsonl", "A08-adds.jsonl", "A08-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
print("lines ruled in A08's files:", len(ruled))

EXPECT = {"O": ("accept", None), "M": ("accept", None), "J": ("reject", None), "JM": ("reject", None),
          "ONE": ("reject", None), "OTHER": ("reject", None), "P-G6": ("particular", None),
          "S-O": ("accept", "specification"), "S-M": ("accept", "specification"),
          "S-BOUND": ("accept", "specification"), "S-RF": ("accept", "specification"),
          "S-HELD": ("accept", "specification"), "EL": ("accept", "none"), "FAM": ("accept", "elaboration")}
CLASS = {"O": "order", "M": "order", "J": "joint", "JM": "joint", "ONE": "one", "OTHER": "other", "P-G6": "other",
         "S-O": "order", "S-M": "order", "S-BOUND": "bound", "S-RF": "recordfirst", "EL": "el", "FAM": "family"}

line_class, words, jm = {}, set(), set()
for name in ("A08-inst-spec.txt", "A08-restrict-spec.txt"):
    for i, (c, ev) in spec(name).items():
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d, (i, c, ruled[i]["decision"])
        if k:
            assert ruled[i].get("kind") == k, (i, c, ruled[i].get("kind"))
        if c == "FAM":
            assert ruled[i].get("pair"), i
        if c == "S-HELD":
            line_class[i] = ("early" if "early record" in ev else
                             "attempt" if "A07's bound" in ev else "held")
        else:
            line_class[i] = CLASS[c]
        if c in ("M", "S-M"):
            words.add(i)
        if c == "JM":
            jm.add(i)
for r in load("A08-adds.jsonl"):
    i, k = r["adaptation"], r.get("kind")
    assert r["decision"] == "accept", i
    if k == "none":
        line_class[i] = "el"
    else:
        assert k == "specification", i
        line_class[i] = ("order" if "A08's own mechanism" in r["reason"] else
                         "early" if "early record" in r["reason"] else "held")
        if line_class[i] == "order":
            words.add(i)
for r in load("A08-absent.jsonl"):
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
print("lines showing the mechanism in words:", len(words), "; joint lines with a record asked for or given later:",
      len(jm))
by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A08 line:", len(by_room))
PRI = ("order", "bound", "recordfirst", "joint", "attempt", "early", "family", "held", "one", "el", "other", "limit")
for c in PRI:
    print("  rooms showing %-11s %d" % (c, sum(1 for s in by_room.values() if c in s)))
first = Counter(next(c for c in PRI if c in s) for s in by_room.values())
print("rooms once, by priority:", {c: first[c] for c in PRI})
order = {r for r, s in by_room.items() if "order" in s}
bound = {r for r, s in by_room.items() if "bound" in s}
rf = {r for r, s in by_room.items() if "recordfirst" in s}
episode = order | bound
print("rooms in both the order and the bound:", len(order & bound), "; the order and record first:", len(order & rf))
print("rooms with an episode (order or bound):", len(episode))
print("  order: %d, share %.3f" % (len(order), len(order) / len(episode)))
print("  bound only: %d, share %.3f" % (len(bound - order), len(bound - order) / len(episode)))
rf_only = rf - episode
print("rooms with record first and no order or bound: %d: %s" % (len(rf_only), " ".join(sorted(rf_only))))
print("  with them in the denominator, the order holds in %d of %d (%.3f)" % (
    len(order), len(episode | rf_only), len(order) / len(episode | rf_only)))
named = {room(i) for i in words}
print("rooms where the mechanism is named in words: %d (%.3f of the order rooms)" % (len(named), len(named) / len(order)))
joint = {r for r, s in by_room.items() if "joint" in s and not s & {"order", "bound", "recordfirst"}}
print("rooms with one act holding both ends and no order, bound or record first: %d" % len(joint))
wide = episode | rf_only | joint
print("  with those rooms too in the denominator, the order holds in %d of %d (%.3f)" % (
    len(order), len(wide), len(order) / len(wide)))
fam = {r for r, s in by_room.items() if "family" in s}
print("rooms showing the family: %d: %s" % (len(fam), " ".join(sorted(fam))))
print("C2's count: both 289, holds 225, share 0.779 (null mean 0.565, p95 0.609)")
