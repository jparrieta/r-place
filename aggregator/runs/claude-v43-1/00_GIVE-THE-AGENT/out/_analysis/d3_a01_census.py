#!/usr/bin/env python3
"""A01's order test (D3a-29, G34): the census of my rulings, by room, beside C2's count.

Each ruled line gets the class it was ruled under:
  instantiate (A01-inst-spec.txt): O order; BOUND-S the call reports a start or progress, or a report comes first;
    BOUND-L a call for a placed mark; NS what follows reports no state; ONE one end; OTHER another canvas or the close;
  restrict (A01-restrict-spec.txt): S-O order; S-BOUND the bound's pattern (its start subtype where the evidence says the
    call reports a start or work under way); S-HELD held by another statement; EL an evidence limit;
  add-condition (A01-adds.jsonl): order where the reason names A01's order, bound where it names A01's bound, else held;
  absent (A01-absent.jsonl): a reject is the order; an accept is an evidence limit; a particular is other.
Every class is checked against the decision and kind written to the ledger. A room is counted in each class its lines
show, then once by priority: order, bound, held, ns, one, el, other, limit. An episode is the order or the bound.

  python3 out/_analysis/d3_a01_census.py
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
for f in ("A01-inst.jsonl", "A01-restrict.jsonl", "A01-adds.jsonl", "A01-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r

EXPECT = {"O": ("accept", "specification"), "BOUND-S": ("reject", None), "BOUND-L": ("reject", None),
          "NS": ("reject", None), "ONE": ("reject", None), "OTHER": ("reject", None),
          "S-O": ("accept", "specification"), "S-BOUND": ("accept", "specification"),
          "S-HELD": ("accept", "specification"), "EL": ("accept", "none")}
CLASS = {"O": "order", "BOUND-S": "bound", "BOUND-L": "bound", "NS": "ns", "ONE": "one", "OTHER": "other",
         "S-O": "order", "S-BOUND": "bound", "S-HELD": "held", "EL": "el"}
START = re.compile(r"reports a start|start under way|work under way|reports progress|report comes before|"
                   r"comes first|before the call|placed before|with no call|work done|work before")

line_class, start_sub = {}, set()
for name in ("A01-inst-spec.txt", "A01-restrict-spec.txt"):
    for i, (c, ev) in spec(name).items():
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d, (i, c, ruled[i]["decision"])
        if k:
            assert ruled[i].get("kind") == k, (i, c, ruled[i].get("kind"))
        line_class[i] = CLASS[c]
        if c == "BOUND-S" or (c == "S-BOUND" and START.search(ev)):
            start_sub.add(i)
for r in load("A01-adds.jsonl"):
    assert r["decision"] == "accept" and r["kind"] == "specification", r["adaptation"]
    if "A01's order" in r["reason"]:
        line_class[r["adaptation"]] = "order"
    elif "A01's bound" in r["reason"]:
        line_class[r["adaptation"]] = "bound"
    else:
        line_class[r["adaptation"]] = "held"
for r in load("A01-absent.jsonl"):
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
print("bound lines with the call reporting a start, or a report first:", len(start_sub))

by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A01 line:", len(by_room))
for c in ("order", "bound", "held", "ns", "one", "el", "other", "limit"):
    print("  rooms showing %-6s %d" % (c, sum(1 for s in by_room.values() if c in s)))
PRI = ("order", "bound", "held", "ns", "one", "el", "other", "limit")
first = Counter(next(c for c in PRI if c in s) for s in by_room.values())
print("rooms once, by priority:", {c: first[c] for c in PRI})

order = {r for r, s in by_room.items() if "order" in s}
bound = {r for r, s in by_room.items() if "bound" in s}
start_rooms = {room(i) for i in start_sub}
both = order & bound
episode = order | bound
print("rooms in both the order and the bound:", len(both))
print("rooms with an episode (order or bound):", len(episode))
print("  order: %d, share %.3f" % (len(order), len(order) / len(episode)))
print("  bound only: %d; of them with a call reporting a start or a report first: %d"
      % (len(bound - order), len((bound - order) & start_rooms)))
print("  order only (no bound line): %d, share of episodes %.3f" % (len(order - bound), len(order - bound) / len(episode)))
print("C2's count: both 126, holds 81, share 0.643 (null mean 0.505, p95 0.571)")
