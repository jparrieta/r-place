#!/usr/bin/env python3
"""C2c, read-only: for the concepts a reviewer's error names, what the record holds. Per concept: its hour, the
coder's label and the passage whole, the assignment line(s) that cite it (second-order theme, third-order theme),
and the elements of c2_elements_p3.json whose themes take it. With --first, the hours of each element's first cited
concept in each named room, so an order claim can be read against the room.

    python3 out/_analysis/c2c_concept_check.py metroid:c0001 metroid:c0002 [--first P01,P03]
"""
import argparse, collections, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("keys", nargs="+")
ap.add_argument("--first", default="")
a = ap.parse_args()
keys = [tuple(k.split(":", 1)) for k in a.keys]
subs = sorted(set(s for s, _ in keys))
els = json.load(open(os.path.join(OUT, "_analysis", "c2_elements_p3.json"), encoding="utf-8"))["elements"]
by_theme = collections.defaultdict(list)
for e in els:
    if e["id"] == "P17n":
        continue
    for t in e.get("themes") or []:
        by_theme[t].append(e["id"])
codes = {}
for s in subs:
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--sub", s, "--json",
                        "--limit", "100000"], cwd=ROOT, capture_output=True, text=True)
    for l in p.stdout.splitlines():
        if l.startswith("{"):
            c = json.loads(l)
            codes[(c["sub"], c["code_id"])] = c
cites = collections.defaultdict(list)
first = collections.defaultdict(dict)
want = [x for x in a.first.split(",") if x]
for l in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r["sub"] not in subs:
        continue
    for t, cs in (r.get("support_by_theme") or {}).items():
        for c in cs:
            cites[(r["sub"], c)].append((r["theme_id"], t))
            for e in by_theme.get(t, []):
                h = (codes.get((r["sub"], c)) or {}).get("hour")
                if e in want and h is not None:
                    f = first[r["sub"]].get(e)
                    if f is None or h < f[0]:
                        first[r["sub"]][e] = (h, c, t)
for k in keys:
    c = codes.get(k) or {}
    print("== %s/%s h%s  [%s]" % (k[0], k[1], c.get("hour"), c.get("first_order") or c.get("label") or ""))
    print("   %s" % " ".join(str(c.get("text") or "").split()))
    for tid, t in cites.get(k, []):
        print("   cited: %s under %s -> elements %s" % (tid, t, ", ".join(by_theme.get(t, [])) or "none"))
    if not cites.get(k):
        print("   cited under no third-order theme")
for s in subs:
    if want:
        print("first concepts in %s: %s" % (s, "; ".join("%s h%s %s (%s)" % (e, first[s][e][0], first[s][e][1], first[s][e][2])
                                                         if e in first[s] else "%s none" % e for e in want)))
