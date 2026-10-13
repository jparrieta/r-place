#!/usr/bin/env python3
"""C1, the pair test (section 5), as declared in the diary before it ran: every unordered pair of third-order themes
placed together in one line of assignments_final.jsonl (third_order only), kept when ten or more second-order themes
carry both; its arguable rate (share of those lines with confidence 'arguable') and its confidence distribution,
against the corpus rate (arguable among placed lines) and, beside it, the rate among lines placing two themes or more.
A pair is materially above when its rate is ten points or more over the corpus rate. --write records
out/_analysis/c1_pair_test.json (refusing to overwrite); --items T3-a,T3-b prints that pair's items.

    python3 out/_analysis/c1_pair_test.py [--write] [--items T3-a,T3-b]
"""
import argparse, collections, itertools, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true"); ap.add_argument("--items")
    a = ap.parse_args()
    rows = [json.loads(x) for x in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8") if x.strip()]
    S = {d["id"]: d for d in map(json.loads, open(os.path.join(OUT, "scheme_v2.jsonl"), encoding="utf-8"))}
    placed = [r for r in rows if r.get("third_order")]
    multi = [r for r in placed if len(r["third_order"]) >= 2]
    corpus = sum(r.get("confidence") == "arguable" for r in placed) / len(placed)
    multi_rate = sum(r.get("confidence") == "arguable" for r in multi) / len(multi)
    pairs = collections.defaultdict(list)
    for r in multi:
        for x, y in itertools.combinations(sorted(set(r["third_order"])), 2):
            pairs[(x, y)].append(r)
    if a.items:
        x, y = sorted(a.items.split(","))
        for r in pairs.get((x, y), []):
            print("%s:%s %s %s" % (r["sub"], r["theme_id"], r.get("confidence"), ",".join(r["third_order"])))
        return
    out = []
    for (x, y), rs in pairs.items():
        if len(rs) < 10:
            continue
        arg = sum(r.get("confidence") == "arguable" for r in rs)
        rate = arg / len(rs)
        out.append({"pair": [x, y], "names": [S[x]["name"], S[y]["name"]], "families": [S[x]["family"], S[y]["family"]],
                    "n": len(rs), "arguable": arg, "clear": len(rs) - arg, "rate": round(rate, 3),
                    "above_by": round(rate - corpus, 3), "material": rate >= corpus + 0.10})
    out.sort(key=lambda d: (-d["rate"], -d["n"]))
    print("corpus arguable rate %.3f (%d of %d placed lines); lines placing two themes or more %.3f (%d); pairs with ten or more: %d; materially above (>= %.3f): %d"
          % (corpus, sum(r.get("confidence") == "arguable" for r in placed), len(placed), multi_rate, len(multi), len(out),
             corpus + 0.10, sum(d["material"] for d in out)))
    for d in out:
        print("%-8s %-8s n=%3d arguable %3d clear %3d rate %.3f %s  %s | %s" % (d["pair"][0], d["pair"][1], d["n"], d["arguable"], d["clear"],
              d["rate"], "MATERIAL" if d["material"] else "        ", d["names"][0], d["names"][1]))
    if a.write:
        p = os.path.join(OUT, "_analysis", "c1_pair_test.json")
        if os.path.exists(p):
            sys.exit("c1_pair_test.json exists; supersede it with a new name")
        json.dump({"corpus_rate": round(corpus, 3), "multi_rate": round(multi_rate, 3), "placed": len(placed), "multi": len(multi),
                   "threshold": round(corpus + 0.10, 3), "pairs": out}, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("wrote out/_analysis/c1_pair_test.json")


if __name__ == "__main__":
    main()
