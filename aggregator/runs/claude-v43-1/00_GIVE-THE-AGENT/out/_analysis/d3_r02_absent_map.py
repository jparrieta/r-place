#!/usr/bin/env python3
"""D3a-49: write R02's absent map (R02-absent-map.json) from R02-absent-spec.txt, whose rows were checked by
d3_check_spec.py against d3_absent_cites_R02_1.txt to _3.txt. Each row: id|REJ|evidence. A REJ row names a line whose
concepts show R02, so the claim of absence fails (G2, G3, G54 and its reading 45). R02's absent lines are all
unobserved or not-testable and none is marked NONPORTABLE, so no specification or particular is named. Refuses a
repeated id or an unknown class. Writes the map only.

  python3 out/_analysis/d3_r02_absent_map.py
"""
import json

SPEC = "out/_analysis/d3_rulings/R02-absent-spec.txt"
OUT = "out/_analysis/d3_rulings/R02-absent-map.json"
RULE = "G2, G3 and G54, quotes read"
rej = {}
for ln in open(SPEC, encoding="utf-8"):
    if not ln.strip():
        continue
    aid, cls, ev = ln.rstrip("\n").split("|", 2)
    assert aid not in rej, aid
    if cls != "REJ":
        raise SystemExit("unknown class %r for %s" % (cls, aid))
    rej[aid] = ("%s: %s; R02 is shown, a member acting for a room toward another room, so the claim of absence fails"
                % (RULE, ev))
json.dump({"reject": rej, "specification": {}, "particular": {}}, open(OUT, "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("wrote %s: reject %d, specification 0, particular 0" % (OUT, len(rej)))
