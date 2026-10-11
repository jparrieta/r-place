#!/usr/bin/env python3
"""B1e: candidate confusion pairs from the rule 0 record.

For each unordered pair of third-order themes: rule 0 lines that put both on one second-order theme,
by direction (which one was primary), and bag lines that keep one and name the other. A pair often
placed together, with both directions common, is a pair where a reader must choose which carries the
theme and may choose differently. Prints the top pairs with their families and one exposing
second-order theme per pair (seeded pick among the pair's rule 0 lines, its label from the store).

Usage: python3 out/_analysis/b1e_confusions.py [--top 30]
"""
import collections, json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def main():
    top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 30
    fam = {}
    name = {}
    for r in jl(os.path.join(OUT, "scheme.jsonl")):
        fam[r["id"]] = r["family"]
        name[r["id"]] = r["name"]
    label = {(r["sub"], r["theme_id"]): r.get("label") or r.get("second_order") for r in jl(os.path.join(ROOT, "package", "store", "themes.jsonl"))}
    d = collections.Counter()
    bag = collections.Counter()
    lines = collections.defaultdict(list)
    for r in jl(os.path.join(OUT, "multiplacement_log.jsonl")):
        if r.get("item_is_a_bag"):
            others = r.get("would_need") or []
            if isinstance(others, str):
                others = [x for x in others.replace(";", ",").split(",") if x.strip()]
            for o in others:
                o = o.strip()
                if o and o != r["primary"]:
                    bag[tuple(sorted((r["primary"], o)))] += 1
            continue
        a, b = r["primary"], r["additional"]
        d[(a, b)] += 1
        lines[tuple(sorted((a, b)))].append((r["sub"], r["theme_id"]))
    pairs = set(tuple(sorted(k)) for k in d) | set(bag)
    rows = []
    for p in pairs:
        ab, ba = d[(p[0], p[1])], d[(p[1], p[0])]
        tot = ab + ba
        bal = min(ab, ba) / max(ab, ba) if max(ab, ba) else 0
        rows.append((tot + bag[p], tot, ab, ba, bal, bag[p], p))
    rows.sort(key=lambda x: (-x[0], x[6]))
    print("pair\tfamilies\trule0 total\t(a primary, b primary)\tbalance\tbag\texposing")
    for tot_all, tot, ab, ba, bal, bg, p in rows[:top]:
        cand = sorted(lines[p])
        random.Random("b1e-conf:%s:%s" % p).shuffle(cand)
        ex = cand[0] if cand else None
        exs = "%s %s %s" % (ex[0], ex[1], label.get(ex, "?")) if ex else "-"
        print("%s %s / %s %s\t%s/%s\t%d\t(%d, %d)\t%.2f\t%d\t%s" % (p[0], name.get(p[0]), p[1], name.get(p[1]),
                                                          fam.get(p[0]), fam.get(p[1]), tot, ab, ba, bal, bg, exs))


if __name__ == "__main__":
    main()
