#!/usr/bin/env python3
"""C1, read-only: what the last pass did to the rooms-by-third-order matrix. Counts per third-order theme of
second-order themes placed and of rooms holding it, in assign_final.jsonl (stage B's settled line) and in
assignments_final.jsonl (now), and the themes whose counts changed most; also out/_views/rooms-x-third.tsv's shape.
Prints only.

    python3 out/_analysis/c1_views_diff.py [--top N]
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def counts(rows):
    items, rooms = collections.Counter(), collections.defaultdict(set)
    for r in rows:
        for t in r.get("third_order") or []:
            items[t] += 1
            rooms[t].add(r["sub"])
    return items, {t: len(v) for t, v in rooms.items()}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args()
    i0, r0 = counts(jl("assign_final.jsonl"))
    i1, r1 = counts(jl("assignments_final.jsonl"))
    S = {r["id"]: r for r in jl("scheme_final.jsonl")}
    ths = sorted(set(i0) | set(i1))
    d = sorted(ths, key=lambda t: (i1.get(t, 0) - i0.get(t, 0), t))
    print("placements: settled line %d, now %d; themes placed: %d and %d" % (sum(i0.values()), sum(i1.values()), len(i0), len(i1)))
    print("largest falls (theme, name, items before -> now, rooms before -> now):")
    for t in d[:a.top]:
        print("  %s %s: %d -> %d; rooms %d -> %d" % (t, S.get(t, {}).get("name", ""), i0.get(t, 0), i1.get(t, 0), r0.get(t, 0), r1.get(t, 0)))
    print("rises:")
    for t in [t for t in reversed(d) if i1.get(t, 0) > i0.get(t, 0)][:a.top]:
        print("  %s %s: %d -> %d; rooms %d -> %d" % (t, S.get(t, {}).get("name", ""), i0.get(t, 0), i1.get(t, 0), r0.get(t, 0), r1.get(t, 0)))
    gone = [t for t in ths if i0.get(t, 0) and not i1.get(t, 0)]
    print("themes placed nowhere now: %s" % (gone or "none"))
    thin = [(t, i1.get(t, 0), r1.get(t, 0)) for t in sorted(S) if r1.get(t, 0) < 2]
    print("themes now in fewer than two rooms: %s" % thin)
    v = os.path.join(OUT, "_views", "rooms-x-third.tsv")
    if os.path.exists(v):
        lines = open(v, encoding="utf-8").read().splitlines()
        print("_views/rooms-x-third.tsv: %d lines, %d columns in the header" % (len(lines), len(lines[0].split("\t")) if lines else 0))


if __name__ == "__main__":
    main()
