#!/usr/bin/env python3
"""E1b-03: the defects the moves and provenance audit found, as defects.jsonl lines (appended by a stdout redirect,
once).

    python3 out/_analysis/e1b03_defects_lines.py >> out/defects.jsonl

Found by audit-E1/moves.py, provenance_D6.py and manifest.py. Nothing earlier is changed (rule 18).
"""
import json

L = [
    {"where": "model/history.jsonl, 18 lines of C2a-01 to C2a-03 (event added), and their 18 C2 move snaps",
     "what": "The instrument's: the move is named 'sequencing', which is not one of Grodal, Anteby and Holm's eight. D3 corrected 'stabilizing' for move 174 by an appended line; no line or note declares or corrects 'sequencing'. Each move has its snap, so the provenance stands and only the name is wrong. Found by audit-E1/moves.py.",
     "sure": True},
    {"where": "run_manifest.json; adaptations-recheck.jsonl and rooms/<sub>/verdict-D-recheck.jsonl (the D3 re-check return)",
     "what": "The instrument's: the re-check return has no manifest entry. Each room's run-recheck.json names the readers' model and a session but no seed and no decoding, so the re-check's figures have partial provenance. Found by audit-E1/manifest.py, read at E1b-03.",
     "sure": True},
]
for x in L:
    print(json.dumps({"stage": "E1", "leg": "E1b-03", "where": x["where"], "what": x["what"], "sure": x["sure"]},
                     ensure_ascii=False))
