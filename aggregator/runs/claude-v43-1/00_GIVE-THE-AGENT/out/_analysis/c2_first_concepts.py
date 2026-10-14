#!/usr/bin/env python3
"""C2, read-only: the concepts behind an order test, for reading a mechanism and its failure clause.

    python3 out/_analysis/c2_first_concepts.py --elements c2_elements_p3.json --pair K04:P19 --rooms sadboys,maryland [--n 2]
    python3 out/_analysis/c2_first_concepts.py --elements c2_elements_p3.json --pair K04:P19 --rooms BOTH
    python3 out/_analysis/c2_first_concepts.py --elements c2_elements_p3.json --theme T3-162

With --pair: per room (--rooms BOTH: every room carrying both elements), the first --n cited concepts of FROM and of TO by hour (code, hour, third-order theme, the
coder's label and the passage, whole). With --theme: every concept the assignment lines cite under one third-order
theme, across rooms, in room order then hour, with label and passage whole. The concepts are read once through
`mem.py codes --grep . --json` (one logged read). Cited concepts are those of `support_by_theme`, as in the order tests.
"""
import argparse, collections, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--elements", default="c2_elements_p3.json")
ap.add_argument("--pair", default="")
ap.add_argument("--rooms", default="")
ap.add_argument("--theme", default="")
ap.add_argument("--n", type=int, default=2)
ap.add_argument("--fails", action="store_true", help="with --pair, only the rooms where the first-first order fails")
a = ap.parse_args()
els = dict((e["id"], e) for e in json.load(open(os.path.join(OUT, "_analysis", a.elements), encoding="utf-8"))["elements"])
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", ".", "--json", "--limit",
                    "10000000"], cwd=ROOT, capture_output=True, text=True)
codes = dict(((c["sub"], c["code_id"]), c) for c in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")))
rows = [json.loads(l) for l in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8") if l.strip()]


def cited(themes, only=None):
    out = collections.defaultdict(list)
    for r in rows:
        if only and r["sub"] not in only:
            continue
        for t, ids in (r.get("support_by_theme") or {}).items():
            if t in themes:
                for i in ids:
                    c = codes.get((r["sub"], i))
                    if c and c.get("hour") is not None:
                        out[r["sub"]].append((c["hour"], t, c))
    return out


def show(t, c):
    print("    %s h%.2f %s [%s] %s || %s" % (c["code_id"], c["hour"], t, c.get("author"), c.get("first_order"),
                                          " ".join(str(c.get("text") or "").split())))


if a.pair:
    f, t = a.pair.split(":")
    rooms = [x for x in a.rooms.split(",") if x]
    if rooms == ["BOTH"]:
        F, T = cited(els[f]["themes"]), cited(els[t]["themes"])
        rooms = sorted(set(F) & set(T))
        print("rooms carrying both %s and %s: %d" % (f, t, len(rooms)))
    F, T = cited(els[f]["themes"], set(rooms)), cited(els[t]["themes"], set(rooms))
    if a.fails:
        rooms = [s for s in rooms if F.get(s) and T.get(s) and not min(x[0] for x in F[s]) < min(x[0] for x in T[s])]
        print("rooms where the first %s does not come before the first %s: %d" % (f, t, len(rooms)))
    for s in rooms:
        print("== %s" % s)
        for k, side in ((f, F), (t, T)):
            print("  first %s:" % k)
            for h, th, c in sorted(side.get(s, []), key=lambda x: x[0])[:a.n]:
                show(th, c)
if a.theme:
    got = cited([a.theme])
    n = sum(len(v) for v in got.values())
    print("%s: %d cited concepts in %d rooms" % (a.theme, n, len(got)))
    for s in sorted(got):
        print("== %s" % s)
        for h, th, c in sorted(got[s], key=lambda x: x[0]):
            show(th, c)
