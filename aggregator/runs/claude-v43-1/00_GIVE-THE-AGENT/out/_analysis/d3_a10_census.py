#!/usr/bin/env python3
"""A10's order test (D3a-37, G42): the census of my rulings, by room, beside C2's count and F-019's.

Each ruled line gets the class it was ruled under (the rules were logged before this script ran):
  instantiate (A10-inst-spec.txt): O order; M order named in words; J one act; MF move first; NP one end;
  restrict (A10-restrict-spec.txt): S-O order; S-M order named in words; S-MF move first; S-MO move only;
    S-BOUND bound; S-GU gave up; S-NM no move; S-HELD held; EL evidence limit; P-G6 other;
  add-condition and contradict (A10-adds.jsonl): no move where the reason says the census counts it so; else held;
  absent (A10-absent.jsonl): a reject is the order; a specification is held; a particular is other; an accept with
    kind none is a limit.
Every class is checked against the decision and kind written in the rulings files. A room is counted in each class
its lines show, then once by priority: order, move first, bound, one act, gave up, no move, move only, held, one end,
el, other, limit. A room whose lines show both the order and move first is resolved by its first acts (RESOLVE, with
the earliest doubt and the earliest move after a loss its lines cite).

  python3 out/_analysis/d3_a10_census.py
"""
import json
from collections import Counter

R = "out/_analysis/d3_rulings/"

# room: (class kept, earliest doubt cited, earliest move after a loss cited, the lines that cite them)
RESOLVE = {"bangladesh": ("movefirst", "58.95", "57.19",
                          "bangladesh-056's c0016, a fresh start after the flag is defaced, before bangladesh-040's "
                          "c0017, the room's first doubt")}


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
for f in ("A10-inst.jsonl", "A10-restrict.jsonl", "A10-adds.jsonl", "A10-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
print("lines ruled in A10's files:", len(ruled))

SPEC = ("accept", "specification")
EXPECT = {"O": ("accept", None), "M": ("accept", None), "J": ("reject", None), "MF": ("reject", None),
          "NP": ("reject", None), "S-O": SPEC, "S-M": SPEC, "S-MF": SPEC, "S-MO": SPEC, "S-BOUND": SPEC,
          "S-GU": SPEC, "S-NM": SPEC, "S-HELD": SPEC, "EL": ("accept", "none"), "P-G6": ("particular", None)}
CLASS = {"O": "order", "M": "order", "J": "joint", "MF": "movefirst", "NP": "one",
         "S-O": "order", "S-M": "order", "S-MF": "movefirst", "S-MO": "moveonly", "S-BOUND": "bound",
         "S-GU": "gaveup", "S-NM": "nomove", "S-HELD": "held", "EL": "el", "P-G6": "other"}

line_class, words, evidence = {}, set(), {}
for name in ("A10-inst-spec.txt", "A10-restrict-spec.txt"):
    for i, (c, ev) in spec(name).items():
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d, (i, c, ruled[i]["decision"])
        if k:
            assert ruled[i].get("kind") == k, (i, c, ruled[i].get("kind"))
        line_class[i] = CLASS[c]
        evidence[i] = (c, ev)
        if c in ("M", "S-M"):
            words.add(i)
for r in load("A10-adds.jsonl"):
    i = r["adaptation"]
    assert r["decision"] == "accept" and r.get("kind") == "specification", i
    line_class[i] = "nomove" if "counted in the census as no move" in r["reason"] else "held"
for r in load("A10-absent.jsonl"):
    i = r["adaptation"]
    if r["decision"] == "reject":
        line_class[i] = "order"
        evidence[i] = ("absent reject", r["reason"])
    elif r["decision"] == "particular":
        line_class[i] = "other"
    elif r.get("kind") == "specification":
        line_class[i] = "held"
    else:
        assert r["decision"] == "accept" and r.get("kind") == "none", i
        line_class[i] = "limit"
assert set(line_class) == set(ruled), set(ruled) ^ set(line_class)

print("lines by class:", dict(Counter(line_class.values())))
print("lines showing the mechanism in words:", len(words))
by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A10 line:", len(by_room))
PRI = ("order", "movefirst", "bound", "joint", "gaveup", "nomove", "moveonly", "held", "one", "el", "other", "limit")
for c in PRI:
    print("  rooms showing %-10s %d" % (c, sum(1 for s in by_room.values() if c in s)))

both = sorted(r for r, s in by_room.items() if {"order", "movefirst"} <= s)
print("rooms whose lines show both the order and move first: %d" % len(both))
for r in both:
    if r in RESOLVE:
        keep, dh, mh, cites = RESOLVE[r]
        print("  %s: kept as %s (earliest doubt h+%s, earliest move h+%s; %s)" % (r, keep, dh, mh, cites))
        by_room[r] = by_room[r] - ({"order", "movefirst"} - {keep})
    else:
        print("  %s: UNRESOLVED" % r)
        for i in sorted(evidence):
            if room(i) == r and line_class[i] in ("order", "movefirst"):
                print("     %s %s: %s" % (i, evidence[i][0], evidence[i][1][:420]))

first = Counter(next(c for c in PRI if c in s) for s in by_room.values())
print("rooms once, by priority:", {c: first[c] for c in PRI})
order = {r for r, s in by_room.items() if "order" in s}
mf = {r for r, s in by_room.items() if "movefirst" in s} - order
bound = {r for r, s in by_room.items() if "bound" in s} - order - mf
ordered = order | mf | bound
print("rooms whose lines order both ends: %d (order %d, move first %d, bound %d)" % (
    len(ordered), len(order), len(mf), len(bound)))
print("  the order holds in %d of %d (%.3f)" % (len(order), len(ordered), len(order) / len(ordered)))
print("  move first: %s" % " ".join(sorted(mf)))
print("  bound: %s" % " ".join(sorted(bound)))
joint = {r for r, s in by_room.items() if "joint" in s} - ordered
print("rooms with one act holding both ends and no ordered episode: %d: %s" % (len(joint), " ".join(sorted(joint))))
print("  with them in the denominator, the order holds in %d of %d (%.3f)" % (
    len(order), len(ordered | joint), len(order) / len(ordered | joint)))
moved = ordered | joint
gave = {r for r, s in by_room.items() if "gaveup" in s} - moved
nomove = {r for r, s in by_room.items() if "nomove" in s} - moved - gave
print("rooms showing doubt and then a move, giving up or no move: %d (moved %d, gave up %d, no move %d)" % (
    len(moved | gave | nomove), len(moved), len(gave), len(nomove)))
print("  moved: share %.3f" % (len(moved) / len(moved | gave | nomove)))
print("  gave up: %s" % " ".join(sorted(gave)))
named = {room(i) for i in words} & order
print("order rooms whose lines show the mechanism in words: %d (%.3f of the order rooms)" % (
    len(named), len(named) / len(order)))
only = {r for r, s in by_room.items() if "moveonly" in s} - moved
print("rooms with a move and no doubt of their own (move only, not carrying both): %d: %s" % (
    len(only), " ".join(sorted(only))))
print("C2's count: both 21, holds 11, share 0.524 (null mean 0.298, p95 0.429); C5c read: the judgment first in 10 of 20")
print("F-019: of 36 rooms with doubt and a loss, 10 moved; of the 26 with no move, 11 gave the work up")
