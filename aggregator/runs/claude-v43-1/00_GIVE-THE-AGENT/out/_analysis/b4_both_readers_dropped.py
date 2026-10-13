#!/usr/bin/env python3
"""List rulings in a packet that leave out a theme both readers placed.

A check for the reading first applied at B4a-07 (kanye t28, msu t11): a theme
both readers placed, with a concept of its own, is not dropped by the level rule
on a placement count that only my B1 tips. The script only lists candidates;
each is read by hand. Bags and unresolved lines are skipped.

Usage: python3 out/_analysis/b4_both_readers_dropped.py --packet 7 [--leg B4a-07]
"""
import argparse
import json
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--packet", type=int, required=True)
ap.add_argument("--leg", default=None)
args = ap.parse_args()

path = Path(__file__).resolve().parents[1] / "disagreements.jsonl"
rows = []
for line in path.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    d = json.loads(line)
    if d.get("packet") != args.packet:
        continue
    if args.leg and d.get("leg") != args.leg:
        continue
    if d.get("unresolved") or d.get("taxonomy") == "item-is-a-bag":
        continue
    readers = d.get("readers") or [[], []]
    if len(readers) < 2:
        continue
    both = set(readers[0]) & set(readers[1])
    dropped = sorted(t for t in both if t not in (d.get("ruling") or []))
    if dropped:
        rows.append((d.get("n"), d.get("sub"), d.get("theme_id"), d.get("class"),
                     dropped, d.get("ruling"), d.get("b1"), d.get("taxonomy")))

for r in rows:
    print(f"{r[0]}\t{r[1]} {r[2]}\tclass {r[3]}\tdropped {','.join(r[4])}\truling {','.join(r[5])}\tb1 {','.join(r[6] or [])}\t{r[7]}")
print(f"[{len(rows)} rulings leave out a theme both readers placed]")
