#!/usr/bin/env python3
"""C1, the revision rate (section 3): class each difference between my re-decisions and the current line by the rule
declared before the draw.
  error: a different primary, or a line theme whose concepts (support_by_theme) my decision places elsewhere, so
         under my reading it takes no concept. To be moved.
  lean:  my decision adds a theme the line lacks (three concepts or more, or a tie at the top). Measured, not moved.
  floor: a line theme my decision lacks while some of its concepts stay free (one or two by my reading). Measured.
An error is applied only where `mem.py reassign` can write the whole decision: not a bag (reassign leaves
also_present as it is) and not an empty decision (no C1 verb empties a line). Those are listed as carried.
Also reports the rate with my first answers in place of the corrections (corrections.json).
--write records c1_revision/classes.json; --moves writes c1_revision/moves.json for c1_reassign_list.py.

    python3 out/_analysis/c1_revision_classify.py [--write] [--moves]
"""
import argparse, glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DIR = os.path.join(OUT, "_analysis", "c1_revision")


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def jac(a, b):
    a, b = set(a), set(b)
    return 1.0 if not a and not b else len(a & b) / len(a | b)


def figures(sample, mine, line):
    js = [jac(mine[it], line[it]) for it in sample]
    diff = sum(set(mine[it]) != set(line[it]) for it in sample)
    prim = sum(mine[it][:1] == line[it][:1] for it in sample)
    n = len(sample)
    return {"n": n, "sets_differ": diff, "rate": round(diff / n, 3), "mean_jaccard": round(sum(js) / n, 3),
            "primary_agree": round(prim / n, 3)}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true"); ap.add_argument("--moves", action="store_true")
    a = ap.parse_args()
    sample = json.load(open(os.path.join(DIR, "sample.json"), encoding="utf-8"))["items"]
    dec = {d["item"]: d for p in sorted(glob.glob(os.path.join(DIR, "dec-*.json"))) for d in json.load(open(p, encoding="utf-8"))}
    if sorted(dec) != sorted(sample):
        sys.exit("decided %d of %d" % (len(dec), len(sample)))
    corr = {c["item"]: c for c in json.load(open(os.path.join(DIR, "corrections.json"), encoding="utf-8"))}
    cur = {"%s:%s" % (r["sub"], r["theme_id"]): r for r in jl("assignments_final.jsonl")}
    settled = {"%s:%s" % (r["sub"], r["theme_id"]): r.get("third_order") or [] for r in jl("assign_final.jsonl")}
    current = {it: cur[it].get("third_order") or [] for it in cur}
    mine = {it: list(dec[it]["codes"]) for it in sample}
    first = {it: (corr[it]["first"] if it in corr else mine[it]) for it in sample}
    figs = {"final": {"settled": figures(sample, mine, settled), "current": figures(sample, mine, current)},
            "first_answers": {"settled": figures(sample, first, settled), "current": figures(sample, first, current)}}
    for k, v in figs.items():
        for name, f in v.items():
            print("%-13s against the %-7s line: %d of %d differ (%.1f%%); mean Jaccard %.3f; primary agreement %.3f"
                  % (k, name, f["sets_differ"], f["n"], 100.0 * f["rate"], f["mean_jaccard"], f["primary_agree"]))
    rows, moves = [], {}
    for it in sample:
        m, ln = mine[it], current[it]
        if set(m) == set(ln) and m[:1] == ln[:1]:
            continue
        codes = dec[it]["codes"]
        used = {c for cs in codes.values() for c in cs}
        sup = cur[it].get("support_by_theme") or {}
        lacks = []
        for th in [x for x in ln if x not in m]:
            s = sup.get(th) or []
            lacks.append({"theme": th, "line_support": len(s), "free": [c for c in s if c not in used],
                          "placed_elsewhere": len([c for c in s if c in used])})
        adds = [{"theme": th, "concepts": len(codes[th])} for th in m if th not in ln]
        prim = m[:1] != ln[:1]
        zero = [x["theme"] for x in lacks if x["line_support"] and not x["free"]]
        unknown = [x["theme"] for x in lacks if not x["line_support"]]
        cls = "error" if prim or zero else ("lean" if adds and not lacks else "floor" if lacks and not adds else "lean+floor")
        bag = bool(dec[it].get("bag"))
        apply = cls == "error" and not bag and bool(m)
        ap_overlap = sorted(set(cur[it].get("also_present") or {}) & set(m)) if apply else []
        rows.append({"item": it, "mine": m, "line": ln, "class": cls, "primary_differs": prim, "zero": zero,
                     "unknown_support": unknown, "lacks": lacks, "adds": adds, "bag": bag, "apply": apply,
                     "carried": cls == "error" and not apply, "also_present_overlap": ap_overlap,
                     "corrected": it in corr, "note": dec[it].get("note")})
        if apply:
            why = dec[it].get("note") or "rule 0 by concept count"
            moves[it] = {"theme": ",".join(m), "codes": ";".join("%s=%s" % (th, ",".join(codes[th])) for th in m),
                         "reason": "C1 revision rate (seed 20261013), re-decided under scheme_v2 and J's floor: " + why}
    by = {}
    for r in rows:
        by[r["class"]] = by.get(r["class"], 0) + 1
    print("differences by class:", by, "| errors applied:", len(moves), "| errors carried:",
          sum(r["carried"] for r in rows))
    for r in rows:
        print("%-24s %-10s mine %-22s line %-22s%s%s%s%s%s" % (
            r["item"], r["class"], ",".join(r["mine"]) or "-", ",".join(r["line"]) or "-",
            " PRIMARY" if r["primary_differs"] else "",
            "".join(" lacks %s(line %d, free %d)" % (x["theme"], x["line_support"], len(x["free"])) for x in r["lacks"]),
            "".join(" adds %s(%d)" % (x["theme"], x["concepts"]) for x in r["adds"]),
            " BAG" if r["bag"] else "", " CARRIED" if r["carried"] else ""))
        if r["also_present_overlap"]:
            print("    also_present also lists %s" % ",".join(r["also_present_overlap"]))
    if a.write:
        json.dump({"figures": figs, "by_class": by, "rows": rows}, open(os.path.join(DIR, "classes.json"), "w", encoding="utf-8"),
                  indent=1, ensure_ascii=False)
        print("wrote out/_analysis/c1_revision/classes.json")
    if a.moves:
        p = os.path.join(DIR, "moves.json")
        if os.path.exists(p):
            sys.exit("moves.json exists; supersede it with a new name")
        json.dump(moves, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("wrote out/_analysis/c1_revision/moves.json (%d)" % len(moves))


if __name__ == "__main__":
    main()
