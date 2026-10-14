#!/usr/bin/env python3
"""C4a, stage C4 section 2, list 2: enter into the model, as hypotheses, the mechanisms that only the field shows and
that a room could answer from its own record. Each entry is `origin: from-field`, `status: tentative`, with
`field_support` (the field's threads and items, as field/model.md and field/check.md give them) and the field's own
mark (firm or provisional), and each gets a model/history.jsonl line. Room items found in my store are listed as the
room side, not as support. The arrow is not counted here and is not in the model's standing count (`in_model`
false); stage D sends each entry to every room. Refuses to run if an id exists.

    python3 out/_analysis/c4_field_entries.py
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
M = os.path.join(ROOT, "out", "model")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

REP = ["r/place 62mg1j c60256", "r/place 62mg1j c60257", "r/place 62mg1j c60265", "r/place 62qib1 c720095",
       "r/place 62qib1 c720105", "r/place 62qib1 c720108", "r/place 62qib1 c720109"]
KEEP = ["r/place 63f0qb c3920184", "r/place 63f0qb c3920185", "r/place 63f0qb c3920186", "r/place 63f0qb c3920193",
        "r/place 63e1pb c3910162", "r/place 63e1pb c3910163", "r/place 63b6md c3850139", "r/place 63b6md c3850142"]

elements = [
    {"id": "P21", "kind": "process", "origin": "from-field", "status": "tentative",
     "statement": "Members dispute who may commit the room to an agreement with other rooms: they say that one "
                  "member's agreement does not bind every placer, deny that a treaty speaks for them, or ask another "
                  "group for a leader to deal with.",
     "tier": ["T3-126"], "fourth": "T4-016", "dimension": ["D04"],
     "range": "from one member saying that a deal cannot stop everyone to a treaty announced in r/place answered "
              "'You don't speak for me, man.'",
     "level": "between rooms; a room shows its side in its own members' talk",
     "evidence": {"findings": [], "codes": ["flyers:c0166", "flyers:c0169"]},
     "field_support": REP,
     "field_mark": "firm: the disclaimers, the denial and the request for a group leader are public exchanges; "
                   "provisional: that an agreement or coalition prompts the dispute",
     "since": LEG, "leg": LEG},
    {"id": "P22", "kind": "process", "origin": "from-field", "status": "tentative",
     "statement": "After placement ends, members contest which version of the canvas and of the event is kept: they "
                  "ask a cleanup of a shared copy to fix their work, take part in it, argue that the cleanup should "
                  "keep the damage as history, and correct accounts of the event that describe their group wrongly.",
     "tier": ["T4-027"], "fourth": "T4-027", "dimension": ["D07"],
     "range": "from one member asking that a logo be cleaned in a shared copy to a room arguing that its scars are "
              "its history",
     "level": "the event (a shared copy and public histories of the whole canvas); a room shows its side in its "
              "own members' talk after hour 73",
     "evidence": {"findings": [], "codes": ["AMD:c0435", "SquareSpiral:c0217", "strangerthings:c0145"],
                  "note": "room items found by a keyword search after hour 73 (c4_grep_hours.py), not by a theme; no "
                          "third-order theme carries this yet"},
     "field_support": KEEP,
     "field_mark": "firm: the sector instructions, the question of who decides, the retention decision, the "
                   "objection to sterilising history and the correction promised are public exchanges; provisional: "
                   "that preserving a shared object requires negotiating its legitimate version; the execution of "
                   "the cleanup is not observed",
     "since": LEG, "leg": LEG},
]
arrows = [
    {"id": "A21", "from": "P08", "to": "P21", "kind": "order", "origin": "from-field", "status": "tentative",
     "in_model": False, "strength": None, "counts": None,
     "connection": "in a room carrying both, the first agreement with another room (a border, a truce or a deal) "
                   "comes before the first dispute over who may commit the room",
     "mechanism": "An agreement made with another room in the room's name puts its members' compliance in question. "
                  "Members who did not make it say that it does not bind them, or that no one can bind every placer, "
                  "and the other side asks who can speak for the group.",
     "mechanism_fails_if": "In a room carrying both, the dispute over who may commit the room comes only before any "
                           "agreement with another room, or the dispute answers no agreement.",
     "level": "between rooms; the order is counted inside each room's record",
     "field_support": REP + ["r/place 62qib1 (a treaty announced between major factions)"],
     "field_mark": "provisional: 'a protective coalition claim prompts participants to examine who can commit a "
                   "group' (field/model.md, process 4); the field's instance is a protective treaty, which my model "
                   "would place under deals (P08) or coalitions (P17)",
     "room_side": ["flyers:c0166", "flyers:c0169"],
     "grounding": "tentative: not counted; stage D asks every room", "since": LEG, "leg": LEG},
]

ef, af, hf = (os.path.join(M, f) for f in ("elements.jsonl", "arrows.jsonl", "history.jsonl"))
have = {json.loads(l)["id"] for f in (ef, af) for l in open(f, encoding="utf-8") if l.strip()}
if have & {"P21", "P22", "A21"}:
    sys.exit("P21, P22 or A21 already exists; nothing written")
hist = [{"t": T, "stage": "C4", "leg": LEG, "id": r["id"], "event": "entered from the field",
         "move": "developing or dropping working hypotheses", "origin": "from-field", "status": "tentative",
         "why": "stage C4 section 2, list 2: a mechanism the field shows and a room could answer from its own record; "
                "entered as a hypothesis for stage D", "field_support": r["field_support"], "was": None}
        for r in elements + arrows]
with open(ef, "a", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in elements))
with open(af, "a", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in arrows))
with open(hf, "a", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in hist))
print("entered: %s; history lines: %d" % (", ".join(r["id"] for r in elements + arrows), len(hist)))
