#!/usr/bin/env python3
"""B2b-r3: append round 3's four waivers to out/return_waivers.jsonl (J, QB2-013, 13:47 Berlin): kept lines that
set item_is_a_bag true with also_present {} because no other theme reaches the three-concept floor. Checks each
named line against the raw return and the translated copy; refuses a second write. Dry run unless --write."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RD = "_fleet_raw/B2/round-3"
NAMED = [("P03-r3-2/r3.jsonl", 6), ("P03-r3-2/r3.jsonl", 10), ("P03-r3-2/r3.jsonl", 11), ("P03-r3-2/r6.jsonl", 6)]
REASON = "item_is_a_bag true with no theme at the three-concept floor (also_present {}); the placement scored as given"

wp = os.path.join(OUT, "return_waivers.jsonl")
have = [json.loads(x) for x in open(wp, encoding="utf-8") if x.strip()]
if any(w["round_dir"] == RD for w in have):
    sys.exit("round 3 waivers already written")
new = []
for f, n in NAMED:
    x = json.loads(open(os.path.join(OUT, RD, f), encoding="utf-8").read().splitlines()[n - 1])
    y = json.loads(open(os.path.join(OUT, "_analysis", "b2_r3_returns", f), encoding="utf-8").read().splitlines()[n - 1])
    if not (x.get("item_is_a_bag") and not x.get("also_present")):
        sys.exit("%s line %d is not a bag line with an empty also_present" % (f, n))
    new.append({"round_dir": RD, "file": f, "item": "%s/%s" % (y["sub"], y["theme_id"]), "line": n,
                "reason": REASON, "ruled_by": "J 2026-10-12 QB2-013"})
for w in new:
    print(json.dumps(w))
if "--write" in sys.argv:
    with open(wp, "a", encoding="utf-8") as fh:
        for w in new:
            fh.write(json.dumps(w, ensure_ascii=False) + "\n")
    print("return_waivers.jsonl now %d lines" % (len(have) + len(new)))
