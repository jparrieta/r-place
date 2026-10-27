#!/usr/bin/env python3
"""D6a-03: proposal PR-D6-06, the check before repair: a step inside P05 (keeping), answering F27's note (notes-D5.md,
D5a-27: 'a step the room models propose') with the form lines of D03. The rooms are the defining members whose P05
add-step or link lines, read whole (d6a03_D03_hows.txt and the D5 dumps), say that keepers checked the current canvas or
whether a change was intended before undoing it (my reading). Prints one JSON line; append with >>.

    python3 out/_analysis/d6a03_proposal_06.py >> out/proposals-D6.jsonl
"""
import json, os

AN = os.path.dirname(os.path.abspath(__file__))
READ = {"D": ["OnePiece", "radiohead", "chicubs", "homestuck", "androidgaming"], "A": ["clg"]}
TAG = {"A": "d5a36", "D": "d5a39"}
codes, rooms = [], []
for f, subs in READ.items():
    lines = json.load(open(os.path.join(AN, "%s_lines.json" % TAG[f]), encoding="utf-8"))["lines"]
    for s in subs:
        ls = [l for l in lines if l["sub"] == s and l["element"] == "P05" and l["op"] in ("add-step", "link")
              and l.get("role") == "defining"]
        assert ls, (f, s)
        codes.append("%s:%s" % (s, ls[0]["codes"][0]))
        rooms.append(s)
print(json.dumps({
    "id": "PR-D6-06",
    "what": "The check before repair: before undoing pixels that differ from the form they know, keepers refresh the "
            "canvas, ask for the intended form or check whether the change is intended.",
    "change": "A step inside P05 (keeping): checking the current canvas and the intended form before a repair. It is a "
              "route by which keepers learn of a planned change other than being told, beside the two the held P05 "
              "proposal names (the change read from its shape; informed members holding it). P05's statement and the "
              "held proposal are not changed by this proposal; findings F-024 to F-027 stand as they are.",
    "why": "Form D, Keeping, with help or carrying on, specifies P05 by add-step lines in 21 of 96 defining rooms (22 per "
           "cent, against 14 of the 558); five of them say keepers checked before repairing, and one room of form A says "
           "the same in a link line. Branch F27's note records the step from the room models of r/OnePiece, r/cowchop "
           "and r/armok (notes-D5.md, D5a-27).",
    "evidence": {"codes": codes, "rooms_by_form": READ, "fractal_lines": ["P05|D", "P05 by F27 in D"],
                 "branch_note": "notes-D5.md, D5a-27 (F27)"},
    "affected_rooms": sorted(rooms, key=str.lower),
    "base_model_version": "46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525",
    "status": "unvalidated", "leg": "D6a-03",
}, ensure_ascii=False))
