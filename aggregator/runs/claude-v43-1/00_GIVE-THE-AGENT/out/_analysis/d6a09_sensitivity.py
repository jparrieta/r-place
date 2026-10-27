#!/usr/bin/env python3
"""D6a-09 (J's ruling 1b, 27 Oct 09:27 Berlin): the sensitivity of the form lines to the rule's two thresholds. The rule
of D6a-01 (_analysis/d6_fractal.py) is re-run on the same D5 facts files for every form and unit of
fractal-forms-D6.jsonl, with the ratio threshold at 1.0, 1.1, 1.2 (the rule), 1.3, 1.4 and 1.5 and the floor at 10 per
cent (the rule) and 15 per cent of the form's defining rooms (never under 5). The run at 1.2 and 10 per cent must give
back every one of the 396 written relations; the script stops if it does not. A changed cell (specifies or restricts as
written) is robust if it keeps its written relation at ratio 1.5 and floor 15 per cent, and marginal otherwise.

    python3 out/_analysis/d6a09_sensitivity.py --table > out/_analysis/d6a09_sensitivity_table.json
    python3 out/_analysis/d6a09_sensitivity.py --tsv > out/form-cells-sensitivity-D6.tsv
    python3 out/_analysis/d6a09_sensitivity.py --md > out/retelling-D6-parts/D6a09-sensitivity.md
"""
import argparse, collections, json, math, os, re

ap = argparse.ArgumentParser()
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument("--table", action="store_true")
g.add_argument("--tsv", action="store_true")
g.add_argument("--md", action="store_true", help="print the retelling's sensitivity section (retelling-D6-parts)")
a = ap.parse_args()
AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
TAG = {"A": "d5a36", "B": "d5a37", "C": "d5a38", "D": "d5a39", "E": "d5a40", "F": "d5a41"}
OPS_S = ("add-step", "add-condition", "link")
RATIOS = (1.0, 1.1, 1.2, 1.3, 1.4, 1.5)
FLOORS = (0.10, 0.15)
written = [json.loads(l) for l in open(os.path.join(OUT, "fractal-forms-D6.jsonl"), encoding="utf-8")]
facts = {f: json.load(open(os.path.join(AN, "%s_facts.json" % t), encoding="utf-8")) for f, t in TAG.items()}
tabs = {f: {(r["element"], r["op"]): r for r in facts[f]["elements"]} for f in TAG}


def relation(u, f, ratio, frac):
    floor = max(5, math.ceil(frac * facts[f]["n_def"]))
    ops = {op: tabs[f].get((u, op)) for op in OPS_S + ("restrict", "contradict")}
    lean = {op: r for op, r in ops.items() if r and r["form_def"] >= floor and (r["ratio"] or 0) >= ratio}
    s_lean = {op: r for op, r in lean.items() if op in OPS_S}
    if "contradict" in lean:
        return "replaces", ["contradict"], floor
    if "restrict" in lean and lean["restrict"]["form_def"] >= max([r["form_def"] for r in s_lean.values()] or [0]):
        return "restricts", ["restrict"], floor
    if s_lean:
        return "specifies", sorted(s_lean, key=lambda op: -s_lean[op]["form_def"]), floor
    return "untouched", [], floor


mismatch = [(w["element"], w["form"]) for w in written if relation(w["element"], w["form"], 1.2, 0.10)[0] != w["relation"]]
if mismatch:
    raise SystemExit("the base run does not give back the written relations: %s" % mismatch)
changed = [w for w in written if w["relation"] != "untouched"]
rows = []
for frac in FLOORS:
    for ratio in RATIOS:
        by_form = collections.Counter()
        kept = new = 0
        for w in written:
            rel = relation(w["element"], w["form"], ratio, frac)[0]
            if rel != "untouched":
                by_form[w["form"]] += 1
            if w["relation"] != "untouched" and rel == w["relation"]:
                kept += 1
            if w["relation"] == "untouched" and rel != "untouched":
                new += 1
        rows.append({"ratio": ratio, "floor": frac, "changed": sum(by_form.values()),
                     "by_form": {f: by_form.get(f, 0) for f in "ABCDEF"},
                     "written_cells_kept": kept, "cells_not_written_changed": new})
robust = [w for w in changed if relation(w["element"], w["form"], 1.5, 0.15)[0] == w["relation"]]
if a.table:
    print(json.dumps({"base": {"ratio": 1.2, "floor": 0.10}, "written_changed": len(changed), "rows": rows,
                      "robust": len(robust), "marginal": len(changed) - len(robust),
                      "robust_by_form": dict(collections.Counter(w["form"] for w in robust)),
                      "changed_by_form": dict(collections.Counter(w["form"] for w in changed)),
                      "robust_by_relation": dict(collections.Counter(w["relation"] for w in robust)),
                      "changed_by_relation": dict(collections.Counter(w["relation"] for w in changed))},
                     ensure_ascii=False))
