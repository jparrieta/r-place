#!/usr/bin/env python3
"""Read-only. Rulings that place three themes, each with three concepts or more, are bags if a fourth placed theme
also reached three concepts. This prints, for each such non-bag ruling, the sentences of its why that speak of a
theme not kept or of the limit, so the line can be read and, where it was a bag, re-ruled.

    python3 out/_analysis/b4_limit_drop_scan.py
"""
import json
import re

for x in open("out/disagreements.jsonl", encoding="utf-8"):
    d = json.loads(x)
    if d["taxonomy"] == "item-is-a-bag" or not d["ruling"]:
        continue
    sup = d.get("support_by_theme") or {}
    sents = re.split(r"(?<=[.;])\s+", d.get("why") or "")
    if len(d["ruling"]) == 3 and min(len(sup.get(t, [])) for t in d["ruling"]) >= 3:
        hits = [s for s in sents if "not kept" in s or "limit" in s or "fourth" in s]
    else:
        hits = [s for s in sents if "left out together" in s or "by the limit" in s or "limit of three" in s]
    if hits:
        print("%s %s %s/%s %s" % (d["packet"], d["n"], d["sub"], d["theme_id"], {t: len(v) for t, v in sup.items()}))
        for s in hits:
            print("    " + s)
