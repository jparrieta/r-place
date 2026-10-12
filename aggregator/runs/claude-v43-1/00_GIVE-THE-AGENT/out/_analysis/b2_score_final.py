#!/usr/bin/env python3
"""B2d: score the gold round and the two stability rounds (stage B2 section 5), by the definitions declared in
notes-B2.md (b2_score.py's jac and alpha), from the translated copies (out/_analysis/b2_r<round>_returns/).

  gold     fidelity against gold_items.jsonl and against the rechecked gold placements (the latest record in
           rechecks-B2.jsonl with source gold_items.jsonl), primary match, pairwise, primary pairwise, alpha,
           items with two readers differing, second placements, also_present; per family (the family of my
           primary) and per theme where a theme is in my set for three or more items
  stab-1, stab-2  the same figures; the stability figure is the agreement of the arm with itself across the two
           rewordings: per item, the mean Jaccard over the nine (stab-1 reader, stab-2 reader) pairs, beside each
           round's own pairwise; alpha over the six readers; and the gold round set against each
  confusions  the nineteen pairs of confusions.md scored over every round's reader pairs (rounds 1 to 3, gold,
           stab-1, stab-2): a reader pair splits on (A, B) when one reader's primary is A and the other's B, or
           one set holds A without B and the other B without A; and the hardest pair's estimate
Writes out/_analysis/b2_final_score.json and b2_gold_items.tsv. Reads only otherwise."""
import collections, importlib.util, itertools, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
spec = importlib.util.spec_from_file_location("b2s", os.path.join(AN, "b2_score.py"))
b2s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b2s)
jac, alpha, jl = b2s.jac, b2s.alpha, b2s.jl


def mean(x):
    return sum(x) / len(x) if x else float("nan")


def read_dir(d, items):
    """{item: [(reader, line)]} from a folder of packet folders of rN.jsonl; lines on no known item dropped."""
    out, drop = collections.defaultdict(list), 0
    for pk in sorted(os.listdir(d)):
        p = os.path.join(d, pk)
        if not os.path.isdir(p):
            continue
        for f in sorted(os.listdir(p)):
            if not re.fullmatch(r"r\d+\.jsonl", f):
                continue
            for x in jl(os.path.join(p, f)):
                it = "%s/%s" % (re.sub(r"^/?r/", "", str(x.get("sub"))), x.get("theme_id"))
                if it in items:
                    out[it].append(("%s/%s" % (pk, f[:-6]), x))
                else:
                    drop += 1
    return out, drop


def figures(lines, A, R):
    f, fr, pw, pp, prim, units, dis = [], [], [], [], [], [], []
    multi = ap_lines = ap_themes = over20 = under3 = 0
    per_item = {}
    for it in sorted(A):
        sets = [x["third_order"] for _, x in lines[it]]
        units.append(sets)
        fi = [jac(s, A[it]) for s in sets]
        f += fi; fr += [jac(s, R[it]) for s in sets]
        prim += [s[0] == A[it][0] for s in sets]
        pj = [jac(x, y) for x, y in itertools.combinations(sets, 2)]
        pw.append(mean(pj)); pp.append(mean([x[0] == y[0] for x, y in itertools.combinations(sets, 2)]))
        if any(set(x) != set(y) for x, y in itertools.combinations(sets, 2)):
            dis.append(it)
        per_item[it] = (sets, mean(fi), mean(pj))
        for _, x in lines[it]:
            multi += len(x["third_order"]) > 1
            apx = x.get("also_present") or {}
            if apx:
                ap_lines += 1; ap_themes += len(apx); over20 += len(apx) > 20
                under3 += sum(1 for v in apx.values() if len(v) < 3)
    return {"fidelity": mean(f), "fidelity_rechecked": mean(fr), "primary": mean(prim), "pairwise": mean(pw),
            "primary_pairwise": mean(pp), "alpha": alpha(units), "items_with_disagreement": dis,
            "lines": sum(len(v) for v in lines.values()), "multi": multi, "also_present_lines": ap_lines,
            "also_present_themes": ap_themes, "also_present_over20": over20, "also_present_under3": under3}, per_item


