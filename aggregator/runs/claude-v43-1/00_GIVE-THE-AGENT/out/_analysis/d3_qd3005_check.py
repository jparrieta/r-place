#!/usr/bin/env python3
"""QD3-005: check the count file (_analysis/d3_qd3005_count.jsonl) against the population and tally it.
Every line of the population (instantiate and restrict lines of the closed groups whose latest ruling is an accepted
elaboration or a one-room particular, as d3_qd3005_population.py buckets them) must appear once, and no other line.
Then: counts by outcome, element and op, and by the id named; the latest ruling of each line (so that the file
describes the ledger as it stands); and the pairs that would break if the lines marked 'specification' moved,
that is, accepted elaborations outside that set whose pair is inside it. Writes nothing.

  python3 out/_analysis/d3_qd3005_check.py --elements R01,P01,... [--count out/_analysis/d3_qd3005_count.jsonl]
"""
import argparse
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d3_qd3005_population import OPS, bucket  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--elements", required=True)
    ap.add_argument("--count", default="out/_analysis/d3_qd3005_count.jsonl")
    a = ap.parse_args()
    els = {e for e in a.elements.split(",") if e}
    meta = {}
    for ln in open("out/adaptations.jsonl", encoding="utf-8"):
        if ln.strip():
            x = json.loads(ln)
            meta[x["id"]] = x
    latest = {}
    for ln in open("out/adjudications.jsonl", encoding="utf-8"):
        if ln.strip():
            r = json.loads(ln)
            latest[r["adaptation"]] = r
    pop = {}
    for i, r in latest.items():
        x = meta.get(i, {})
        if x.get("op") in OPS and x.get("element") in els:
            b = bucket(r, x.get("kind"))
            if b in ("elaboration", "particular, one room"):
                pop[i] = b
    rows = [json.loads(l) for l in open(a.count, encoding="utf-8") if l.strip()]
    ids = [r["adaptation"] for r in rows]
    dup = sorted(i for i, n in Counter(ids).items() if n > 1)
    missing = sorted(set(pop) - set(ids))
    extra = sorted(set(ids) - set(pop))
    print(f"population {len(pop)} ({Counter(pop.values())}); count file {len(rows)} rows")
    print(f"duplicates {dup}; missing {missing}; not in population {extra}")
    by = Counter()
    named = Counter()
    for r in rows:
        x = meta.get(r["adaptation"], {})
        by[(r["would"], str(x.get("element")), str(x.get("op")), pop.get(r["adaptation"], "?"))] += 1
        if r["would"] == "specification":
            for n in r["names"].split(", "):
                named[n] += 1
    print("by outcome, element, op and present ruling:")
    for k, n in sorted(by.items()):
        print("   " + " | ".join(k) + f" | {n}")
    print("outcomes: " + ", ".join(f"{k} {v}" for k, v in Counter(r["would"] for r in rows).most_common()))
    print("named by the lines that would move: " + ", ".join(f"{k} {v}" for k, v in named.most_common()))
    move = {r["adaptation"] for r in rows if r["would"] == "specification"}
    unsure = {r["adaptation"] for r in rows if r["would"] == "uncertain"}
    broke = []
    for i, r in latest.items():
        if i in move or r.get("decision") != "accept" or r.get("kind") != "elaboration":
            continue
        p = r.get("pair")
        if p in move or p in unsure:
            x = meta.get(i, {})
            broke.append((i, str(x.get("element")), str(x.get("op")), p, "uncertain" if p in unsure else "moves"))
    print(f"accepted elaborations outside the move set whose pair would move: {len(broke)}")
    for b in sorted(broke):
        print("   " + " | ".join(b))
    inner = sorted((i, latest[i].get("pair") or "-") for i in move)
    print("pairs of the lines that would move (pair, and whether it moves too or is already a specification):")
    for i, p in inner:
        pr = latest.get(p, {})
        state = "moves too" if p in move else f"{pr.get('decision')}/{pr.get('kind')}"
        print(f"   {i} -> {p} ({state})")


if __name__ == "__main__":
    main()
