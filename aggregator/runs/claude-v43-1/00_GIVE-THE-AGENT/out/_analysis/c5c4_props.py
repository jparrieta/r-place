#!/usr/bin/env python3
"""C5c-04, pass 8: N05's boundary in c5_propositions.json takes T4-002's accepted advice (a quiet week before the canvas
does not show when a room began). The `old` must occur once. Writes the spec only; c5_propositions.py --replace then
rewrites propositions.jsonl.

    python3 out/_analysis/c5c4_props.py [--write]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sp = os.path.join(ROOT, "out", "_analysis", "c5_propositions.json")
spec = json.load(open(sp, encoding="utf-8"))
old = "Subs opened for the canvas, which have no prior business to protect (78 of 705 rooms have no posts in the week before)."
new = ("Subs opened for the canvas, which have no prior business to protect; the record does not show how many there are "
       "(78 of 705 rooms have no posts in the week before, and when they began is not shown).")
t = spec["N05"]["boundary"]
if t.count(old) != 1:
    sys.exit("N05 boundary: old text found %d times" % t.count(old))
spec["N05"]["boundary"] = t.replace(old, new)
print(spec["N05"]["boundary"])
if "--write" in sys.argv:
    json.dump(spec, open(sp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("c5_propositions.json written")
