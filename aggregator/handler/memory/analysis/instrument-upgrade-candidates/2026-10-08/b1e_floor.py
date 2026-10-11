#!/usr/bin/env python3
"""B1e: the floor and the tier for every theme of scheme_current.jsonl.

A theme whose rooms are one, once rooms that tell one episode count as one (episodes-B1.jsonl,
read as the close-check reads it), goes to the rare tier. Otherwise the floor is a pair of rooms in
different episode units, not named together by any episode line of the theme (or of no theme),
one holding at least twice the other's items in the window (package/store/rooms.jsonl). Pairs with
exemplar rooms come first, then the widest ratio. Themes with no such pair are printed for a hand
choice of side or form.

Usage: python3 out/_analysis/b1e_floor.py [--tsv out/_analysis/b1e_floor.tsv]
"""
import collections, glob, itertools, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def units_of(rooms, joined):
    units = [{s} for s in rooms]
    for g in joined:
        hit = [u for u in units if u & g]
        if len(hit) > 1:
            merged = set().union(*hit)
            units = [u for u in units if u not in hit] + [merged]
    return units


def main():
    tsv = None
    if "--tsv" in sys.argv:
        tsv = sys.argv[sys.argv.index("--tsv") + 1]
    cur = jl(os.path.join(OUT, "scheme", "scheme_current.jsonl"))
    size = {r["sub"].lower(): r.get("items_in_window") for r in jl(os.path.join(ROOT, "package", "store", "rooms.jsonl"))}
    joins = collections.defaultdict(list)
    for e in jl(os.path.join(OUT, "episodes-B1.jsonl")):
        g = {x.lower() for x in e.get("rooms") or []}
        for t in (e.get("themes") or ["*"]):
            joins[t].append(g)
    exrooms = collections.defaultdict(set)
    for p in sorted(glob.glob(os.path.join(OUT, "_analysis", "b1e_draft_G*.jsonl"))):
        for r in jl(p):
            for e in r.get("exemplars") or []:
                exrooms[r["id"]].add(e["sub"].lower())
    rows, nosize, rare = [], [], []
    for r in cur:
        tid = r["theme"]
        rooms = sorted({m["sub"] for m in r["members"]})
        low = {x.lower(): x for x in rooms}
        joined = joins.get(tid, []) + joins.get("*", [])
        units = units_of(set(low), joined)
        if len(units) < 2:
            rare.append((tid, rooms, len(rooms)))
            rows.append((tid, "rare", "", "", "", "one room" if len(rooms) == 1 else "%d rooms that tell one episode" % len(rooms)))
            continue
        unit_of = {s: i for i, u in enumerate(units) for s in u}
        best = None
        for a, b in itertools.combinations(sorted(low), 2):
            if unit_of[a] == unit_of[b]:
                continue
            if any({a, b} <= g for g in joined):
                continue
            na, nb = size.get(a), size.get(b)
            if not (isinstance(na, int) and isinstance(nb, int)) or min(na, nb) <= 0:
                continue
            if max(na, nb) < 2 * min(na, nb):
                continue
            ex = (a in exrooms[tid]) + (b in exrooms[tid])
            key = (ex, max(na, nb) / min(na, nb))
            if best is None or key > best[0]:
                big, small = (a, b) if na >= nb else (b, a)
                best = (key, big, small)
        if best is None:
            nosize.append((tid, rooms))
            rows.append((tid, "main?", "", "", "", "no size pair: " + ", ".join(rooms)))
            continue
        _, big, small = best
        why = "%s holds %s items in the window and %s %s, over twice as many" % (
            low[big], format(size[big], ","), low[small], format(size[small], ","))
        rows.append((tid, "main", low[big], low[small], "size", why))
    if tsv:
        with open(tsv, "w", encoding="utf-8") as f:
            f.write("id\ttier\troom_a\troom_b\tunlike\twhy\n")
            for x in rows:
                f.write("\t".join(x) + "\n")
    print("themes %d; main by size %d; rare %d; no size pair %d" % (
        len(rows), sum(1 for x in rows if x[1] == "main"), len(rare), len(nosize)))
    for tid, rooms, n in rare:
        print("rare\t%s\t%d room(s)\t%s" % (tid, n, ", ".join(rooms)))
    for tid, rooms in nosize:
        print("nosize\t%s\t%s" % (tid, ", ".join("%s %s" % (x, size.get(x.lower())) for x in rooms)))


if __name__ == "__main__":
    main()
