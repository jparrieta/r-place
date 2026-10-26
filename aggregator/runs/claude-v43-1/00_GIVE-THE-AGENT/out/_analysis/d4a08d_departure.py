#!/usr/bin/env python3
"""D4a-08, J's ruling of 22:18 Berlin: the six forms of D4a-08c are the cut. Prints the departures.jsonl line.

    python3 out/_analysis/d4a08d_departure.py >> out/departures.jsonl
"""
import json

J = ("6 it is. Please tell the agent to document how they are allocated and the allocation it did earlier, as we need "
     "this soon. Also they need to push the full analysis down to the leaves so we get all the further cuts at smaller "
     "levels. Not that they needed it, but we do for the graph.")
print(json.dumps({
    "stage": "D4", "leg": "D4a-08", "date": "2026-10-26",
    "provision": "the room forms of D4a-05 to D4a-08b (departures.jsonl lines 11 to 15): which cut is the room forms, and "
                 "how far the room-forms tree is written",
    "why": "J read D4a-08c and ruled, 26 October 2026, through the handler, 22:18 Berlin: \"%s\" Required: the six forms "
           "of D4a-08c (changes two thirds, codes one third; the core placed by its codes) are the cut of the room forms; "
           "the allocation is documented in room-forms-allocation.md, with the earlier allocations of D4a-05 to D4a-08c "
           "in order; and the same weighting is written down to the single rooms, all 705 placed as they were placed, as "
           "a linkage, a Newick tree and a table of each room's label at every cut below the six. The splits below the "
           "forms are not named or argued. The leg is not closed until J or the handler says so." % J,
    "applies_backwards": False,
    "scope": "An addition after the 35 branches, as at D4a-05 to D4a-08; not a recut. branches.jsonl, crosslinks.jsonl, "
             "tree-D4.md, room-forms-D4a05.* to room-forms-D4a08c.* and every D5 file stay as they are. The earlier room-form "
             "cuts stay as written and are superseded, not withdrawn. New files: room-forms-allocation.md and the "
             "room-forms-tree files.",
}, ensure_ascii=False))