elif a.tsv:
    # D6a-10 (J): a last column, size_mark: size-dependent where the cell fails the size-held test
    # (_analysis/d6a10_size_test.json, by the rule logged at D6a-10), else the threshold mark, robust or marginal
    size = {(r["element"], r["form"]): r["survives"]
            for r in json.load(open(os.path.join(AN, "d6a10_size_test.json"), encoding="utf-8"))["rows"]}
    cols = ["element", "form", "dimension", "relation", "deciding_ops", "holders", "ratio", "floor_10pc", "floor_15pc",
            "relation_at_1.5_10pc", "relation_at_1.2_15pc", "relation_at_1.5_15pc", "mark", "size_mark"]
    print("\t".join(cols))
    for w in changed:
        rel, dec, fl10 = relation(w["element"], w["form"], 1.2, 0.10)
        top = tabs[w["form"]][(w["element"], dec[0])]
        fl15 = max(5, math.ceil(0.15 * facts[w["form"]]["n_def"]))
        r1 = relation(w["element"], w["form"], 1.5, 0.10)[0]
        r2 = relation(w["element"], w["form"], 1.2, 0.15)[0]
        r3 = relation(w["element"], w["form"], 1.5, 0.15)[0]
        print("\t".join(str(x) for x in [w["element"], w["form"], w["dimension"], rel, ",".join(dec), top["form_def"],
                                          top["ratio"], fl10, fl15, r1, r2, r3,
                                          "robust" if r3 == rel else "marginal",
                                          ("robust" if r3 == rel else "marginal") if size[(w["element"], w["form"])]
                                          else "size-dependent"]))
else:
    names = open(os.path.join(OUT, "room-forms-names.md"), encoding="utf-8").read()
    FNAME = {m.group(1): m.group(2).strip() for m in re.finditer(r"\| ([A-F]) \| ([^|]+) \|", names)}
    get = {(r["ratio"], r["floor"]): r for r in rows}
    cell = lambda r: "%d (%s)" % (r["changed"], ", ".join("%s %d" % (f, r["by_form"][f]) for f in "ABCDEF"))  # noqa: E731
    L = ["## The sensitivity of the form lines to the rule's thresholds", "",
         "Written at D6a-09 on J's ruling 1b (27 October, 09:27 Berlin) by `_analysis/d6a09_sensitivity.py`, which re-runs "
         "the rule of D6a-01 on the same facts files. The rule names a cell changed where an op is held by at least the "
         "floor (the larger of 5 and a share of the form's defining rooms) at the ratio threshold or more times the 558 "
         "defining rooms' share. Run at the rule's own thresholds (ratio 1.2, floor 10 per cent), the script gives back "
         "all 396 written relations. The table counts the changed cells at each setting, all forms first, then by form.",
         "", "| ratio threshold | changed cells, floor 10 per cent | changed cells, floor 15 per cent |", "|---|---|---|"]
    for ratio in RATIOS:
        lab = "%.1f%s" % (ratio, " (the rule)" if ratio == 1.2 else "")
        L.append("| %s | %s | %s |" % (lab, cell(get[(ratio, 0.10)]), cell(get[(ratio, 0.15)])))
    flips = [r for r in rows if r["ratio"] >= 1.2 and r["written_cells_kept"] != r["changed"]]
    new10 = get[(1.0, 0.10)]["cells_not_written_changed"]
    L += ["", "Raising either threshold only removes cells: at every setting stricter than the rule, each cell still "
              "changed keeps its written relation%s. Lowering the ratio adds cells the rule leaves untouched (%d more at "
              "1.0 with the 10 per cent floor)." % ("" if not flips else " (except at %d settings)" % len(flips), new10),
          "",
          "**The cells kept at the stricter rule.** J's ruling names two marks. A changed cell is marked \"robust\" if it "
          "keeps its written relation at ratio 1.5 and floor 15 per cent, and \"marginal\" otherwise. Of the %d changed "
          "cells, %d are kept and %d are marginal. Each cell's mark, holders, ratio and relation at the stricter settings "
          "are in `form-cells-sensitivity-D6.tsv`." % (len(changed), len(robust), len(changed) - len(robust)), ""]
    for f in "ABCDEF":
        rb = [w for w in robust if w["form"] == f]
        n = sum(1 for w in changed if w["form"] == f)
        L.append("- **%s, %s:** %d of %d kept%s." % (
            f, FNAME[f], len(rb), n,
            (": " + ", ".join("%s (%s)" % (w["element"], w["relation"]) for w in rb)) if rb else ""))
    a15 = get[(1.5, 0.10)]["by_form"]["A"]
    L += ["", "Most single cells do not survive the stricter rule, though D, E and F keep their central changes: D its "
              "keeping and carrying on (P05, P13), E the play run as work (K01), F building again after a move and border "
              "talk before keeping (P03, A04). B keeps its scripts and its chat (P14, P23), and C keeps the design (P02). "
              "A keeps none of its changes at ratio 1.5 and floor 15 per cent, and %d of 11 at ratio 1.5 with the 10 per "
              "cent floor, so A's telling (terms, plans and their reach) rests on cells that do not survive a stricter "
              "rule. A cell marked marginal is a lean of the form at the rule's thresholds, not a finding that survives "
              "a change of rule." % a15]
    print("\n".join(L))
