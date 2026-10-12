#!/usr/bin/env python3
"""B2b-r2-p2: print round 2's reader lines, with each theme's reason, for the items that divided readers
or where no reader matched my placement (the material for the verdicts). Reads b2_r2_items.tsv and the
returns; a mistyped heading is mapped by position as b2_score_r2.py does. --item X prints one item;
--max-why N clips each reason (default 400 characters; these are reader returns, not room reads)."""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RAW = os.path.join(OUT, "_fleet_raw", "B2", "round-2")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--item"); ap.add_argument("--max-why", type=int, default=400)
    ap.add_argument("--skip-bags", action="store_true")
    a = ap.parse_args()
    order = json.load(open(os.path.join(OUT, "_analysis", "b2_order_r2b.json"), encoding="utf-8"))["packets"]
    lines = {}
    for pk, its in order.items():
        for slot in ("r1", "r2", "r3"):
            for x in jl(os.path.join(RAW, pk, slot + ".jsonl")):
                it = "%s/%s" % (x["sub"], x["theme_id"])
                if it not in its:
                    it = its[x["position"] - 1]
                lines.setdefault(it, []).append((slot, x))
    rows = [r.split("\t") for r in open(os.path.join(OUT, "_analysis", "b2_r2_items.tsv"), encoding="utf-8").read().splitlines()[1:]]
    for r in rows:
        it, src, conf, A, R, readers, fid, fidr, pw, dis = r
        if a.item and it != a.item:
            continue
        if not a.item and (a.skip_bags and src == "biggest-bag"):
            continue
        if not a.item and dis == "no" and float(fid) > 0.99:
            continue
        print("== %s (%s, %s) mine %s; rechecked %s; fidelity %s, pairwise %s" % (it, src, conf, A, R, fid, pw))
        for slot, x in lines[it]:
            print("  %s %s %s multi=%s" % (slot, ",".join(x["third_order"]), x.get("confidence"), x.get("multi")))
            for t, y in (x.get("why") or {}).items():
                y = " ".join(str(y).split())
                print("     %s: %s" % (t, y[:a.max_why] + ("..." if len(y) > a.max_why else "")))
            ml = x.get("multiplacement_log")
            if ml:
                print("     why_not_one: %s" % " ".join(str(ml.get("why_not_one")).split())[:a.max_why])
        print()


if __name__ == "__main__":
    main()