def main():
    gold = {r["item"]: r for r in jl(os.path.join(OUT, "gold_items.jsonl"))}
    auth = {r["item"]: r for r in jl(os.path.join(OUT, "author_items.jsonl"))}
    A = {it: r["third_order"] for it, r in gold.items()}
    rec = {}
    for r in jl(os.path.join(OUT, "rechecks-B2.jsonl")):
        it = "%s/%s" % (r["sub"], r["theme_id"])
        if r.get("source") == "gold_items.jsonl" and it in gold and (it not in rec or r["t"] >= rec[it]["t"]):
            rec[it] = r
    R = {it: (rec[it]["now"] if it in rec else A[it]) for it in A}
    moved = sorted(it for it in A if set(R[it]) != set(A[it]))
    fam = {r["id"]: r["family"] for r in jl(os.path.join(OUT, "scheme_final.jsonl"))}
    rounds = {}
    for rnd in ("gold", "stab-1", "stab-2"):
        lines, drop = read_dir(os.path.join(AN, "b2_r%s_returns" % rnd), set(A))
        bad = [it for it in A if len(lines.get(it, [])) != 3]
        if bad or drop:
            raise SystemExit("%s: items without three lines %s; lines dropped %d" % (rnd, bad, drop))
        rounds[rnd] = lines
    res, per = {}, {}
    print("rechecked gold placements: %d of 40 moved (%s)" % (len(moved), ", ".join(moved)))
    for rnd, lines in rounds.items():
        res[rnd], per[rnd] = figures(lines, A, R)
        s = res[rnd]
        print("%-7s fidelity %.3f (primary %.3f), vs rechecked %.3f; pairwise %.3f (primary %.3f); alpha %.3f; "
              "%d items differ; %d of %d lines multi; also_present %d lines, %d themes, over 20: %d, under 3: %d" % (
              rnd, s["fidelity"], s["primary"], s["fidelity_rechecked"], s["pairwise"], s["primary_pairwise"],
              s["alpha"], len(s["items_with_disagreement"]), s["multi"], s["lines"], s["also_present_lines"],
              s["also_present_themes"], s["also_present_over20"], s["also_present_under3"]))
    # stability: the arm against itself across the two rewordings
    def cross(r1, r2):
        per_it = {}
        for it in A:
            a = [x["third_order"] for _, x in rounds[r1][it]]
            b = [x["third_order"] for _, x in rounds[r2][it]]
            per_it[it] = (mean([jac(x, y) for x in a for y in b]), mean([x[0] == y[0] for x in a for y in b]))
        return per_it
    st = {}
    for r1, r2 in (("stab-1", "stab-2"), ("gold", "stab-1"), ("gold", "stab-2")):
        c = cross(r1, r2)
        st["%s|%s" % (r1, r2)] = {"jaccard": mean([v[0] for v in c.values()]), "primary": mean([v[1] for v in c.values()]),
                                  "items_below_half": sorted(it for it, v in c.items() if v[0] < 0.5)}
        print("cross %-14s Jaccard %.3f, primary %.3f; items under 0.5: %d" % (
            "%s|%s" % (r1, r2), st["%s|%s" % (r1, r2)]["jaccard"], st["%s|%s" % (r1, r2)]["primary"],
            len(st["%s|%s" % (r1, r2)]["items_below_half"])))
    six = [[x["third_order"] for _, x in rounds["stab-1"][it]] + [x["third_order"] for _, x in rounds["stab-2"][it]] for it in sorted(A)]
    nine = [s + [x["third_order"] for _, x in rounds["gold"][it]] for s, it in zip(six, sorted(A))]
    st["alpha_six"], st["alpha_nine"] = alpha(six), alpha(nine)
    fid_change = [abs(per["stab-1"][it][1] - per["stab-2"][it][1]) for it in A]
    st["fidelity_item_change_mean"] = mean(fid_change)
    print("alpha over the six stability readers %.3f; over all nine readers %.3f; mean change of an item's fidelity "
          "between the rewordings %.3f" % (st["alpha_six"], st["alpha_nine"], st["fidelity_item_change_mean"]))
    print("stab items under 0.5 across rewordings: %s" % ", ".join(st["stab-1|stab-2"]["items_below_half"]))
    # per family and per theme, gold round
    byfam = collections.defaultdict(list)
    for it in A:
        byfam[fam[A[it][0]]].append(it)
    fams = {}
    print("per family (gold round; family of my primary):")
    for g in sorted(byfam):
        its = byfam[g]
        fams[g] = {"n": len(its), "fidelity": mean([per["gold"][i][1] for i in its]), "pairwise": mean([per["gold"][i][2] for i in its])}
        print("  %s n=%d fidelity %.2f pairwise %.2f" % (g, len(its), fams[g]["fidelity"], fams[g]["pairwise"]))
    bythm = collections.defaultdict(list)
    for it in A:
        for t in A[it]:
            bythm[t].append(it)
    thm = {t: {"n": len(v), "fidelity": mean([per["gold"][i][1] for i in v]), "pairwise": mean([per["gold"][i][2] for i in v])}
           for t, v in bythm.items() if len(v) >= 3}
    print("per theme with three or more gold items: %s" % ", ".join("%s n=%d fid %.2f pw %.2f" % (t, v["n"], v["fidelity"], v["pairwise"]) for t, v in sorted(thm.items())))
    # confusions scorecard over every round
    pairs = []
    for m in re.finditer(r"^(\d+)\. \*\*(T3-\d{3}) [^/]*/ (T3-\d{3})", open(os.path.join(OUT, "confusions.md"), encoding="utf-8").read(), re.M):
        pairs.append((int(m.group(1)), m.group(2), m.group(3)))
    items = set(A) | set(auth)
    allr = {}
    r1, d1 = read_dir(os.path.join(OUT, "_fleet_raw", "B2", "round-1"), items)
    r2, d2 = read_dir(os.path.join(OUT, "_fleet_raw", "B2", "round-2"), items)
    r3, d3 = read_dir(os.path.join(AN, "b2_r3_returns"), items)
    allr.update({"1": r1, "2": r2, "3": r3}); allr.update(rounds)
    print("confusions: lines dropped as on no item: round 1 %d, round 2 %d, round 3 %d" % (d1, d2, d3))
    score = []
    for n, a, b in pairs:
        touched = split = psplit = 0
        for rnd, L in allr.items():
            for it, v in L.items():
                sets = [x["third_order"] for _, x in v]
                for x, y in itertools.combinations(sets, 2):
                    if not ({a, b} & (set(x) | set(y))):
                        continue
                    touched += 1
                    if {x[0], y[0]} == {a, b}:
                        psplit += 1
                    if (a in x and b not in x and b in y and a not in y) or (b in x and a not in x and a in y and b not in y):
                        split += 1
        score.append({"rank": n, "pair": [a, b], "reader_pairs_touching": touched, "split": split, "primary_split": psplit,
                      "split_rate": split / touched if touched else None})
    order = sorted(score, key=lambda s: -(s["split_rate"] or 0))
    print("confusions scored (predicted rank, pair, reader pairs touching, splits, primary splits, rate; observed rank):")
    for s in score:
        s["observed_rank"] = order.index(s) + 1
        print("  %2d %s/%s touching %d split %d primary %d rate %s observed rank %d" % (
            s["rank"], s["pair"][0], s["pair"][1], s["reader_pairs_touching"], s["split"], s["primary_split"],
            "%.2f" % s["split_rate"] if s["split_rate"] is not None else "-", s["observed_rank"]))
    hard = [s for s in score if set(s["pair"]) == {"T3-005", "T3-021"}][0]
    hp = sum(1 for rnd, L in allr.items() for it, v in L.items()
             for x, y in itertools.combinations([z["third_order"] for _, z in v], 2)
             if ({"T3-005", "T3-021"} & {x[0], y[0]}))
    hard["primary_disagreement_rate"] = hard["primary_split"] / hp if hp else None
    print("hardest pair T3-005/T3-021: reader pairs with either as a primary %d, primaries split between the two %d (%.1f%%)" % (
        hp, hard["primary_split"], 100 * (hard["primary_disagreement_rate"] or 0)))
    with open(os.path.join(AN, "b2_gold_items.tsv"), "w", encoding="utf-8") as fh:
        fh.write("item\tmine\trechecked\tgold_readers\tstab1_readers\tstab2_readers\tgold_fidelity\tgold_pairwise\tstab_cross\n")
        c = cross("stab-1", "stab-2")
        for it in sorted(A):
            fh.write("\t".join([it, ",".join(A[it]), ",".join(R[it])] +
                               [" | ".join(",".join(s) for s in per[r][it][0]) for r in ("gold", "stab-1", "stab-2")] +
                               ["%.2f" % per["gold"][it][1], "%.2f" % per["gold"][it][2], "%.2f" % c[it][0]]) + "\n")
    json.dump({"rounds": res, "stability": st, "families": fams, "themes": thm, "confusions": score, "rechecked_moved": moved},
              open(os.path.join(AN, "b2_final_score.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
