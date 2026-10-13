"""List rulings where a placed theme has no concept of its own.

Rule 0 (as amended, J 2026-10-11) needs each placed theme to rest on concepts
of its own. b4_rule_append.py refuses only identical lists; this script finds
every placed theme whose support is wholly contained in the other placed
themes' support. Read-only.

Usage: python3 out/_analysis/b4_own_support_check.py [--leg B4a-03]
"""
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("--leg", default=None)
args = ap.parse_args()

rows = [json.loads(l) for l in open("out/disagreements.jsonl")]
found = 0
for d in rows:
    if args.leg and d.get("leg") != args.leg:
        continue
    ruling = d.get("ruling") or []
    sup = d.get("support_by_theme") or {}
    if len(ruling) < 2:
        continue
    for t in ruling:
        mine = set(sup.get(t) or [])
        others = set()
        for u in ruling:
            if u != t:
                others |= set(sup.get(u) or [])
        if mine and mine <= others:
            found += 1
            print(d.get("sub"), d.get("theme_id"), "|", t, sorted(mine), "| ruling", ruling)
print("themes without a concept of their own:", found)
