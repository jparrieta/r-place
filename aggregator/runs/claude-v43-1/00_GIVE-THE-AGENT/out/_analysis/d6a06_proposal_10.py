#!/usr/bin/env python3
"""D6a-06: proposal PR-D6-10, the play run as work, answering form E's note (notes-D5.md, D5a-40: 'the model holds the
play only as a key') with the form lines of D06. The rooms are the defining members of forms D, E and F that hold a K01
add-step line (the cells K01|D, K01|E and K01|F; read whole in d6a06_D06_hows.txt). Prints one JSON line; append with >>.

    python3 out/_analysis/d6a06_proposal_10.py >> out/proposals-D6.jsonl
"""
import json, os

AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
TAG = {"D": "d5a39", "E": "d5a40", "F": "d5a41"}
f01 = set(json.loads(open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8").readline())["members"])
codes, rooms, by_form, in_f01 = [], [], {}, {}
for f, t in TAG.items():
    lines = json.load(open(os.path.join(AN, "%s_lines.json" % t), encoding="utf-8"))["lines"]
    subs = []
    for l in lines:
        if l["element"] == "K01" and l["op"] == "add-step" and l.get("role") == "defining" and l["sub"] not in subs:
            subs.append(l["sub"])
            codes.append("%s:%s" % (l["sub"], l["codes"][0]))
    by_form[f] = sorted(subs, key=str.lower)
    in_f01[f] = len(set(subs) & f01)
    rooms += subs
n = {f: len(v) for f, v in by_form.items()}
print(json.dumps({
    "id": "PR-D6-10",
    "what": "The play run as work: inside the sub's April Fools key, moderators and members do organized work with the "
            "steps the model gives the canvas work. They start the play and set its rules, enforce the rules by real "
            "removals and bots, test whether claims are jokes, repair what the play breaks, argue and set its end, and "
            "ask that its changes last.",
    "change": "A process element under Host framing, beside K01: the sub administers its play. K01's statement (the key) "
              "is not changed by this proposal. The element would bring into the model what the ruling of D3a-55 put "
              "outside its scope, the sub's own business on the canvas days, so it is a change of scope as well as a new "
              "element; a later model decides whether the scope is widened.",
    "why": "Three forms specify K01 by add-step lines: E in %d of 84 defining rooms (66.7 per cent, against 103 of the "
           "558, 18.5 per cent), D in %d of 96 (21 of its 24 holders are rooms of D.2, Keeping inside the sub's play) and "
           "F in %d of 34. Branch F01 (103 rooms) states the change; its rooms are %d of these holders in E, %d in D and "
           "%d in F, and its five subforms (F02 to F06) lean to E. In the lines read, the play runs beside the canvas "
           "work; in a few rooms it reaches it (r/battlecats and r/bindingofisaac, D5a-02; r/osu and r/polandball, "
           "d6a06_D06_hows.txt and F21's line)."
           % (n["E"], n["D"], n["F"], in_f01["E"], in_f01["D"], in_f01["F"]),
    "evidence": {"codes": codes, "rooms_by_form": by_form,
                 "fractal_lines": ["K01|D", "K01|E", "K01|F", "K01 by F01 to F06 and F21 in E", "K01 by F04 in D and F"],
                 "form_note": "notes-D5.md, D5a-40 (form E: the model holds the play only as a key)"},
    "affected_rooms": sorted(rooms, key=str.lower),
    "base_model_version": "46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525",
    "status": "unvalidated", "leg": "D6a-06",
}, ensure_ascii=False))
