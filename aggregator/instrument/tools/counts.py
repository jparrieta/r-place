#!/usr/bin/env python3
"""counts.py, v38: the denominators, from the canonical files. Run it; never copy its numbers by hand.

    python3 tools/counts.py [ROOT] [OUT] [--json]

ROOT is the analyst's folder (default .), OUT its out/ (default ROOT/out). Reads
package/store/{rooms,codes,themes,threads,items}.jsonl and, if it exists, out/dropped.jsonl
(stage A1's screen, {"sub", "why"} per line). Prints:

    census_rooms                 rooms in the frame (package/FRAME.md names the same count)
    dropped                      rooms stage A1 dropped; null until dropped.jsonl exists
    analysed_rooms               census less dropped; null until dropped.jsonl exists
    concepts, themes, threads, items    over the census and over the analysed set
    rooms_without_theme, rooms_with_one_or_two_themes    over the analysed set (or the census)
    assignment_items_expected    every second-order theme of the analysed set: what stage B3's
                                 batches must cover and what assignments_final.jsonl must count

Counts only. It says nothing about what a count means (contract §5: code mass measures the
coding, not the room).
"""
import collections, json, os, sys


def jl(p):
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def compute(root, out):
    """The census, the analysed set and the denominators, as a dict; None when the store has no rooms."""
    S = os.path.join(root, "package", "store")
    rooms = [r["sub"] for r in jl(os.path.join(S, "rooms.jsonl"))]
    if not rooms:
        return None
    dp = os.path.join(out, "dropped.jsonl")
    dropped = sorted({d["sub"] for d in jl(dp)}) if os.path.exists(dp) else None
    analysed = None if dropped is None else sorted(set(rooms) - set(dropped))
    scope = set(analysed) if analysed is not None else set(rooms)

    def per(name):
        c = collections.Counter(r["sub"] for r in jl(os.path.join(S, name + ".jsonl")))
        return sum(c.values()), sum(v for k, v in c.items() if k in scope), c

    concepts, concepts_a, _ = per("codes")
    themes_all = jl(os.path.join(S, "themes.jsonl"))
    tc = collections.Counter(t["sub"] for t in themes_all)
    threads, threads_a, _ = per("threads")
    items, items_a, _ = per("items")
    res = {
        "census_rooms": len(rooms),
        "dropped": None if dropped is None else len(dropped),
        "analysed_rooms": None if analysed is None else len(analysed),
        "scope": "analysed set" if analysed is not None else "census (dropped.jsonl not yet written)",
        "concepts": {"census": concepts, "scope": concepts_a},
        "themes": {"census": len(themes_all), "scope": sum(v for k, v in tc.items() if k in scope)},
        "threads": {"census": threads, "scope": threads_a},
        "items": {"census": items, "scope": items_a},
        "rooms_without_theme": sorted(r for r in scope if tc.get(r, 0) == 0),
        "rooms_with_one_or_two_themes": sum(1 for r in scope if tc.get(r, 0) in (1, 2)),
        "assignment_items_expected": sum(v for k, v in tc.items() if k in scope),
    }
    return res


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    root = args[0] if args else "."
    out = args[1] if len(args) > 1 else os.path.join(root, "out")
    res = compute(root, out)
    if res is None:
        print("no rooms in %s" % os.path.join(root, "package", "store"), file=sys.stderr)
        return 2
    if "--json" in argv:
        print(json.dumps(res, indent=1))
        return 0
    for k, v in res.items():
        if isinstance(v, list):
            v = "%d %s" % (len(v), v[:10] if v else "")
        print("%-30s %s" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
