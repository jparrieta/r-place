#!/usr/bin/env python3
"""B4c: the comparison and the figures, as declared in notes-B4.md ("The check (B4c)", before any figure).

Reads out/_analysis/b4c_readings.jsonl (the assembly), assign_final.jsonl (the settled line), disagreements.jsonl,
b3_classes.jsonl (the two B3 readers and my B1 grouping), sample-B4.jsonl, sample-B4-R.jsonl, scheme_final.jsonl
(families) and out/_analysis/b3_check_record.json (B3's per-family agreement, read, not recomputed).

  reassign.jsonl                arm 1's readings of U and A, one line per reading, stratum uniform|adjudicated,
                                outcome agrees | disagrees-contested | disagrees-unanimous | disagrees-unresolved
  reassign-openai-astra.jsonl   arm 2's readings of U and A, the same fields
  readings-R-B4.jsonl           both arms' readings of R, with arm; no outcome (R has no settled line)
  out/_analysis/b4c_figures.json   every figure, per arm and stratum, never pooled

agrees is Jaccard 1 against the settled set. Fresh against settled is mean Jaccard over readings whose settled
line is resolved; exact and primary match beside it. The readers' agreement with each other is mean Jaccard over
items with both readings, primary and exact beside, and alpha by b2_score.alpha (distance 1 - Jaccard, chance over
the pooled sets). Dry run (figures printed, nothing written) without --write.

    python3 out/_analysis/b4c_compare.py [--write]
"""
import argparse, collections, hashlib, importlib.util, itertools, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
spec = importlib.util.spec_from_file_location("b2s", os.path.join(AN, "b2_score.py"))
b2s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b2s)
jac, alpha, jl = b2s.jac, b2s.alpha, b2s.jl
A1, A2 = "deepseek-v4.1-flash", "openai-gpt-6-astra"
NAME = {"U": "uniform", "A": "adjudicated"}
SETTLED_SHA = "d3506a8871eeb106d934824e342acb374931501c2b4dd377cc277094624bcd6b"


def mean(x):
    x = list(x)
    return sum(x) / len(x) if x else None


def r3(v):
    return None if v is None else round(v, 3)


def prim(a, b):
    return bool(a) and bool(b) and a[0] == b[0]


