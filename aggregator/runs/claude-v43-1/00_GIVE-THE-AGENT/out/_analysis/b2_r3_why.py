#!/usr/bin/env python3
"""B2b-r3: print the round-3 readers' lines (placement, confidence, why, also_present keys, why_not_one) for
the items named on the command line, from the translated copies in out/_analysis/b2_r3_returns/. Reads only.
    python3 out/_analysis/b2_r3_why.py guatemala/t02 nVade/t04 ..."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "out", "_analysis", "b2_r3_returns")
want = set(sys.argv[1:])
for pk in sorted(os.listdir(RAW)):
    for f in sorted(os.listdir(os.path.join(RAW, pk))):
        for x in (json.loads(l) for l in open(os.path.join(RAW, pk, f), encoding="utf-8") if l.strip()):
            it = "%s/%s" % (x["sub"], x["theme_id"])
            if it not in want:
                continue
            ml = x.get("multiplacement_log") or {}
            print("%s %s/%s %s conf=%s bag=%s ap=%s" % (it, pk, f[:-6], ",".join(x["third_order"]), x.get("confidence"),
                  x.get("item_is_a_bag"), ",".join(sorted((x.get("also_present") or {}).keys())) or "-"))
            for k, v in (x.get("why") or {}).items():
                print("    why %s: %s" % (k, v))
            if ml.get("why_not_one"):
                print("    why_not_one: %s" % ml["why_not_one"])
