#!/usr/bin/env python3
"""A17's order test (D3a-44, G49): the census of the rulings by line and by room, with the rules logged before this
script was written. Classes come from the spec files (instantiate, restrict, add-condition, add-step) and the absent
rulings; each class is checked against the decision and kind written in the rulings files. Tags (INV, DEAL, OTHER, PO,
R) come from the A17-tags files. Prints counts only. Writes nothing.

  python3 out/_analysis/d3_a17_census.py
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
for f in ("A17-inst.jsonl", "A17-restrict.jsonl", "A17-addcond.jsonl", "A17-addstep.jsonl", "A17-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
print("lines ruled in A17's files:", len(ruled))

SPEC, NONE, REJ, PART = ("accept", "specification"), ("accept", "none"), ("reject", None), ("particular", None)
EXPECT = {"O-A": SPEC, "O-H": SPEC, "BOUND": REJ, "J": REJ, "NA": REJ, "V": REJ, "NT": REJ, "ONE": REJ, "AFTER": REJ,
          "P-G6": PART, "S-O-A": SPEC, "S-O-H": SPEC, "S-BOUND": SPEC, "EL-NA": NONE, "EL-NT": NONE, "EL-ONE": NONE,
          "EL-AFTER": NONE, "EL-J": NONE}
CLASS = {"BOUND": "bound", "J": "oneact", "NA": "notattack", "V": "visitor", "NT": "notterms", "ONE": "one",
         "AFTER": "after", "P-G6": "other"}


def cls_of(c):
    if c.startswith("S-"):
        c = c[2:]
    elif c.startswith("EL-"):
        c = c[3:]
    if c in ("O-A", "O-H"):
        return "order", c[2]
    return CLASS[c], None


line_class, kind, source = {}, {}, {}
for name, src in (("A17-inst-spec.txt", "instantiate"), ("A17-restrict-spec.txt", "restrict"),
                  ("A17-addcond-spec.txt", "add-condition"), ("A17-addstep-spec.txt", "add-step")):
    for i, c in spec(name).items():
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d and (k is None or ruled[i].get("kind") == k), (i, c)
        line_class[i], kind[i] = cls_of(c)
        source[i] = src
for r in load("A17-absent.jsonl"):
    i = r["adaptation"]
    source[i] = "absent"
    if r["decision"] == "reject":
        line_class[i], kind[i] = "order", "ungraded"
    elif r["decision"] == "particular":
        line_class[i] = "other"
    elif r.get("kind") == "specification":
        line_class[i] = "absentspec"
    else:
        assert r["decision"] == "accept" and r.get("kind") == "none", i
        line_class[i] = "limit"
assert set(line_class) == set(ruled), set(ruled) ^ set(line_class)

tags = {}
for f in sorted(glob.glob(R + "A17-tags-*.txt")):
    if f.endswith(("-inst.txt", "-restrict.txt")):
        continue
    for l in open(f, encoding="utf-8"):
        if l.strip():
            i, t = l.strip().split("|")
            assert i in ruled, (f, i)
            tags.setdefault(i, set()).update(t.split(","))
for i, t in sorted(tags.items()):
    if "PO" in t:
        assert line_class[i] == "other", i
        line_class[i], kind[i] = "order", "PO"
        print("particular counted with the order (PO):", i)
po_absent = [i for i in ruled if source[i] == "absent" and ruled[i]["decision"] == "particular"
             and "counts it apart, marked PO" in ruled[i].get("reason", "")]
for i in po_absent:
    line_class[i], kind[i] = "order", "PO"
    print("absent particular counted with the order (PO):", i)

print("lines by class:", dict(sorted(Counter(line_class.values()).items())))
order_lines = [i for i, c in line_class.items() if c == "order"]
print("order lines: %d; by kind (A answered in the thread, H by the hours or a post's words, ungraded absent "
      "rejects, PO particulars): %s" % (len(order_lines), dict(sorted(Counter(kind[i] for i in order_lines).items()))))
print("  order lines by source:", dict(sorted(Counter(source[i] for i in order_lines).items())))
print("  lines whose first end or first talk is a coded post above the concepts (R): %d, of which order lines %d" % (
    sum(1 for i in ruled if "R" in tags.get(i, ())), sum(1 for i in order_lines if "R" in tags.get(i, ()))))


def form(i):
    t = tags.get(i, ())
    return next((f for f in ("INV", "DEAL", "OTHER") if f in t), None)


thread = [i for i in order_lines if kind[i] == "A" or (kind[i] == "PO" and form(i))]
forms = Counter(form(i) or "unmarked" for i in thread)
print("  order lines answered in the thread (with PO lines that carry a form): %d; first answer INV %d, DEAL %d, "
      "OTHER %d, unmarked %d" % (len(thread), forms["INV"], forms["DEAL"], forms["OTHER"], forms["unmarked"]))

by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A17 line:", len(by_room))
PRI = ("order", "bound", "oneact", "visitor", "notattack", "notterms", "one", "after", "other", "absentspec", "limit")
for c in PRI:
    print("  rooms showing %-12s %d" % (c, sum(1 for s in by_room.values() if c in s)))
first = Counter(next(c for c in PRI if c in s) for s in by_room.values())
print("rooms once, by priority:", {c: first[c] for c in PRI})
order = {r for r, s in by_room.items() if "order" in s}
bound = {r for r, s in by_room.items() if "bound" in s}
episode = order | bound
print("rooms with an episode (the order or the bound): %d; the order in %d (%.3f); the bound only in %d (%.3f)" % (
    len(episode), len(order), len(order) / len(episode), len(episode - order), len(episode - order) / len(episode)))
print("  rooms showing both the order and the bound: %d: %s" % (len(order & bound), " ".join(sorted(order & bound))))
print("  bound-only rooms: %s" % " ".join(sorted(episode - order)))
oneact_only = {r for r, s in by_room.items() if "oneact" in s and not s & {"order", "bound"}}
print("  one-act rooms with neither the order nor the bound: %d; with them in the denominator, the order holds in %d "
      "of %d (%.3f)" % (len(oneact_only), len(order), len(episode | oneact_only),
                        len(order) / len(episode | oneact_only)))
visitor_rooms = {r for r, s in by_room.items() if "visitor" in s}
print("rooms with a visitor's call answered by terms: %d, of which order rooms %d" % (len(visitor_rooms),
                                                                                     len(visitor_rooms & order)))
room_form = {}
for i in thread:
    f = form(i)
    if f:
        room_form.setdefault(room(i), set()).add(f)
print("order rooms with a marked in-thread answer: %d; INV only %d, DEAL only %d, OTHER only %d, more than one form %d"
      % (len(room_form), sum(1 for s in room_form.values() if s == {"INV"}),
         sum(1 for s in room_form.values() if s == {"DEAL"}), sum(1 for s in room_form.values() if s == {"OTHER"}),
         sum(1 for s in room_form.values() if len(s) > 1)))
thread_rooms = {room(i) for i in thread}
hours_only = {room(i) for i in order_lines if kind[i] == "H"} - thread_rooms
absent_only = {room(i) for i in order_lines if kind[i] == "ungraded"} - thread_rooms - {
    room(i) for i in order_lines if kind[i] == "H"}
print("order rooms with an in-thread answer: %d; by the hours or a post's words only: %d; by an ungraded absent "
      "reject only: %d" % (len(thread_rooms & order), len(hours_only), len(absent_only)))
for label, rooms in (("support-transition rooms", ("czech", "PlaceNL", "thailand")),
                     ("the counterexample response's room", ("strangerthings",))):
    print("%s: %s" % (label, "; ".join("%s %s" % (r, sorted(by_room.get(r, ()))) for r in rooms)))
print("Beside: C2 counted the order in 95 of 172 rooms carrying both (0.552; null mean 0.423, p95 0.477), from 73 "
      "transitions in 35 rooms; the counterexample response counts 77 of 172 that talk borders before any attack call")
