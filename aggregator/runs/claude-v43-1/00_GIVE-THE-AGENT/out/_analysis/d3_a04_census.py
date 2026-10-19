#!/usr/bin/env python3
"""A04's order test (D3a-31, G36): the census of my rulings, by room, beside C2's count and C5's range.

Each ruled line gets the class it was ruled under:
  instantiate (A04-inst-spec.txt): O order; BOUND talk before any upkeep or damage; J damage named only inside the talk
    or talk as the means of defence (counted apart); ASK a proposal to ask with no request made (counted apart);
    NP not P08's terms; MOVE a loss or move in place of upkeep; ONE one end; OTHER the neighbour's upkeep or after
    hour 73; P-G6 NONPORTABLE (other);
  restrict and contradict (A04-restrict-spec.txt, A04-contradict-spec.txt): S-O order; S-BOUND bound; S-HELD held by
    another statement; EL evidence limit;
  add-condition and add-step (A04-adds.jsonl): bound where the reason names A04's bound, other for the paired
    elaboration, else held;
  absent (A04-absent-v2.jsonl): a reject is the order, a particular is other, an accept is an evidence limit.
Every class is checked against the decision and kind written to the ledger. A room is counted in each class its lines
show, then once by priority: order, bound, joint, ask, held, move, np, one, el, other, limit. An episode is the order
or the bound.

  python3 out/_analysis/d3_a04_census.py
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
for f in ("A04-inst.jsonl", "A04-restrict.jsonl", "A04-contradict.jsonl", "A04-adds.jsonl", "A04-absent-v2.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
print("lines ruled in A04's files:", len(ruled))

EXPECT = {"O": ("accept", "specification"), "BOUND": ("reject", None), "J": ("reject", None), "ASK": ("reject", None),
          "NP": ("reject", None), "MOVE": ("reject", None), "ONE": ("reject", None), "OTHER": ("reject", None),
          "P-G6": ("particular", None), "S-O": ("accept", "specification"), "S-BOUND": ("accept", "specification"),
          "S-HELD": ("accept", "specification"), "EL": ("accept", "none")}
CLASS = {"O": "order", "BOUND": "bound", "J": "joint", "ASK": "ask", "NP": "np", "MOVE": "move", "ONE": "one",
         "OTHER": "other", "P-G6": "other", "S-O": "order", "S-BOUND": "bound", "S-HELD": "held", "EL": "el"}

line_class = {}
for name in ("A04-inst-spec.txt", "A04-restrict-spec.txt", "A04-contradict-spec.txt"):
    for i, c in spec(name).items():
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d, (i, c, ruled[i]["decision"])
        if k:
            assert ruled[i].get("kind") == k, (i, c, ruled[i].get("kind"))
        line_class[i] = CLASS[c]
for r in load("A04-adds.jsonl"):
    assert r["decision"] == "accept", r["adaptation"]
    if r["kind"] == "elaboration":
        line_class[r["adaptation"]] = "other"
    else:
        assert r["kind"] == "specification", r["adaptation"]
        line_class[r["adaptation"]] = "bound" if "A04's own bound" in r["reason"] or "A04's bound" in r["reason"] else "held"
for r in load("A04-absent-v2.jsonl"):
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
print("rooms with an A04 line:", len(by_room))
PRI = ("order", "bound", "joint", "ask", "held", "move", "np", "one", "el", "other", "limit")
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
apart = {r for r, s in by_room.items() if s & {"joint", "ask"} and not s & {"order", "bound"}}
print("rooms with only damage-inside-talk or a proposal to ask, no order or bound: %d" % len(apart))
print("  with them in the denominator, the order holds in %d of %d (%.3f)" % (
    len(order), len(episode | apart), len(order) / len(episode | apart)))
print("C2's count: both 401, holds 235, share 0.586 (null mean 0.501, p95 0.539)")
print("C5's range, where border talk comes first: terms or space with no damage named in 19 of 26 to 36 of 38 records")
