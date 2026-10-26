#!/usr/bin/env python3
"""D4a-05: print the dated amendment (J, 26 October 2026) as a departures.jsonl line. Append by redirect.

    python3 out/_analysis/d4a05_amendment.py >> out/departures.jsonl
"""
import json

print(json.dumps({
    "stage": "D4", "leg": "D4a-05", "date": "2026-10-26",
    "provision": ("stage D4 sections 2 and 4 (a branch is keyed on shared change keys; a group that meets only at "
                  "the dimension or the bare target is a grouping, not a branch; branches may overlap), and the "
                  "D4a-04 decision that no join of the top-level branches is defensible under those rules"),
    "why": ("A dated amendment under J's ruling of 7 October, given by J through the handler after D5 closed. "
            "J, 26 October 2026, 17:27 Berlin: \"I need to tell it to make something with 4 to 8 big forms and then "
            "continue clustering down to 700.\" J, 18:01 Berlin: stage D6 builds on these 4 to 8 forms, with the 35 "
            "branches as the level below. The handler's instruction, on J's: rebuild the D4 tree with the room as "
            "the unit; each of the 705 rooms appears once; a room goes to the branch holding most of its selected "
            "changes, its other branches listed as secondary; arrows count through their third-order theme; rooms "
            "are compared at the third-order, fourth-order and dimension levels, each counting equally, by the mix "
            "of their changes and not their number; op and element do not count on their own; changes made by one "
            "room only do not dominate; no broad form without a shared pattern beyond breadth; 4 to 8 forms at the "
            "top where the split is clearest, comparable in size, the largest-to-smallest ratio reported and "
            "justified above 3; below each form, split level by level down to the rooms, each kept level justified "
            "as a split and not noise; the 21 rooms with no selected change stay together as the core."),
    "applies_backwards": False,
    "scope": ("Forward from D4a-05. The room tree is added above the 35 branches, which stay as the level below "
              "(J, 18:01). It recuts no branch, changes no key, member, cross-link, D5 account or the model "
              "(46384686...); branches.jsonl, crosslinks.jsonl and the forms stay as written. The room tree is "
              "written to its own files (room-tree-D4.*)."),
}, ensure_ascii=False))