def agreement(pairs):
    """pairs: list of (set1, set2) per item; B2's definition."""
    if not pairs:
        return {"items": 0}
    return {"items": len(pairs), "jaccard": r3(mean(jac(a, b) for a, b in pairs)),
            "exact": r3(mean(set(a) == set(b) for a, b in pairs)), "primary": r3(mean(prim(a, b) for a, b in pairs)),
            "alpha": r3(alpha([[a, b] for a, b in pairs]))}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    if hashlib.sha256(open(os.path.join(OUT, "assign_final.jsonl"), "rb").read()).hexdigest() != SETTLED_SHA:
        sys.exit("assign_final.jsonl is not the settled line of B4a-07")
    rd = jl(os.path.join(AN, "b4c_readings.jsonl"))
    fin = {(x["sub"], x["theme_id"]): x for x in jl(os.path.join(OUT, "assign_final.jsonl"))}
    dis = {(x["sub"], x["theme_id"]) for x in jl(os.path.join(OUT, "disagreements.jsonl"))}
    b3 = {(x["sub"], x["theme_id"]): x for x in jl(os.path.join(OUT, "b3_classes.jsonl"))}
    s0 = {(x["sub"], x["theme_id"]): x for x in jl(os.path.join(OUT, "sample-B4.jsonl"))}
    sr = {(x["sub"], x["theme_id"]): x for x in jl(os.path.join(OUT, "sample-B4-R.jsonl"))}
    fam = {r["id"]: r["family"] for r in jl(os.path.join(OUT, "scheme_final.jsonl"))}
    b3rec = json.load(open(os.path.join(AN, "b3_check_record.json"), encoding="utf-8"))["agreement"]["families"]

    def settled(k):
        f = fin[k]
        return [] if f.get("unresolved") is True else [t for t in f.get("third_order") or [] if t and t != "unresolved"]

    rows = {A1: [], A2: []}
    rrows = []
    for x in rd:
        k = (x["sub"], x["theme_id"])
        c = b3[k]
        base = {"sub": k[0], "theme_id": k[1], "item": x["item"], "arm": x["arm"], "packet": x["packet"],
                "position": x["position"], "reader": x["reader"], "replicate": x["replicate"],
                "third_order": x["third_order"], "confidence": x["confidence"], "multi": x["multi"], "bag": x["bag"],
                "support": x["support"], "support_by_theme": x["support_by_theme"], "also_present": x["also_present"],
                "class": c["class"], "fleet": [c.get("r1"), c.get("r2")], "b1": c.get("b1")}
        if x["stratum"] == "R":
            earlier = set(c.get("r1") or []) | set(c.get("r2") or []) | set(c.get("b1") or [])
            F = set(x["third_order"])
            among = "empty" if not F else "all" if F <= earlier else "some" if F & earlier else "none"
            rrows.append(dict(base, stratum="R", also_in=sr[k].get("also_in"), among=among,
                              settled_unresolved=settled(k) == []))
            continue
        S = settled(k)
        con = k in dis
        F = x["third_order"]
        if not S:
            out = "disagrees-unresolved"
        elif set(F) == set(S):
            out = "agrees"
        else:
            out = "disagrees-contested" if con else "disagrees-unanimous"
        line = dict(base, stratum=NAME[x["stratum"]], settled=S, settled_source=fin[k].get("source"),
                    contested=con, outcome=out, jaccard=r3(jac(F, S)) if S else None,
                    primary_match=prim(F, S) if S else None,
                    family_settled=fam.get(S[0]) if S else None)
        if out == "disagrees-contested":
            line["same_split"] = any(set(F) == set(v or []) for v in (c.get("r1"), c.get("r2"), c.get("b1")) if v)
        if fin[k].get("source") == "b1_grouping_kept":
            placed = list((fin[k].get("support_by_theme") or {}).keys())
            line["settled_placed"] = placed
            line["jaccard_placed"] = r3(jac(F, placed))
        rows[x["arm"]].append(line)

    figs = {"arms": {}, "R": {}, "inputs": {"assign_final": SETTLED_SHA}}
    for arm in (A1, A2):
        L = rows[arm]
        fa = {}
        groups = {"U": [r for r in L if r["stratum"] == "uniform"], "A": [r for r in L if r["stratum"] == "adjudicated"]}
        groups["U class 1"] = [r for r in groups["U"] if r["class"] == 1]
        groups["U class 2 (b1_grouping_kept)"] = [r for r in groups["U"] if r["class"] == 2]
        groups["U adjudicated (classes 3-5)"] = [r for r in groups["U"] if r["class"] >= 3]
        groups["A class 3"] = [r for r in groups["A"] if r["class"] == 3]
        groups["A class 4"] = [r for r in groups["A"] if r["class"] == 4]
        groups["A class 5"] = [r for r in groups["A"] if r["class"] == 5]
        for g, G in groups.items():
            res = [r for r in G if r["outcome"] != "disagrees-unresolved"]
            byitem = collections.defaultdict(list)
            for r in G:
                byitem[(r["sub"], r["theme_id"])].append(r)
            pairs = [(v[0]["third_order"], v[1]["third_order"]) for v in byitem.values() if len(v) == 2]
            fleet = [(b3[k]["r1"] or [], b3[k]["r2"] or []) for k in byitem]
            d = {"readings": len(G), "items": len(byitem), "resolved_readings": len(res),
                 "unresolved_excluded": len(G) - len(res),
                 "fresh_vs_settled": {"jaccard": r3(mean(r["jaccard"] for r in res)),
                                      "exact": r3(mean(r["outcome"] == "agrees" for r in res)),
                                      "primary": r3(mean(r["primary_match"] for r in res))},
                 "outcomes": dict(collections.Counter(r["outcome"] for r in G)),
                 "readers_agreement": agreement(pairs), "b3_readers_same_items": agreement(fleet)}
            con = [r for r in res if r["contested"]]
            una = [r for r in res if not r["contested"]]
            d["disagree_rate"] = {"contested": r3(mean(r["outcome"] != "agrees" for r in con)), "contested_n": len(con),
                                  "unanimous": r3(mean(r["outcome"] != "agrees" for r in una)), "unanimous_n": len(una)}
            dc = [r for r in G if r["outcome"] == "disagrees-contested"]
            d["same_split_again"] = {"n": len(dc), "share": r3(mean(r["same_split"] for r in dc))}
            c2 = [r for r in res if "jaccard_placed" in r]
            if c2:
                d["class2_against_placed"] = {"readings": len(c2), "jaccard": r3(mean(r["jaccard_placed"] for r in c2)),
                                              "exact": r3(mean(r["jaccard_placed"] == 1 for r in c2))}
            fa[g] = d
        # per family
        pf = {}
        for s in ("U", "A"):
            G = groups[s]
            byf = collections.defaultdict(list)
            for r in G:
                if r["family_settled"]:
                    byf[r["family_settled"]].append(r)
            byitem = collections.defaultdict(list)
            for r in G:
                byitem[(r["sub"], r["theme_id"])].append(r)
            ag = collections.defaultdict(list)
            for k, v in byitem.items():
                if len(v) == 2:
                    for f in {fam.get(v[0]["third_order"][0]) if v[0]["third_order"] else None,
                              fam.get(v[1]["third_order"][0]) if v[1]["third_order"] else None} - {None}:
                        ag[f].append((v[0]["third_order"], v[1]["third_order"]))
            tab = {}
            for f in sorted(set(byf) | set(ag)):
                R_ = byf.get(f, [])
                tab[f] = {"items_settled": len({(r["sub"], r["theme_id"]) for r in R_}), "readings": len(R_),
                          "fresh_vs_settled": r3(mean(r["jaccard"] for r in R_)),
                          "exact": r3(mean(r["outcome"] == "agrees" for r in R_)),
                          "readers_items": len(ag.get(f, [])), "readers_jaccard": r3(mean(jac(x, y) for x, y in ag.get(f, []))),
                          "b3_corpus_jaccard": r3(b3rec.get(f, {}).get("jaccard"))}
            ranked = sorted((v["fresh_vs_settled"], f) for f, v in tab.items() if v["items_settled"] >= 10)
            pf[s] = {"table": tab, "worst": [f for _, f in ranked[:3]], "ranked": [[f, v] for v, f in ranked]}
        fa["families"] = pf
        un = collections.defaultdict(list)
        for r in L:
            if r["outcome"] == "disagrees-unanimous":
                un[r["item"]].append(r["third_order"])
        fa["unanimous_disagreed_items"] = dict(sorted(un.items()))
        figs["arms"][arm] = fa
    # R
    for arm in (A1, A2):
        G = [r for r in rrows if r["arm"] == arm]
        byitem = collections.defaultdict(list)
        for r in G:
            byitem[(r["sub"], r["theme_id"])].append(r)
        pairs = [(v[0]["third_order"], v[1]["third_order"]) for v in byitem.values() if len(v) == 2]
        d = {"readings": len(G), "items": len(byitem), "readers_agreement": agreement(pairs),
             "primaries_meet": sum(prim(x, y) for x, y in pairs),
             "among_earlier": dict(collections.Counter(r["among"] for r in G)),
             "b3_readers_same_items": agreement([(b3[k]["r1"] or [], b3[k]["r2"] or []) for k in byitem])}
        for cl in (3, 4, 5):
            P = [(v[0]["third_order"], v[1]["third_order"]) for k, v in byitem.items() if len(v) == 2 and b3[k]["class"] == cl]
            d["class %d" % cl] = dict(agreement(P), primaries_meet=sum(prim(x, y) for x, y in P),
                                      among_earlier=dict(collections.Counter(r["among"] for r in G if r["class"] == cl)))
        # the 18 read twice
        ua = {}
        for r in rows[arm]:
            ua.setdefault((r["sub"], r["theme_id"]), []).append(r["third_order"])
        tw = [k for k in byitem if sr[k].get("also_in")]
        rp = [(byitem[k][0]["third_order"], byitem[k][1]["third_order"]) for k in tw if len(byitem[k]) == 2]
        up = [(ua[k][0], ua[k][1]) for k in tw if len(ua.get(k, [])) == 2]
        cross = [jac(x["third_order"], y) for k in tw for x in byitem[k] for y in ua.get(k, [])]
        d["read_twice_18"] = {"items": len(tw), "R_context": agreement(rp), "U_or_A_context": agreement(up),
                              "cross_context_jaccard": r3(mean(cross)), "cross_pairs": len(cross)}
        figs["R"][arm] = d
    p2 = jl(os.path.join(AN, "b4c_pass2.jsonl"))
    figs["pass2_changed"] = {arm: {"lines": sum(1 for x in p2 if x["arm"] == arm),
                                   "changed": sum(1 for x in p2 if x["arm"] == arm and x.get("changed") is True)}
                             for arm in (A1, A2)}
    # print
    for arm in (A1, A2):
        print("== %s" % arm)
        for g, d in figs["arms"][arm].items():
            if g in ("families", "unanimous_disagreed_items"):
                continue
            print("  %-30s readings %4d items %3d excl %2d | fresh-settled J %s exact %s prim %s | readers J %s exact %s prim %s alpha %s | B3 J %s alpha %s"
                  % (g, d["readings"], d["items"], d["unresolved_excluded"], d["fresh_vs_settled"]["jaccard"],
                     d["fresh_vs_settled"]["exact"], d["fresh_vs_settled"]["primary"],
                     d["readers_agreement"].get("jaccard"), d["readers_agreement"].get("exact"),
                     d["readers_agreement"].get("primary"), d["readers_agreement"].get("alpha"),
                     d["b3_readers_same_items"].get("jaccard"), d["b3_readers_same_items"].get("alpha")))
            print("  %-30s outcomes %s; disagree rate %s; same split %s; %s" % ("", d["outcomes"], d["disagree_rate"],
                  d["same_split_again"], d.get("class2_against_placed", "")))
        for s in ("U", "A"):
            print("  families %s worst %s" % (s, figs["arms"][arm]["families"][s]["worst"]))
            print("    ranked %s" % figs["arms"][arm]["families"][s]["ranked"])
        print("  unanimous items disagreed: %d" % len(figs["arms"][arm]["unanimous_disagreed_items"]))
    for arm in (A1, A2):
        print("== R %s: %s" % (arm, json.dumps(figs["R"][arm])))
    print("pass 2 changed %s" % figs["pass2_changed"])
    both = sorted(set(figs["arms"][A1]["unanimous_disagreed_items"]) | set(figs["arms"][A2]["unanimous_disagreed_items"]))
    print("unanimous items disagreed in either arm: %d" % len(both))
    if not a.write:
        return
    for name, L in (("reassign.jsonl", rows[A1]), ("reassign-openai-astra.jsonl", rows[A2]), ("readings-R-B4.jsonl", rrows)):
        p = os.path.join(OUT, name)
        if os.path.exists(p):
            sys.exit("%s exists" % p)
        with open(p, "w", encoding="utf-8") as fh:
            for r in L:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    figs["unanimous_either_arm"] = both
    json.dump(figs, open(os.path.join(AN, "b4c_figures.json"), "w", encoding="utf-8"), indent=1)
    print("wrote reassign.jsonl (%d), reassign-openai-astra.jsonl (%d), readings-R-B4.jsonl (%d), b4c_figures.json"
          % (len(rows[A1]), len(rows[A2]), len(rrows)))


if __name__ == "__main__":
    main()
