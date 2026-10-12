#!/usr/bin/env python3
"""B2b-r3-p3: the rechecks the second freeze edits (scheme_edits 303 to 306) owe, from
out/_analysis/b2_rechecks_owed_freeze2.txt, recorded with b2_rechecks_freeze.py's machinery and the reasons below.
None moves. The items on T3-009 were read whole for edits 305 and 306 (thanks to allies and reflection against
the celebrating, by count); the items holding a link to the finished work for edits 303 and 304.
Dry run unless --write; --max N slices the calls."""
import importlib.util, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = importlib.util.spec_from_file_location("rf", os.path.join(ROOT, "out", "_analysis", "b2_rechecks_freeze.py"))
rf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rf)

rf.WHY = {
 "edit:303": ("the T3-038/T3-070 question now keeps T3-038 for the work in progress and points a link that only shows "
              "the finished work at T3-026; the item's placement does not rest on such a link"),
 "edit:304": ("the T3-070/T3-038 question now keeps T3-038 for the work in progress and points a link that only shows "
              "the finished work at T3-026; the item's placement does not rest on such a link"),
 "edit:305": ("T3-072's decide_when_both now counts thanks to allies against the celebrating, as T3-009's does; the "
              "item's celebrating holds more than any thanks to allies"),
 "edit:306": ("T3-157's decide_when_both now counts the reflection against the celebrating, as T3-009's does; the "
              "item's celebrating holds more than any reflection on working together"),
}
rf.ITEM = {
 "n64/t02": ("c0014 (credit with a link to see the finished logo) and c0015 (the link) now point to the finished work "
             "(T3-026, T3-009) and leave T3-038's support; c0011 and c0012 (built from the image, started at stated "
             "coordinates) still outnumber the one call (c0010), so T3-038 stands"),
 "mcgillrobotics/t02": ("two concepts celebrate (c0005, c0006) against one thanking participants (c0004) and the end "
                        "marked (c0003); no ally thanked and no reflection, so T3-009 stands"),
 "montenegro/t04": "three concepts celebrate and congratulate (c0011, c0012, c0013); no ally and no reflection; T3-009 stands",
 "mordhau/t05": ("praise for the small sub's work (c0011) with the forums credited (c0016) and the logo said to stand "
                 "(c0026); no ally thanked and no reflection, so T3-009 stands"),
 "redhotchilipeppers/t09": ("six concepts celebrate (c0086, c0087, c0100, c0104, c0106, c0129) against one thanking "
                            "Discord friends and the neighbour (c0101); T3-009 stands, T3-043 for the props (c0102)"),
 "ukraine/t07": ("praise and the final result (c0036, c0049) against one remark on teaming up (c0047) and the end "
                 "marked (c0048); T3-009 stands"),
}
rf.CODES = {"furry/t10": rf.CODES["furry/t10"], "n64/t02": {"T3-038": ["c0011", "c0012"]}}

_open = open


def _owed_file(path, *a, **k):
    if path.endswith("b2_rechecks_owed_freeze.txt"):
        path = path.replace("b2_rechecks_owed_freeze.txt", "b2_rechecks_owed_freeze2.txt")
    return _open(path, *a, **k)


rf.open = _owed_file
if __name__ == "__main__":
    rf.main()
