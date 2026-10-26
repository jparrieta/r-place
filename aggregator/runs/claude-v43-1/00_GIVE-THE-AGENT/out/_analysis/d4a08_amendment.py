#!/usr/bin/env python3
"""D4a-08: print the dated amendment (J, 26 October 2026, 21:05 and 21:06 Berlin) as a departures.jsonl line.

    python3 out/_analysis/d4a08_amendment.py >> out/departures.jsonl
"""
import json

print(json.dumps({
    "stage": "D4", "leg": "D4a-08", "date": "2026-10-26",
    "provision": "the room forms of D4a-05 to D4a-07 (departures.jsonl lines 11 to 14): rooms compared by their selected changes only; and the leg's close",
    "why": ("J read the D4a-07 cut and said, 26 October 2026, through the handler, 21:05 Berlin: \"How about using the "
            "code counts, dimensions for example, as well?\" and 21:06: \"Yes. Please also tell it not to close but write "
            "us so we can iterate.\" Required: beside the D4a-07 change profile, each room gets a code profile, its coded "
            "concepts lifted to the third-order themes, the fourth-order themes and the dimensions, as shares within each "
            "level; how the two blocks are combined is stated and logged before the run. The leg is not closed: the cut is "
            "written down and logged, and the analyst waits for J and the handler in this conversation; done.sh runs only "
            "when told."),
    "applies_backwards": False,
    "scope": ("An addition after the 35 branches, as at D4a-05 to D4a-07; not a recut. branches.jsonl, crosslinks.jsonl, "
              "tree-D4.md, room-forms-D4a05.*, room-forms-D4a06.*, room-forms-D4a07.* and every D5 file stay as they are. "
              "New files: room-forms-D4a08.md, .jsonl and .tsv."),
}, ensure_ascii=False))
