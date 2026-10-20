#!/usr/bin/env python3
"""A11's test (D3a-38, G43): the census of my rulings, by room, beside C2's transitions and its room-level order.

Each ruled line gets the class it was ruled under (the rules were logged before this script ran):
  instantiate (A11-inst-spec.txt): T transition in words; TO transition by P04's other forms; TF template first;
    E1 one end; P-G6 other;
  restrict (A11-restrict-spec.txt): S-T transition in words; S-TO transition by other forms; S-TF template first;
    S-X across threads; S-TALK talk only; S-LAY layout only; ONE one post; EL evidence limit; P-G6 other;
  add lines (A11-adds.jsonl): the transition or template first where the reason says the census counts them so;
    else held;
  absent (A11-absent.jsonl): a reject is the transition (in words where the reason names the mechanism); a
    particular is other; an accept with kind none is a limit.
Every class is checked against the decision and kind written in the rulings files. A room is counted in each class
its lines show, then once by priority: transition, template first, across threads, one post, talk only, layout only,
one end, held, el, other, limit.

  python3 out/_analysis/d3_a11_census.py
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
for f in ("A11-inst.jsonl", "A11-restrict.jsonl", "A11-adds.jsonl", "A11-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
print("lines ruled in A11's files:", len(ruled))

SPEC = ("accept", "specification")
EXPECT = {"T": SPEC, "TO": SPEC, "TF": ("reject", None), "E1": ("reject", None), "P-G6": ("particular", None),
          "S-T": SPEC, "S-TO": SPEC, "S-TF": SPEC, "S-X": SPEC, "S-TALK": SPEC, "S-LAY": SPEC,
          "ONE": ("accept", "none"), "EL": ("accept", "none")}
CLASS = {"T": "transition", "TO": "transition", "TF": "templatefirst", "E1": "oneend", "P-G6": "other",
         "S-T": "transition", "S-TO": "transition", "S-TF": "templatefirst", "S-X": "across", "S-TALK": "talkonly",
         "S-LAY": "layoutonly", "ONE": "onepost", "EL": "el"}
line_class, words = {}, set()
for name in ("A11-inst-spec.txt", "A11-restrict-spec.txt"):
    for i, c in spec(name).items():
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d, (i, c, ruled[i]["decision"])
        if k:
            assert ruled[i].get("kind") == k, (i, c, ruled[i].get("kind"))
        line_class[i] = CLASS[c]
        if c in ("T", "S-T"):
            words.add(i)
for r in load("A11-adds.jsonl"):
    i = r["adaptation"]
    assert r["decision"] == "accept" and r.get("kind") == "specification", i
    if "counted in the census as the transition" in r["reason"]:
        line_class[i] = "transition"
        words.add(i)
    elif "counted in the census as template first" in r["reason"]:
        line_class[i] = "templatefirst"
    else:
        line_class[i] = "held"
for r in load("A11-absent.jsonl"):
    i = r["adaptation"]
    if r["decision"] == "reject":
        line_class[i] = "transition"
        if "mechanism in the members' words" in r["reason"]:
            words.add(i)
    elif r["decision"] == "particular":
        line_class[i] = "other"
    else:
        assert r["decision"] == "accept" and r.get("kind") == "none", i
        line_class[i] = "limit"
assert set(line_class) == set(ruled), set(ruled) ^ set(line_class)

print("lines by class:", dict(Counter(line_class.values())))
print("lines showing the mechanism in words:", len(words))
by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A11 line:", len(by_room))
PRI = ("transition", "templatefirst", "across", "onepost", "talkonly", "layoutonly", "oneend", "held", "el", "other",
       "limit")
for c in PRI:
    print("  rooms showing %-13s %d" % (c, sum(1 for s in by_room.values() if c in s)))
first = Counter(next(c for c in PRI if c in s) for s in by_room.values())
print("rooms once, by priority:", {c: first[c] for c in PRI})
trans = {r for r, s in by_room.items() if "transition" in s}
tf = {r for r, s in by_room.items() if "templatefirst" in s} - trans
across = {r for r, s in by_room.items() if "across" in s} - trans - tf
both = trans | tf | across
print("rooms whose lines show both ends: %d (transition %d, template first %d, across threads %d)" % (
    len(both), len(trans), len(tf), len(across)))
print("  the transition shows in %d of %d (%.3f)" % (len(trans), len(both), len(trans) / len(both)))
both_tf = {r for r, s in by_room.items() if {"transition", "templatefirst"} <= s}
print("  rooms showing both the transition and template first: %d" % len(both_tf))
one = {r for r, s in by_room.items() if "onepost" in s} - both
print("rooms with one post holding both ends and no other episode: %d" % len(one))
print("  with them in the denominator, the transition shows in %d of %d (%.3f)" % (
    len(trans), len(both | one), len(trans) / len(both | one)))
named = {room(i) for i in words} & trans
print("transition rooms whose lines show the mechanism in words: %d (%.3f of the transition rooms)" % (
    len(named), len(named) / len(trans)))
talk = {r for r, s in by_room.items() if "talkonly" in s} - both - one
lay = {r for r, s in by_room.items() if "layoutonly" in s} - both - one - talk
print("rooms showing only the failure clause's cases: talk only %d, layout only %d" % (len(talk), len(lay)))
print("C2's grounding: 82 transitions in 36 rooms; room-level order 111 of 185 (0.600; null mean 0.618, p95 0.670)")
