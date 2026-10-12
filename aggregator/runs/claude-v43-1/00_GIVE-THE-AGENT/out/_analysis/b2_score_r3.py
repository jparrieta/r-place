#!/usr/bin/env python3
"""B2b-r3: score pilot round 3, by the definitions declared in notes-B2.md (b2_score.py's jac and alpha).

Round 3 is round 2's 50 items on the scheme after edits 287 to 295, with round 2's readers (QB2-007), sent in
fleet ids as five self-contained packets. Per packet the handler kept the first three valid replies in reader
order (RESCUE-2026-10-12.json); b2_translate_fleet.py --round 3 translated those to room ids in
out/_analysis/b2_r3_returns/, which this reads. The same figures as b2_score_r2.py, and item for item against
round 2 (out/_analysis/b2_r2_items.tsv): pairwise and fidelity per item, which moved. Also the
three-concept floor for also_present (QB2-008), counted from the readers' own lists.
Writes out/_analysis/b2_r3_items.tsv and b2_r3_score.json.
"""
import collections, importlib.util, itertools, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
spec = importlib.util.spec_from_file_location("b2s", os.path.join(OUT, "_analysis", "b2_score.py"))
b2s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b2s)
jac, alpha, jl = b2s.jac, b2s.alpha, b2s.jl
RAW = os.path.join(OUT, "_analysis", "b2_r3_returns")


def mean(x):
    return sum(x) / len(x) if x else float("nan")


