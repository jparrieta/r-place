#!/usr/bin/env python3
"""D3a-33: write an absent map's reasons as spec rows ('id|CLASS|reason'), so d3_spec_quotes.py can check their quotes.

  python3 out/_analysis/d3_map_to_spec.py --map out/_analysis/d3_rulings/A06-absent-map.json --out out/_analysis/d3_rulings/A06-absent-map-check.txt
"""
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("--map", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
m = json.load(open(a.map, encoding="utf-8"))
rows = [f"{i}|{cls.upper()}|{reason}" for cls, d in m.items() for i, reason in d.items()]
with open(a.out, "w", encoding="utf-8") as f:
    f.write("\n".join(rows) + "\n")
print("wrote", len(rows), "rows to", a.out)
