#!/usr/bin/env python3
"""A21's order test, part 2 (D3a-27): the census of my rulings, by room.

Order rooms: lines that show A21's order, an agreement and after it a P21 form answering it
(accepted instantiate and add-step specifications, restrict specifications, rejected absent lines).
Reverse rooms: lines that show a P21 form at the making of terms or answering no agreement
(accepted restrict corrections, and instantiate rejects whose reasons say so). Corrections are split
by family: F1 'while ... terms are proposed or accepted' / 'at the making', F2 'no agreement in force'
answering an appeal, complaint, accusation, request or demand.
P21's shown rooms (accepted P21 instantiate, rejected P21 absent, and the re-ruling) are crossed with both.

  python3 out/_analysis/d3_a21_census.py
"""
import json

R = "out/_analysis/d3_rulings/"


def load(name):
    return [json.loads(l) for l in open(R + name) if l.strip()]


def room(aid):
    return aid.rsplit("-", 1)[0]


order, reverse, f1, f2 = set(), set(), set(), set()
for r in load("A21-inst.jsonl"):
    if r["decision"] == "accept":
        order.add(room(r["adaptation"]))
    elif "at the making" in r["reason"] or "before any agreement" in r["reason"] or "no agreement in force" in r["reason"]:
        reverse.add(room(r["adaptation"]))
        (f2 if "no agreement in force" in r["reason"] else f1).add(room(r["adaptation"]))
for r in load("A21-restrict.jsonl") + load("A21-addstep.jsonl"):
    k = r.get("kind")
    if r["decision"] == "accept" and k == "specification":
        order.add(room(r["adaptation"]))
    elif r["decision"] == "accept" and k == "correction":
        reverse.add(room(r["adaptation"]))
        (f2 if "no agreement in force" in r["reason"] or "answers no agreement" in r["reason"]
         or "answers an encroachment" in r["reason"] or "answers an accusation" in r["reason"] else f1).add(room(r["adaptation"]))
for r in load("A21-absent.jsonl"):
    if r["decision"] == "reject":
        order.add(room(r["adaptation"]))

p21 = set()
for r in load("P21-inst.jsonl"):
    if r["decision"] == "accept":
        p21.add(room(r["adaptation"]))
for r in load("P21-absent.jsonl") + load("P21-rerule-PinkUnion.jsonl"):
    if r["decision"] == "reject":
        p21.add(room(r["adaptation"]))

both = order & reverse
print("rooms showing A21's order:", len(order))
print("rooms showing a P21 form at the making of terms or with no agreement:", len(reverse),
      "(F1 at the making %d, F2 no agreement %d)" % (len(f1 - f2), len(f2)))
print("rooms in both:", len(both), sorted(both))
print("order only:", len(order - reverse), " reverse only:", len(reverse - order))
print("P21 shown rooms:", len(p21), " of them with A21's order:", len(p21 & order),
      " with the reverse:", len(p21 & reverse), " with neither:", len(p21 - order - reverse))
print("A21 order rooms not among P21's shown rooms:", len(order - p21))
