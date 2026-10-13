#!/usr/bin/env python3
"""Agreement before and after, and placement counts, for a range of items in one packet.

Read-only. Uses the same definitions as b4_packet_summary.py: before is reader against reader over every item;
after is each reader against the ruling over the items not unresolved; mean Jaccard on placement sets, primary
match beside it. Written at B4a-04 to set packet 4's items ruled before J's rulings of 13 October (1 to 400)
beside those ruled after (401 to 461).

Usage: python3 out/_analysis/b4_agreement_range.py --packet 4 --ranges 1-400,401-461
"""
import argparse
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def jac(a, b):
    a, b = set(a), set(b)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", type=int, required=True)
    ap.add_argument("--ranges", required=True)
    a = ap.parse_args()
    rows = [d for d in jl(os.path.join(OUT, "disagreements.jsonl")) if d.get("packet") == a.packet]
    print("| items | rulings | mean Jaccard before | primary before | mean Jaccard after | primary after "
          "| three themes placed | named_neither | a theme no placement held |")
    print("|---|---|---|---|---|---|---|---|---|")
    for rg in a.ranges.split(","):
        lo, hi = (int(x) for x in rg.split("-"))
        sel = [d for d in rows if lo <= d["n"] <= hi]
        bj, bp, aj, apm = [], [], [], []
        three = nn = unplaced = 0
        for d in sel:
            r1, r2 = d["readers"]
            bj.append(jac(r1, r2))
            bp.append(1.0 if (r1[:1] == r2[:1] and r1) else 0.0)
            if len(d["ruling"]) == 3:
                three += 1
            if d.get("named_neither"):
                nn += 1
            held = set(r1) | set(r2) | set(d.get("b1") or [])
            if any(t not in held for t in d["ruling"]):
                unplaced += 1
            if d["unresolved"]:
                continue
            for r in (r1, r2):
                aj.append(jac(r, d["ruling"]))
                apm.append(1.0 if (r[:1] == d["ruling"][:1]) else 0.0)
        print("| %d-%d | %d | %.3f | %.3f | %.3f | %.3f | %d | %d | %d |" % (
            lo, hi, len(sel), mean(bj), mean(bp), mean(aj), mean(apm), three, nn, unplaced))


if __name__ == "__main__":
    main()
