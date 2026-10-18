#!/usr/bin/env python3
"""D3: for every ruling written in one leg that re-rules a line ruled before, tally the change from the line's
previous ruling (decision/kind) to the new one, by element and op. Reads adjudications.jsonl in order, so the
previous ruling is the last line for the same id before the re-ruling, and adaptations.jsonl for element and op.

  python3 out/_analysis/d3_rerule_transitions.py --leg D3a-11 [--ids]
"""
import argparse
import collections
import json


def label(r):
    k = r.get("kind")
    return f"{r.get('decision')}/{k}" if k else str(r.get("decision"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--leg", required=True)
    ap.add_argument("--ids", action="store_true", help="list the ids under each change")
    a = ap.parse_args()
    meta = {}
    for ln in open("out/adaptations.jsonl", encoding="utf-8"):
        if ln.strip():
            x = json.loads(ln)
            meta[x["id"]] = (x.get("element"), x.get("op"))
    seen = {}
    tally = collections.Counter()
    ids = collections.defaultdict(list)
    first = 0
    for ln in open("out/adjudications.jsonl", encoding="utf-8"):
        if not ln.strip():
            continue
        r = json.loads(ln)
        i = r["adaptation"]
        if r.get("leg") == a.leg:
            if i in seen:
                el, op = meta.get(i, (None, None))
                key = (str(el), str(op), label(seen[i]), label(r))
                tally[key] += 1
                ids[key].append(i)
            else:
                first += 1
        seen[i] = r
    print(f"leg {a.leg}: {sum(tally.values())} re-rulings; {first} first rulings")
    by_change = collections.Counter()
    for (el, op, was, now), n in sorted(tally.items()):
        by_change[(was, now)] += n
        print(f"{el} | {op} | {was} -> {now} | {n}")
        if a.ids:
            print("   " + " ".join(ids[(el, op, was, now)]))
    print("by change:")
    for (was, now), n in sorted(by_change.items(), key=lambda kv: -kv[1]):
        print(f"   {was} -> {now} | {n}")


if __name__ == "__main__":
    main()
