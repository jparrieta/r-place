#!/usr/bin/env python3
"""D3b, G4: a pair must be a second room's accepted line on the same element. Checks every latest D3b ruling that
carries a pair: the pair exists in a ledger, belongs to another room, sits on the same element, and its own latest
ruling is accept. Prints each failure and a count. Writes nothing.

    python3 out/_analysis/d3b_pair_element_check.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


led = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations.jsonl")) + jl(os.path.join(OUT, "adaptations-recheck.jsonl"))}
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
n = bad = 0
for aid, r in last.items():
    if r.get("leg") != "D3b" or not r.get("pair"):
        continue
    n += 1
    l, p = led.get(aid), led.get(r["pair"])
    why = []
    if p is None:
        why.append("pair not in a ledger")
    else:
        if p["sub"] == l["sub"]:
            why.append("pair in the same room")
        if p.get("element") != l.get("element"):
            why.append(f"pair on {p.get('element')}, line on {l.get('element')}")
        pr = last.get(r["pair"])
        if not pr or pr.get("decision") != "accept":
            why.append(f"pair's latest ruling {pr.get('decision') if pr else 'none'}")
    if why:
        bad += 1
        print(f"{aid}  {l.get('element')}  pair {r['pair']}: {'; '.join(why)}")
print(f"[{n} D3b rulings with a pair; {bad} fail]")
