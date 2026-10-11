#!/usr/bin/env python3
"""B2 check legs: score a pilot round against the author's placements, by the definitions declared in notes-B2.md.

  fidelity            mean Jaccard(reader set, author set) over readers and items
  pairwise agreement  mean Jaccard over the reader pairs of each item, then over items
  alpha               Krippendorff's alpha, distance 1 - Jaccard between sets, chance over the pooled sets of the round
  primary             exact agreement on the first theme (reported beside, never in place)
Also: the items where any two readers differ, base rates per theme (readers against the author),
the position curve (each reader's first ten items against its last ten: arguable rate and
agreement with the other two), and a per-item table written to out/_analysis/b2_r<k>_items.tsv.

Usage: python3 out/_analysis/b2_score.py --round 1 --readers r12,r15,r16 [--author out/author_items.jsonl] [--alt FILE]
--alt scores fidelity a second time against another placement file (the rechecked placements).
"""
import argparse, collections, itertools, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def jac(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if a | b else 1.0


def alpha(units):
    """units: list of lists of sets (values per item, >= 2 values). Distance 1 - Jaccard."""
    units = [u for u in units if len(u) >= 2]
    n = sum(len(u) for u in units)
    do_num = 0.0
    for u in units:
        m = len(u)
        do_num += sum(1 - jac(a, b) for i, a in enumerate(u) for j, b in enumerate(u) if i != j) / (m - 1)
    do = do_num / n
    pooled = [v for u in units for v in u]
    de = sum(1 - jac(a, b) for i, a in enumerate(pooled) for j, b in enumerate(pooled) if i != j) / (n * (n - 1))
    return 1 - do / de if de else 1.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", required=True)
    ap.add_argument("--readers", required=True)
    ap.add_argument("--author", default=os.path.join(OUT, "author_items.jsonl"))
    ap.add_argument("--alt")
    ap.add_argument("--raw", default=None)
    a = ap.parse_args()
    raw = a.raw or os.path.join(OUT, "_fleet_raw", "B2", "round-%s" % a.round)
    readers = a.readers.split(",")
    auth = {r["item"] if "item" in r else "%s/%s" % (r["sub"], r["theme_id"]): r for r in jl(a.author)}
    alt = {("%s/%s" % (r["sub"], r["theme_id"])): r for r in jl(a.alt)} if a.alt else None
    lines = {}
    for rd in readers:
        p = [os.path.join(dp, f) for dp, _, fs in os.walk(raw) for f in fs if f == rd + ".jsonl"]
        lines[rd] = {"%s/%s" % (x["sub"], x["theme_id"]): x for x in jl(p[0])}
    items = sorted(auth)
    fid, fid_p, fid_alt, pw, prim, units, dis = [], [], [], [], [], [], []
    rows = []
    for it in items:
        A = auth[it]["third_order"]
        sets = [lines[rd][it]["third_order"] for rd in readers if it in lines[rd]]
        for s in sets:
            fid.append(jac(s, A)); fid_p.append(s[0] == A[0])
            if alt is not None:
                fid_alt.append(jac(s, alt[it]["third_order"]))
        pj = [jac(x, y) for x, y in itertools.combinations(sets, 2)]
        pw.append(sum(pj) / len(pj))
        prim.append(sum(x[0] == y[0] for x, y in itertools.combinations(sets, 2)) / len(pj))
        units.append(sets)
        differs = any(set(x) != set(y) for x, y in itertools.combinations(sets, 2))
        if differs:
            dis.append(it)
        rows.append((it, auth[it].get("source", ""), auth[it]["confidence"], ",".join(A),
                     " | ".join(",".join(s) for s in sets),
                     "%.2f" % (sum(jac(s, A) for s in sets) / len(sets)), "%.2f" % pw[-1],
                     "yes" if differs else "no"))
    print("round %s, readers %s, items %d" % (a.round, ",".join(readers), len(items)))
    print("fidelity vs author (mean Jaccard) %.3f; primary match %.3f" % (sum(fid) / len(fid), sum(fid_p) / len(fid_p)))
    if alt is not None:
        print("fidelity vs rechecked placements %.3f" % (sum(fid_alt) / len(fid_alt)))
    print("pairwise agreement (mean Jaccard) %.3f; primary pairwise %.3f; alpha %.3f" % (
        sum(pw) / len(pw), sum(prim) / len(prim), alpha(units)))
    print("items where any two readers differ: %d of %d" % (len(dis), len(items)))
    for rd in readers:
        f = [jac(lines[rd][it]["third_order"], auth[it]["third_order"]) for it in items]
        print("  reader %s: fidelity %.3f, multi %d, arguable %d, read whole %d" % (
            rd, sum(f) / len(f), sum(1 for it in items if len(lines[rd][it]["third_order"]) > 1),
            sum(1 for it in items if lines[rd][it].get("confidence") == "arguable"),
            sum(1 for it in items if lines[rd][it].get("read") == "whole")))
    by_src = collections.defaultdict(list)
    for it in items:
        by_src[auth[it].get("source", "")].append(it)
    for s, its in sorted(by_src.items()):
        f = [jac(lines[rd][it]["third_order"], auth[it]["third_order"]) for it in its for rd in readers]
        p = [r for r in rows if r[0] in its]
        print("  source %s (%d): fidelity %.3f, pairwise %.3f" % (s, len(its), sum(f) / len(f),
                                                            sum(float(r[6]) for r in p) / len(p)))
    for c in ("clear", "arguable"):
        its = [it for it in items if auth[it]["confidence"] == c]
        if its:
            f = [jac(lines[rd][it]["third_order"], auth[it]["third_order"]) for it in its for rd in readers]
            print("  author %s (%d): fidelity %.3f" % (c, len(its), sum(f) / len(f)))
    # base rates
    base_a, base_r = collections.Counter(), collections.Counter()
    for it in items:
        for t in auth[it]["third_order"]:
            base_a[t] += 1
        for rd in readers:
            for t in lines[rd][it]["third_order"]:
                base_r[t] += 1
    print("base rates (author count; readers' count over 3 readers):")
    for t in sorted(set(base_a) | set(base_r)):
        print("  %s author %d readers %d (%.1f per reader)" % (t, base_a[t], base_r[t], base_r[t] / len(readers)))
    # position curve
    print("position curve (positions 1-10 against 31-40):")
    for rd in readers:
        by_pos = sorted(items, key=lambda it: lines[rd][it]["position"])
        others = [o for o in readers if o != rd]
        for name, its in (("first 10", by_pos[:10]), ("last 10", by_pos[-10:])):
            arg = sum(1 for it in its if lines[rd][it].get("confidence") == "arguable")
            ag = [jac(lines[rd][it]["third_order"], lines[o][it]["third_order"]) for it in its for o in others]
            fa = [jac(lines[rd][it]["third_order"], auth[it]["third_order"]) for it in its]
            print("  %s %s: arguable %d/10, agreement with the other two %.2f, fidelity %.2f" % (
                rd, name, arg, sum(ag) / len(ag), sum(fa) / len(fa)))
    with open(os.path.join(OUT, "_analysis", "b2_r%s_items.tsv" % a.round), "w", encoding="utf-8") as f:
        f.write("item\tsource\tauthor_conf\tauthor\treaders (%s)\tfidelity\tpairwise\tdisagree\n" % ",".join(readers))
        for r in rows:
            f.write("\t".join(r) + "\n")
    json.dump({"fidelity": sum(fid) / len(fid), "pairwise": sum(pw) / len(pw), "alpha": alpha(units),
               "items_with_disagreement": dis, "fidelity_alt": (sum(fid_alt) / len(fid_alt)) if fid_alt else None},
              open(os.path.join(OUT, "_analysis", "b2_r%s_score.json" % a.round), "w"))


if __name__ == "__main__":
    main()
