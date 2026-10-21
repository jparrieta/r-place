#!/usr/bin/env python3
"""D3a-51: write K03's absent map (K03-absent-map.json) from K03-absent-spec.txt, whose rows were checked by
d3_check_spec.py against d3_absent_cites_K03_1.txt to _4.txt. Each row: id|REJ|evidence, id|P-G6|evidence or
id|SPEC|evidence. A REJ row names a line whose concepts show K03, so the claim of absence fails (G2, G3, G55 and its
reading 11); a P-G6 row is a NONPORTABLE line whose concepts do not show K03, a particular (G6); a SPEC row is an
evidenced absence (not-needed) whose concepts show no quarrel from before the canvas, a specification. Refuses a
repeated id or an unknown class. Writes the map only.

  python3 out/_analysis/d3_k03_absent_map.py
"""
import json

SPEC = "out/_analysis/d3_rulings/K03-absent-spec.txt"
OUT = "out/_analysis/d3_rulings/K03-absent-map.json"
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
