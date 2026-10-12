#!/usr/bin/env python3
"""B2b-r2-p2: how coarse are the second-order themes? The material for the recut proposal (QB2-008).

Over the store's 7,844 second-order themes: concepts per theme; kinds per theme in B1's working grouping
(scheme/scheme_current.jsonl); B1's bag records (multiplacement_log lines flagged item_is_a_bag); and, for
round 2's ten biggest bags, the kinds readers named once J's floor (three concepts of its own) is applied to
their also_present. Also threads per theme (the concepts' thread ids in the store), a candidate neutral cut.
Writes out/_analysis/b2_recut_survey.tsv (one line per theme). Prints the distributions.
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
S = os.path.join(ROOT, "package", "store")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def q(xs, ps=(0.5, 0.9, 0.99)):
    xs = sorted(xs)
    return " ".join("p%d %s" % (int(p * 100), xs[min(len(xs) - 1, int(p * len(xs)))]) for p in ps)


def main():
    themes = {(t["sub"], t["theme_id"]): t for t in jl(os.path.join(S, "themes.jsonl"))}
    codes = {(c["sub"], c["code_id"]): c for c in jl(os.path.join(S, "codes.jsonl"))}
    lab2id = {(t["sub"], t["second_order"]): t["theme_id"] for t in themes.values()}
    kinds = collections.defaultdict(set)
    for r in jl(os.path.join(OUT, "scheme", "scheme_current.jsonl")):
        for m in r["members"]:
            kinds[(m["sub"], lab2id.get((m["sub"], m["second_order"]), m["theme_id"]))].add(r["theme"])
    bags = set()
    for r in jl(os.path.join(OUT, "multiplacement_log.jsonl")):
        if r.get("item_is_a_bag"):
            bags.add((r["sub"], r["theme_id"]))
    keyc = None
    for c in list(codes.values())[:1]:
        keyc = [k for k in c if "thread" in k.lower() or k in ("post", "link_id", "anchor")]
    rows = []
    for k, t in themes.items():
        cids = t.get("code_ids") or []
        thr = set()
        for cid in cids:
            thr.add(str((codes.get((k[0], cid)) or {}).get("thread_id") or ""))
        rows.append((k, len(cids), len(kinds.get(k, ())), k in bags, len(thr - {""})))
    n = len(rows)
    print("second-order themes %d; code fields with a thread: %s" % (n, keyc))
    print("concepts per theme: %s; max %d" % (q([r[1] for r in rows]), max(r[1] for r in rows)))
    print("working kinds per theme: %s" % q([r[2] for r in rows]))
    dk = collections.Counter(min(r[2], 5) for r in rows)
    print("themes by working kinds (5 = five or more): %s" % dict(sorted(dk.items())))
    print("B1 bag records: %d themes" % sum(1 for r in rows if r[3]))
    for lo in (50, 100, 200, 300):
        big = [r for r in rows if r[1] >= lo]
        print("themes with >= %d concepts: %d, holding %d concepts (%.1f%% of all); of them B1 bags %d; >3 working kinds %d" % (
            lo, len(big), sum(r[1] for r in big), 100.0 * sum(r[1] for r in big) / sum(r[1] for r in rows),
            sum(1 for r in big if r[3]), sum(1 for r in big if r[2] > 3)))
    print("threads per theme: %s" % q([r[4] for r in rows]))
    big = sorted((r for r in rows if r[1] >= 100), key=lambda r: -r[1])
    print("themes with >= 100 concepts, by room: %s" % dict(collections.Counter(r[0][0] for r in big).most_common(12)))
    with open(os.path.join(OUT, "_analysis", "b2_recut_survey.tsv"), "w", encoding="utf-8") as f:
        f.write("sub\ttheme_id\tconcepts\tworking_kinds\tb1_bag\tthreads\n")
        for k, c, w, bg, th in sorted(rows):
            f.write("%s\t%s\t%d\t%d\t%s\t%d\n" % (k[0], k[1], c, w, "yes" if bg else "no", th))
    # round 2's readers, J's floor applied
    raw = os.path.join(OUT, "_fleet_raw", "B2", "round-2")
    auth = {r["item"]: r for r in jl(os.path.join(OUT, "author_items.jsonl"))}
    order = json.load(open(os.path.join(OUT, "_analysis", "b2_order_r2b.json"), encoding="utf-8"))["packets"]
    print("the ten biggest bags, kinds named by readers with J's floor (>= 3 concepts of the item's own):")
    for pkn, its in order.items():
        for slot in ("r1", "r2", "r3"):
            for x in jl(os.path.join(raw, pkn, slot + ".jsonl")):
                it = "%s/%s" % (x["sub"], x["theme_id"])
                if it not in its:
                    it = its[x["position"] - 1]
                if auth[it].get("source") != "biggest-bag":
                    continue
                sub, tid = it.split("/")
                ap = x.get("also_present") or {}
                kept = [t for t, cs in ap.items()
                        if sum(1 for c in (cs if isinstance(cs, list) else [cs]) if (codes.get((sub, c)) or {}).get("theme_id", tid) == tid and (sub, c) in codes) >= 3]
                own = [t for t, cs in ap.items()]
                print("  %-22s %s: named %d, with the floor %d" % (it, slot, len(own), len(kept)))


if __name__ == "__main__":
    main()
