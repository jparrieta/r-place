#!/usr/bin/env python3
"""D4a-05: explore the shared lines to find which definition of a room's 'selected changes' leaves 21 rooms
with none (the PI's message). Read-only; prints counts.

    python3 out/_analysis/d4a05_explore.py
"""
import collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import adaptation_ledger as al  # noqa: E402

L = al.shared_lines(OUT)
rooms = set(al.effective_rooms(OUT))
print("shared lines", len(L), "rooms with a return", len(rooms))
print("ops", collections.Counter(r.get("op") for r in L))
print("element first letters", collections.Counter((r.get("element") or "?")[0] for r in L))
CHANGE = {"add-step", "add-condition", "link", "restrict", "contradict", "propose"}
lift_ok = collections.Counter(bool(r.get("lift")) and len(r.get("lift") or []) >= 4 for r in L)
print("lines with a full lift", lift_ok)
print("lift shapes", collections.Counter(len(r.get("lift") or []) for r in L))
ex = [r for r in L if (r.get("element") or "").startswith("A")][:2]
for r in ex:
    print("arrow example", {k: r.get(k) for k in ("sub", "op", "element", "source", "lift", "kind")})


def T3(r):
    lf = r.get("lift") or []
    return next((x for x in lf if str(x).startswith("T3-")), None)


for label, pred in [
    ("change ops (incl propose)", lambda r: r.get("op") in CHANGE),
    ("change ops (no propose)", lambda r: r.get("op") in CHANGE - {"propose"}),
    ("change ops, element only", lambda r: r.get("op") in CHANGE - {"propose"} and not (r.get("element") or "").startswith("A")),
]:
    per = collections.Counter(r["sub"] for r in L if pred(r))
    none = sorted(s for s in rooms if per.get(s, 0) == 0)
    print(label, "rooms with none:", len(none))
    # with keys held by >= 2 rooms at T3 (op, element, T3)
    keyrooms = collections.defaultdict(set)
    for r in L:
        if pred(r) and T3(r):
            keyrooms[(r["op"], r["element"], T3(r))].add(r["sub"])
    for floor in (2, 5):
        per2 = collections.Counter()
        for k, ss in keyrooms.items():
            if len(ss) >= floor:
                for s in ss:
                    per2[s] += 1
        none2 = sorted(s for s in rooms if per2.get(s, 0) == 0)
        print("   with keys held by >=%d rooms: rooms with none %d" % (floor, len(none2)), none2[:30] if len(none2) <= 30 else "")
    # by T3 node alone (not op/element), held by >=2 rooms
    noderooms = collections.defaultdict(set)
    for r in L:
        if pred(r) and T3(r):
            noderooms[T3(r)].add(r["sub"])
    for floor in (2, 5):
        per3 = collections.Counter()
        for k, ss in noderooms.items():
            if len(ss) >= floor:
                for s in ss:
                    per3[s] += 1
        none3 = sorted(s for s in rooms if per3.get(s, 0) == 0)
        print("   T3 nodes held by >=%d rooms: rooms with none %d" % (floor, len(none3)), none3 if len(none3) <= 30 else "")
