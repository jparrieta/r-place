#!/usr/bin/env python3
"""D6a-01: departures.jsonl line 19, the shape of fractal-D6.jsonl and the per-dimension closes (QD6-001 asked).
Prints one JSON line; append with >>.

    python3 out/_analysis/d6a01_departure.py >> out/departures.jsonl
"""
import json

print(json.dumps({
    "stage": "D6", "leg": "D6a-01", "date": "2026-10-27",
    "provision": "the principal investigator's message of 27 October (03:28 UTC, on J's word): fractal-D6.jsonl has one "
                 "line per element and room form (A to F), a branch only where it explains a form; the stage file's "
                 "'branch' is read as room form",
    "why": "The stage's close-check (tools/checks/stage_D6.py, lines 35 to 36) refuses a fractal line whose branch field is "
           "not an id in branches.jsonl, and a room form's letter is not one; lines 72 to 79 treat the presence of "
           "retelling-D6.md as the last leg and then require figure-D6.md, handback-D6.md, a line for every branch and every "
           "branch named in the telling. Part 1 of retelling-D6.md (dimension by dimension) is written leg by leg, so no "
           "per-dimension leg can pass the full check before D6b.",
    "applies_backwards": "False",
    "scope": "Until QD6-001 is answered: fractal lines carry the form's letter in 'branch' (with 'level': 'room form' and "
             "'form_name'), and name any explaining D4 branch in 'branches'; each per-dimension leg closes at its safe stop "
             "with done.sh D6 --pause, its pause line saying where to pick up; at D6b every branch is named in the telling "
             "and given at least one line where it explains a form. branches.jsonl, the D4 tree and the model are not "
             "touched.",
}, ensure_ascii=False))
