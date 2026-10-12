#!/usr/bin/env python3
"""B3a-p2: the gold check of stage B3 section 3.2 on dispatch group 1, by the rule declared in notes-B3.md
("Leg B3a-p2: the gold check after group 1") before any figure was computed.

Reads one valid reply per packet of group 1 (out/_fleet_raw/B3/<batch>/rN.jsonl whose rN.meta.json says valid),
pass-1 lines only (no `revises`, no `predicted_confusion`). Each line is keyed on (batch, position); the item is
batches-B3.jsonl's item at that position; the typed fleet theme id is checked against it through fleet_ids.jsonl.
A gold copy is a position whose item is in the batch's gold_items.

Per copy: Jaccard against gold_items.jsonl, against the rechecked placement (b2_gold_items.tsv), primary match;
the B2 figure of the same copy is the mean over B2's nine frozen-scheme readings of the item (gold, stab-1,
stab-2). Fall = B2 mean - B3 mean over the same copies; beyond the floor when over 1 - 0.807. Bootstrap 95%
interval resampling batches (seed 20261015). Writes out/_analysis/b3_gold_group1.json and .tsv.
"""
import collections, importlib.util, json, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
RAW = os.path.join(OUT, "_fleet_raw", "B3")
spec = importlib.util.spec_from_file_location("b2s", os.path.join(AN, "b2_score.py"))
b2s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b2s)
jac, jl = b2s.jac, b2s.jl
FLOOR = 1 - 0.807


def mean(x):
    return sum(x) / len(x) if x else float("nan")


