#!/usr/bin/env python3
"""E1b-05: the defects the diary, probe and unplaced audits found, as defects.jsonl lines (appended by a stdout
redirect, once).

    python3 out/_analysis/e1b05_defects_lines.py >> out/defects.jsonl

Found by audit-E1/probes_notes.py and unplaced_kinds.py, read by hand. Nothing earlier is changed (rule 18).
"""
import json

L = [
    {"where": "out/_probe/ (B1b-01, B1b-03 to B1b-08, B1b-17 to B1b-21 with B1b-19-p2, D5a-33; D4a-06 to D4a-08, D6a-01)",
     "what": "The instrument's: 18 recall-probe misses that neither the head, the diary nor the question files answered at the close: the last three rooms opened in 13 B1 legs and one D5 leg, which the diary never names, and the changed ids of three D4 legs and the first D6 leg, which their diary lines do not name. The record a later leg reads first did not carry them. Found by audit-E1/probes_notes.py (probes-E1.md).",
     "sure": True},
    {"where": "assignments_final.jsonl; the 151 unplaced second-order themes (audit-E1/unplaced_kinds.json)",
     "what": "The instrument's: 10 unplaced second-order themes name an act the scheme holds and should have been placed: germany/t19, h3h3productions/t27, h3h3productions/t30, hungary/t05, linux/t03, oman/t06, opticgaming/t12, orderofthebluecorner/t02, rainbowgrid/t06, romania/t18. Most hold one concept. The other 141 are April Fools play, talk about the event, or lost posts, rightly outside. Found by audit-E1/unplaced_kinds.py, read by hand.",
     "sure": False},
]
for x in L:
    print(json.dumps({"stage": "E1", "leg": "E1b-05", "where": x["where"], "what": x["what"], "sure": x["sure"]},
                     ensure_ascii=False))
