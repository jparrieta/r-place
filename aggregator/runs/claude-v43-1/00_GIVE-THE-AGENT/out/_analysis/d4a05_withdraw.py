#!/usr/bin/env python3
"""D4a-05: print (a) the departures.jsonl line that records J's two later messages, and (b) the tier_history.jsonl
line of move 278, which withdraws the 32 sub-form declarations (moves 246 to 277). Append each by redirect.

    python3 out/_analysis/d4a05_withdraw.py --what departure >> out/departures.jsonl
    python3 out/_analysis/d4a05_withdraw.py --what tier >> out/tier_history.jsonl
"""
import argparse, datetime, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T = json.load(open(os.path.join(ROOT, "out", "_analysis", "d4a05_tree3.json"), encoding="utf-8"))
subs = [n["id"] for n in T["nodes"] if n["id"] not in T["forms"]]
ap = argparse.ArgumentParser()
ap.add_argument("--what", required=True)
a = ap.parse_args()
if a.what == "departure":
    print(json.dumps({
        "stage": "D4", "leg": "D4a-05", "date": "2026-10-26",
        "provision": "the dated amendment of departures.jsonl line 11 (D4a-05), its scope",
        "why": ("J's two later messages through the handler. J, 18:35 Berlin: \"I mean as a leg that happened after "
                "not instead.\" J, 18:36 Berlin: \"Let the agent know that as the cut is made we will need to talk to "
                "it, so that we go over the clustering in a way it makes sense for us all.\" So the room forms are an "
                "addition after D5, not a recut of D4: branches.jsonl, crosslinks.jsonl, tree-D4.md and every D5 "
                "account stay exactly as they were (checked against the D5b close snap: 78 files unchanged). The leg "
                "stops at the top cut, the 8 forms and the core; the split down to the rooms waits for the talk with J."),
        "applies_backwards": False,
        "scope": ("The room forms are written to out/room-forms-D4a05.jsonl, .md and .tsv. The 32 sub-form "
                  "declarations made before these messages arrived (moves 246 to 277) are withdrawn by move 278 and "
                  "held as working material in out/_analysis/ for the talk; they are in no delivered file."),
    }, ensure_ascii=False))
if a.what == "tier":
    print(json.dumps({
        "t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stage": "D4", "leg": "D4a-05", "tier": "room-sub-form", "id": "room sub-forms of moves 246 to 277",
        "move": "dropping", "event": "room sub-form declarations withdrawn", "move_no": 278,
        "why": ("J, 26 October 2026, 18:36 Berlin, through the handler: stop at the top cut; the split down to the "
                "rooms comes after J goes over the clustering with the analyst. The 32 declarations were made before "
                "the message arrived; they are withdrawn as declarations and held as working material."),
        "ground": "J's instruction", "withdrawn": subs, "members_n": None}, ensure_ascii=False))
