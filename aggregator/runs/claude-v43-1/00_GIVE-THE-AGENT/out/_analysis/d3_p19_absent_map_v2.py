#!/usr/bin/env python3
"""D3a-53: version 2 of d3_p19_absent_map.py, reading P19-absent-spec-v2.txt (the first spec plus the four lines
the guard's second look added) and writing P19-absent-map-v2.json. Classes and reasons are as in version 1. Writes
the map only.

  python3 out/_analysis/d3_p19_absent_map_v2.py
"""
import json

SPEC = "out/_analysis/d3_rulings/P19-absent-spec-v2.txt"
OUT = "out/_analysis/d3_rulings/P19-absent-map-v2.json"
RULE = "G2, G3 and G57, quotes read"
rej, spec, part = {}, {}, {}
for ln in open(SPEC, encoding="utf-8"):
    if not ln.strip():
        continue
    aid, cls, ev = ln.rstrip("\n").split("|", 2)
    assert aid not in rej and aid not in part, aid
    if cls == "REJ":
        rej[aid] = ("%s: %s; P19 is shown, one room's work, or a wish to place one, inside another room's ground or "
                    "under its protection, with that room as the one that may allow it, so the claim of absence fails"
                    % (RULE, ev))
    elif cls == "P-G6":
        part[aid] = "%s: %s; the line is marked NONPORTABLE and fails portability, a particular (G6)" % (RULE, ev)
    else:
        raise SystemExit("unknown class %r for %s" % (cls, aid))
json.dump({"reject": rej, "specification": spec, "particular": part}, open(OUT, "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("wrote %s: reject %d, specification %d, particular %d" % (OUT, len(rej), len(spec), len(part)))
