#!/usr/bin/env python3
"""C2, pass 2: write out/_analysis/c2_elements_p2.json, the pass 1 elements plus the candidate elements declared in
notes-C2.md (pass 2, before any count). Candidate members are read from fourth/fourth.jsonl, never typed: P16 is all of
Reciprocity, P17 all of Meta-organization, P18 all of Rivalry; K03 is the one third-order theme T3-086.
Refuses to overwrite.

    python3 out/_analysis/c2_elements_p2_build.py
"""
import json, os, sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(OUT, "_analysis", "c2_elements_p2.json")
if os.path.exists(DEST):
    sys.exit("c2_elements_p2.json exists; not overwritten")
p1 = json.load(open(os.path.join(OUT, "_analysis", "c2_elements_p1.json"), encoding="utf-8"))
t4 = dict((r["id"], r) for r in (json.loads(l) for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"), encoding="utf-8") if l.strip()))
dim = dict((m, d["id"]) for d in (json.loads(l) for l in open(os.path.join(OUT, "dimensions.jsonl"), encoding="utf-8") if l.strip()) for m in d["members"])
owner = dict((m, k) for k, r in t4.items() for m in r["members"])


def by_name(name):
    hit = [k for k, r in t4.items() if r["name"] == name]
    if len(hit) != 1:
        sys.exit("fourth-order theme %r not found once" % name)
    return hit[0]


rec, meta, riv = by_name("Reciprocity"), by_name("Meta-organization"), by_name("Rivalry")
cands = [
    {"id": "P16", "kind": "process",
     "statement": "Rooms help one another's works and trade help: they give pixels to a neighbour's mark, ask other rooms for help, barter help for space or repair, thank their allies, greet them, and turn requests away.",
     "tier": [rec], "dimension": [dim[rec]],
     "range": "from one member placing a pixel on a neighbour's flag to rooms trading night-time repairs for room on their mark",
     "themes": t4[rec]["members"], "codes": [], "status": "candidate"},
    {"id": "P17", "kind": "process",
     "statement": "Rooms join other rooms in coalitions and host them: they meet in shared chats, form alliances, gather kindred rooms, make joint marks, ask a host for space or vet others' requests to build on their own mark.",
     "tier": [meta], "dimension": [dim[meta]],
     "range": "from two rooms agreeing to defend each other to a flag hosting dozens of other rooms' works by vote",
     "themes": t4[meta]["members"], "codes": [], "status": "candidate"},
    {"id": "P18", "kind": "process",
     "statement": "Rooms carry a contest with a rival room in talk: they trade taunts, flood the rival's threads, claim victory, salute the rival after the fight and blame attackers after the close.",
     "tier": [riv], "dimension": [dim[riv]],
     "range": "from one taunt in a thread to days of chants, victory claims and an after-the-fight salute",
     "themes": t4[riv]["members"], "codes": [], "status": "candidate"},
    {"id": "K03", "kind": "condition",
     "statement": "The community carries a quarrel from before the canvas into it: a rival sub, a sports or national rivalry, an old dispute.",
     "tier": ["T3-086"], "dimension": [dim[owner["T3-086"]]],
     "range": "from one member naming the sub's old rival to a room whose first canvas act is against that rival",
     "themes": ["T3-086"], "codes": [], "status": "candidate"},
]
out = {"about": "pass 2 elements: the pass 1 elements (unchanged) plus the candidates declared in notes-C2.md, pass 2",
       "elements": p1["elements"] + cands}
with open(DEST, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
for c in cands:
    print(c["id"], c["tier"], c["dimension"], len(c["themes"]), "themes:", ", ".join(c["themes"]))
