#!/usr/bin/env python3
"""D3b: find a pair for an elaboration. Lists the accepted lines of one element (both ledgers, latest ruling of each)
whose ruling reason or line 'how' matches a pattern, with room, op, kind and the first 200 characters of the reason.
Writes nothing.

    python3 out/_analysis/d3b_pair_search.py --element P02 --grep "chat|discord" [--kind elaboration] [--limit 40]
"""
import argparse, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--grep", required=True)
ap.add_argument("--kind")
ap.add_argument("--limit", type=int, default=40)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


led = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations.jsonl")) + jl(os.path.join(OUT, "adaptations-recheck.jsonl"))}
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
pat = re.compile(a.grep, re.I)
n = 0
for aid, r in last.items():
    l = led.get(aid)
    if not l or l.get("element") != a.element or r.get("decision") != "accept":
        continue
    if a.kind and r.get("kind") != a.kind:
        continue
    text = (r.get("reason") or "") + " " + (l.get("how") or "")
    if not pat.search(text):
        continue
    n += 1
    if n <= a.limit:
        print(f"{aid}  {l['sub']}  {l['op']}  {r.get('kind')}  {(r.get('reason') or '')[:200]}")
print(f"[{n} matching accepted lines on {a.element}; {min(n, a.limit)} shown]")
