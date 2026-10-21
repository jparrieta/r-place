#!/usr/bin/env python3
"""A20's order test (D3a-47, G52): the census of the rulings by line and by room, with the rules logged before this
script was written. Each line takes its latest ruling (the instantiate, restrict, add-condition and absent files, then
A20-rerule). Classes come from the current spec files and are checked against that latest decision and kind; absent
rejects are order lines, graded by their own words. Tags (MW, NF, R, AC, VC, RM, PO) come from the current tag files,
and every order line must carry exactly one of MW and NF. Prints counts only. Writes nothing.

  python3 out/_analysis/d3_a20_census.py
"""
import json
import re
from collections import Counter

R = "out/_analysis/d3_rulings/"


def load(name):
    return [json.loads(l) for l in open(R + name, encoding="utf-8") if l.strip()]


def spec(name):
    out = {}
    for l in open(R + name, encoding="utf-8"):
        if l.strip():
            p = l.rstrip("\n").split("|", 2)
            assert p[0] not in out, (name, p[0])
            out[p[0]] = p[1]
    return out


def room(aid):
    return aid.rsplit("-", 1)[0]


ruled = {}
for f in ("A20-inst.jsonl", "A20-restrict.jsonl", "A20-addcond.jsonl", "A20-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
first_count = len(ruled)
reruled = []
for r in load("A20-rerule.jsonl"):
    assert r["adaptation"] in ruled, r["adaptation"]
    ruled[r["adaptation"]] = r
    reruled.append(r["adaptation"])
print("lines ruled in A20's files: %d; re-ruled by a later line: %d (%s)" % (first_count, len(reruled),
                                                                          " ".join(reruled)))

SPEC, NONE, REJ, PART = ("accept", "specification"), ("accept", "none"), ("reject", None), ("particular", None)
EXPECT = {"O-A": SPEC, "O-H": SPEC, "BOUND": REJ, "J": REJ, "NC": REJ, "NL": REJ, "ONE": REJ, "AFTER": REJ,
          "P-G6": PART, "S-O-A": SPEC, "S-O-H": SPEC, "S-BOUND": SPEC, "EL-J": NONE, "EL-NC": NONE, "EL-NL": NONE,
          "EL-ONE": NONE, "EL-AFTER": NONE}
CLASS = {"BOUND": "bound", "J": "oneact", "NC": "nc", "NL": "nl", "ONE": "one", "AFTER": "after", "P-G6": "other"}


def cls_of(c):
    if c.startswith("S-"):
        c = c[2:]
    elif c.startswith("EL-"):
        c = c[3:]
    if c in ("O-A", "O-H"):
        return "order", c[2]
    return CLASS[c], None


line_class, kind, source = {}, {}, {}
for name, src in (("A20-inst-spec-v2.txt", "instantiate"), ("A20-restrict-spec.txt", "restrict"),
                  ("A20-addcond-spec.txt", "add-condition")):
    for i, c in spec(name).items():
        assert i not in line_class, i
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d and (k is None or ruled[i].get("kind") == k), (i, c, ruled[i]["decision"])
        line_class[i], kind[i] = cls_of(c)
        source[i] = src
absent_text = {}
for l in open(R + "A20-absent-rows.txt", encoding="utf-8"):
    if l.strip():
        aid, _, ev = l.rstrip("\n").split("|", 2)
        absent_text[aid] = ev
ungraded = []
# Two rejects whose words the patterns miss, graded by reading their rows: 4chan-059 ('then the host sub's line, in
# the chain') and completeanarchy-039 (the call and the canvas-sub proposal in other threads, so by the hours).
BY_READING = {"4chan-059": "A", "completeanarchy-039": "H"}
for r in load("A20-absent.jsonl"):
    i = r["adaptation"]
    r = ruled[i]
    source[i] = "absent"
    if r["decision"] == "reject":
        ev = absent_text[i]
        if i in BY_READING:
            k = BY_READING[i]
        elif re.search(r"then the line, in the (chain|thread)", ev):
            k = "A"
        elif "then the line, by the hours" in ev or "words name" in ev:
            k = "H"
        else:
            k = "ungraded"
            ungraded.append(i)
        line_class[i], kind[i] = "order", k
    elif r["decision"] == "particular":
        line_class[i] = "other"
    else:
        assert r["decision"] == "accept" and r.get("kind") == "none", i
        line_class[i] = "limit"
assert set(line_class) == set(ruled), set(ruled) ^ set(line_class)
print("lines by source:", dict(sorted(Counter(source.values()).items())))
for s in ("instantiate", "restrict", "add-condition", "absent"):
    print("  %s by class: %s" % (s, dict(sorted(Counter(line_class[i] for i in line_class if source[i] == s).items()))))
print("absent rejects the script cannot grade by their words: %d (%s)" % (len(ungraded), " ".join(ungraded)))

tags = {}
for f in ("A20-tags-inst-v2.txt", "A20-tags-restrict.txt", "A20-tags-add.txt", "A20-tags-absent.txt"):
    for l in open(R + f, encoding="utf-8"):
        if l.strip():
            i, t = l.strip().split("|")
            assert i in ruled and i not in tags, (f, i)
            tags[i] = set(t.split(","))
for i, t in sorted(tags.items()):
    if "PO" in t:
        assert line_class[i] == "other", i
        line_class[i], kind[i] = "order", "PO"
        print("particular counted with the order (PO):", i)

print("lines by class:", dict(sorted(Counter(line_class.values()).items())))
order_lines = [i for i, c in line_class.items() if c == "order"]
print("order lines: %d; by kind (A in the chain or thread, H by the hours or a post's words, PO particulars, "
      "ungraded): %s" % (len(order_lines), dict(sorted(Counter(kind[i] for i in order_lines).items()))))
print("  order lines by source:", dict(sorted(Counter(source[i] for i in order_lines).items())))
for i in order_lines:
    got = tags.get(i, set()) & {"MW", "NF"}
    assert len(got) == 1, (i, tags.get(i))
mech = {i: next(iter(tags[i] & {"MW", "NF"})) for i in order_lines}
print("order lines whose first line answers canvas posts (MW) or no flood (NF): %s" % dict(Counter(mech.values())))
for s in ("instantiate", "restrict", "add-condition", "absent"):
    print("  %s: %s" % (s, dict(Counter(mech[i] for i in order_lines if source[i] == s))))
for m in ("MW", "NF", "R", "AC", "VC", "RM", "PO"):
    hit = [i for i in tags if m in tags[i]]
    print("%s: %d lines (%s); rooms %d" % (m, len(hit), dict(sorted(Counter(line_class[i] for i in hit).items())),
                                        len({room(i) for i in hit})))

by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A20 line:", len(by_room))
PRI = ("order", "bound", "oneact", "nc", "nl", "one", "after", "other", "limit")
for c in PRI:
    print("  rooms showing %-8s %d" % (c, sum(1 for s in by_room.values() if c in s)))
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
room_mech = {}
for i in order_lines:
    room_mech.setdefault(room(i), set()).add(mech[i])
mw_rooms = {r for r, s in room_mech.items() if "MW" in s}
nf_only = {r for r, s in room_mech.items() if s == {"NF"}}
print("order rooms with an MW order line: %d; with NF order lines only: %d (%.3f of the order rooms)" % (
    len(mw_rooms), len(nf_only), len(nf_only) / len(order)))
ac_rooms = {room(i) for i in order_lines if "AC" in tags.get(i, ())}
before = {room(i) for i in order_lines if "AC" not in tags.get(i, ())}
print("order rooms with an AC line: %d; order rooms with an order line before hour 73: %d; before hour 73 the order "
      "holds in %d of %d episode rooms (%.3f)" % (len(ac_rooms), len(before), len(before),
                                                 len(before | (bound - order)),
                                                 len(before) / len(before | (bound - order))))
vc_rooms = {room(i) for i in order_lines if "VC" in tags.get(i, ())}
print("order rooms whose first call is a visitor's (VC): %d (%s)" % (len(vc_rooms), " ".join(sorted(vc_rooms))))
thread_rooms = {room(i) for i in order_lines if kind[i] == "A"}
hours_only = {room(i) for i in order_lines if kind[i] in ("H", "PO")} - thread_rooms
rest = order - thread_rooms - hours_only
print("order rooms in the chain or thread: %d; by the hours or a post's words only: %d; other: %d (%s)" % (
    len(thread_rooms), len(hours_only), len(rest), " ".join(sorted(rest))))
for label, rooms in (("support-transition rooms", ("nintendo", "rocketleague", "france")),
                     ("C2's sampled rooms", ("transformers", "darksouls", "crusaderkings", "rotmg"))):
    print("%s: %s" % (label, "; ".join("%s %s" % (r, sorted(by_room.get(r, ("no line",)))) for r in rooms)))
print("Beside: C2 counted the order in 132 of 155 rooms carrying both (0.852; null mean 0.538, p95 0.594); pass 4 "
      "found 5 of 155 with no line after the first call; before hour 73, the calls come before the whole line in 122 "
      "of 144; the counterexample response counts 23 of 155 rooms that draw the line first")
