#!/usr/bin/env python3
"""B1e: how each room's second-order themes sit on the scheme.

Per room: second-order themes in the store, placed, unplaced (unplaced-B1.jsonl), placements, themes
under more than one kind, bag lines, distinct kinds and families, and the share of placed themes
under one kind. Prints the rooms with the most themes placed singly across the most families (the
scheme's cleanest fit) and the rooms with the highest share of multi-kind, bagged or unplaced
themes (its worst fit), with at least --min themes.

Also prints the size distribution (second-order themes per third-order theme) and the ten biggest
bags: second-order themes ranked by the concepts under them, with their placements.

Usage: python3 out/_analysis/b1e_rooms_fit.py [--min 8] [--top 12]
"""
import collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def arg(k, d):
    return int(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d


def main():
    mn, top = arg("--min", 8), arg("--top", 12)
    fam = {r["id"]: r["family"] for r in jl(os.path.join(OUT, "scheme.jsonl"))}
    themes = jl(os.path.join(ROOT, "package", "store", "themes.jsonl"))
    lab2id = {(r["sub"], r["second_order"]): r["theme_id"] for r in themes}
    store_n = collections.Counter(r["sub"] for r in themes)
    kinds = collections.defaultdict(set)
    size = {}
    for r in jl(os.path.join(OUT, "scheme", "scheme_current.jsonl")):
        size[r["theme"]] = len(r["members"])
        for m in r["members"]:
            so = m["second_order"]
            tid = so if (m["sub"], so) not in lab2id else lab2id[(m["sub"], so)]
            kinds[(m["sub"], tid)].add(r["theme"])
    unpl = collections.Counter(r["sub"] for r in jl(os.path.join(OUT, "unplaced-B1.jsonl")))
    bags = collections.Counter(r["sub"] for r in jl(os.path.join(OUT, "multiplacement_log.jsonl")) if r.get("item_is_a_bag"))
    per = collections.defaultdict(lambda: {"placed": 0, "multi": 0, "k": set(), "f": set(), "pl": 0})
    for (sub, tid), ks in kinds.items():
        p = per[sub]
        p["placed"] += 1
        p["pl"] += len(ks)
        p["multi"] += len(ks) > 1
        p["k"] |= ks
        p["f"] |= {fam[k] for k in ks}
    rows = []
    for sub, p in per.items():
        n = store_n[sub]
        if n < mn:
            continue
        single = (p["placed"] - p["multi"]) / p["placed"]
        bad = (p["multi"] + bags[sub] + unpl[sub]) / n
        rows.append((sub, n, p["placed"], unpl[sub], p["pl"], p["multi"], bags[sub], len(p["k"]), len(p["f"]), single, bad))
    print("room\tthemes\tplaced\tunplaced\tplacements\tmulti\tbags\tkinds\tfamilies\tsingle share\tbad share")
    print("-- cleanest fit: all placed singly, most families")
    for r in sorted(rows, key=lambda x: (-x[9], -x[8], -x[1], x[0]))[:top]:
        print("%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%.2f\t%.2f" % r)
    print("-- worst fit: highest share of multi-kind, bagged or unplaced themes")
    for r in sorted(rows, key=lambda x: (-x[10], -x[1], x[0]))[:top]:
        print("%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%.2f\t%.2f" % r)
    s = sorted(size.values())
    q = lambda f: s[min(len(s) - 1, int(f * len(s)))]
    bins = collections.Counter()
    for v in s:
        bins["1" if v == 1 else "2-9" if v < 10 else "10-24" if v < 25 else "25-49" if v < 50 else "50-99" if v < 100 else "100-199" if v < 200 else "200-399" if v < 400 else "400+"] += 1
    print("-- size distribution over %d themes: min %d, quartiles %d, %d, %d, max %d, mean %.1f" % (
        len(s), s[0], q(0.25), q(0.5), q(0.75), s[-1], sum(s) / len(s)))
    print("   " + ", ".join("%s: %d" % (b, bins[b]) for b in ("1", "2-9", "10-24", "25-49", "50-99", "100-199", "200-399", "400+")))
    print("   largest: " + ", ".join("%s %d" % (t, n) for t, n in sorted(size.items(), key=lambda x: -x[1])[:8]))
    codes = collections.Counter()
    for c in jl(os.path.join(ROOT, "package", "store", "codes.jsonl")):
        if c.get("theme_id"):
            codes[(c["sub"], c["theme_id"])] += 1
    lab = {(r["sub"], r["theme_id"]): r["second_order"] for r in themes}
    print("-- ten biggest bags: second-order themes ranked by concepts under them")
    for (sub, tid), n in codes.most_common(10):
        print("%s %s\t%d concepts\t%s\t%s" % (sub, tid, n, ",".join(sorted(kinds.get((sub, tid), []))) or "unplaced", lab.get((sub, tid))))


if __name__ == "__main__":
    main()
