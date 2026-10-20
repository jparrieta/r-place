#!/usr/bin/env python3
"""A14's order test (D3a-41, G46): the census of the rulings by line and by room, with the rules logged before this
script was written. Classes come from the spec files (instantiate, restrict, add-condition, add-step) and the absent
rulings; each class is checked against the decision and kind written in the rulings files. Tags come from the
A14-tags files. Beside it, A13's ruled lines whose reasons name A14. Prints counts only. Writes nothing.

  python3 out/_analysis/d3_a14_census.py
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
for f in ("A14-inst.jsonl", "A14-restrict.jsonl", "A14-addc.jsonl", "A14-adds.jsonl", "A14-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
print("lines ruled in A14's files:", len(ruled))

SPEC, NONE, REJ, PART = ("accept", "specification"), ("accept", "none"), ("reject", None), ("particular", None)
EXPECT = {"O-S": SPEC, "O-X": SPEC, "O-U": SPEC, "M-S": SPEC, "M-X": SPEC, "M-U": SPEC, "BOUND": REJ, "J": REJ,
          "NT": REJ, "NH": REJ, "ONE": REJ, "AFTER": REJ, "P-G6": PART, "S-O-S": SPEC, "S-O-X": SPEC, "S-O-U": SPEC,
          "S-M-S": SPEC, "S-M-U": SPEC, "S-BOUND": SPEC, "S-HELD": SPEC, "EL-J": NONE, "EL-NT": NONE, "EL-NH": NONE,
          "EL-ONE": NONE, "EL-AFTER": NONE}
CLASS = {"BOUND": "bound", "J": "oneoffer", "NT": "notterms", "NH": "nothelp", "ONE": "one", "AFTER": "after",
         "HELD": "held", "P-G6": "other"}


def cls_of(c):
    if c.startswith("S-"):
        c = c[2:]
    elif c.startswith("EL-"):
        c = c[3:]
    if c[:2] in ("O-", "M-"):
        return "order", c[2:], c[0] == "M"
    return CLASS[c], None, False


line_class, channel, words, source = {}, {}, set(), {}
for name, src in (("A14-inst-spec.txt", "instantiate"), ("A14-restrict-spec.txt", "restrict"),
                  ("A14-addc-spec.txt", "add-condition"), ("A14-adds-spec.txt", "add-step")):
    for i, c in spec(name).items():
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d and (k is None or ruled[i].get("kind") == k), (i, c)
        line_class[i], channel[i], w = cls_of(c)
        source[i] = src
        if w:
            words.add(i)
for r in load("A14-absent.jsonl"):
    i = r["adaptation"]
    source[i] = "absent"
    if r["decision"] == "reject":
        line_class[i], channel[i] = "order", "ungraded"
    elif r["decision"] == "particular":
        line_class[i] = "other"
    else:
        assert r["decision"] == "accept" and r.get("kind") == "none", i
        line_class[i] = "limit"
assert set(line_class) == set(ruled), set(ruled) ^ set(line_class)

tags = {}
for f in glob.glob(R + "A14-tags-*.txt"):
    for l in open(f, encoding="utf-8"):
        if l.strip():
            i, t = l.strip().split("|")
            assert i in ruled, (f, i)
            tags.setdefault(i, set()).update(t.split(","))
for i, t in sorted(tags.items()):
    if "PO" in t:
        line_class[i], channel[i] = "order", "S"
        print("particular counted with the order (PO):", i)
nb_off_order = [i for i, t in tags.items() if "NB" in t and line_class[i] != "order"]
assert not nb_off_order, nb_off_order

print("lines by class:", dict(sorted(Counter(line_class.values()).items())))
order_lines = [i for i, c in line_class.items() if c == "order"]
print("order lines: %d; named in words %d; by the hours, thread, reply chain or post's words %d; absent rejects %d" % (
    len(order_lines), len(words & set(order_lines)),
    sum(1 for i in order_lines if i not in words and channel.get(i) != "ungraded"),
    sum(1 for i in order_lines if channel.get(i) == "ungraded")))
print("  order lines by source:", dict(sorted(Counter(source[i] for i in order_lines).items())))
print("  channel of the first help among order lines:", dict(sorted(Counter(channel[i] for i in order_lines).items())))
print("  order lines naming the first terms from the room's record (R): %d" % sum(
    1 for i in order_lines if "R" in tags.get(i, ())))
nb = {i for i in order_lines if "NB" in tags.get(i, ())}
print("  order lines whose help names an alliance, exchange, joint work or neighbour relation (NB): %d" % len(nb))

by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A14 line:", len(by_room))
PRI = ("order", "bound", "oneoffer", "held", "notterms", "nothelp", "one", "after", "other", "limit")
for c in PRI:
    print("  rooms showing %-9s %d" % (c, sum(1 for s in by_room.values() if c in s)))
first = Counter(next(c for c in PRI if c in s) for s in by_room.values())
print("rooms once, by priority:", {c: first[c] for c in PRI})
order = {r for r, s in by_room.items() if "order" in s}
episode = {r for r, s in by_room.items() if s & {"order", "bound"}}
print("rooms with an episode (the order or the bound): %d; the order in %d (%.3f)" % (
    len(episode), len(order), len(order) / len(episode)))
print("  episode rooms with help first only (the bound): %d (%.3f)" % (
    len(episode - order), len(episode - order) / len(episode)))
oneoffer_only = {r for r, s in by_room.items() if "oneoffer" in s and not s & {"order", "bound"}}
print("  with %d one-offer rooms in the denominator, the order holds in %d of %d (%.3f)" % (
    len(oneoffer_only), len(order), len(episode | oneoffer_only), len(order) / len(episode | oneoffer_only)))
named = {room(i) for i in words if line_class[i] == "order"}
print("rooms where the order is named in words: %d (%.3f of the order rooms)" % (len(named), len(named) / len(order)))
named_nb = named | {room(i) for i in nb}
print("  with NB added (F-020's wider grounds): %d (%.3f of the order rooms)" % (
    len(named_nb), len(named_nb) / len(order)))
ch_rooms = {d: {room(i) for i in order_lines if channel[i] == d} for d in ("S", "X", "U", "ungraded")}
print("order rooms by the channel their lines show:", {d: len(s) for d, s in ch_rooms.items()})
only_x = {r for r in order if not any(room(i) == r and channel[i] in ("S", "U", "ungraded") for i in order_lines)}
print("order rooms whose order lines show help only with a third room: %d" % len(only_x))

a13 = []
for f in ("A13-inst.jsonl", "A13-restrict.jsonl", "A13-addc.jsonl", "A13-adds.jsonl", "A13-absent.jsonl",
          "A13-rerule.jsonl"):
    a13 += [r for r in load(f) if "A14" in r["reason"]]
a13_rooms = {room(r["adaptation"]) for r in a13}
print("A13's ruled lines whose reasons name A14: %d in %d rooms; of those rooms, %d show A14's order here, %d have an "
      "A14 line of another class, %d have no A14 line" % (
          len(a13), len(a13_rooms), len(a13_rooms & order), len((a13_rooms & set(by_room)) - order),
          len(a13_rooms - set(by_room))))
print("Beside: C2 counted the order in 138 of 214 rooms carrying both (0.645; null mean 0.591, p95 0.636), from 108 "
      "transitions in 44 rooms; the counterexample response counts 76 of 214 trading help before any border talk; "
      "F-020: the first help names a deal, border, truce, alliance, exchange or neighbour relation in 63 of 127 where "
      "border talk comes first (0.496)")
