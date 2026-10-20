#!/usr/bin/env python3
"""A13's order test (D3a-40, G45): the census of the rulings by line and by room, with the rules logged before this
script was written. Classes come from the spec files (instantiate, restrict, add-condition, add-step), the re-ruling
spec, and the absent rulings; each class is checked against the decision and kind written in the rulings files.
Tags come from the A13-tags files. Prints counts only. Writes nothing.

  python3 out/_analysis/d3_a13_census.py
"""
import glob
import json
from collections import Counter

R = "out/_analysis/d3_rulings/"


def load(name):
    return [json.loads(l) for l in open(R + name, encoding="utf-8") if l.strip()]


def spec(name):
    out = {}
    for l in open(R + name, encoding="utf-8"):
        if l.strip():
            p = l.rstrip("\n").split("|", 2)
            out[p[0]] = p[1]
    return out


def room(aid):
    return aid.rsplit("-", 1)[0]


ruled = {}
for f in ("A13-inst.jsonl", "A13-restrict.jsonl", "A13-addc.jsonl", "A13-adds.jsonl", "A13-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
print("lines ruled in A13's files:", len(ruled))

SPEC, NONE, REJ, PART = ("accept", "specification"), ("accept", "none"), ("reject", None), ("particular", None)
EXPECT = {"O-IN": SPEC, "O-OUT": SPEC, "O-TR": SPEC, "M-IN": SPEC, "M-OUT": SPEC, "M-TR": SPEC, "BOUND": REJ, "SP": REJ,
          "J": REJ, "NH": REJ, "ONE": REJ, "AFTER": REJ, "P-G6": PART, "S-O-IN": SPEC, "S-O-OUT": SPEC, "S-O-TR": SPEC,
          "S-M-IN": SPEC, "S-M-OUT": SPEC, "S-M-TR": SPEC, "S-BOUND": SPEC, "S-SP": SPEC, "S-HELD": SPEC, "EL-J": NONE,
          "EL-NH": NONE, "EL-ONE": NONE}
CLASS = {"O": "order", "M": "order", "BOUND": "bound", "SP": "second", "J": "joint", "NH": "nothelp", "ONE": "one",
         "AFTER": "after", "HELD": "held", "P-G6": "other"}


def cls_of(c):
    c = c[2:] if c.startswith(("S-", "EL-")) and not c.startswith("EL-") else c
    c = c[3:] if c.startswith("EL-") else c
    if c[:2] in ("O-", "M-"):
        return CLASS[c[0]], c[2:], c[0] == "M"
    return CLASS[c], None, False


line_class, direction, words = {}, {}, set()
for name in ("A13-inst-spec.txt", "A13-restrict-spec.txt", "A13-addc-spec.txt", "A13-adds-spec.txt"):
    for i, c in spec(name).items():
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d and (k is None or ruled[i].get("kind") == k), (i, c)
        line_class[i], direction[i], w = cls_of(c)
        if w:
            words.add(i)
rerule = {r["adaptation"]: r for r in load("A13-rerule.jsonl")}
for i, c in spec("A13-rerule-spec.txt").items():
    assert rerule[i]["decision"] == EXPECT[c][0], (i, c)
    print("re-ruled: %s, %s -> %s" % (i, line_class[i], cls_of(c)[0]))
    line_class[i], direction[i], _ = cls_of(c)
    words.discard(i)
for r in load("A13-absent.jsonl"):
    i = r["adaptation"]
    if r["decision"] == "reject":
        line_class[i], direction[i] = "order", "ungraded"
    elif r["decision"] == "particular":
        line_class[i] = "other"
    else:
        assert r["decision"] == "accept" and r.get("kind") == "none", i
        line_class[i] = "limit"
assert set(line_class) == set(ruled), set(ruled) ^ set(line_class)

tags = {}
for f in glob.glob(R + "A13-tags-*.txt"):
    for l in open(f, encoding="utf-8"):
        if l.strip():
            i, t = l.strip().split("|")
            assert i in ruled, (f, i)
            tags.setdefault(i, set()).update(t.split(","))
for i, t in tags.items():
    if "PO" in t:
        line_class[i], direction[i] = "order", "TR"
        print("particular counted with the order (PO):", i)

print("lines by class:", dict(sorted(Counter(line_class.values()).items())))
order_lines = [i for i, c in line_class.items() if c == "order"]
print("order lines: %d; named in words %d; by the hours or the reply chain %d; absent rejects %d" % (
    len(order_lines), len(words & set(order_lines)),
    sum(1 for i in order_lines if i not in words and direction.get(i) != "ungraded"),
    sum(1 for i in order_lines if direction.get(i) == "ungraded")))
print("  direction of the first help among order lines:", dict(sorted(Counter(direction[i] for i in order_lines).items())))
print("  order lines naming the upkeep from the room's record (R): %d" % sum(1 for i in order_lines if "R" in tags.get(i, ())))
print("  one-act lines naming the night shortage (JM): %d" % sum(1 for i, c in line_class.items() if c == "joint" and "JM" in tags.get(i, ())))

by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A13 line:", len(by_room))
PRI = ("order", "bound", "second", "joint", "held", "nothelp", "one", "after", "other", "limit")
for c in PRI:
    print("  rooms showing %-8s %d" % (c, sum(1 for s in by_room.values() if c in s)))
first = Counter(next(c for c in PRI if c in s) for s in by_room.values())
print("rooms once, by priority:", {c: first[c] for c in PRI})
order = {r for r, s in by_room.items() if "order" in s}
episode = {r for r, s in by_room.items() if s & {"order", "bound", "second"}}
print("rooms with an episode (the order, the bound or the second path): %d; the order in %d (%.3f)" % (
    len(episode), len(order), len(order) / len(episode)))
help_first = episode - order
print("  episode rooms with help first only (the bound or the second path): %d (%.3f)" % (
    len(help_first), len(help_first) / len(episode)))
joint_only = {r for r, s in by_room.items() if "joint" in s and not s & {"order", "bound", "second"}}
print("  with %d one-act rooms in the denominator, the order holds in %d of %d (%.3f)" % (
    len(joint_only), len(order), len(episode | joint_only), len(order) / len(episode | joint_only)))
named = {room(i) for i in words if line_class[i] == "order"}
print("rooms where the order is named in words: %d (%.3f of the order rooms)" % (len(named), len(named) / len(order)))
dir_rooms = {d: {room(i) for i in order_lines if direction[i] == d} for d in ("IN", "OUT", "TR", "ungraded")}
print("order rooms by the direction their lines show:", {d: len(s) for d, s in dir_rooms.items()})
only_out = {r for r in order if not any(room(i) == r and direction[i] in ("IN", "TR", "ungraded") for i in order_lines)}
print("order rooms whose order lines show only help given (spare capacity): %d" % len(only_out))
print("Beside: C2 counted the order in 171 of 240 rooms carrying both (0.713; null mean 0.596, p95 0.642), from 106 "
      "transitions in 44 rooms; the counterexample response counts 69 of 240 giving or asking for help before upkeep")
