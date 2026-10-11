#!/usr/bin/env python3
"""B2 check legs: append the items that divided readers in a round to out/exemplar_candidates.jsonl
(stage B2 section 4: stage B3's exemplar arm draws from them, not from clear cases).

Usage: python3 out/_analysis/b2_exemplar_candidates.py --round 1 --readers r12,r15,r16 [--write]
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


ap = argparse.ArgumentParser()
ap.add_argument("--round", required=True)
ap.add_argument("--readers", required=True)
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
raw = os.path.join(OUT, "_fleet_raw", "B2", "round-%s" % a.round)
auth = {r["item"]: r for r in jl(os.path.join(OUT, "author_items.jsonl"))}
lines = {}
for rd in a.readers.split(","):
    p = [os.path.join(dp, f) for dp, _, fs in os.walk(raw) for f in fs if f == rd + ".jsonl"][0]
    lines[rd] = {"%s/%s" % (x["sub"], x["theme_id"]): x for x in jl(p)}
score = json.load(open(os.path.join(OUT, "_analysis", "b2_r%s_score.json" % a.round)))
rows = []
for it in score["items_with_disagreement"]:
    rows.append({"key": it, "sub": it.split("/")[0], "theme_id": it.split("/")[1], "round": int(a.round),
                 "author": auth[it]["third_order"], "author_confidence": auth[it]["confidence"],
                 "readers": {rd: lines[rd][it]["third_order"] for rd in lines},
                 "themes_in_play": sorted({t for rd in lines for t in lines[rd][it]["third_order"]} | set(auth[it]["third_order"])),
                 "source": auth[it].get("source")})
print("%d candidates" % len(rows))
if a.write:
    with open(os.path.join(OUT, "exemplar_candidates.jsonl"), "a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("appended to out/exemplar_candidates.jsonl")
