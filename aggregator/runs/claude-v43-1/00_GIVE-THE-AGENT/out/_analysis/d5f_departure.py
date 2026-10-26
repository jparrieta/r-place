#!/usr/bin/env python3
"""D5a-36: the dated amendment for stage D5 run once more, one account per room form. Prints the departures.jsonl line.

    python3 out/_analysis/d5f_departure.py >> out/departures.jsonl
"""
import json

print(json.dumps({
    "stage": "D5", "leg": "D5a-36", "date": "2026-10-26",
    "provision": "stage D5's unit (one account per branch of branches.jsonl, legs D5a-01 to D5a-35, then D5b)",
    "why": "The principal investigator's message, on J's instruction, after D4a-08 closed (22:09 UTC): J, 26 October 2026, "
           "22:18 Berlin: \"6 it is.\" J, 22:51 Berlin: \"ok fine. so let's continue.\" Earlier, J, 18:01 Berlin: stage D6 "
           "builds on the forms, with the 35 branches as the level below; J, 18:36 Berlin: \"you will still need to run D5 on "
           "the 4 to 8\". Required: D5 runs once more, one leg per form of the six-form cut (room-forms-D4a08c.*, "
           "room-forms-allocation.md, room-forms-tree-*), D5a-36 to D5a-41 for forms A to F, each writing "
           "forms/room-form-<letter>-account.md the way D5 wrote the branch accounts, with the stage's rules (section 1's "
           "arithmetic before any claim of absence; the canvas only where declared). Each account says what the form's rooms "
           "do and where they specify, restrict or replace the global model, element by element and arrow by arrow, with two "
           "or three rooms that show it best and one that shows it least well; which of the 35 branches its rooms come from; "
           "in its restrict lines, the arrow failing apart from the record unable to show it; its split below the form from "
           "room-forms-tree-rooms.tsv, only as far as it reads as a split; and its thin and core rooms named, weighing less.",
    "applies_backwards": False,
    "scope": "An addition after D5b, not a recut. The 35 branch accounts (forms/F01-account.md to F35-account.md), "
             "branches-D5.jsonl, waterfall-D5.md, survival-D5.md, handback-D5.md, the D4 files and the room-forms files "
             "stay as they are. New files: forms/room-form-A-account.md to forms/room-form-F-account.md and "
             "room-forms-D5.jsonl, one line per form.",
}, ensure_ascii=False))
