#!/usr/bin/env python3
"""A15's order test (D3a-42, G47): the census of the rulings by line and by room, with the rules logged before this
script was written. Classes come from the spec files (instantiate, restrict, add-condition, add-step), the re-ruling
spec (which replaces the class of the two lines it re-rules) and the absent rulings; each class is checked against the
decision and kind written in the rulings files. Tags come from the A15-tags files. Prints counts only. Writes nothing.

  python3 out/_analysis/d3_a15_census.py
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
for f in ("A15-inst.jsonl", "A15-restrict.jsonl", "A15-addc.jsonl", "A15-adds.jsonl", "A15-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
for r in load("A15-rerule.jsonl"):
    assert r["adaptation"] in ruled, r["adaptation"]
    ruled[r["adaptation"]] = r
print("lines ruled in A15's files:", len(ruled), "(re-rulings applied: %d)" % len(load("A15-rerule.jsonl")))

SPEC, NONE, REJ, PART = ("accept", "specification"), ("accept", "none"), ("reject", None), ("particular", None)
EXPECT = {"O-C": SPEC, "O-A": SPEC, "O-E": SPEC, "M-C": SPEC, "M-A": SPEC, "M-E": SPEC, "BOUND": REJ, "J": REJ,
          "NC": REJ, "NA": REJ, "ONE": REJ, "AFTER": REJ, "P-G6": PART, "S-O-C": SPEC, "S-O-A": SPEC, "S-O-E": SPEC,
          "S-M-C": SPEC, "S-M-A": SPEC, "S-BOUND": SPEC, "S-HELD": SPEC, "EL-J": NONE, "EL-NC": NONE, "EL-NA": NONE,
          "EL-ONE": NONE, "EL-AFTER": NONE}
CLASS = {"BOUND": "bound", "J": "onecall", "NC": "notcall", "NA": "notattack", "ONE": "one", "AFTER": "after",
         "HELD": "held", "P-G6": "other"}


def cls_of(c):
    if c.startswith("S-"):
        c = c[2:]
    elif c.startswith("EL-"):
        c = c[3:]
    if c[:2] in ("O-", "M-"):
        return "order", c[2:], c[0] == "M"
    return CLASS[c], None, False


line_class, kind, words, source = {}, {}, set(), {}
specs = {}
for name, src in (("A15-inst-spec.txt", "instantiate"), ("A15-restrict-spec.txt", "restrict"),
                  ("A15-addc-spec.txt", "add-condition"), ("A15-adds-spec.txt", "add-step")):
    for i, c in spec(name).items():
        specs[i] = (c, src)
for i, c in spec("A15-rerule-spec.txt").items():
    specs[i] = (c, specs[i][1])
for i, (c, src) in specs.items():
    d, k = EXPECT[c]
    assert ruled[i]["decision"] == d and (k is None or ruled[i].get("kind") == k), (i, c)
    line_class[i], kind[i], w = cls_of(c)
    source[i] = src
    if w:
        words.add(i)
absent_spec = set()
for r in load("A15-absent.jsonl"):
    i = r["adaptation"]
    source[i] = "absent"
    if r["decision"] == "reject":
        line_class[i], kind[i] = "order", "ungraded"
    elif r["decision"] == "particular":
        line_class[i] = "other"
    elif r.get("kind") == "specification":
        line_class[i] = "absentspec"
        absent_spec.add(i)
    else:
        assert r["decision"] == "accept" and r.get("kind") == "none", i
        line_class[i] = "limit"
assert set(line_class) == set(ruled), set(ruled) ^ set(line_class)

tags = {}
for f in glob.glob(R + "A15-tags-*.txt"):
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

print("lines by class:", dict(sorted(Counter(line_class.values()).items())))
order_lines = [i for i, c in line_class.items() if c == "order"]
print("order lines: %d; named in words %d; by the hours, thread, reply chain or post's words %d; absent rejects %d" % (
    len(order_lines), len(words & set(order_lines)),
    sum(1 for i in order_lines if i not in words and kind.get(i) not in ("ungraded",)),
    sum(1 for i in order_lines if kind.get(i) == "ungraded")))
print("  order lines by source:", dict(sorted(Counter(source[i] for i in order_lines).items())))
print("  kind of the first attack among order lines:", dict(sorted(Counter(kind[i] for i in order_lines).items())))
print("  order lines naming the first call from the room's record (R): %d" % sum(
    1 for i in order_lines if "R" in tags.get(i, ())))
ac = {i for i, t in tags.items() if "AC" in t}
print("  lines marked AC (the attack after the room's own work was complete): %d, of which order lines %d; by class %s" % (
    len(ac), len(ac & set(order_lines)), dict(sorted(Counter(line_class[i] for i in ac).items()))))

by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add(c)
print("rooms with an A15 line:", len(by_room))
PRI = ("order", "bound", "onecall", "notcall", "notattack", "one", "after", "held", "other", "absentspec", "limit")
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
onecall_only = {r for r, s in by_room.items() if "onecall" in s and not s & {"order", "bound"}}
print("  with %d one-call rooms in the denominator, the order holds in %d of %d (%.3f)" % (
    len(onecall_only), len(order), len(episode | onecall_only), len(order) / len(episode | onecall_only)))
named = {room(i) for i in words if line_class[i] == "order"}
print("rooms where the order is named in words: %d (%.3f of the order rooms): %s" % (
    len(named), len(named) / len(order), " ".join(sorted(named))))
graded = [i for i in order_lines if kind[i] in ("C", "A", "E")]
first_kind = {}
for r in order:
    ks = [kind[i] for i in graded if room(i) == r]
    if ks:
        first_kind[r] = "E" if "E" in ks and not ({"C", "A"} & set(ks)) else ("A" if "A" in ks and "C" not in ks else "C")
print("order rooms with a graded line, by the kind their lines show (C if any call or plan, else A, else E): %s" % (
    dict(sorted(Counter(first_kind.values()).items()))))
ac_rooms = {room(i) for i in ac}
print("rooms with an AC mark: %d, of which order rooms %d" % (len(ac_rooms), len(ac_rooms & order)))
for label, rooms in (("bound's story rooms", ("edmontonoilers", "canucks", "anarcho_capitalism")),
                     ("support-transition rooms", ("Temple", "completeanarchy", "stlouis"))):
    print("%s: %s" % (label, "; ".join("%s %s" % (r, sorted(by_room.get(r, ()))) for r in rooms)))
print("Beside: C2 counted the order in 93 of 129 rooms carrying both (0.721; null mean 0.487, p95 0.55), and in 91 of "
      "129 (0.705) without joining, from 34 transitions in 19 rooms; the counterexample response counts 36 of 129 that "
      "call an attack before any call to place")
