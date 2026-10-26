#!/usr/bin/env python3
"""D4a-07: print the dated amendment (J, 26 October 2026, 20:35 to 20:37 Berlin) as a departures.jsonl line.

    python3 out/_analysis/d4a07_amendment.py >> out/departures.jsonl
"""
import json

print(json.dumps({
    "stage": "D4", "leg": "D4a-07", "date": "2026-10-26",
    "provision": "the room forms of D4a-05 and D4a-06 (departures.jsonl lines 11 to 13): an arrow line counted only at the third-order theme of the room's evidence",
    "why": ("J read the D4a-06 interview answers and asked, 26 October 2026, 20:35 to 20:37 Berlin, through the handler: "
            "\"How come arrows are not used?\" \"The arrow can work at any level. Just as the T3 are T4 and Ds.\" "
            "\"Add the arrow and give your ideas as proposals but not mandated.\" Required: each changed arrow is lifted as "
            "a link at each level (source to target at the third-order themes, the fourth-order themes and the dimensions), "
            "and within each level a room's profile holds both the nodes its changes touch and the links its arrow changes "
            "touch. The leg stops after the top cut. The handler's list of proposals (placement, form B, form H, the count, "
            "the floor, restrict lines, the reading) is taken, changed or declined with reasons in the report."),
    "applies_backwards": False,
    "scope": ("An addition after the 35 branches, as at D4a-05 and D4a-06; not a recut. branches.jsonl, crosslinks.jsonl, "
              "tree-D4.md, room-forms-D4a05.*, room-forms-D4a06.* and every D5 file stay as they are. New files: "
              "room-forms-D4a07.md, .jsonl and .tsv."),
}, ensure_ascii=False))
