#!/usr/bin/env python3
"""D3b: the cited codes of named first-return lines (for example D3a-55 propose lines), with their last ruling, so
that a re-check line's codes can be checked against the room's accepted proposal (G61 (3)). Reads only.

    python3 out/_analysis/d3b_proposal_codes.py Thegreatblackhole-003 GrowTheTree-041
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
want = set(sys.argv[1:])
last = {}
for l in open(os.path.join(OUT, "adjudications.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    last[r["adaptation"]] = r
for l in open(os.path.join(OUT, "adaptations.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r["id"] in want:
        ev = r.get("evidence") or []
        if isinstance(ev, dict):
            ev = ev.get("codes") or []
        d = last.get(r["id"], {})
        print("%s  %s  codes %s  ruling %s/%s" % (r["id"], r["op"], ",".join(str(c).split(":")[-1] for c in ev),
                                                 d.get("decision"), d.get("kind")))
