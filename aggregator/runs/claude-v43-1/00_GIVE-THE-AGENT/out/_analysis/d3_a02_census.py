#!/usr/bin/env python3
"""A02's order test (D3a-28, G33): the census of my rulings, by room, beside C2's count.

Each ruled line gets the class it was ruled under:
  instantiate (A02-inst-spec.txt): O order, J+ joint opening with a later call, J lone joint opening,
    BOUND the bound's pattern, ONE one end only, OTHER a visitor's own or another mark;
  restrict (A02-restrict-spec.txt): S-O order, S-J+, S-BOUND, EL a lone joint opening (evidence limit),
    C correction, P-LOCAL the falsifier (a start drawing helpers with no call), P-G6 non-portable;
  add-condition and add-step (A02-adds.jsonl): a joint opening, or J+ where the reason names a later
    call or rally around the mark;
  absent (A02-absent-v2.jsonl): a reject is the order, or J+ where the reason names a joint opening
    followed by a later call; an accept is an evidence limit.
Every class is checked against the decision and kind written to the ledger. A room is counted in each
class its lines show, then once by priority: order, J+, bound, falsifier, joint, one end, other, limit.

  python3 out/_analysis/d3_a02_census.py
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
for f in ("A02-inst-v2.jsonl", "A02-restrict.jsonl", "A02-adds.jsonl", "A02-absent-v2.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r

EXPECT = {"O": ("accept", "specification"), "J+": ("accept", "specification"), "J": ("reject", None),
          "BOUND": ("reject", None), "ONE": ("reject", None), "OTHER": ("reject", None),
          "S-O": ("accept", "specification"), "S-J+": ("accept", "specification"),
          "S-BOUND": ("accept", "specification"), "EL": ("accept", "none"), "C": ("accept", "correction"),
          "P-LOCAL": ("particular", None), "P-G6": ("particular", None)}
CLASS = {"O": "order", "J+": "jplus", "J": "joint", "BOUND": "bound", "ONE": "one", "OTHER": "other",
         "S-O": "order", "S-J+": "jplus", "S-BOUND": "bound", "EL": "joint", "C": "correction",
         "P-LOCAL": "falsifier", "P-G6": "other"}

line_class = {}
for name in ("A02-inst-spec.txt", "A02-restrict-spec.txt"):
    for i, c in spec(name).items():
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d, (i, c, ruled[i]["decision"])
        if k:
            assert ruled[i].get("kind") == k, (i, c, ruled[i].get("kind"))
        line_class[i] = CLASS[c]
adds_jplus = []
for r in load("A02-adds.jsonl"):
    assert r["decision"] == "accept" and r["kind"] == "specification", r["adaptation"]
    later = "later rally" in r["reason"] or "later call" in r["reason"]
    line_class[r["adaptation"]] = "jplus" if later else "joint"
    if later:
        adds_jplus.append(r["adaptation"])
absent_jplus = []
for r in load("A02-absent-v2.jsonl"):
    i = r["adaptation"]
    if r["decision"] == "reject":
        jp = "joint opening followed by a later call" in r["reason"]
        line_class[i] = "jplus" if jp else "order"
        if jp:
            absent_jplus.append(i)
    else:
        assert r["decision"] == "accept" and r["kind"] == "none", i
        line_class[i] = "limit"
assert set(line_class) == set(ruled), set(ruled) ^ set(line_class)

print("lines by class:", dict(Counter(line_class.values())))
print("adds read as J+ (a later rally or call named):", adds_jplus)
print("absent rejects read as J+:", len(absent_jplus), absent_jplus)

by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A02 line:", len(by_room))
for c in ("order", "jplus", "bound", "falsifier", "correction", "joint", "one", "other", "limit"):
    print("  rooms showing %-10s %d" % (c, sum(1 for s in by_room.values() if c in s)))

PRI = ("order", "jplus", "bound", "falsifier", "joint", "one", "other", "limit")
first = Counter(next(c for c in PRI if c in s) for s in by_room.values())
print("rooms once, by priority:", {c: first[c] for c in PRI})

order = {r for r, s in by_room.items() if "order" in s}
holds = {r for r, s in by_room.items() if s & {"order", "jplus"}}
bound = {r for r, s in by_room.items() if "bound" in s}
fals = {r for r, s in by_room.items() if "falsifier" in s}
joint_only = {r for r, s in by_room.items() if "joint" in s and not s & {"order", "jplus", "bound", "falsifier"}}
episode = holds | bound | fals
print("rooms in both the hold (order or J+) and the bound:", len(holds & bound), sorted(holds & bound))
print("rooms with an order episode (hold, bound or falsifier):", len(episode))
print("  holds (order or J+): %d, share %.3f" % (len(holds), len(holds) / len(episode)))
print("  order alone: %d, share %.3f" % (len(order), len(order) / len(episode)))
print("  bound only: %d %s" % (len(bound - holds), sorted(bound - holds)))
print("  falsifier:", sorted(fals))
print("rooms with a joint opening and no episode (counted apart):", len(joint_only))
print("C2's count: both 89, holds 64, share 0.719 (null mean 0.473, p95 0.539)")
