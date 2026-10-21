#!/usr/bin/env python3
"""D3a-52: read K04-absent-spec.txt ('id|class|evidence', classes REJ and P-G6; K04 has no observed-absent or
not-needed line, so no SPEC) and write K04-absent-map.json for d3_absent_rulings.py. Writes the map only.

  python3 out/_analysis/d3_k04_absent_map.py
"""
import json

SPEC = "out/_analysis/d3_rulings/K04-absent-spec.txt"
OUT = "out/_analysis/d3_rulings/K04-absent-map.json"
RULE = "G2, G3, G56 and G56a, quotes read"
rej, spec, part = {}, {}, {}
for ln in open(SPEC, encoding="utf-8"):
    if not ln.strip():
        continue
    aid, cls, ev = ln.rstrip("\n").split("|", 2)
    assert aid not in rej and aid not in part, aid
    if cls == "REJ":
        rej[aid] = ("%s: %s; K04 is shown, members acting in canvas talk as the body their community was before the "
                    "canvas, so the claim of absence fails" % (RULE, ev))
    elif cls == "P-G6":
        part[aid] = "%s: %s; the line is marked NONPORTABLE and fails portability, a particular (G6)" % (RULE, ev)
    else:
        raise SystemExit("unknown class %r for %s" % (cls, aid))
json.dump({"reject": rej, "specification": spec, "particular": part}, open(OUT, "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("wrote %s: reject %d, specification %d, particular %d" % (OUT, len(rej), len(spec), len(part)))
