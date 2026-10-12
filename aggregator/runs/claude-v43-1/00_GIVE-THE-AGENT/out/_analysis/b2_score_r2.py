#!/usr/bin/env python3
"""B2b-r2-p2: score pilot round 2, by the definitions declared in notes-B2.md (b2_score.py's jac and alpha).

Round 2 went out as five self-contained packets, each to three fresh readers (r1, r2, r3 inside each
packet folder of _fleet_raw/B2/round-2/): fifteen readers, three per item. Per item: fidelity (each
reader's set against the author's, Jaccard), pairwise agreement (mean Jaccard over the item's three
reader pairs), primary match and primary pairwise; alpha over all items (distance 1 - Jaccard, chance
over the round's pooled sets). Fidelity a second time against the rechecked placements
(out/_analysis/b2_rechecked_author.jsonl). Also: the round-1 items alone (the same 40 items scored at
round 1), by source and by confidence; bags: readers' item_is_a_bag and the Jaccard of their
also_present themes against mine (not in the Jaccard above); base rates; per-packet position halves.
Writes out/_analysis/b2_r2_items.tsv and b2_r2_score.json.
"""
import collections, importlib.util, itertools, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
spec = importlib.util.spec_from_file_location("b2s", os.path.join(OUT, "_analysis", "b2_score.py"))
b2s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b2s)
jac, alpha, jl = b2s.jac, b2s.alpha, b2s.jl
RAW = os.path.join(OUT, "_fleet_raw", "B2", "round-2")


def mean(x):
    return sum(x) / len(x) if x else float("nan")


