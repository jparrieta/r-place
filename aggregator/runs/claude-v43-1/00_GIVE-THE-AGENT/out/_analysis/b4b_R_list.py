#!/usr/bin/env python3
"""B4b-p2, read-only: stratum R's items with their class, packet, taxonomy and the placements each already had
(reading A, reading B, my B1), from disagreements.jsonl; for the notes and for the check leg's diagnostic.

    python3 out/_analysis/b4b_R_list.py
"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "out")
jl = lambda p: [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]
dg = {(x["sub"], x["theme_id"]): x for x in jl("disagreements.jsonl")}
for r in jl("sample-B4-R.jsonl"):
    d = dg[(r["sub"], r["theme_id"])]
    rd = d.get("readers") or [[], []]
    print("%d\t%s\tclass %s\tpacket %s\t%s\t%s %s\tA %s\tB %s\tB1 %s" % (
        r["order"], r["item"], d.get("class"), d.get("packet"), d.get("taxonomy"), d.get("theme") or "", d.get("field") or "",
        ",".join(rd[0]), ",".join(rd[1]) if len(rd) > 1 else "", ",".join(d.get("b1") or [])))
