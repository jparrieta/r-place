#!/usr/bin/env python3
"""D6a-01: proposal PR-D6-01, the call returns. The affected rooms are the defining members of forms C, D and F whose P01
link (or C's add-step) lines, read whole in d6a01_D01_hows.txt, say that a call came again after a finished part, a later
canvas, damage, a loss, a failed attempt or a move (my reading; rooms whose P01 lines say something else are left out).
Prints one JSON line; append with >>.

    python3 out/_analysis/d6a01_proposal_01.py >> out/proposals-D6.jsonl
"""
import json, os

AN = os.path.dirname(os.path.abspath(__file__))
READ = {
    "C": ["starbound", "earthbound", "mit", "esperanto", "bretagne", "ProfessorLayton", "Honduras"],
    "D": ["bindingofisaac", "rotmg", "edmontonoilers", "frankocean", "homestuck", "giivasunner", "iastate", "flyers",
          "nightinthewoods", "rojava", "sadboys"],
    "F": ["twentyonepilots", "snsd", "penguins", "gratefuldead", "dbz"],
}
TAG = {"C": "d5a38", "D": "d5a39", "F": "d5a41"}
codes, rooms = [], []
for f, subs in READ.items():
    lines = json.load(open(os.path.join(AN, "%s_lines.json" % TAG[f]), encoding="utf-8"))["lines"]
    for s in subs:
        ls = [l for l in lines if l["sub"] == s and l["element"] == "P01" and l["op"] in ("link", "add-step")
              and l.get("role") == "defining"]
        assert ls, (f, s)
        codes.append("%s:%s" % (s, ls[0]["codes"][0]))
        rooms.append(s)
rec = {
    "id": "PR-D6-01",
    "what": "The call returns: after a finished part, a later canvas, damage, a loss, a failed attempt or a move, the room "
            "calls for hands again.",
    "change": "A loop on P01 (the call): arrows into P01 from P11 (a work marked as up), P13 (carrying on), P05 (keeping, "
              "under damage) and P10 (the move after a loss), or a clause in P01's statement that the call recurs at "
              "those points. The model now has the call only at the start (A02, A01) and the account grounds no loop.",
    "why": "Three room forms specify P01 by link lines at 1.4 to 1.7 times the 558 defining rooms' share: C, The design "
           "reopened (14 defining rooms), D, Keeping, with help or carrying on (16), and F, Moving for the spot (6); read "
           "whole, 23 of these rooms' lines say the call came again at one of those points (C 7, D 11, F 5).",
    "evidence": {"codes": codes, "rooms_by_form": READ, "lines_read": "out/_analysis/d6a01_D01_hows.txt",
                 "fractal_lines": ["P01|C", "P01|D", "P01|F"]},
    "affected_rooms": sorted(rooms, key=str.lower),
    "base_model_version": "46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525",
    "status": "unvalidated",
    "leg": "D6a-01",
    "note": "A proposal, not an amendment: it can enter a later model only through a supported return to the affected "
            "rooms' original leads and a new validation cycle.",
}
print(json.dumps(rec, ensure_ascii=False))
