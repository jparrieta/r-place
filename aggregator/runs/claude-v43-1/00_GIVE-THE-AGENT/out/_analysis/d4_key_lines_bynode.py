#!/usr/bin/env python3
"""D4: the lines behind one level-4 adaptation key, grouped by their level-3 node, for reading a candidate group and
its possible subforms (cut rules R1a, R2, R3). Prints the element's statement; the rooms per level-3 node; how many of
the key's rooms are already members of each declared branch (branches.jsonl); the other change keys of the same
element at level 4 held by 5 or more of the key's rooms (R1b); then every line, by node, with its room, id, kind and
how sentence (statement and condition when they differ). Read-only.

    python3 out/_analysis/d4_key_lines_bynode.py --key restrict:P05:T4-006
"""
import argparse, collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import distance  # noqa: E402
from adaptation_ledger import shared_lines  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--key", required=True)
a = ap.parse_args()
op, el, node = a.key.split(":")
CHANGE = {"add-step", "add-condition", "link", "restrict", "contradict"}


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


rec = {r["id"]: r for r in jl(os.path.join(OUT, "model", "elements.jsonl"))}.get(el, {})
print("%s %s (%s): %s" % (el, rec.get("status"), rec.get("kind"), rec.get("statement")))
print("  range: %s" % rec.get("range"))
SL = shared_lines(OUT)
lines = [l for l in SL if l["op"] == op and l["element"] == el and distance.node_at(l, "4") == node]
rooms = {l["sub"] for l in lines}
by3 = collections.defaultdict(list)
for l in lines:
    by3[distance.node_at(l, "3")].append(l)
print("key %s: %d rooms, %d lines; kinds %s" % (a.key, len(rooms), len(lines),
                                              dict(collections.Counter(l["kind"] for l in lines))))
print("rooms by level-3 node: %s" % "; ".join("%s %d" % (k, len({l['sub'] for l in v})) for k, v in
                                             sorted(by3.items(), key=lambda x: -len({l['sub'] for l in x[1]}))))
for b in jl(os.path.join(OUT, "branches.jsonl")):
    n = len(rooms & set(b["members"]))
    if n:
        print("  in %s (%s): %d" % (b["id"], b["name"][:60], n))
other = collections.defaultdict(set)
for l in SL:
    if l["element"] == el and l["op"] in CHANGE and l["sub"] in rooms:
        k4 = "%s:%s:%s" % (l["op"], el, distance.node_at(l, "4"))
        if k4 != a.key:
            other[k4].add(l["sub"])
print("other change keys of %s at level 4 held by 5+ of these rooms: %s" % (
    el, "; ".join("%s %d" % (k, len(s)) for k, s in sorted(other.items(), key=lambda x: -len(x[1])) if len(s) >= 5)
    or "none"))
for k3, ls in sorted(by3.items(), key=lambda x: -len({l['sub'] for l in x[1]})):
    print("\n== %s (%d rooms)" % (k3, len({l['sub'] for l in ls})))
    for l in sorted(ls, key=lambda x: (x["sub"].lower(), x["id"])):
        extra = ""
        if l.get("condition") and l.get("condition") != l.get("how"):
            extra = " | condition: %s" % l["condition"]
        print("- %s | %s | %s | %s%s" % (l["sub"], l["id"], l["kind"], l.get("how") or l.get("statement") or "", extra))
