#!/usr/bin/env python3
"""A19's order test (D3a-46, G51): the census of the rulings by line and by room, with the rules logged before this
script was written. Each line takes its latest ruling (the instantiate, restrict, add-condition and absent files, then
A19-rerule, -2 and -3). Classes come from the current spec files and are checked against that latest decision and
kind. Tags (ALLY, CHAT, HUB, TALLY, JOINT, MW, R, ENTRY, TH, PO) come from the current tag files. Prints counts only.
Writes nothing.

  python3 out/_analysis/d3_a19_census.py
"""
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
            assert p[0] not in out, (name, p[0])
            out[p[0]] = p[1]
    return out


def room(aid):
    return aid.rsplit("-", 1)[0]


ruled = {}
for f in ("A19-inst.jsonl", "A19-restrict.jsonl", "A19-addcond.jsonl", "A19-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
first_count = len(ruled)
reruled = []
for f in ("A19-rerule.jsonl", "A19-rerule-2.jsonl", "A19-rerule-3.jsonl"):
    for r in load(f):
        assert r["adaptation"] in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
        reruled.append(r["adaptation"])
print("lines ruled in A19's files: %d; re-ruled by a later line: %d (%s)" % (first_count, len(reruled),
                                                                          " ".join(reruled)))

SPEC, NONE, REJ, PART = ("accept", "specification"), ("accept", "none"), ("reject", None), ("particular", None)
EXPECT = {"O-A": SPEC, "O-H": SPEC, "BOUND": REJ, "J": REJ, "HOST": REJ, "NC": REJ, "NU": REJ, "ONE": REJ,
          "AFTER": REJ, "P-G6": PART, "S-O-A": SPEC, "S-O-H": SPEC, "S-BOUND": SPEC, "EL-J": NONE, "EL-HOST": NONE,
          "EL-NC": NONE, "EL-NU": NONE, "EL-ONE": NONE, "EL-AFTER": NONE}
CLASS = {"BOUND": "bound", "J": "oneact", "HOST": "host", "NC": "nc", "NU": "nu", "ONE": "one", "AFTER": "after",
         "P-G6": "other"}


def cls_of(c):
    if c.startswith("S-"):
        c = c[2:]
    elif c.startswith("EL-"):
        c = c[3:]
    if c in ("O-A", "O-H"):
        return "order", c[2]
    return CLASS[c], None


line_class, kind, source, raw = {}, {}, {}, {}
for name, src in (("A19-inst-spec.txt", "instantiate"), ("A19-restrict-spec-v4.txt", "restrict"),
                  ("A19-addcond-spec-v2.txt", "add-condition")):
    for i, c in spec(name).items():
        assert i not in line_class, i
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d and (k is None or ruled[i].get("kind") == k), (i, c, ruled[i]["decision"])
        line_class[i], kind[i] = cls_of(c)
        source[i], raw[i] = src, c
for r in load("A19-absent.jsonl"):
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
print("lines by source:", dict(sorted(Counter(source.values()).items())))
for s in ("instantiate", "restrict", "add-condition", "absent"):
    print("  %s by class: %s" % (s, dict(sorted(Counter(line_class[i] for i in line_class if source[i] == s).items()))))

tags = {}
for f in ("A19-tags-inst.txt", "A19-tags-restrict-v4.txt", "A19-tags-add-v2.txt"):
    for l in open(R + f, encoding="utf-8"):
        if l.strip():
            i, t = l.strip().split("|")
            assert i in ruled and i not in tags, (f, i)
            tags[i] = set(t.split(","))
for f in ("A19-rerule-tags-2.txt", "A19-rerule-tags-3.txt"):
    for l in open(R + f, encoding="utf-8"):
        if l.strip():
            i, t = l.strip().split("|")
            assert set(t.split(",")) <= tags.get(i, set()), (f, i)
for i, t in sorted(tags.items()):
    if "PO" in t:
        assert line_class[i] == "other", i
        line_class[i], kind[i] = "order", "PO"
        print("particular counted with the order (PO):", i)

print("lines by class:", dict(sorted(Counter(line_class.values()).items())))
order_lines = [i for i, c in line_class.items() if c == "order"]
print("order lines: %d; by kind (A in the thread, H by the hours or a post's words, ungraded absent rejects, PO "
      "particulars): %s" % (len(order_lines), dict(sorted(Counter(kind[i] for i in order_lines).items()))))
print("  order lines by source:", dict(sorted(Counter(source[i] for i in order_lines).items())))

FORMS = ("ALLY", "CHAT", "HUB", "TALLY", "JOINT")
graded = [i for i in order_lines if kind[i] in ("A", "H")]


def pick(i):
    got = [o for o in FORMS if o in tags.get(i, ())]
    assert len(got) == 1, (i, tags.get(i))
    return got[0]


forms = Counter(pick(i) for i in graded)
print("graded order lines (A and H): %d; first coalition form %s" % (len(graded), dict(forms)))
for k in ("A", "H"):
    sub = [i for i in graded if kind[i] == k]
    print("  %s lines %d: forms %s" % (k, len(sub), dict(Counter(pick(i) for i in sub))))
for c in sorted(set(line_class.values()) - {"order"}):
    f = Counter(o for i in line_class if line_class[i] == c for o in FORMS if o in tags.get(i, ()))
    if f:
        print("  forms tagged on %s lines: %s" % (c, dict(f)))
for m in ("MW", "R", "ENTRY", "TH"):
    hit = [i for i in tags if m in tags[i]]
    print("%s: %d lines (%s); rooms %d" % (m, len(hit), dict(sorted(Counter(line_class[i] for i in hit).items())),
                                        len({room(i) for i in hit})))
print("  MW among graded order lines: %d of %d" % (sum(1 for i in graded if "MW" in tags[i]), len(graded)))

by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A19 line:", len(by_room))
PRI = ("order", "bound", "oneact", "host", "nc", "nu", "one", "after", "other", "absentspec", "limit")
for c in PRI:
    print("  rooms showing %-10s %d" % (c, sum(1 for s in by_room.values() if c in s)))
first = Counter(next(c for c in PRI if c in s) for s in by_room.values())
print("rooms once, by priority:", {c: first[c] for c in PRI})
order = {r for r, s in by_room.items() if "order" in s}
bound = {r for r, s in by_room.items() if "bound" in s}
episode = order | bound
print("rooms with an episode (the order or the bound): %d; the order in %d (%.3f); the bound only in %d (%.3f)" % (
    len(episode), len(order), len(order) / len(episode), len(episode - order), len(episode - order) / len(episode)))
print("  rooms showing both the order and the bound: %d: %s" % (len(order & bound), " ".join(sorted(order & bound))))
entry_rooms = {room(i) for i in tags if "ENTRY" in tags[i]}
print("  bound-only rooms: %s" % " ".join("%s%s" % (r, " (ENTRY)" if r in entry_rooms else "")
                                          for r in sorted(episode - order)))
oneact_only = {r for r, s in by_room.items() if "oneact" in s and not s & {"order", "bound"}}
print("  one-act rooms with neither the order nor the bound: %d; with them in the denominator, the order holds in %d "
      "of %d (%.3f)" % (len(oneact_only), len(order), len(episode | oneact_only),
                        len(order) / len(episode | oneact_only)))
host_only = {r for r, s in by_room.items() if "host" in s and not s & {"order", "bound", "oneact"}}
print("rooms whose only second end shown is hosting (no order, bound or one act): %d: %s" % (
    len(host_only), " ".join(sorted(host_only))))
th_rooms = {room(i) for i in tags if "TH" in tags[i]}
print("TH rooms (a coalition answering a warning, no upkeep before it): %d; of them with the order elsewhere: %d" % (
    len(th_rooms), len(th_rooms & order)))
print("ENTRY rooms: %d; of them bound-only %d, with the order %d" % (
    len(entry_rooms), len(entry_rooms & (bound - order)), len(entry_rooms & order)))
thread_rooms = {room(i) for i in graded if kind[i] == "A"}
hours_only = {room(i) for i in graded if kind[i] == "H"} - thread_rooms
absent_only = {room(i) for i in order_lines if kind[i] == "ungraded"} - thread_rooms - hours_only
print("order rooms in the thread or chain: %d; by the hours or a post's words only: %d; by an ungraded absent "
      "reject only: %d" % (len(thread_rooms), len(hours_only), len(absent_only)))
for label, rooms in (("support-transition rooms", ("criticalrole", "naruto", "yugioh")),
                     ("the two sampled rooms that failed at C2", ("lakers", "bretagne")),
                     ("the bound's named late rooms", ("bretagne", "MiamiHurricanes", "yuyuyu"))):
    print("%s: %s" % (label, "; ".join("%s %s" % (r, sorted(by_room.get(r, ("no line",)))) for r in rooms)))
print("Beside: pass 4 counted the order in 87 of 121 rooms carrying both (0.719; null mean 0.614, p95 0.678) and "
      "found 7 of 121 with no coalition after the first upkeep; the counterexample response counts 51 of 157 rooms "
      "that join a coalition before any upkeep (0.325)")
