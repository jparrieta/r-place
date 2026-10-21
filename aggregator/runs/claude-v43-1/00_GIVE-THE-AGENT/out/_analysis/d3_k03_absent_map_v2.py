#!/usr/bin/env python3
"""D3a-51: version 2 of d3_k03_absent_map.py, reading K03-absent-spec-v2.txt (the first spec plus the two rows the
guard's second look added) and writing K03-absent-map-v2.json. Classes and reasons are as in version 1. Writes the map
only.

  python3 out/_analysis/d3_k03_absent_map_v2.py
"""
import json

SPEC = "out/_analysis/d3_rulings/K03-absent-spec-v2.txt"
OUT = "out/_analysis/d3_rulings/K03-absent-map-v2.json"
RULE = "G2, G3 and G55, quotes read"
rej, spec, part = {}, {}, {}
for ln in open(SPEC, encoding="utf-8"):
    if not ln.strip():
        continue
    aid, cls, ev = ln.rstrip("\n").split("|", 2)
    assert aid not in rej and aid not in spec and aid not in part, aid
    if cls == "REJ":
        rej[aid] = ("%s: %s; K03 is shown, members bringing in a quarrel from before the canvas, so the claim of "
                    "absence fails" % (RULE, ev))
    elif cls == "SPEC":
        spec[aid] = ("%s: %s; the absence is evidenced, since the concepts show no quarrel from before the canvas, "
                     "a specification" % (RULE, ev))
    elif cls == "P-G6":
        part[aid] = "%s: %s; a particular (G6)" % (RULE, ev)
    else:
        raise SystemExit("unknown class %r for %s" % (cls, aid))
json.dump({"reject": rej, "specification": spec, "particular": part}, open(OUT, "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("wrote %s: reject %d, specification %d, particular %d" % (OUT, len(rej), len(spec), len(part)))
