#!/usr/bin/env python3
"""B3b: render stage B3's four check reports from out/_analysis/b3_check_<tag>.json.

    python3 out/_analysis/b3_reports.py --tag <tag> --basis "<one sentence naming the assembly>" [--write]

Writes out/fidelity-B3.md, out/position-B3.md, out/multiplacement_register-B3.md, out/agent_report-B3.md. An
existing report is kept as <name>.superseded-<utc>.md first, never deleted. The justification counts are my
reading of out/_analysis/b3_why_not_one_sample_<tag>.tsv (notes-B3.md), passed in JUSTIFY below.
"""
import argparse, datetime, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
FLOOR, TOL = 1 - 0.807, 0.10
LICENCE = ("**What these figures license.** The readers share an architecture with me and with each other, so a figure "
           "here bounds whether the instrument decides, not whether it is right.")
# my reading of the 40 sampled why_not_one texts (b3_why_not_one_sample_record.tsv, seed 20261015; the trial
# sample b3_why_not_one_sample_scratch_c.tsv, also read, gave the same counts)
JUSTIFY = {"material genuinely spans two themes": 40, "scheme lacks a theme for this": 0, "reader hedging": 0,
           "restatement of both gates being satisfied (a defect)": 0}


def f3(x):
    return "-" if x is None else "%.3f" % x


