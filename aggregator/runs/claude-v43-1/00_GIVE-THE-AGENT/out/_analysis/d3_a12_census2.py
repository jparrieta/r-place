#!/usr/bin/env python3
"""A12's test (D3a-39, G44), second run: d3_a12_census.py with the re-rulings of A12-rerule-spec.txt applied. A line
re-ruled there takes the class its re-ruling names (COND: a conditional or asking answer only), checked against the
decision written in A12-rerule.jsonl. Rules as logged before the first run. Prints counts only. Writes nothing.

  python3 out/_analysis/d3_a12_census2.py
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
            out[p[0]] = (p[1], p[2])
    return out


def room(aid):
    return aid.rsplit("-", 1)[0]


ruled = {}
for f in ("A12-inst.jsonl", "A12-restrict.jsonl", "A12-addc.jsonl", "A12-adds.jsonl", "A12-absent.jsonl"):
    for r in load(f):
        assert r["adaptation"] not in ruled, r["adaptation"]
        ruled[r["adaptation"]] = r
print("lines ruled in A12's files:", len(ruled))

SPEC, NONE, REJ = ("accept", "specification"), ("accept", "none"), ("reject", None)
EXPECT = {"T-B": SPEC, "T-R": SPEC, "T-O": SPEC, "PROP": REJ, "START": REJ, "UNC": REJ, "AFTER": REJ, "CALL": REJ,
          "REF": REJ, "PLEDGE": REJ, "S-B": SPEC, "S-R": SPEC, "S-O": SPEC, "S-COND": SPEC, "S-RB": SPEC, "S-RR": SPEC,
          "S-CALL": SPEC, "S-PROP": SPEC, "S-START": SPEC, "S-PLEDGE": SPEC, "EL": NONE}
CLASS = {"T-B": "pair-bare", "T-R": "pair-reason", "T-O": "pair-other", "PROP": "proposal", "START": "start",
         "UNC": "uncoded", "AFTER": "after", "CALL": "callonly", "REF": "refusal", "PLEDGE": "pledge",
         "S-B": "pair-bare", "S-R": "pair-reason", "S-O": "pair-other", "S-COND": "cond", "S-RB": "refusal-bare",
         "S-RR": "refusal", "S-CALL": "callonly", "S-PROP": "proposal", "S-START": "start", "S-PLEDGE": "pledge",
         "EL": "limit"}
line_class = {}
for name in ("A12-inst-spec.txt", "A12-restrict-spec.txt", "A12-addc-spec.txt", "A12-adds-spec.txt"):
    for i, (c, _) in spec(name).items():
        d, k = EXPECT[c]
        assert ruled[i]["decision"] == d and (k is None or ruled[i].get("kind") == k), (i, c)
        line_class[i] = CLASS[c]
rows = spec("A12-absent-rows.txt")
for r in load("A12-absent.jsonl"):
    i = r["adaptation"]
    if r["decision"] == "reject":
        ev = rows[i][1]
        line_class[i] = ("pair-bare" if "a bare join" in ev else
                         "pair-other" if "part done" in ev else "pair-join")
    elif r.get("kind") == "specification":
        line_class[i] = "refusal"
    else:
        assert r["decision"] == "accept" and r.get("kind") == "none", i
        line_class[i] = "limit"
assert set(line_class) == set(ruled), set(ruled) ^ set(line_class)

RERULE = {"COND": ("reject", "cond")}
rerule = {r["adaptation"]: r for r in load("A12-rerule.jsonl")}
re_spec = spec("A12-rerule-spec.txt")
assert set(rerule) == set(re_spec), set(rerule) ^ set(re_spec)
for i, (c, _) in re_spec.items():
    d, cls = RERULE[c]
    assert rerule[i]["decision"] == d and i in ruled, (i, c)
    print("re-ruled: %s, %s -> %s" % (i, line_class[i], cls))
    line_class[i] = cls

tags = {}
for f in glob.glob(R + "A12-tags-*.txt"):
    for l in open(f, encoding="utf-8"):
        if l.strip():
            i, t = l.strip().split("|")
            assert i in ruled, (f, i)
            tags.setdefault(i, set()).update(t.split(","))
print("lines by class:", dict(sorted(Counter(line_class.values()).items())))
PAIR = ("pair-bare", "pair-reason", "pair-other", "pair-join")
pair_lines = [i for i, c in line_class.items() if c in PAIR]
print("pair lines: %d (bare %d, with a reason %d, part done or thanks %d, ungraded join in absent %d)" % (
    len(pair_lines), *[sum(1 for i in pair_lines if line_class[i] == c) for c in PAIR]))
graded = [i for i in pair_lines if line_class[i] in ("pair-bare", "pair-reason")]
bare = sum(1 for i in graded if line_class[i] == "pair-bare")
print("  among pair lines whose strongest answer is a join graded bare or with a reason: bare %d of %d (%.3f)" % (
    bare, len(graded), bare / len(graded)))
print("  pair lines whose call is named from the room's record (R): %d" % sum(1 for i in pair_lines if "R" in tags.get(i, ())))
print("  pair lines that also hold a join with a condition (COND) %d, with a question back (ASK) %d" % (
    sum(1 for i in pair_lines if "COND" in tags.get(i, ())), sum(1 for i in pair_lines if "ASK" in tags.get(i, ()))))
rb = {i for i, c in line_class.items() if c == "refusal-bare"} | {i for i, t in tags.items() if "RB" in t}
rr = {i for i, c in line_class.items() if c == "refusal"} | {i for i, t in tags.items() if "RR" in t}
print("lines showing a bare refusal or hostile reply: %d; a refusal with a reason: %d; both: %d" % (
    len(rb), len(rr), len(rb & rr)))
print("rooms showing a bare refusal: %d; a refusal with a reason: %d" % (len({room(i) for i in rb}), len({room(i) for i in rr})))
cond_lines = {i for i, c in line_class.items() if c == "cond"} | {i for i, t in tags.items() if t & {"COND", "ASK"}}
print("lines showing a conditional or asking answer (class or tag): %d; as the line's only answer (class cond): %d" % (
    len(cond_lines), sum(1 for c in line_class.values() if c == "cond")))

by_room = {}
for i, c in line_class.items():
    by_room.setdefault(room(i), set()).add("pair" if c in PAIR else "refusal" if c.startswith("refusal") else c)
print("rooms with an A12 line:", len(by_room))
PRI = ("pair", "cond", "refusal", "callonly", "proposal", "start", "pledge", "uncoded", "after", "limit")
for c in PRI:
    print("  rooms showing %-9s %d" % (c, sum(1 for s in by_room.values() if c in s)))
first = Counter(next(c for c in PRI if c in s) for s in by_room.values())
print("rooms once, by priority:", {c: first[c] for c in PRI})
call_rooms = {r for r, s in by_room.items() if s & {"pair", "cond", "refusal", "callonly"}}
pair_rooms = {r for r, s in by_room.items() if "pair" in s}
print("rooms whose lines show a call (the pair, a conditional answer, a refusal or call only): %d; the pair in %d (%.3f)" % (
    len(call_rooms), len(pair_rooms), len(pair_rooms) / len(call_rooms)))
bare_rooms = {room(i) for i in pair_lines if line_class[i] == "pair-bare"}
print("rooms whose lines show a bare join answering a call: %d (%.3f of the pair rooms)" % (
    len(bare_rooms), len(bare_rooms) / len(pair_rooms)))
print("Beside: F-023, acceptances of calls to place bare in 25 of 31 and refusals with a reason in 3 of 3; F-014, "
      "refusals of attack calls with a reason in 23 of 38; C2's exemplars, 3 rooms (lebanon, DestinyTheGame, pcmasterrace)")
