#!/usr/bin/env python3
"""C1, read-only: for one third-order theme, the themes the fresh readers of stage B4 swapped it with. On each
disagrees-contested reading of reassign.jsonl (arm 1) and reassign-openai-astra.jsonl (arm 2, reported beside, never
pooled) where the theme is in the settled set and not the fresh one, or the reverse, count the themes on the other side
(fresh-only when the theme was dropped, settled-only when it was added). Prints the counts and the items.

    python3 out/_analysis/c1_swaps.py --theme T3-010
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--theme", required=True)
    a = ap.parse_args()
    for name in ("reassign.jsonl", "reassign-openai-astra.jsonl"):
        dropped, added, items = collections.Counter(), collections.Counter(), []
        for r in jl(name):
            if r.get("outcome") != "disagrees-contested":
                continue
            S, F = set(r.get("settled") or []), set(r.get("third_order") or [])
            if a.theme in S and a.theme not in F:
                for t in F - S:
                    dropped[t] += 1
                items.append("%s/%s dropped (fresh %s)" % (r.get("sub"), r.get("theme_id"), ",".join(sorted(F)) or "-"))
            elif a.theme in F and a.theme not in S:
                for t in S - F:
                    added[t] += 1
                items.append("%s/%s added (settled %s)" % (r.get("sub"), r.get("theme_id"), ",".join(sorted(S)) or "-"))
        print("%s: %s dropped by fresh readers %d times, in place of %s" % (name, a.theme, sum(1 for i in items if " dropped " in i),
                                                                           dict(dropped.most_common(8))))
        print("   added by fresh readers %d times, where the settled line had %s" % (sum(1 for i in items if " added " in i),
                                                                                     dict(added.most_common(8))))
        for i in items:
            print("   " + i)


if __name__ == "__main__":
    main()
