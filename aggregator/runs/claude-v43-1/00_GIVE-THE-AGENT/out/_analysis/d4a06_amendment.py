#!/usr/bin/env python3
"""D4a-06: print the dated amendment (J, 26 October 2026, 19:50 Berlin) as a departures.jsonl line. Append by redirect.

    python3 out/_analysis/d4a06_amendment.py >> out/departures.jsonl
"""
import json

print(json.dumps({
    "stage": "D4", "leg": "D4a-06", "date": "2026-10-26",
    "provision": "the room forms of D4a-05 (departures.jsonl lines 11 and 12), their method",
    "why": ("J read the analyst's interview answers to his four questions after D4a-05 and said, 26 October 2026, "
            "19:50 Berlin, through the handler: \"Go ahead this sounds good.\" So the top cut is redone with the fixes "
            "proposed: a floor on thin rooms, stated before the run, below which a room does not shape the forms and is "
            "placed afterwards; J's placement rule taken literally, each room to the form whose signature holds most of "
            "its selected changes, ties and secondary forms listed, no room duplicated, and the rooms that move against "
            "a placement by the whole mix counted; the count from 4 to 8 chosen by measures that do not favour more "
            "groups, the gap between Ward merge heights and stability on matched subsamples without replacement against "
            "a shuffled null, both given if they disagree; the members of each form read as rooms; and the raiding and "
            "takeover rooms and the rich rooms the model fit without change said where they fall."),
    "applies_backwards": False,
    "scope": ("An addition after the 35 branches, as at D4a-05; not a recut. branches.jsonl, crosslinks.jsonl, "
              "tree-D4.md, room-forms-D4a05.* and every D5 file stay as they are. New files: room-forms-D4a06.md, "
              ".jsonl and .tsv. The leg stops at the top cut; the split below waits for J's talk."),
}, ensure_ascii=False))
