#!/usr/bin/env python3
"""A18's order test (D3a-45, G50): the census of the rulings by line and by room, with the rules logged before this
script was written. Classes come from the spec files (instantiate, restrict, add-condition) and the absent rulings;
each class is checked against the decision and kind written in the rulings files. Tags (TAUNT, VICT, SALUTE, FLOOD,
BLAME, SAME, ELSE, AC, R, PO, PRE) come from the A18-tags files. Prints counts only. Writes nothing.

  python3 out/_analysis/d3_a18_census.py
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
for f in ("A18-inst.jsonl", "A18-restrict.jsonl", "A18-addcond.jsonl", "A18-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
print("lines ruled in A18's files:", len(ruled))

SPEC, NONE, REJ, PART = ("accept", "specification"), ("accept", "none"), ("reject", None), ("particular", None)
EXPECT = {"O-A": SPEC, "O-H": SPEC, "BOUND": REJ, "J": REJ, "NA": REJ, "SUF": REJ, "V": REJ, "NT": REJ, "ONE": REJ,
          "AFTER": REJ, "P-G6": PART, "S-O-A": SPEC, "S-O-H": SPEC, "S-BOUND": SPEC, "EL-NA": NONE, "EL-SUF": NONE,
          "EL-NT": NONE, "EL-ONE": NONE, "EL-AFTER": NONE, "EL-J": NONE, "EL-V": NONE}
CLASS = {"BOUND": "bound", "J": "oneact", "NA": "notattack", "SUF": "suffered", "V": "visitor", "NT": "nottaunt",
         "ONE": "one", "AFTER": "after", "P-G6": "other"}


def cls_of(c):
    if c.startswith("S-"):
        c = c[2:]
    elif c.startswith("EL-"):
        c = c[3:]
    if c in ("O-A", "O-H"):
        return "order", c[2]
    return CLASS[c], None


line_class, kind, source = {}, {}, {}
for name, src in (("A18-inst-spec.txt", "instantiate"), ("A18-restrict-spec.txt", "restrict"),
                  ("A18-addcond-spec.txt", "add-condition")):
    for i, c in spec(name).items():
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d and (k is None or ruled[i].get("kind") == k), (i, c)
        line_class[i], kind[i] = cls_of(c)
        source[i] = src
for r in load("A18-absent.jsonl"):
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
for f in sorted(glob.glob(R + "A18-tags-*.txt")):
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
    if "PRE" in t:
        assert line_class[i] == "bound", i
    if t & {"TAUNT", "VICT", "SALUTE", "FLOOD", "BLAME", "SAME", "ELSE", "AC"}:
        assert line_class[i] == "order", i
po_absent = [i for i in ruled if source[i] == "absent" and ruled[i]["decision"] == "particular"
             and "counts the line apart, marked PO" in ruled[i].get("reason", "")]
for i in po_absent:
    line_class[i], kind[i] = "order", "PO"
    print("absent particular counted with the order (PO):", i)

print("lines by class:", dict(sorted(Counter(line_class.values()).items())))
order_lines = [i for i, c in line_class.items() if c == "order"]
print("order lines: %d; by kind (A answered in the thread, H by the hours or a post's words, ungraded absent "
      "rejects, PO particulars): %s" % (len(order_lines), dict(sorted(Counter(kind[i] for i in order_lines).items()))))
print("  order lines by source:", dict(sorted(Counter(source[i] for i in order_lines).items())))
print("  lines whose first end is a coded post above the concepts (R): %d, of which order lines %d" % (
    sum(1 for i in ruled if "R" in tags.get(i, ())), sum(1 for i in order_lines if "R" in tags.get(i, ()))))

graded = [i for i in order_lines if kind[i] in ("A", "H")]
assert all(tags.get(i) for i in graded), [i for i in graded if not tags.get(i)]


def pick(i, opts):
    t = tags.get(i, ())
    got = [o for o in opts if o in t]
    assert len(got) == 1, (i, t)
    return got[0]


FORMS = ("TAUNT", "VICT", "SALUTE", "FLOOD", "BLAME")
forms = Counter(pick(i, FORMS) for i in graded)
rival = Counter(pick(i, ("SAME", "ELSE")) for i in graded)
ac = sum(1 for i in graded if "AC" in tags[i])
print("graded order lines (A and H): %d; forms %s; rival %s; first taunt after the close (AC) %d" % (
    len(graded), dict(forms), dict(rival), ac))
for k in ("A", "H"):
    sub = [i for i in graded if kind[i] == k]
    print("  %s lines %d: forms %s; rival %s; AC %d" % (
        k, len(sub), dict(Counter(pick(i, FORMS) for i in sub)), dict(Counter(pick(i, ("SAME", "ELSE")) for i in sub)),
        sum(1 for i in sub if "AC" in tags[i])))

by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A18 line:", len(by_room))
PRI = ("order", "bound", "oneact", "visitor", "suffered", "notattack", "nottaunt", "one", "after", "other",
       "absentspec", "limit")
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
pre_rooms = {room(i) for i, t in tags.items() if "PRE" in t}
print("  bound-only rooms: %s" % " ".join("%s%s" % (r, " (PRE)" if r in pre_rooms else "")
                                          for r in sorted(episode - order)))
oneact_only = {r for r, s in by_room.items() if "oneact" in s and not s & {"order", "bound"}}
print("  one-act rooms with neither the order nor the bound: %d; with them in the denominator, the order holds in %d "
      "of %d (%.3f)" % (len(oneact_only), len(order), len(episode | oneact_only),
                        len(order) / len(episode | oneact_only)))
suf_only = {r for r, s in by_room.items() if "suffered" in s and not s & {"order", "bound"}}
print("rooms with a taunt after an attack the room suffers and neither the order nor the bound: %d" % len(suf_only))
visitor_rooms = {r for r, s in by_room.items() if "visitor" in s}
print("rooms with a visitor's call answered by taunts: %d" % len(visitor_rooms))
room_rival = {}
room_form = {}
for i in graded:
    room_rival.setdefault(room(i), set()).add(pick(i, ("SAME", "ELSE")))
    room_form.setdefault(room(i), set()).add(pick(i, FORMS))
print("graded order rooms: %d; SAME only %d, ELSE only %d, both %d" % (
    len(room_rival), sum(1 for s in room_rival.values() if s == {"SAME"}),
    sum(1 for s in room_rival.values() if s == {"ELSE"}), sum(1 for s in room_rival.values() if len(s) > 1)))
print("graded order rooms by form (rooms with each form): %s" % dict(Counter(f for s in room_form.values() for f in s)))
thread_rooms = {room(i) for i in graded if kind[i] == "A"}
hours_only = {room(i) for i in graded if kind[i] == "H"} - thread_rooms
absent_only = {room(i) for i in order_lines if kind[i] == "ungraded"} - thread_rooms - hours_only
po_only = {room(i) for i in order_lines if kind[i] == "PO"} - thread_rooms - hours_only - absent_only
print("order rooms with an in-thread answer: %d; by the hours or a post's words only: %d; by an ungraded absent "
      "reject only: %d; by a PO particular only: %d" % (len(thread_rooms), len(hours_only), len(absent_only),
                                                       len(po_only)))
for label, rooms in (("support-transition rooms", ("rpi", "anarcho_capitalism", "clg")),
                     ("C2's sampled rooms", ("reddevils", "nbaspurs", "cardinals", "portugal")),
                     ("A18's subs", ("unitedkingdom", "rpi", "anarcho_capitalism", "clg"))):
    print("%s: %s" % (label, "; ".join("%s %s" % (r, sorted(by_room.get(r, ()))) for r in rooms)))
print("Beside: C2 counted the order in 56 of 68 rooms carrying both (0.824; null mean 0.591, p95 0.676), from 50 "
      "transitions in 14 rooms; pass 4 found 2 of 68 rooms with no taunt after the first attack; the counterexample "
      "response counts 12 of 68 that taunt before any attack")
