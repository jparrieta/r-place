#!/usr/bin/env python3
"""C1, read-only: for gate changes that write J's floor into a pairing sentence (QC1-002; gates 22 to 26), list the
owed, not yet rechecked lines that hold both themes of the sentence's pair, with each theme's concept count. Under
the old sentence both were placed whenever each had concepts of its own; under the new one the smaller stays only
with three concepts or more. A line holding both with the smaller below three follows the old answer and moves.

    python3 out/_analysis/c1_floor_pairs.py --change gate:22 --pairs "T3-015|T3-063"
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--change", required=True); ap.add_argument("--pairs", required=True)
    a = ap.parse_args()
    o = next((x for x in vlib.owed_rechecks(OUT, "C1") if x["ref"] == a.change), None)
    if o is None:
        sys.exit("no change %s" % a.change)
    fin = {(r["sub"], r["theme_id"]): r for r in map(json.loads, open(os.path.join(OUT, "assignments_final.jsonl")))}
    pairs = [p.split("|") for p in a.pairs.split(";")]
    todo = [tuple(k) for k in o["owed"] if k not in o["done"]]
    both = []
    for k in todo:
        r = fin[k]
        th, sup = r.get("third_order") or [], r.get("support_by_theme") or {}
        for x, y in pairs:
            if x in th and y in th:
                n = {t: len(sup.get(t) or []) for t in (x, y)}
                small = min((x, y), key=lambda t: (n[t], -th.index(t)))
                both.append((k, x, y, n, small, n[small] < 3, th))
    moves = [b for b in both if b[5]]
    print("%s: %d owed to do; %d hold both themes of a pair; %d with the smaller below three (move)" % (
        a.change, len(todo), len(both), len(moves)))
    for k, x, y, n, small, mv, th in both:
        print("  %s %s/%s: %s; %s (%d) %s" % ("MOVE" if mv else "keep", k[0], k[1], ",".join(th), small, n[small],
                                            "below the floor" if mv else "meets the floor"))


if __name__ == "__main__":
    main()
