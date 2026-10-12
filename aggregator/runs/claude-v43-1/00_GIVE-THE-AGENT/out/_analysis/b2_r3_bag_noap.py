#!/usr/bin/env python3
"""B2b-r3: list the kept round-3 return lines that set item_is_a_bag true and name no also_present (validate.py's
error), with the translated item, the placement and the reader's why. Reads only."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
raw = os.path.join(OUT, "_fleet_raw", "B2", "round-3")
kept = json.load(open(os.path.join(raw, "RESCUE-2026-10-12.json"), encoding="utf-8"))["packets"]
for pk in sorted(kept):
    for slot in kept[pk]["kept"]:
        tr = [json.loads(l) for l in open(os.path.join(OUT, "_analysis", "b2_r3_returns", pk, slot + ".jsonl"), encoding="utf-8") if l.strip()]
        for i, l in enumerate(open(os.path.join(raw, pk, slot + ".jsonl"), encoding="utf-8"), 1):
            x = json.loads(l)
            if x.get("item_is_a_bag") and not x.get("also_present"):
                y = tr[i - 1]
                print("%s/%s.jsonl line %d: %s/%s (%s) placed %s; also_present %r; multi %s" % (
                    pk, slot, i, y["sub"], y["theme_id"], x["theme_id"], ",".join(x["third_order"]), x.get("also_present"), x.get("multi")))
                for k, v in (x.get("why") or {}).items():
                    print("    why %s: %s" % (k, v))
