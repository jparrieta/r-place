#!/usr/bin/env python3
"""Read-only. A ruling that keeps fewer than four themes can still have been a bag if themes of three concepts or
more were dropped on a tie. This prints, for each non-bag ruling, the sentences of its why that drop themes on a tie
or as 'not kept' and that also name a count of three concepts or more, for reading.

    python3 out/_analysis/b4_tie_drop_scan.py
"""
import json
import re

BIG = r"\b(three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+) concepts\b"
for x in open("out/disagreements.jsonl", encoding="utf-8"):
    d = json.loads(x)
    if d["taxonomy"] == "item-is-a-bag" or not d["ruling"]:
        continue
    sup = d.get("support_by_theme") or {}
    big = sum(1 for t in d["ruling"] if len(sup.get(t, [])) >= 3)
    sents = re.split(r"(?<=[.;])\s+", d.get("why") or "")
    hits = [s for s in sents if ("not kept" in s or "none is kept" in s or "neither is kept" in s
                                 or "keeps none" in s or "left out" in s) and re.search(BIG, s)]
    if hits:
        print("%s %s %s/%s ruling-themes-at-3: %d %s" % (d["packet"], d["n"], d["sub"], d["theme_id"], big,
                                                       {t: len(v) for t, v in sup.items()}))
        for s in hits:
            print("    " + s)
