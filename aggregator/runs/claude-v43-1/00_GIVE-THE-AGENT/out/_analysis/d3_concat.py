#!/usr/bin/env python3
"""D3a-34: join spec part files into one spec file, in the order given, refusing a repeated id.

  python3 out/_analysis/d3_concat.py --out out/_analysis/d3_rulings/A07-inst-spec.txt \
      --parts out/_analysis/d3_rulings/A07-inst-spec-1.txt out/_analysis/d3_rulings/A07-inst-spec-2.txt
"""
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--parts", nargs="+", required=True)
a = ap.parse_args()
rows, seen = [], set()
for p in a.parts:
    for l in open(p, encoding="utf-8"):
        if l.strip():
            i = l.split("|", 1)[0]
            assert i not in seen, i
            seen.add(i)
            rows.append(l.rstrip("\n"))
with open(a.out, "w", encoding="utf-8") as f:
    f.write("\n".join(rows) + "\n")
print("wrote", len(rows), "rows to", a.out)
