#!/usr/bin/env python3
"""C2d-01, pass 4: the element changes the two recuts entail (pass 4, declarations 1 and 2), in model/elements.jsonl,
each with a model/history.jsonl line carrying the old line as `was`. Also writes out/_analysis/c2_elements_p4.json, the
membership file the order tests read: every element's third-order themes recomputed from fourth/fourth.jsonl as it now
stands, plus two analysis-only ids for the host's line by actor (P20r, the host sub's rulings; P20o, members'
objections), found by name inside Boundary work. Refuses to rewrite c2_elements_p4.json.

  P17  narrowed to coalitions: the hosting clause leaves its statement and range (move splitting).
  P02  gains the land's flag and emblems as the mark's content (move merging).
  K04  (candidate) loses the flag-building clause; the nation beyond the mark stays (move splitting).

    python3 out/_analysis/c2d_elements_p4.py [--write]
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
EP = os.path.join(OUT, "model", "elements.jsonl")
HP = os.path.join(OUT, "model", "history.jsonl")
DEST = os.path.join(OUT, "_analysis", "c2_elements_p4.json")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
rows = [json.loads(l) for l in open(EP, encoding="utf-8") if l.strip()]
E = dict((r["id"], r) for r in rows)
was = dict((k, json.loads(json.dumps(E[k]))) for k in ("P17", "P02", "K04"))
E["P17"]["statement"] = ("Rooms join other rooms in coalitions: they meet in shared chats, form alliances, gather kindred "
                         "rooms in a hub, tally kindred rooms' works and make joint marks.")
E["P17"]["range"] = "from two rooms agreeing to defend each other to a council of kindred rooms holding a stretch of the canvas together"
E["P02"]["statement"] = ("The room settles what its mark will show of it: a member proposes a picture, the room argues its "
                         "design, makes its land's flag or emblems the mark, signs it or leaves it unsigned, or claims a mark "
                         "others made.")
E["P02"]["range"] = ("from a single member's unanswered proposal to a design argued over days and redone, or a nation's flag "
                     "sized and filled with its emblems")
E["K04"]["statement"] = ("The room acts as a body it was before the canvas, or as a faith in a colour: it argues the nation's "
                         "history, belonging and politics beyond its flag, carries in the sub's quarrel, lore, jokes or "
                         "ideology, or professes and spreads a colour.")
E["K04"]["range"] = "from a fandom's running joke in canvas talk to a canvas fight told as the nation's history"
hist = [
    ("P17", "narrowed", "splitting", "pass 4 declaration 1: the hosting themes left Meta-organization for Territoriality; "
     "the coalition element keeps the coalitions and loses its hosting clause; hosting stays the candidate P19"),
    ("P02", "widened", "merging", "pass 4 declaration 2: building the homeland's flag and drawing national emblems joined "
     "Collective representation by the rule written first (acts that draw or settle the room's own mark)"),
    ("K04", "narrowed", "splitting", "pass 4 declaration 2: the flag and emblem themes left Flagging the nation; the "
     "candidate keeps the nation claimed beyond the mark"),
]
t4 = dict((r["id"], r) for r in (json.loads(l) for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"), encoding="utf-8") if l.strip()))
t3 = dict((r["id"], r) for r in (json.loads(l) for l in open(os.path.join(OUT, "scheme_v2.jsonl"), encoding="utf-8") if l.strip()))
p3 = json.load(open(os.path.join(OUT, "_analysis", "c2_elements_p3.json"), encoding="utf-8"))


def themes(tier):
    out = []
    for x in tier:
        out += t4[x]["members"] if x in t4 else [x]
    return out


els = []
for e in p3["elements"]:
    if e["id"] == "P17n":
        continue
    cur = E.get(e["id"])
    if cur is None:
        sys.exit("element %s is in c2_elements_p3.json and not in elements.jsonl" % e["id"])
    n = dict(e)
    n.update({"statement": cur["statement"], "tier": cur["tier"], "dimension": cur["dimension"], "range": cur["range"],
              "status": cur["status"], "themes": themes(cur["tier"])})
    els.append(n)
bw = [k for k, r in t4.items() if r["name"] == "Boundary work"][0]


def named(names):
    hit = [m for m in t4[bw]["members"] if t3[m]["name"] in names]
    if len(hit) != len(names):
        sys.exit("not every named theme is in Boundary work: %s" % names)
    return hit


rul = named(["routing canvas posts into megathreads", "removing canvas posts by rule", "opening a canvas sub",
             "moderators disowning the canvas work", "pausing the sub's usual events", "changing the sub's posting rules"])
obj = named(["objecting to the canvas flood", "arguing the canvas's worth"])
if sorted(rul + obj) != sorted(t4[bw]["members"]):
    sys.exit("rulings and objections do not partition Boundary work")
els.append({"id": "P20r", "kind": "process", "statement": "The host sub's rulings on canvas talk: megathreads, removals by "
            "rule, a canvas sub, changed rules, paused events, the moderators disowning the work (analysis id, pass 4).",
            "tier": rul, "dimension": E["P20"]["dimension"], "themes": rul, "status": "analysis"})
els.append({"id": "P20o", "kind": "process", "statement": "Members' objections to the canvas in the host sub: the flood "
            "objected to, the canvas's worth argued (analysis id, pass 4).", "tier": obj, "dimension": E["P20"]["dimension"],
            "themes": obj, "status": "analysis"})
print("P17 themes %s" % themes(E["P17"]["tier"]))
print("P02 themes %d; K04 themes %d; P19 %s; P20r %s; P20o %s" % (len(themes(E["P02"]["tier"])), len(themes(E["K04"]["tier"])),
                                                              E["P19"]["tier"], rul, obj))
if "--write" in sys.argv:
    if os.path.exists(DEST):
        sys.exit("c2_elements_p4.json exists; not rewritten")
    with open(EP, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(HP, "a", encoding="utf-8") as f:
        for k, ev, mv, why in hist:
            f.write(json.dumps({"t": T, "stage": "C2", "leg": LEG, "id": k, "event": ev, "move": mv, "why": why,
                                "was": was[k]}, ensure_ascii=False) + "\n")
    json.dump({"about": "pass 4 element membership for the order tests (c2d_elements_p4.py): elements.jsonl as rewritten "
               "at C2d-01, themes recomputed from fourth.jsonl after the two recuts; P20r and P20o are analysis ids for "
               "the host's line by actor", "elements": els}, open(DEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("elements.jsonl rewritten (%d lines); %d history lines; %s written (%d elements)" % (len(rows), len(hist),
                                                                                           os.path.relpath(DEST, ROOT), len(els)))
