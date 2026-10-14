#!/usr/bin/env python3
"""C2, pass 3: write out/_analysis/c2_elements_p3.json, the pass 2 elements plus the candidates declared in notes-C2.md
(pass 3, before any count). Members are read from fourth/fourth.jsonl and scheme_v2.jsonl, never typed:
- K04 is all members of Flagging the nation, Neo-tribes and Frame bridging;
- P19 is the four members of Meta-organization named for hosting (asking a host for space, disputing who approves a
  spot, relying on a bigger neighbour, vetting others' requests to build);
- P17n is P17 narrowed to the other five members of Meta-organization (an analysis id for the test only);
- P20 is all members of Boundary work.
Refuses to overwrite.

    python3 out/_analysis/c2_elements_p3_build.py
"""
import json, os, sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(OUT, "_analysis", "c2_elements_p3.json")
if os.path.exists(DEST):
    sys.exit("c2_elements_p3.json exists; not overwritten")
p2 = json.load(open(os.path.join(OUT, "_analysis", "c2_elements_p2.json"), encoding="utf-8"))
t4 = dict((r["id"], r) for r in (json.loads(l) for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"), encoding="utf-8") if l.strip()))
t3 = dict((r["id"], r) for r in (json.loads(l) for l in open(os.path.join(OUT, "scheme_v2.jsonl"), encoding="utf-8") if l.strip()))
dim = dict((m, d["id"]) for d in (json.loads(l) for l in open(os.path.join(OUT, "dimensions.jsonl"), encoding="utf-8") if l.strip()) for m in d["members"])


def by_name(name):
    hit = [k for k, r in t4.items() if r["name"] == name]
    if len(hit) != 1:
        sys.exit("fourth-order theme %r not found once" % name)
    return hit[0]


def t3_by_name(name, inside):
    hit = [k for k in t4[inside]["members"] if t3[k]["name"] == name]
    if len(hit) != 1:
        sys.exit("third-order theme %r not found once in %s" % (name, inside))
    return hit[0]


nation, tribes, bridging = by_name("Flagging the nation"), by_name("Neo-tribes"), by_name("Frame bridging")
meta, boundary = by_name("Meta-organization"), by_name("Boundary work")
host_names = ["asking a host for space", "disputing who approves a spot", "relying on a bigger neighbour",
              "vetting others' requests to build"]
hosting = [t3_by_name(n, meta) for n in host_names]
coalition = [m for m in t4[meta]["members"] if m not in hosting]
k04 = t4[nation]["members"] + t4[tribes]["members"] + t4[bridging]["members"]
if len(set(dim[x] for x in (nation, tribes, bridging))) != 1:
    sys.exit("K04's fourth-order themes do not share one dimension")
cands = [
    {"id": "K04", "kind": "condition",
     "statement": "The room acts as a body it was before the canvas, or as a faith in a colour: it builds and argues the homeland's flag and history, carries in the sub's quarrel, lore, jokes or ideology, or professes and spreads a colour.",
     "tier": [nation, tribes, bridging], "dimension": [dim[nation]],
     "range": "from a fandom's running joke in canvas talk to a nation's flag fought over as its history",
     "themes": k04, "codes": [], "status": "candidate"},
    {"id": "P19", "kind": "process",
     "statement": "One room's work lives on another room's mark or territory under the host's rule: guests ask for space or protection, hosts rule on requests, and both sides dispute who may approve.",
     "tier": hosting, "dimension": [dim[meta]],
     "range": "from a small room asking to slip into a neighbour's lot to a flag hosting dozens of works by application and vote",
     "themes": hosting, "codes": [], "status": "candidate"},
    {"id": "P17n", "kind": "process",
     "statement": "Rooms join other rooms in coalitions: they meet in shared chats, form alliances, gather kindred rooms in a hub, tally kindred rooms' works and make joint marks.",
     "tier": coalition, "dimension": [dim[meta]],
     "range": "from two rooms agreeing to defend each other to a league's hub sub coordinating dozens of teams",
     "themes": coalition, "codes": [], "status": "candidate"},
    {"id": "P20", "kind": "process",
     "statement": "The host sub draws a line around canvas talk: moderators gather it into a megathread, remove canvas posts by rule, change posting rules, pause the sub's usual events or disown the work; members open a canvas sub, object to the flood or argue the canvas's worth.",
     "tier": [boundary], "dimension": [dim[boundary]],
     "range": "from one member asking for a megathread to moderators moving all canvas talk to a new sub and removing the rest",
     "themes": t4[boundary]["members"], "codes": [], "status": "candidate"},
]
have = set(e["id"] for e in p2["elements"])
if have & set(c["id"] for c in cands):
    sys.exit("a pass 3 candidate id is already among the pass 2 elements")
out = {"about": "pass 3 elements: the pass 2 elements (unchanged) plus the candidates declared in notes-C2.md, pass 3",
       "elements": p2["elements"] + cands}
with open(DEST, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
for c in cands:
    print(c["id"], c["tier"], c["dimension"], len(c["themes"]), "themes:", ", ".join(c["themes"]))
