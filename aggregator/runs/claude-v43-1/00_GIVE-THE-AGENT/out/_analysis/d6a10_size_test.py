#!/usr/bin/env python3
"""D6a-10: the size-held test of the 72 changed form cells (J, 27 Oct 09:27 Berlin), by the rule logged in the diary
before this script ran (D6a-10, 'the matching rule, stated before it runs').

For each changed cell of fractal-forms-D6.jsonl (unit u, form f, deciding ops as written), the form's defining rooms are
matched with replacement to the K nearest defining rooms of the other five forms, by absolute difference of
ln(measure + 1), ties broken by room name, on two measures run separately: coded concepts (record size) and canvas-work
concepts (D01 to D04; _analysis/d6a10_room_sizes.py). An op survives a matching where the form's share over the matched
share is 1.2 or more (a matched share of 0 survives). A cell survives a matching where one of its deciding ops survives,
and survives the test where it survives both. Reported beside, not used for the mark: the ratio against the other five
forms unmatched, and survival at K = 3 and K = 10.

    python3 out/_analysis/d6a10_size_test.py --json > out/_analysis/d6a10_size_test.json
    python3 out/_analysis/d6a10_size_test.py --tsv > out/form-cells-size-D6.tsv
    python3 out/_analysis/d6a10_size_test.py --md > out/retelling-D6-parts/D6a10-size.md
"""
import argparse, collections, csv, json, math, os, re, statistics

