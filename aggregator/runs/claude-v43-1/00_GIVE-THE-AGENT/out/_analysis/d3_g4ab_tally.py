#!/usr/bin/env python3
"""D3a-11: tally the G4a backward re-ruling files (out/_analysis/d3_rulings/G4aB-*.jsonl) by what each
re-ruling names. A re-ruling of kind elaboration is a re-pairing (kind kept). A specification is counted under
the ids its reason names after 'naming' (another element or arrow), or under 'own statement' when it names none.
Also prints the ops of the re-ruled lines, read from adaptations.jsonl.

  python3 out/_analysis/d3_g4ab_tally.py [--prefix G4aB-] [--show]
"""
import argparse
import collections
import glob
import json
import os
import re


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default="G4aB-")
    ap.add_argument("--show", action="store_true", help="print the ids under each heading")
    ap.add_argument("--total", action="store_true",
                    help="also sum over every file of the prefixes (comma-separated), each named id counted apart")
    a = ap.parse_args()
    ops = {}
    for ln in open("out/adaptations.jsonl", encoding="utf-8"):
        if ln.strip():
            x = json.loads(ln)
            ops[x["id"]] = x.get("op")
    total = 0
    named = collections.Counter()
    paths = sorted(p for pre in a.prefix.split(",") if pre
                   for p in glob.glob(f"out/_analysis/d3_rulings/{pre}*.jsonl"))
    for path in paths:
        rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
        by = collections.defaultdict(list)
        byop = collections.Counter()
        for r in rows:
            byop[ops.get(r["adaptation"], "?")] += 1
            if r.get("kind") == "elaboration":
                key = "re-paired (kind kept)"
            else:
                m = re.search(r"naming ([A-Z]\d\d(?:(?:, | and )[A-Z]\d\d)*)", r["reason"])
                key = "names " + m.group(1) if m else "own statement"
                for e in (re.findall(r"[A-Z]\d\d", m.group(1)) if m else ["own statement"]):
                    named[e] += 1
                if m and len(re.findall(r"[A-Z]\d\d", m.group(1))) > 1:
                    named["(lines naming two or more)"] += 1
            if key == "re-paired (kind kept)":
                named[key] += 1
            by[key].append(r["adaptation"])
        total += len(rows)
        print(f"{os.path.basename(path)}: {len(rows)} lines; ops {dict(byop)}")
        for k in sorted(by, key=lambda k: -len(by[k])):
            print(f"   {k}: {len(by[k])}" + (f"  {' '.join(by[k])}" if a.show else ""))
    print(f"all files: {total} re-rulings")
    if a.total:
        print("over all files, each named id counted apart:")
        for k, n in sorted(named.items(), key=lambda kv: -kv[1]):
            print(f"   {k}: {n}")


if __name__ == "__main__":
    main()