def main():
    auth = {r["item"]: r for r in jl(os.path.join(OUT, "author_items.jsonl"))}
    alt = {r["item"]: r for r in jl(os.path.join(OUT, "_analysis", "b2_rechecked_author.jsonl"))}
    r2 = {}
    for x in open(os.path.join(OUT, "_analysis", "b2_r2_items.tsv"), encoding="utf-8").read().splitlines()[1:]:
        c = x.split("\t")
        r2[c[0]] = {"readers": c[5], "fid": float(c[6]), "pw": float(c[8]), "dis": c[9]}
    r1items = {x.split("\t")[0] for x in open(os.path.join(OUT, "_analysis", "b2_r1_items.tsv"), encoding="utf-8").read().splitlines()[1:]}
    lines = collections.defaultdict(list)
    order = json.load(open(os.path.join(OUT, "_analysis", "b2_order_r3.json"), encoding="utf-8"))["packets"]
    for pk in sorted(os.listdir(RAW)):
        d = os.path.join(RAW, pk)
        for f in sorted(os.listdir(d)):
            for x in jl(os.path.join(d, f)):
                it = "%s/%s" % (x["sub"], x["theme_id"])
                by_pos = order[pk][x["position"] - 1]
                if it != by_pos:
                    print("MISMATCH %s/%s position %d: returned %s, the packet holds %s there" % (pk, f[:-6], x["position"], it, by_pos))
                lines[it].append(("%s/%s" % (pk, f[:-6]), x))
    errs = ["%s has %d reader lines" % (it, len(lines.get(it, []))) for it in auth if len(lines.get(it, [])) != 3]
    if errs or set(lines) - set(auth):
        sys.exit("\n".join(errs + ["not an item: %s" % it for it in set(lines) - set(auth)]))
    rows, units, dis = [], [], []
    acc = collections.defaultdict(list)
    moved = {"up": [], "down": [], "same": []}
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
        d = mean(pj) - r2[it]["pw"]
        moved["up" if d > 0.005 else "down" if d < -0.005 else "same"].append(it)
        groups = ["all"] + (["r1items"] if it in r1items else ["bags10"]) + ["src:" + auth[it].get("source", "")]
        for g in groups:
            acc[g + ":fid"] += f; acc[g + ":fidalt"] += fr; acc[g + ":pw"].append(mean(pj))
            acc[g + ":prim"] += [s[0] == A[0] for s in sets]; acc[g + ":pprim"].append(mean(pp))
        rows.append([it, auth[it].get("source", ""), auth[it]["confidence"], ",".join(A), ",".join(R),
                     " | ".join(",".join(s) for s in sets), "%.2f" % mean(f), "%.2f" % mean(fr), "%.2f" % mean(pj),
                     "yes" if differs else "no", r2[it]["readers"], "%.2f" % r2[it]["fid"], "%.2f" % r2[it]["pw"], "%+.2f" % d])
    print("round 3: %d items, %d reader lines (5 packets x 3 readers)" % (len(auth), sum(len(v) for v in lines.values())))
    for g, name in (("all", "all 50"), ("r1items", "round-1 items (40)"), ("bags10", "the ten biggest bags")):
        print("%-22s fidelity %.3f (primary %.3f); vs rechecked %.3f; pairwise %.3f (primary %.3f)" % (
            name, mean(acc[g + ":fid"]), mean(acc[g + ":prim"]), mean(acc[g + ":fidalt"]), mean(acc[g + ":pw"]), mean(acc[g + ":pprim"])))
    al = alpha(units)
    al40 = alpha([u for it, u in zip(sorted(auth), units) if it in r1items])
    print("alpha %.3f (round-1 items alone %.3f); items where any two readers differ: %d of %d (round-1 items %d)" % (
        al, al40, len(dis), len(auth), sum(1 for it in dis if it in r1items)))
    print("against round 2, pairwise per item: up %d, down %d, same %d" % (len(moved["up"]), len(moved["down"]), len(moved["same"])))
    for k in ("up", "down"):
        print("  %s: %s" % (k, ", ".join(moved[k])))
    for k in sorted(acc):
        if k.startswith("src:") and k.endswith(":fid"):
            s = k[4:-4]
            print("  source %-12s fidelity %.3f, vs rechecked %.3f, pairwise %.3f" % (
                s, mean(acc[k]), mean(acc["src:%s:fidalt" % s]), mean(acc["src:%s:pw" % s])))
    multi = sum(1 for it in auth for _, x in lines[it] if len(x["third_order"]) > 1)
    arg = sum(1 for it in auth for _, x in lines[it] if x.get("confidence") == "arguable")
    whole = sum(1 for it in auth for _, x in lines[it] if x.get("read") == "whole")
    print("reader lines: multi %d of 150, arguable %d, read whole %d" % (multi, arg, whole))
    # also_present: how many lines name any, how many themes, how many under the three-concept floor
    apl = [(it, rd, x) for it in auth for rd, x in lines[it] if x.get("also_present")]
    apn = sum(len(x["also_present"]) for _, _, x in apl)
    under = [(it, rd, t, len(cs)) for it, rd, x in apl for t, cs in x["also_present"].items() if len(cs) < 3]
    bagflag = sum(1 for it in auth for _, x in lines[it] if x.get("item_is_a_bag"))
    print("also_present: %d lines name %d themes; item_is_a_bag true on %d lines; under the three-concept floor: %d" % (
        len(apl), apn, bagflag, len(under)))
    for u in under:
        print("  under floor: %s %s %s (%d concepts)" % u)
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
    print("position halves per packet (arguable; agreement with the other two):")
    for pk in sorted({rd.split("/")[0] for v in lines.values() for rd, _ in v}):
        its = [(it, v) for it, v in lines.items() if v[0][0].startswith(pk + "/")]
        n = len(its)
        if n < 6:
            continue
        for slot in sorted({rd for _, v in its for rd, _ in v}):
            pos = sorted(((dict(v)[slot]["position"], it, v) for it, v in its))
            h = n // 2
            out = []
            for part in (pos[:h], pos[-h:]):
                ar = sum(1 for _, _, v in part if dict(v)[slot].get("confidence") == "arguable")
                ag = mean([jac(dict(v)[slot]["third_order"], x["third_order"]) for _, _, v in part
                           for rd, x in v if rd != slot])
                out.append("arg %d/%d ag %.2f" % (ar, h, ag))
            print("  %s first %d: %s; last %d: %s" % (slot, h, out[0], h, out[1]))
    with open(os.path.join(OUT, "_analysis", "b2_r3_items.tsv"), "w", encoding="utf-8") as f:
        f.write("item\tsource\tauthor_conf\tauthor\trechecked\treaders\tfidelity\tfidelity_rechecked\tpairwise\tdisagree"
                "\tr2_readers\tr2_fidelity\tr2_pairwise\tpairwise_change\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    json.dump({"fidelity": mean(acc["all:fid"]), "fidelity_rechecked": mean(acc["all:fidalt"]),
               "pairwise": mean(acc["all:pw"]), "alpha": al, "primary": mean(acc["all:prim"]),
               "primary_pairwise": mean(acc["all:pprim"]), "items_with_disagreement": dis,
               "r1items": {"fidelity": mean(acc["r1items:fid"]), "fidelity_rechecked": mean(acc["r1items:fidalt"]),
                           "pairwise": mean(acc["r1items:pw"]), "alpha": al40},
               "bags10": {"fidelity": mean(acc["bags10:fid"]), "pairwise": mean(acc["bags10:pw"]),
                          "kinds_jaccard": mean(bagrows)},
               "multi_lines": multi, "also_present_lines": len(apl), "also_present_themes": apn,
               "also_present_under_floor": len(under), "vs_r2": {k: v for k, v in moved.items()}},
              open(os.path.join(OUT, "_analysis", "b2_r3_score.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