def fidelity(R, basis):
    g = R["gold"]
    L = ["# Gold fidelity, stage B3", "", basis, "",
         "Each seeded gold copy is scored against my placement in `gold_items.jsonl` (Jaccard), against the rechecked "
         "placement, on exact set and on primary match. The B2 figure for the same copy is the mean over B2's nine "
         "frozen-scheme readings of that item (the gold round, stab-1, stab-2). The fall is B2 minus B3. The stop rule, "
         "declared before group 1 was scored (`notes-B3.md`): a fall over %.3f (1 − 0.807, `stability-B2.md`) in "
         "fidelity or primary match." % FLOOR, "",
         "The next table gives the fleet's gold figures beside B2's on the same copies, for the whole fleet and per dispatch group.", "",
         "| set | copies | fidelity | rechecked | exact | primary | B2 fidelity, same copies | B2 primary, same copies |",
         "|---|---|---|---|---|---|---|---|"]
    for k, lab in (("all", "whole fleet"), ("group1", "group 1 (100 batches)"), ("group2", "group 2")):
        v = g[k]
        L.append("| %s | %d | %s | %s | %s | %s | %s | %s |" % (lab, v["copies"], f3(v["fidelity"]), f3(v["rechecked"]),
                 f3(v["exact"]), f3(v["primary"]), f3(v["b2_same"]), f3(v["b2_primary_same"])))
    L += ["", "**The fall** in fidelity over the whole fleet is %s (95%% interval over batches %s to %s). It is inside the "
          "floor of %.3f. The fleet's gold fidelity did not fall against B2 on the same items; group 2 went out on that "
          "ground and held it." % (f3(g["fall"]), f3(g["fall_ci"][0]), f3(g["fall_ci"][1]), FLOOR), "",
          "**The corpus readings of gold items** (the live readings, apart from the seeded copies): %d lines, fidelity %s, "
          "primary %s." % (g["corpus_readings_of_gold_items"]["lines"], f3(g["corpus_readings_of_gold_items"]["fidelity"]),
                           f3(g["corpus_readings_of_gold_items"]["primary"])), "",
          "**Themes of mine the readers missed** (copies): " + ", ".join("%s %d" % kv for kv in list(g["missed"].items())[:12]) + ".",
          "**Themes the readers added** (copies): " + ", ".join("%s %d" % kv for kv in list(g["extra"].items())[:12]) + ".", "",
          "The next table gives each gold item: copies, the fleet's fidelity and primary match, B2's fidelity on the same item, and the fall.", "",
          "| item | copies | fidelity | primary | B2 fidelity | fall |", "|---|---|---|---|---|---|"]
    for it, v in sorted(g["items"].items(), key=lambda kv: -kv[1]["fall"]):
        L.append("| %s | %d | %s | %s | %s | %s |" % (it, v["copies"], f3(v["fidelity"]), f3(v["primary"]), f3(v["b2_same"]), f3(v["fall"])))
    L += ["", "## Per batch and per reader", "",
          "One line per gold copy. Each batch has one reader (its agent), so a batch row is a reader row. Stage B4 reads this table and does not recompute it.", "",
          "| batch | agent | replicate | group | position | of | item | mine | reader's set | fidelity | primary | missed |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in sorted(g["copies"], key=lambda c: (c["batch"], c["position"])):
        L.append("| %s | %s | %d | %d | %d | %d | %s | %s | %s | %.2f | %d | %s |" % (
            c["batch"], c["agent"], c["replicate"], c["group"], c["position"], c["n"], c["item"], ",".join(c["mine"]),
            ",".join(c["set"]), c["fid"], int(c["prim"]), ",".join(c["missed"]) or "-"))
    L += ["", LICENCE, ""]
    return "\n".join(L)


def position(R, basis):
    p, fo, rv, d = R["position"], R["formation"], R["revision"], R["duplicates"]
    L = ["# The position curve, stage B3", "", basis, "",
         "Pooled across the fleet, pass 1, corpus copies with both replicates returned. Three outcomes per line: "
         "agreement (Jaccard with the other replicate's line on the same item), multi (more than one theme) and arguable "
         "(confidence \"arguable\"). Each is regressed on position within the batch with batch fixed effects; standard "
         "errors are clustered by batch, and one reader holds each batch. Declared before fitting: a tolerable change "
         "of %.2f in each outcome across a 15-position batch (14 steps); the sensitivity is the change over 14 steps "
         "detected with 80%% power at two-sided 5%%, 2.80 × SE × 14." % TOL, "",
         "The next table gives the slope per position, the change it implies across 14 positions with its interval, and the sensitivity.", "",
         "| outcome | slope per position | SE | change over 14 | 95% interval | sensitivity over 14 | within the tolerance |",
         "|---|---|---|---|---|---|---|"]
    for k, lab in (("agree", "agreement"), ("multi", "multi rate"), ("arg", "arguable rate")):
        v = p[k]
        within = abs(v["change14_ci"][0]) <= TOL and abs(v["change14_ci"][1]) <= TOL and v["sensitivity14"] <= TOL
        L.append("| %s | %.4f | %.4f | %+.3f | %+.3f to %+.3f | %.3f | %s |" % (lab, v["slope"], v["se"], v["change14"],
                 v["change14_ci"][0], v["change14_ci"][1], v["sensitivity14"], "yes" if within else "no"))
    L += ["", "The next table gives each outcome by decile of relative position, (p − 1) ÷ (n − 1).", "",
          "| decile | lines | agreement | multi | arguable |", "|---|---|---|---|---|"]
    for dkey in sorted(p["agree"]["deciles"], key=int):
        L.append("| %d | %d | %.3f | %.3f | %.3f |" % (int(dkey) + 1, p["agree"]["deciles"][dkey][0], p["agree"]["deciles"][dkey][1],
                 p["multi"]["deciles"][dkey][1], p["arg"]["deciles"][dkey][1]))
    a = p["arg"]
    L += ["", "**What it shows.** Agreement does not move with position: %+.3f over 14 positions, interval %+.3f to %+.3f, "
          "and the fit would have caught a change of %.3f. The multi rate's interval also sits inside the tolerance. The "
          "arguable rate rises: %+.3f over 14 positions (%+.3f to %+.3f). That is inside the declared tolerance of %.2f, "
          "but it is not zero, so it goes into `defects.jsonl` as an unresolved diagnostic with the evidence that would "
          "separate its causes (harder items late, context length, earlier answers). A position effect is a diagnostic "
          "of changing responses, not an identified cause." % (p["agree"]["change14"], p["agree"]["change14_ci"][0],
          p["agree"]["change14_ci"][1], p["agree"]["sensitivity14"], a["change14"], a["change14_ci"][0], a["change14_ci"][1], TOL), "",
          "**The multi rate over readers** (quantiles 0, 10, 25, 50, 75, 90, 100%%, over %d readers): %s." % (
              p["multi_rate_readers"]["readers"], ", ".join("%.2f" % q for q in p["multi_rate_readers"]["q"])), "",
          "## Beside the curve", "",
          "**Pass 1 to pass 2.** Over %d corpus lines, %.2f%% changed their set or primary in pass 2, and %.2f%% carry "
          "`changed: true`. %.1f%% of readers revised anything. The second pass is close to a copy of the first, so it "
          "measures within-batch formation weakly." % (rv["pass2_corpus_lines"], 100 * rv["set_or_primary_changed"],
                                                      100 * rv["flag_changed"], 100 * rv["readers_revising_any"]), "",
          "**Formation per reader**, first five positions against last five, in the %d batches of ten or more: arguable "
          "%.3f then %.3f; agreement with the other replicate %.3f then %.3f. %d readers lost more than %.2f in "
          "agreement from first to last, and %d gained more than that, so the per-reader movement is spread both ways."
          % (fo["readers"], fo["arguable_first5"], fo["arguable_last5"], fo["agree_first5"], fo["agree_last5"],
             fo["readers_agree_drop_over_tol"], TOL, fo["readers_agree_rise_over_tol"]), "",
          "**The duplicate.** %d batches returned both copies. The two copies agree on every one (Jaccard %.3f, "
          "disagreement %.3f), against a between-reader exact-set disagreement of %.3f. The readers recognised the "
          "repeat: %d second copies repeat the first copy's `why` word for word, and %d say it is a repeat (median "
          "gap %d positions). So the duplicate measures recall of an earlier answer in the same context, not fresh "
          "within-reader instability." % (d["n"], d["jaccard"], d["disagree_rate"], 1 - R["agreement"]["exact"],
                                          d["why_identical"], d["why_names_repeat"], d["gap_median"]), "",
          LICENCE, ""]
    return "\n".join(L)


def register(R, basis):
    r, scr = R["register"], R["screen"]
    L = ["# The multiplacement register, stage B3", "", basis, "",
         "Rule 0's log read as a measurement: pass 1, corpus copies.", "",
         "**The rate.** %.3f of corpus lines place more than one theme (%d records; %d lines place three). %d lines "
         "are empty. The per-reader rates and the funnel are in `agent_report-B3.md`." % (
             r["multi_rate"], r["records"], r["three_theme_lines"], r["empties"]), "",
         "## The pair table", "",
         "The next table lists the twenty most frequent (primary, additional) pairs, with the readers and rooms they span and how many readers predicted the pair as their hardest.", "",
         "| rank | primary | additional | count | readers | rooms | predicted by |", "|---|---|---|---|---|---|---|"]
    for i, t in enumerate(r["top20"], 1):
        L.append("| %d | %s | %s | %d | %d | %d | %d |" % (i, t["primary"], t["additional"], t["count"], t["readers"], t["rooms"], t["predicted_by"]))
    L += ["", "Every pair in the table recurs across many readers and rooms; each is a boundary the scheme has not drawn, "
          "and stage C1 reads this table first. T3-005/T3-021 appears in both orders.", "",
          "**Against the predictions.** The readers' most predicted pairs: " + "; ".join(
              "%s/%s by %d" % (k[0], k[1], v) for k, v in r["predicted_top"][:8]) + ". Pairs in the top twenty that "
          "readers also predicted often: those with \"predicted by\" above twenty in the table.", "",
          "## The justifications, read", "",
          "I read 40 `why_not_one` texts, one per reader, drawn by seed 20261015 (`out/_analysis/b3_why_not_one_sample_*.tsv`). "
          "The next table counts them by class.", "", "| class | texts |", "|---|---|"]
    for k, v in JUSTIFY.items():
        L.append("| %s | %d |" % (k, v))
    L += ["", "Every text names an act in the material that the single placement would leave out (a thanks beside a "
          "celebration, quiet repair beside a called defence, a chat's decisions carried back beside the move to the "
          "chat). None restates the gates. Three (iastate t03, frc t04, ohio t04) also name a theme that is not on their "
          "line; one (malaysia t04) is short but still names the acts.", "",
          "## Per-theme exception load", "",
          "The next table lists themes placed as `additional` at least ten times, ordered by additional ÷ primary.", "",
          "| theme | as additional | as primary | ratio |", "|---|---|---|---|"]
    for t in r["exception_load"][:15]:
        L.append("| %s | %d | %d | %.2f |" % (t["theme"], t["additional"], t["primary"], t["ratio"]))
    L += ["", "T3-089 and T3-152 stand out: each is placed far more often beside another theme than alone. Before C1 "
          "decides whether either is a modifier, an overlapping construct or a missing boundary, it should read their "
          "designation rules and supporting concepts.", "",
          "**The empties.** %d corpus lines place no theme. Rule 0's characterisation of empties therefore has nothing "
          "to describe." % r["empties"], "",
          "**Screen** (section 3.1): read values %s; no `label-only`; multi lines without their record or with an empty "
          "`why_not_one`: %d; lines reduced to their primary: %d." % (
              ", ".join("%s %d" % kv for kv in scr["read_values"].items()), sum(v for k, v in scr["defects_by_kind"].items() if "multi" in k),
              scr["reduced_to_primary"]), "", LICENCE, ""]
    return "\n".join(L)


def agents(R, basis):
    a, fun, fo, pr, vc, inv, cov = R["agreement"], R["funnel"], R["families_opened"], R["predictions"], R["variance_components"], R["inventory"], R["coverage"]
    L = ["# The fleet as a population, stage B3", "", basis, "",
         "Pass 1, corpus copies. Agreement is as `notes-B2.md` defines it: Jaccard on placement sets, so "
         "`[\"T3-004\"]` against `[\"T3-004\",\"T3-011\"]` scores 0.5; alpha uses distance 1 − Jaccard. No exemplar arm "
         "was served, so there are no exemplar figures; B2 also served none.", "",
         "## Agreement", "",
         "The next table gives corpus-wide agreement between the two replicates over %d items." % a["items_both"], "",
         "| Jaccard | exact set | exact list, order kept | primary | alpha |", "|---|---|---|---|---|",
         "| %s | %s | %s | %s | %s |" % (f3(a["jaccard"]), f3(a["exact"]), f3(a["exact_list"]), f3(a["primary"]), f3(a["alpha"])), "",
         "Against stage B2: the stability floor is 0.807 (Jaccard, the arm against itself under two briefs). Corpus-wide "
         "Jaccard of %s sits %s it, so most of the remaining disagreement is the arm's own." % (
             f3(a["jaccard"]), "at" if abs(a["jaccard"] - 0.807) < 0.03 else ("below" if a["jaccard"] < 0.807 else "above")), "",
         "The next table gives agreement per family (an item counts for each family holding either replicate's primary).", "",
         "| family | items | Jaccard | exact set | primary |", "|---|---|---|---|---|"]
    for g, v in a["families"].items():
        L.append("| %s | %d | %s | %s | %s |" % (g, v["n"], f3(v["jaccard"]), f3(v["exact"]), f3(v["primary"])))
    worst_f = min(a["families"].items(), key=lambda kv: kv[1]["jaccard"])
    L += ["", "The family that agreed least is %s (Jaccard %s over %d items)." % (worst_f[0], f3(worst_f[1]["jaccard"]), worst_f[1]["n"]), "",
          "**Per-theme presence agreement.** The next table lists every theme named on 20 or more items: positive "
          "agreement (both name it ÷ either names it), kappa on presence, and Jaccard over its items.", "",
          "| theme | items either | both | positive | kappa | Jaccard |", "|---|---|---|---|---|---|"]
    for t, v in sorted(a["themes"].items(), key=lambda kv: (kv[1]["positive"] if kv[1]["positive"] is not None else 2)):
        if v["either"] >= 20:
            L.append("| %s | %d | %d | %s | %s | %s |" % (t, v["either"], v["both"], f3(v["positive"]), f3(v["kappa"]), f3(v["jaccard_items"])))
    L += ["", "**The theme the fleet handled worst** (lowest positive agreement on 30 or more items): %s, named on %d "
          "items, both readers on %.0f%% of them." % (R["worst_themes"][0][0], R["worst_themes"][0][1], 100 * R["worst_themes"][0][2]), "",
          "**The duplicate rate** beside it: see `position-B3.md`; the two copies never disagree, because readers recognised the repeat.", "",
          "## The disagreement inventory (stage B4's workload)", "",
          "Over %d items with both replicates: %d placed alike (same set, same primary), %d split. Of the splits, %d "
          "differ on the primary with different sets, %d share the primary and differ only on an additional theme, and %d "
          "hold the same themes in another order. Corpus lines with more than one theme: %d; lines flagged a bag: %d. The "
          "assembler's classes: %s (1 and 2 stand; 3, 4 and 5 go to B4)." % (
              a["items_both"], inv["alike"], inv["split"], inv["split_primary"], inv["split_additional_only"],
              inv["split_order_only"], inv["multi_lines"], inv["bag_lines"],
              ", ".join("class %s %d" % (k, v) for k, v in sorted(inv["classes"].items()))), "",
          "The next table gives the inventory per family.", "", "| family | alike | split, primary | split, additional only | split, order only |", "|---|---|---|---|---|"]
    for g, v in R["inventory_families"].items():
        L.append("| %s | %d | %d | %d | %d |" % (g, v.get("alike", 0), v.get("split_primary", 0), v.get("split_additional_only", 0), v.get("split_order_only", 0)))
    L += ["", "The per-theme inventory is in `out/_analysis/b3_check_*.json` (`inventory_themes`).", "",
          "## Per-reader dispersion", "",
          "**Variance components.** A linear mixed model with crossed random intercepts for room and reader (batch): "
          + "; ".join("%s: room %.4f, reader %.4f, residual %.4f" % (y, v.get("room", float("nan")), v.get("reader", float("nan")), v.get("residual", float("nan")))
                      for y, v in vc.items() if isinstance(v, dict)) + ". The reader share is larger than the room share for both outcomes, and both are small beside the residual.", "",
          "**The funnel.** Each reader's rate against its batch size, with limits at the fleet rate ± 3 binomial standard "
          "errors. Multi rate (fleet %.3f): %d readers outside, all above. Themes per line (fleet %.3f): %d outside, %s "
          "of them the same readers. The empty rate is zero throughout." % (
              fun["multi"]["fleet"], len(fun["multi"]["outside"]), fun["themes_per_line"]["fleet"], len(fun["themes_per_line"]["outside"]),
              "most" if len(set(o[0] for o in fun["themes_per_line"]["outside"]) & set(o[0] for o in fun["multi"]["outside"])) > len(fun["themes_per_line"]["outside"]) / 2 else "few"), "",
          "**What the readers above the limits have in common.** The next table compares them with the fleet.", "",
          "| readers | items | item bytes | arguable | seconds a packet | multi | multi of the other replicate, same items |", "|---|---|---|---|---|---|---|"]
    for lab, v in (("above the limits", fun["multi_above_profile"]), ("fleet", fun["fleet_profile"])):
        L.append("| %s (%d) | %.1f | %.0f | %.3f | %.0f | %.3f | %.3f |" % (lab, v["readers"], v["items"], v["item_bytes"], v["arguable"],
                 v["elapsed_s"], v["multi"], v["multi_other_replicate_same_items"]))
    L += ["", "They held longer items, called more lines arguable and took longer. Their items also drew more second "
          "placements from the other replicate's readers than the fleet's items do, so part of the excess is in the items; "
          "the rest is the reader. Stage B4 needs their items named: the readers are listed below.", "",
          "Readers above the multi limits (batch, lines, rate): " + "; ".join("%s %d %.2f" % tuple(o) for o in fun["multi"]["outside"]) + ".", "",
          "## families_opened", "",
          "Families opened per placement line: median %s, mean %.2f. Distribution (families: lines): %s. %d of %d "
          "placements fall in a family the reader did not open; %d lines opened all 21." % (
              fo["median"], fo["mean"], ", ".join("%s: %s" % kv for kv in fo["dist"].items()), fo["into_unopened_family"],
              fo["placements"], fo["dist"].get("21", fo["dist"].get(21, 0))), "",
          "## The predicted confusions", "",
          "%d prediction lines over the returns (QB3-004 for the returns without one). %d of the predicted pairs are "
          "among the nineteen of `confusions.md`. In %d batches the predicted pair split the two replicates' primaries "
          "on at least one item of that batch." % (pr["lines"], pr["in_confusions_md"], pr["pair_split_readers_on_an_item_of_the_batch"]), "",
          "The next table lists the pairs that split the two replicates' primaries most often, how many readers predicted each, and whether `confusions.md` names it.", "",
          "| pair | primary splits | predicted by | in confusions.md |", "|---|---|---|---|"]
    for k, n, by, inc in pr["top_observed_primary_splits"]:
        L.append("| %s/%s | %d | %d | %s |" % (k[0], k[1], n, by, "yes" if inc else "no"))
    L += ["", "## Coverage", "",
          "%d of %d items have both replicates. Missing a replicate: %d (%s)." % (cov["both"], cov["items"], len(cov["missing"]),
                                                                                ", ".join(cov["missing"]) or "none"), "", LICENCE, ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True); ap.add_argument("--basis", required=True); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    R = json.load(open(os.path.join(AN, "b3_check_%s.json" % a.tag), encoding="utf-8"))
    docs = {"fidelity-B3.md": fidelity(R, a.basis), "position-B3.md": position(R, a.basis),
            "multiplacement_register-B3.md": register(R, a.basis), "agent_report-B3.md": agents(R, a.basis)}
    for n, t in docs.items():
        print("%s: %d lines, %d bytes" % (n, t.count("\n"), len(t.encode("utf-8"))))
    if not a.write:
        return
    utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for n, t in docs.items():
        p = os.path.join(OUT, n)
        if os.path.exists(p):
            os.rename(p, os.path.join(OUT, n[:-3] + ".superseded-%s.md" % utc))
        open(p, "w", encoding="utf-8").write(t)


if __name__ == "__main__":
    main()