def main():
    auth = {r["item"]: r for r in jl(os.path.join(OUT, "author_items.jsonl"))}
    alt = {r["item"]: r for r in jl(os.path.join(OUT, "_analysis", "b2_rechecked_author.jsonl"))}
    r1items = {x.split("\t")[0] for x in open(os.path.join(OUT, "_analysis", "b2_r1_items.tsv"), encoding="utf-8").read().splitlines()[1:]}
    # lines[item] = [(reader, line)], reader = packet/slot
    lines = collections.defaultdict(list)
    errs = []
    order = json.load(open(os.path.join(OUT, "_analysis", "b2_order_r2b.json"), encoding="utf-8"))["packets"]
    for pk in sorted(os.listdir(RAW)):
        d = os.path.join(RAW, pk)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".jsonl"):
                for x in jl(os.path.join(d, f)):
                    it = "%s/%s" % (x["sub"], x["theme_id"])
                    if it not in order[pk]:
                        # a heading mistyped: the packet's item at the line's position, reported
                        by_pos = order[pk][x["position"] - 1]
                        print("MAPPED %s/%s position %d: returned %s, the packet holds %s there" % (
                            pk, f[:-6], x["position"], it, by_pos))
                        it = by_pos
                    lines[it].append(("%s/%s" % (pk, f[:-6]), x))
    for it in auth:
        if len(lines.get(it, [])) != 3:
            errs.append("%s has %d reader lines" % (it, len(lines.get(it, []))))
    if errs:
        sys.exit("\n".join(errs))
    rows, units, dis = [], [], []
    acc = collections.defaultdict(list)
    for it in sorted(auth):
        A, R = auth[it]["third_order"], alt[it]["third_order"]
        sets = [x["third_order"] for _, x in lines[it]]
        f = [jac(s, A) for s in sets]
        fr = [jac(s, R) for s in sets]
        pj = [jac(x, y) for x, y in itertools.combinations(sets, 2)]
        pp = [x[0] == y[0] for x, y in itertools.combinations(sets, 2)]
        units.append(sets)
        differs = any(set(x) != set(y) for x, y in itertools.combinations(sets, 2))
        if differs:
            dis.append(it)
        groups = ["all"] + (["r1items"] if it in r1items else ["bags10"]) + ["src:" + auth[it].get("source", "")]
        for g in groups:
            acc[g + ":fid"] += f; acc[g + ":fidalt"] += fr; acc[g + ":pw"].append(mean(pj))
            acc[g + ":prim"] += [s[0] == A[0] for s in sets]; acc[g + ":pprim"].append(mean(pp))
        rows.append([it, auth[it].get("source", ""), auth[it]["confidence"], ",".join(A), ",".join(R),
                     " | ".join(",".join(s) for s in sets), "%.2f" % mean(f), "%.2f" % mean(fr), "%.2f" % mean(pj),
                     "yes" if differs else "no"])
    print("round 2: %d items, %d reader lines (5 packets x 3 readers)" % (len(auth), sum(len(v) for v in lines.values())))
    for g, name in (("all", "all 50"), ("r1items", "round-1 items (40)"), ("bags10", "the ten biggest bags")):
        print("%-22s fidelity %.3f (primary %.3f); vs rechecked %.3f; pairwise %.3f (primary %.3f)" % (
            name, mean(acc[g + ":fid"]), mean(acc[g + ":prim"]), mean(acc[g + ":fidalt"]), mean(acc[g + ":pw"]), mean(acc[g + ":pprim"])))
    al = alpha(units)
    al40 = alpha([u for it, u in zip(sorted(auth), units) if it in r1items])
    print("alpha %.3f (round-1 items alone %.3f); items where any two readers differ: %d of %d (round-1 items %d)" % (
        al, al40, len(dis), len(auth), sum(1 for it in dis if it in r1items)))
    for k in sorted(acc):
        if k.startswith("src:") and k.endswith(":fid"):
            s = k[4:-4]
            print("  source %-12s fidelity %.3f, vs rechecked %.3f, pairwise %.3f" % (
                s, mean(acc[k]), mean(acc["src:%s:fidalt" % s]), mean(acc["src:%s:pw" % s])))
    multi = sum(1 for it in auth for _, x in lines[it] if len(x["third_order"]) > 1)
    arg = sum(1 for it in auth for _, x in lines[it] if x.get("confidence") == "arguable")
    whole = sum(1 for it in auth for _, x in lines[it] if x.get("read") == "whole")
    print("reader lines: multi %d of 150, arguable %d, read whole %d" % (multi, arg, whole))
    # bags
    print("bags (author item_is_a_bag) and the ten:")
    bagrows = []
    for it in sorted(auth):
        a = auth[it]
        if a.get("source") != "biggest-bag" and not a.get("item_is_a_bag"):
            continue
        ap = set((a.get("also_present") or {}).keys())
        rs = []
        for rd, x in lines[it]:
            xa = set((x.get("also_present") or {}).keys())
            rs.append("%s %s bag=%s ap=%s J=%.2f" % (rd.split("/")[1], ",".join(x["third_order"]),
                      bool(x.get("item_is_a_bag")), ",".join(sorted(xa)) or "-",
                      jac(xa | set(x["third_order"]), ap | set(a["third_order"]))))
            bagrows.append(jac(xa | set(x["third_order"]), ap | set(a["third_order"])))
        print("  %-22s mine %s bag=%s ap=%s\n      %s" % (it, ",".join(a["third_order"]), bool(a.get("item_is_a_bag")),
              ",".join(sorted(ap)) or "-", "\n      ".join(rs)))
    print("  kinds named (placed plus also_present) against mine, mean Jaccard over the ten: %.3f" % mean(bagrows))
    # base rates
    ba, br = collections.Counter(), collections.Counter()
    for it in auth:
        for t in auth[it]["third_order"]:
            ba[t] += 1
        for _, x in lines[it]:
            for t in x["third_order"]:
                br[t] += 1
    print("base rates (author count; readers' count over 3 readers per item):")
    for t in sorted(set(ba) | set(br)):
        print("  %s author %d readers %d (%.1f per reader)" % (t, ba[t], br[t], br[t] / 3))
    # per-packet halves: arguable and agreement with the other two, first half against second half
    print("position halves per packet (arguable; agreement with the other two):")
    for pk in sorted({rd.split("/")[0] for v in lines.values() for rd, _ in v}):
        its = [(it, v) for it, v in lines.items() if v[0][0].startswith(pk + "/")]
        n = len(its)
        if n < 6:
            continue
        for slot in ("r1", "r2", "r3"):
            pos = sorted(((dict(v)["%s/%s" % (pk, slot)]["position"], it, v) for it, v in its))
            h = n // 2
            out = []
            for part in (pos[:h], pos[-h:]):
                ar = sum(1 for _, _, v in part if dict(v)["%s/%s" % (pk, slot)].get("confidence") == "arguable")
                ag = mean([jac(dict(v)["%s/%s" % (pk, slot)]["third_order"], x["third_order"]) for _, _, v in part
                           for rd, x in v if rd != "%s/%s" % (pk, slot)])
                out.append("arg %d/%d ag %.2f" % (ar, h, ag))
            print("  %s %s first %d: %s; last %d: %s" % (pk, slot, h, out[0], h, out[1]))
    with open(os.path.join(OUT, "_analysis", "b2_r2_items.tsv"), "w", encoding="utf-8") as f:
        f.write("item\tsource\tauthor_conf\tauthor\trechecked\treaders\tfidelity\tfidelity_rechecked\tpairwise\tdisagree\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    json.dump({"fidelity": mean(acc["all:fid"]), "fidelity_rechecked": mean(acc["all:fidalt"]),
               "pairwise": mean(acc["all:pw"]), "alpha": al, "primary": mean(acc["all:prim"]),
               "primary_pairwise": mean(acc["all:pprim"]), "items_with_disagreement": dis,
               "r1items": {"fidelity": mean(acc["r1items:fid"]), "fidelity_rechecked": mean(acc["r1items:fidalt"]),
                           "pairwise": mean(acc["r1items:pw"]), "alpha": al40},
               "bags10": {"fidelity": mean(acc["bags10:fid"]), "pairwise": mean(acc["bags10:pw"]),
                          "kinds_jaccard": mean(bagrows)}},
              open(os.path.join(OUT, "_analysis", "b2_r2_score.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