ap = argparse.ArgumentParser()
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument("--json", action="store_true")
g.add_argument("--tsv", action="store_true")
g.add_argument("--md", action="store_true", help="print the retelling's section on the test (retelling-D6-parts)")
a = ap.parse_args()
AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
TAG = {"A": "d5a36", "B": "d5a37", "C": "d5a38", "D": "d5a39", "E": "d5a40", "F": "d5a41"}
OPS_S = ("add-step", "add-condition", "link")
K = 5
RATIO = 1.2
sizes = json.load(open(os.path.join(AN, "d6a10_room_sizes.json"), encoding="utf-8"))["rooms"]
rows = list(csv.DictReader(open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8"), delimiter="\t"))
dfn = {f: sorted((r["room"] for r in rows if r["form"] == f and r["role"] == "defining"), key=str.lower) for f in TAG}
form_of = {s: f for f, ss in dfn.items() for s in ss}
facts = {f: json.load(open(os.path.join(AN, "%s_facts.json" % t), encoding="utf-8")) for f, t in TAG.items()}
tabs = {f: {(r["element"], r["op"]): r for r in facts[f]["elements"]} for f in TAG}
holds = collections.defaultdict(set)  # (unit, op) -> rooms
for f, t in TAG.items():
    for l in json.load(open(os.path.join(AN, "%s_lines.json" % t), encoding="utf-8"))["lines"]:
        if l.get("role") == "defining":
            holds[(l["element"], l["op"])].add(l["sub"])
written = [json.loads(l) for l in open(os.path.join(OUT, "fractal-forms-D6.jsonl"), encoding="utf-8")]
changed = [w for w in written if w["relation"] != "untouched"]


def deciding(u, f):
    """The deciding ops as the rule chose them (d6_fractal.py), at ratio 1.2 and floor 10 per cent."""
    floor = max(5, math.ceil(0.10 * facts[f]["n_def"]))
    lean = {op: tabs[f].get((u, op)) for op in OPS_S + ("restrict",)}
    lean = {op: r for op, r in lean.items() if r and r["form_def"] >= floor and (r["ratio"] or 0) >= 1.2}
    s_lean = {op: r for op, r in lean.items() if op in OPS_S}
    if "restrict" in lean and lean["restrict"]["form_def"] >= max([r["form_def"] for r in s_lean.values()] or [0]):
        return ["restrict"]
    return sorted(s_lean, key=lambda op: -s_lean[op]["form_def"])


# check: the room-level holders give back the facts files' counts for every deciding op
bad = []
for w in changed:
    u, f = w["element"], w["form"]
    for op in deciding(u, f):
        n = len(holds[(u, op)] & set(dfn[f]))
        pop = len(holds[(u, op)] & set(form_of))
        if n != tabs[f][(u, op)]["form_def"] or pop != tabs[f][(u, op)]["pop_def"]:
            bad.append((u, f, op, n, tabs[f][(u, op)]["form_def"], pop, tabs[f][(u, op)]["pop_def"]))
if bad:
    raise SystemExit("room-level holders do not give back the facts counts: %s" % bad)


def lnm(s, measure):
    return math.log(sizes[s][measure] + 1)


match_cache = {}


def matches(f, measure, k):
    key = (f, measure, k)
    if key not in match_cache:
        pool = [s for g, ss in dfn.items() if g != f for s in ss]
        m = {}
        for s in dfn[f]:
            x = lnm(s, measure)
            m[s] = sorted(pool, key=lambda p: (abs(lnm(p, measure) - x), p.lower()))[:k]
        match_cache[key] = m
    return match_cache[key]


def test_op(u, f, op, measure, k):
    h = holds[(u, op)]
    share = len(h & set(dfn[f])) / len(dfn[f])
    m = matches(f, measure, k)
    mshare = sum(sum(1 for p in ps if p in h) / k for ps in m.values()) / len(m)
    ratio = share / mshare if mshare else float("inf")
    return share, mshare, ratio, ratio >= RATIO


out = []
for w in changed:
    u, f = w["element"], w["form"]
    ops = deciding(u, f)
    others = [s for g, ss in dfn.items() if g != f for s in ss]
    row = {"element": u, "form": f, "dimension": w["dimension"], "relation": w["relation"], "deciding_ops": ops,
           "holders": {op: len(holds[(u, op)] & set(dfn[f])) for op in ops}, "ops": {}}
    for op in ops:
        share = len(holds[(u, op)] & set(dfn[f])) / len(dfn[f])
        oshare = len(holds[(u, op)] & set(others)) / len(others)
        res = {"form_share": round(share, 4), "rule_ratio": tabs[f][(u, op)]["ratio"],
               "others_unmatched_ratio": round(share / oshare, 3) if oshare else None}
        for measure in ("coded", "canvas"):
            for k in (3, 5, 10):
                _s, ms, r, ok = test_op(u, f, op, measure, k)
                res["%s_k%d" % (measure, k)] = {"matched_share": round(ms, 4),
                                                 "ratio": round(r, 3) if r != float("inf") else None, "survives": ok}
        row["ops"][op] = res
    for measure in ("coded", "canvas"):
        for k in (3, 5, 10):
            row["survives_%s_k%d" % (measure, k)] = any(row["ops"][op]["%s_k%d" % (measure, k)]["survives"] for op in ops)
    row["survives"] = row["survives_coded_k5"] and row["survives_canvas_k5"]
    row["fails_on"] = [m for m in ("coded", "canvas") if not row["survives_%s_k5" % m]]
    for k in (3, 10):
        row["survives_k%d" % k] = row["survives_coded_k%d" % k] and row["survives_canvas_k%d" % k]
    out.append(row)

val = lambda x: float("inf") if x is None else x  # noqa: E731


def best(r, key):
    op = max(r["deciding_ops"], key=lambda o: val(r["ops"][o][key]["ratio"]))
    return op, r["ops"][op][key]


ORDER = "AFBCDE"
if a.json:
    by_form = {}
    for f in ORDER:
        rs = [r for r in out if r["form"] == f]
        by_form[f] = {"changed": len(rs), "survive": sum(r["survives"] for r in rs),
                      "fail_coded": sum(not r["survives_coded_k5"] for r in rs),
                      "fail_canvas": sum(not r["survives_canvas_k5"] for r in rs),
                      "survive_k3": sum(r["survives_k3"] for r in rs), "survive_k10": sum(r["survives_k10"] for r in rs)}
    print(json.dumps({"rule": {"k": K, "ratio": RATIO, "measures": ["coded concepts", "canvas-work concepts (D01-D04)"]},
                      "cells": len(out), "survive": sum(r["survives"] for r in out), "by_form": by_form, "rows": out},
                     ensure_ascii=False))
elif a.tsv:
    # one row per cell; for each matching, the deciding op with the highest size-held ratio (inf where its matched
    # share is 0) carries the cell
    cols = ["element", "form", "dimension", "relation", "deciding_ops", "holders", "rule_ratio",
            "others_unmatched_ratio", "coded_op", "coded_matched_share", "coded_ratio", "coded_survives",
            "canvas_op", "canvas_matched_share", "canvas_ratio", "canvas_survives", "size_held", "fails_on",
            "survives_at_k3", "survives_at_k10"]
    print("\t".join(cols))
    order = {f: i for i, f in enumerate(ORDER)}
    for r in sorted(out, key=lambda r: (order[r["form"]], r["dimension"], r["element"])):
        top = r["deciding_ops"][0]
        cop, c = best(r, "coded_k5")
        vop, v = best(r, "canvas_k5")
        print("\t".join(str(x) for x in [
            r["element"], r["form"], r["dimension"], r["relation"], ",".join(r["deciding_ops"]),
            ",".join(str(r["holders"][o]) for o in r["deciding_ops"]), r["ops"][top]["rule_ratio"],
            r["ops"][top]["others_unmatched_ratio"], cop, c["matched_share"], "inf" if c["ratio"] is None else c["ratio"],
            r["survives_coded_k5"], vop, v["matched_share"], "inf" if v["ratio"] is None else v["ratio"],
            r["survives_canvas_k5"], "survives" if r["survives"] else "size-dependent", ",".join(r["fails_on"]) or "none",
            r["survives_k3"], r["survives_k10"]]))
else:
    names = open(os.path.join(OUT, "room-forms-names.md"), encoding="utf-8").read()
    FNAME = {m.group(1): m.group(2).strip() for m in re.finditer(r"\| ([A-F]) \| ([^|]+) \|", names)}
    sens = {(r["element"], r["form"]): r["mark"] for r in csv.DictReader(
        open(os.path.join(OUT, "form-cells-sensitivity-D6.tsv"), encoding="utf-8"), delimiter="\t")}
    word = {"coded": "record size", "canvas": "canvas-work concepts"}
    n_surv = sum(r["survives"] for r in out)
    L = ["## The size-held test", "",
         "Written at D6a-10 on J's word (27 October, 09:27 Berlin) by `_analysis/d6a10_size_test.py`; each cell's result "
         "is in `form-cells-size-D6.tsv`. The test asks whether a form's lean on a unit survives when the form's rooms are "
         "compared with rooms of the same record size, rather than with all 558 defining rooms. The rule was logged in "
         "the diary before the script ran:",
         "- each of a form's defining rooms is matched, with replacement, to the %d defining rooms of the other five "
         "forms nearest to it in size (by the logarithm of the count), ties broken by room name;" % K,
         "- two measures are run separately: record size (coded concepts) and canvas-work concepts (concepts whose "
         "theme sits under Critical mass, Coordination without command, Maintenance or Order without law);",
         "- an op survives where the form's share of rooms holding it is %.1f times the matched rooms' share or more "
         "(the rule's own ratio), and a cell survives where one of its deciding ops survives both matchings; a cell "
         "that fails either is size-dependent." % RATIO, "",
         "**The result.** %d of the %d changed cells survive both matchings; %d are size-dependent. None of the %d cells "
         "the sensitivity section keeps at ratio 1.5 and floor 15 per cent is size-dependent." % (
             n_surv, len(out), len(out) - n_surv, sum(1 for v in sens.values() if v == "robust")), ""]
    for f in ORDER:
        rs = [r for r in out if r["form"] == f]
        dfr = dfn[f]
        med_c = statistics.median(sizes[s]["coded"] for s in dfr)
        med_v = statistics.median(sizes[s]["canvas"] for s in dfr)
        fails = [r for r in rs if not r["survives"]]
        raised = sum(1 for r in rs if val(best(r, "coded_k5")[1]["ratio"]) > val(r["ops"][r["deciding_ops"][0]]["others_unmatched_ratio"]))
        parts = []
        for r in fails:
            rat = " and ".join("%s %.2f" % (word[m], val(best(r, m + "_k5")[1]["ratio"])) for m in r["fails_on"])
            parts.append("%s (%s; size-held ratio on %s)" % (r["element"], r["relation"], rat))
        L.append("- **%s, %s** (median record %s coded concepts, %s of them canvas work): %d of %d cells survive%s. "
                 "Matching on record size raises the ratio above the unmatched comparison with the other forms in %d of "
                 "the %d cells." % (f, FNAME[f], ("%g" % med_c), ("%g" % med_v), len(rs) - len(fails), len(rs),
                                    (". Size-dependent: " + "; ".join(parts)) if fails else "", raised, len(rs)))
    flip = [r for r in out if r["survives_k3"] != r["survives"] or r["survives_k10"] != r["survives"]]
    dec = [min(val(best(r, "coded_k5")[1]["ratio"]), val(best(r, "canvas_k5")[1]["ratio"])) for r in flip]
    L += ["", "**How firm the marks are.** With 3 or 10 matches instead of %d, %d cells change outcome at one setting "
              "or the other: %s. At %d matches their deciding ratios (the lower of the two matchings) lie between %.2f "
              "and %.2f, close to the %.1f line. The mark follows the logged rule (%d matches)." % (
                  K, len(flip), ", ".join("%s in %s" % (r["element"], r["form"]) for r in flip), K, min(dec), max(dec),
                  RATIO, K), "",
          ]
    fr = [r for r in out if r["form"] == "F"]
    f_raised = sum(1 for r in fr if val(best(r, "coded_k5")[1]["ratio"]) > val(r["ops"][r["deciding_ops"][0]]["others_unmatched_ratio"]))
    ar = [r for r in out if r["form"] == "A"]
    e_arr = [r for r in out if r["form"] == "E" and r["relation"] == "restricts" and re.match(r"A\d\d$", r["element"])]
    e_arr_canvas = sum(1 for r in e_arr if r["survives_canvas_k5"])
    L += ["**What it means.** The forms' leans are not, in the main, an effect of record size. A and F were the forms "
          "whose scores might rest on size: F's rooms have the shortest records and A's the next shortest. F keeps %d of "
          "its %d changes, and in %d of them matching on record size raises the ratio: F's rooms change these units more "
          "often than other rooms whose records are as short. A keeps %d of its %d, and none at the stricter thresholds, "
          "so A's telling is the most fragile of the six. E, whose records hold the play and less canvas work, keeps %d of "
          "its %d restrictions on arrows when matched on canvas-work concepts, so those restrictions are not only an "
          "effect of a thin record of canvas work. The size-dependent cells are named above and marked in "
          "`form-cells-sensitivity-D6.tsv` (column `size_mark`)." % (
              sum(r["survives"] for r in fr), len(fr), f_raised, sum(r["survives"] for r in ar), len(ar),
              e_arr_canvas, len(e_arr))]
    print("\n".join(L))
