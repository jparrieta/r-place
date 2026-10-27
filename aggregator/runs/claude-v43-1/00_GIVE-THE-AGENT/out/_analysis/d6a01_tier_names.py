#!/usr/bin/env python3
"""D6a-01: the six tier_history lines for the room forms' final names (moves 314 to 319, contrasting), on J's word through
the PI (27 October 00:43 Berlin). Names and glosses are those of out/room-forms-names.md; sizes and earlier names come from
room-forms-D4a08c.jsonl. Prints the lines; append them with >>.

    python3 out/_analysis/d6a01_tier_names.py >> out/tier_history.jsonl
"""
import datetime, json, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FINAL = {
    "A": "Border terms and the announced plan",
    "B": "Behind the thread: chat, scripts, raids",
    "C": "The design reopened",
    "D": "Keeping, with help or carrying on",
    "E": "The sub's play, run as work",
    "F": "Moving for the spot",
}
SPLITS = {"D": {"D.1": "Keeping with the call", "D.2": "Keeping inside the sub's play", "D.2.1": "The play, carried on",
                "D.2.2": "The play, kept"}}
forms = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "room-forms-D4a08c.jsonl"), encoding="utf-8")}
names_md = open(os.path.join(OUT, "room-forms-names.md"), encoding="utf-8").read()
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
for i, f in enumerate("ABCDEF"):
    assert FINAL[f] in names_md, FINAL[f]
    for s in SPLITS.get(f, {}).values():
        assert s in names_md, s
    line = {"t": t, "stage": "D6", "leg": "D6a-01", "tier": "room-form", "id": "D4a08c-%s" % f, "move": "contrasting",
            "event": "room form named (final)", "move_no": 314 + i, "name": FINAL[f], "previous_name": forms[f]["name"],
            "why": "J (27 Oct 00:43 Berlin, through the PI): name the clusters after all are finished; the name says the form's "
                   "pattern of change, read in its D5 account against the other five forms",
            "ground": "the form's D5 account (room-form-%s-account.md) and its line in room-forms-D5.jsonl; no recut" % f,
            "parent": None, "members_n": forms[f]["n"], "names_file": "room-forms-names.md"}
    if f in SPLITS:
        line["splits_named"] = SPLITS[f]
    print(json.dumps(line, ensure_ascii=False))
