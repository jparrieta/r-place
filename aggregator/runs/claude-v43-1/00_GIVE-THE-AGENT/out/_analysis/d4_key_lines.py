#!/usr/bin/env python3
"""D4: the lines behind one adaptation key, for reading what a candidate group shares (stage D4 section 2: a branch
is named by what its keys change). A key is op:element:node at a ladder level (3, 4, dim, target), as distance.py
builds it from the shared lines (adaptation_ledger.shared_lines: the current ledger's accepted or modified lines of
kind specification, elaboration or correction). Prints each holding room once, with its lines on the key: id, kind,
the lift, and the line's statement, condition and how in full. With --children it first counts the rooms per
level-3 node under a level-4 key. Read-only.

    python3 out/_analysis/d4_key_lines.py --key add-step:K01:T4-001 --level 4 [--children] [--offset 0 --limit 40]
"""
import argparse, collections, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import distance  # noqa: E402
from adaptation_ledger import shared_lines  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--key", required=True)
ap.add_argument("--level", required=True, choices=["3", "4", "dim", "target"])
ap.add_argument("--children", action="store_true")
ap.add_argument("--offset", type=int, default=0)
ap.add_argument("--limit", type=int, default=40)
a = ap.parse_args()
op, el, node = a.key.split(":")
lines = [l for l in shared_lines(OUT) if l["op"] == op and l["element"] == el and distance.node_at(l, a.level) == node]
by_room = collections.defaultdict(list)
for l in lines:
    by_room[l["sub"]].append(l)
rooms = sorted(by_room, key=str.lower)
print("key %s at level %s: %d rooms, %d lines; kinds %s" % (a.key, a.level, len(rooms), len(lines),
                                                          dict(collections.Counter(l["kind"] for l in lines))))
if a.children:
    ch = collections.defaultdict(set)
    for l in lines:
        ch[distance.node_at(l, "3")].add(l["sub"])
    print("rooms by level-3 node: %s" % "; ".join("%s %d" % (k, len(v)) for k, v in
                                                 sorted(ch.items(), key=lambda x: -len(x[1]))))
for s in rooms[a.offset:a.offset + a.limit]:
    for l in by_room[s]:
        print("- %s | %s | %s | lift %s" % (s, l["id"], l["kind"], "/".join(str(x) for x in (l.get("lift") or []))))
        for f in ("statement", "condition", "how"):
            if l.get(f):
                print("    %s: %s" % (f, l[f]))
print("[rooms %d to %d of %d]" % (a.offset + 1, min(a.offset + a.limit, len(rooms)), len(rooms)))
