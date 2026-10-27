#!/usr/bin/env python3
"""D6a-07: proposal PR-D6-11, imprinting runs with the work, from the form lines of D07 and the D5 notes on A07 (D5a-31,
across F27, F30 and F31) and A09 (D5a-11). The rooms are the defining members whose deciding lines, read whole
(d6a07_D07_hows.txt), say that the room marked, recorded or began to carry on its work while it was being built, before a
finish, or after the work was cut short or lost (my reading); each room is counted once, at the first cell listed.
Prints one JSON line; append with >>.

    python3 out/_analysis/d6a07_proposal_11.py >> out/proposals-D6.jsonl
"""
import json, os

AN = os.path.dirname(os.path.abspath(__file__))
TAG = {"A": "d5a36", "D": "d5a39", "E": "d5a40", "F": "d5a41"}
LINES = {f: json.load(open(os.path.join(AN, "%s_lines.json" % t), encoding="utf-8"))["lines"] for f, t in TAG.items()}
# (form, element, ops): rooms
READ = [
    ("A", "P11", ("add-step",), ["rocketbeans", "anime", "vocaloid", "asexuality", "AcePlace", "Okami", "taiwan", "faeria"]),
    ("D", "P11", ("add-step",), ["FinalFantasy", "edmontonoilers", "columbia", "rojava"]),
    ("E", "A07", ("restrict",), ["detroitlions", "greenbaypackers", "cfb", "chess", "habs", "ultrahardcore", "totallynotrobots"]),
    ("F", "A07", ("restrict",), ["twentyonepilots", "penguins", "predators", "warthunder"]),
    ("E", "A08", ("restrict",), ["worldoftanks", "uwaterloo", "uoft", "minecraft", "python", "homelab", "oneplus", "seahawks"]),
    ("F", "P12", ("link",), ["pebble", "qotsa"]),
    ("D", "P13", ("add-step", "add-condition"), ["warriors", "homestuck", "lovelive", "texans", "heroesofthestorm",
                                                 "porterrobinson", "greyblob", "italy"]),
    ("E", "P13", ("restrict",), ["pcmasterrace", "thenetherlands"]),
    ("D", "A09", ("restrict",), ["rutgers", "nyjets", "ice_poseidon"]),
]
codes, rooms, by_cell = [], [], {}
for f, el, ops, subs in READ:
    key = "%s|%s" % (el, f)
    by_cell[key] = []
    for s in subs:
        assert s not in rooms, s
        ls = [l for l in LINES[f] if l["sub"] == s and l["element"] == el and l["op"] in ops and l.get("role") == "defining"]
        assert ls, (f, el, s)
        codes.append("%s:%s" % (s, ls[0]["codes"][0]))
        rooms.append(s)
        by_cell[key].append(s)
print(json.dumps({
    "id": "PR-D6-11",
    "what": "Imprinting runs with the work: rooms mark, record and begin to carry on their work while it is being built, "
            "and they mark and record an attempt cut short or lost, not only once the work is up and near the close.",
    "change": "Bounds on P11 and P13 and wider bounds on A07, A08 and A09. P11 ('When a work is up, the room marks it') would "
              "add: the room also marks partial progress, an unfinished attempt and a lost work, and members dispute "
              "credit while the work goes on. P13 ('Near the close and after it') would add: carrying on can begin while "
              "placement is live. The bounds of A07 (the late find and the work the close cut short), A08 (the late side) "
              "and A09 (a next canvas planned while still building) would widen to the whole course of the work. The "
              "arrows' statements and their order counts (A07 139 of 182 rooms, A08 225 of 289, A09 113 of 145) are not "
              "changed: the order holds in most rooms, and the proposal bounds where it does not.",
    "why": "Four forms change the dimension. P11 is specified by A (21 of 135 defining rooms) and D (15 of 96); P13 by D "
           "(30 of 96); A07 is restricted by E (14 of 84) and F (7 of 34), A08 by E (24) and A09 by D (16) and E (10); "
           "P12 is specified by F's links (5). In %d of these rooms the line says the act came during the work, before a "
           "finish, or after the work was cut short or lost (my reading). Branches F17, F18 and F19 (marking and credit "
           "while the work goes on), F11 (carrying on begun before the close) and F09 (rooms that moved mark an "
           "unfinished work) explain parts of it. The D5 notes found the same: A07's bound does not cover marking "
           "during the work, before its finish, after its loss or on a spot held on leave (18 rooms across F27, F30 "
           "and F31), and many A09 restrict lines deny a causal role the arrow does not claim." % len(rooms),
    "evidence": {"codes": codes, "rooms_by_cell": by_cell,
                 "fractal_lines": ["P11|A", "P11|D", "P13|D", "A07|E", "A07|F", "A08|E", "A09|D", "A09|E", "P12|F",
                                   "P11 by F17, F18, F19 in A", "P13 by F11 in D", "A07 by F09 in F"],
                 "notes": "notes-D5.md, D5a-31 (A07 across F27, F30, F31) and D5a-11 (A09's wording)"},
    "affected_rooms": sorted(rooms, key=str.lower),
    "base_model_version": "46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525",
    "status": "unvalidated", "leg": "D6a-07",
}, ensure_ascii=False))