def main():
    order = json.load(open(os.path.join(AN, "b3_dispatch_order.json"), encoding="utf-8"))
    g1 = order["groups"]["1"] if "1" in order["groups"] else list(order["groups"].values())[0]
    partial = json.load(open(os.path.join(RAW, "PARTIAL-2026-10-12T153202Z.json"), encoding="utf-8"))
    if set(partial["only"].split(",")) != set(g1):
        raise SystemExit("the PARTIAL record's packets are not group 1 of b3_dispatch_order.json")
    batches = {b["batch"]: b for b in jl(os.path.join(OUT, "batches-B3.jsonl"))}
    ft = {r["fleet"]: (r["sub"], r["id"]) for r in jl(os.path.join(OUT, "fleet_ids.jsonl")) if r["kind"] != "c"}
    gold = {r["item"]: r["third_order"] for r in jl(os.path.join(OUT, "gold_items.jsonl"))}
    rech, b2 = {}, {}
    for i, ln in enumerate(open(os.path.join(AN, "b2_gold_items.tsv"), encoding="utf-8")):
        c = ln.rstrip("\n").split("\t")
        if i == 0:
            continue
        rech[c[0]] = c[2].split(",")
        b2[c[0]] = [s.split(",") for col in c[3:6] for s in col.split(" | ")]
    if set(b2) != set(gold) or any(len(v) != 9 for v in b2.values()):
        raise SystemExit("b2_gold_items.tsv does not hold nine readings of each gold item")

    probs, copies, lines_seen = [], [], collections.Counter()
    for bid in g1:
        b = batches[bid]
        d = os.path.join(RAW, bid)
        valid = [f for f in sorted(os.listdir(d)) if re.fullmatch(r"r\d+\.meta\.json", f)
                 and json.load(open(os.path.join(d, f), encoding="utf-8")).get("valid")]
        if len(valid) != 1:
            probs.append("%s: %d valid replies" % (bid, len(valid))); continue
        rdr = valid[0].split(".")[0]
        meta = json.load(open(os.path.join(d, valid[0]), encoding="utf-8"))
        p1 = [x for x in jl(os.path.join(d, rdr + ".jsonl")) if "predicted_confusion" not in x and "revises" not in x]
        pos = sorted(x.get("position") for x in p1)
        if pos != list(range(1, b["n_items"] + 1)):
            probs.append("%s: pass-1 positions are not 1..%d" % (bid, b["n_items"]))
        lines_seen["pass1"] += len(p1)
        for x in p1:
            p = x.get("position")
            if not isinstance(p, int) or not 1 <= p <= len(b["items"]):
                continue
            it = b["items"][p - 1]
            typed = ft.get(x.get("theme_id"))
            if typed is None or "%s/%s" % typed != it:
                probs.append("%s position %d: typed %s, the batch holds %s" % (bid, p, x.get("theme_id"), it))
            if x.get("read") == "label-only":
                probs.append("%s position %d: read label-only" % (bid, p))
            if it in b["gold_items"]:
                s = x.get("third_order") or []
                copies.append({"batch": bid, "reader": "%s/%s" % (bid, rdr), "agent": b["agent"],
                               "replicate": b["replicate"], "reissue": meta.get("reissue", 0), "item": it,
                               "position": p, "n_items": b["n_items"], "set": s, "mine": gold[it],
                               "fid": jac(s, gold[it]) if s else 0.0, "fid_r": jac(s, rech[it]) if s else 0.0,
                               "prim": bool(s) and s[0] == gold[it][0],
                               "b2_fid": mean([jac(y, gold[it]) for y in b2[it]]),
                               "b2_fid_r": mean([jac(y, rech[it]) for y in b2[it]]),
                               "b2_prim": mean([y[0] == gold[it][0] for y in b2[it]]),
                               "missed": sorted(set(gold[it]) - set(s)), "extra": sorted(set(s) - set(gold[it]))})
    seeded = sum(len(batches[bid]["gold_items"]) for bid in g1)

    def figs(cs):
        return {k: mean([c[k] for c in cs]) for k in ("fid", "fid_r", "prim", "b2_fid", "b2_fid_r", "b2_prim")}
    F = figs(copies)
    fall = {"fidelity": F["b2_fid"] - F["fid"], "rechecked": F["b2_fid_r"] - F["fid_r"], "primary": F["b2_prim"] - F["prim"]}
    byb = collections.defaultdict(list)
    for c in copies:
        byb[c["batch"]].append(c)
    rng, boot = random.Random(20261015), {k: [] for k in fall}
    keys = sorted(byb)
    for _ in range(4000):
        cs = [c for k in (rng.choice(keys) for _ in keys) for c in byb[k]]
        f = figs(cs)
        boot["fidelity"].append(f["b2_fid"] - f["fid"]); boot["rechecked"].append(f["b2_fid_r"] - f["fid_r"])
        boot["primary"].append(f["b2_prim"] - f["prim"])
    ci = {k: (sorted(v)[int(0.025 * len(v))], sorted(v)[int(0.975 * len(v)) - 1]) for k, v in boot.items()}
    stop = fall["fidelity"] > FLOOR or fall["primary"] > FLOOR
    byi = collections.defaultdict(list)
    for c in copies:
        byi[c["item"]].append(c)
    items = {it: dict(figs(cs), n=len(cs)) for it, cs in byi.items()}
    over = sorted(it for it, f in items.items() if f["b2_fid"] - f["fid"] > FLOOR)
    missed = collections.Counter(t for c in copies for t in c["missed"])
    extra = collections.Counter(t for c in copies for t in c["extra"])

    for p in probs:
        print("problem: " + p)
    print("group 1: %d batches; pass-1 lines %d; gold copies seeded %d, returned %d, on %d gold items, in %d batches"
          % (len(g1), lines_seen["pass1"], seeded, len(copies), len(byi), len(byb)))
    print("B3 group 1: fidelity %.3f, against rechecked %.3f, primary %.3f" % (F["fid"], F["fid_r"], F["prim"]))
    print("B2 nine readings, same copies: fidelity %.3f, against rechecked %.3f, primary %.3f" % (F["b2_fid"], F["b2_fid_r"], F["b2_prim"]))
    for k in fall:
        print("fall %-9s %+.3f (95%% interval over batches %+.3f to %+.3f); floor %.3f" % (k, fall[k], ci[k][0], ci[k][1], FLOOR))
    print("decision by the declared rule: %s" % ("STOP: group 2 does not go out as built" if stop else "group 2 goes out as built"))
    print("items whose own fall in fidelity is beyond the floor: %s" % (", ".join(
        "%s (n=%d, B3 %.2f, B2 %.2f)" % (it, items[it]["n"], items[it]["fid"], items[it]["b2_fid"]) for it in over) or "none"))
    print("themes of mine missed (copies): %s" % dict(missed.most_common()))
    print("themes added beyond mine (copies): %s" % dict(extra.most_common()))
    print("exact set match with mine: %d of %d copies; empty sets: %d" % (
        sum(set(c["set"]) == set(c["mine"]) for c in copies), len(copies), sum(not c["set"] for c in copies)))
    with open(os.path.join(AN, "b3_gold_group1.tsv"), "w", encoding="utf-8") as fh:
        fh.write("batch\treader\tagent\treplicate\treissue\tposition\tn_items\titem\tmine\treader_set\tfidelity\t"
                 "fidelity_rechecked\tprimary\tb2_fidelity_same_item\tmissed\textra\n")
        for c in sorted(copies, key=lambda c: (c["batch"], c["position"])):
            fh.write("\t".join(str(v) for v in (c["batch"], c["reader"], c["agent"], c["replicate"], c["reissue"],
                     c["position"], c["n_items"], c["item"], ",".join(c["mine"]), ",".join(c["set"]),
                     "%.3f" % c["fid"], "%.3f" % c["fid_r"], int(c["prim"]), "%.3f" % c["b2_fid"],
                     ",".join(c["missed"]), ",".join(c["extra"]))) + "\n")
    json.dump({"group1_batches": len(g1), "gold_seeded": seeded, "gold_returned": len(copies), "problems": probs,
               "b3": {k: F[k] for k in ("fid", "fid_r", "prim")}, "b2_same_copies": {k: F[k] for k in ("b2_fid", "b2_fid_r", "b2_prim")},
               "fall": fall, "interval_95_batches": ci, "floor": FLOOR, "stop": stop, "items": items,
               "items_beyond_floor": over, "missed": missed, "extra": extra},
              open(os.path.join(AN, "b3_gold_group1.json"), "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
