#!/usr/bin/env python3
"""D3a-48: write P06's absent map (P06-absent-map.json) from P06-absent-spec.txt, whose rows were checked by
d3_check_spec.py against d3_absent_cites_P06_v2.txt. Each row: id|REJ|evidence or id|P-G6|evidence. A REJ row names a
line whose concepts show P06, so the claim of absence fails (G2, G3, G53); a P-G6 row is a NONPORTABLE line whose
concepts do not show P06 in this room's record, a particular (G6). P06's absent lines are all unobserved or
not-testable, so no specification is named. Refuses a repeated id or an unknown class. Writes the map only.

  python3 out/_analysis/d3_p06_absent_map.py
"""
import json

SPEC = "out/_analysis/d3_rulings/P06-absent-spec.txt"
OUT = "out/_analysis/d3_rulings/P06-absent-map.json"
RULE = "G2, G3 and G53, quotes read"
rej, part = {}, {}
for ln in open(SPEC, encoding="utf-8"):
    if not ln.strip():
        continue
    aid, cls, ev = ln.rstrip("\n").split("|", 2)
    assert aid not in rej and aid not in part, aid
    if cls == "REJ":
        rej[aid] = ("%s: %s; P06 is shown, members of the room working out who changed the room's work or why, "
                    "so the claim of absence fails" % (RULE, ev))
    elif cls == "P-G6":
        part[aid] = "%s: %s" % (RULE, ev)
    else:
        raise SystemExit("unknown class %r for %s" % (cls, aid))
json.dump({"reject": rej, "specification": {}, "particular": part}, open(OUT, "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("wrote %s: reject %d, specification 0, particular %d" % (OUT, len(rej), len(part)))
