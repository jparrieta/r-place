#!/usr/bin/env python3
"""B3b: stage B3 section 3 on the assembled returns, by the declarations in notes-B3.md ("Declarations for the
check, made before any figure is fitted").

    python3 out/_analysis/b3_check.py --from <out dir holding the assembly> --tag <name> [--write-defects]

Reads the assembly (assign_raw, assign_pass2, multiplacement_log, predicted_confusion-B3, b3_classes) from
--from, and everything else from the real out/. Writes out/_analysis/b3_check_<tag>.json (every figure),
out/_analysis/b3_why_not_one_sample_<tag>.tsv (the justifications to read) and
out/_analysis/b3_scheme_undecided_<tag>.tsv (reader texts saying the scheme did not decide). With
--write-defects, appends stage B3's lines to out/defects.jsonl (refuses if it already holds stage B3 lines).
"""
import argparse, collections, importlib.util, itertools, json, math, os, random, re, statistics, warnings

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
spec = importlib.util.spec_from_file_location("b2s", os.path.join(AN, "b2_score.py"))
b2s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b2s)
jac, jl = b2s.jac, b2s.jl
SEED, FLOOR, TOL, STEPS = 20261015, 1 - 0.807, 0.10, 14
UNDECIDED = re.compile(r"no (third-order )?theme (fits|covers|captures)|scheme (does not|doesn't|cannot|can't|has no|lacks)|"
                       r"none of the (themes|gates|families)|neither gate|no gate (fits|is met)|not decide|undecid|"
                       r"no family (fits|covers)|missing (a )?theme", re.I)


def mean(x):
    x = list(x)
    return sum(x) / len(x) if x else float("nan")


def alpha_fast(units):
    """b2_score.alpha, computed over distinct sets with counts (the pooled pairs are too many to walk)."""
    units = [u for u in units if len(u) >= 2]
    n = sum(len(u) for u in units)
    do = sum(sum(1 - jac(a, b) for i, a in enumerate(u) for j, b in enumerate(u) if i != j) / (len(u) - 1) for u in units) / n
    cnt = collections.Counter(frozenset(v) for u in units for v in u)
    keys = list(cnt)
    de = 0.0
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            de += 2 * cnt[a] * cnt[b] * (1 - jac(sorted(a), sorted(b)))
    de /= n * (n - 1)
    return 1 - do / de


def ols_fe(y, x, g):
    """slope of y on x with group fixed effects (within transform), SE clustered by group."""
    y, x, g = np.asarray(y, float), np.asarray(x, float), np.asarray(g)
    yd, xd = y.copy(), x.copy()
    for k in np.unique(g):
        m = g == k
        yd[m] -= y[m].mean(); xd[m] -= x[m].mean()
    sxx = (xd * xd).sum()
    b = (xd * yd).sum() / sxx
    e = yd - b * xd
    meat = sum(((xd[g == k] * e[g == k]).sum()) ** 2 for k in np.unique(g))
    G = len(np.unique(g))
    se = math.sqrt(meat / sxx ** 2 * G / (G - 1))
    return b, se


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="src", required=True); ap.add_argument("--tag", required=True)
    ap.add_argument("--write-defects", action="store_true")
    a = ap.parse_args()
    src = a.src
    raw = jl(os.path.join(src, "assign_raw.jsonl"))
    p2 = jl(os.path.join(src, "assign_pass2.jsonl"))
    ml = jl(os.path.join(src, "multiplacement_log.jsonl"))
    pred = jl(os.path.join(src, "predicted_confusion-B3.jsonl"))
    classes = {"%s/%s" % (c["sub"], c["theme_id"]): c for c in jl(os.path.join(src, "b3_classes.jsonl"))}
    batches = {b["batch"]: b for b in jl(os.path.join(src, "batches-B3.jsonl"))}
    fam = {r["id"]: r["family"] for r in jl(os.path.join(OUT, "scheme_final.jsonl"))}
    gold = {r["item"]: r["third_order"] for r in jl(os.path.join(OUT, "gold_items.jsonl"))}
    order = json.load(open(os.path.join(AN, "b3_dispatch_order.json"), encoding="utf-8"))
    g1 = set(order["groups"]["1"])
    R = {}

    def key(x):
        return "%s/%s" % (x["sub"], x["theme_id"])

    def S(x):
        return [t for t in (x.get("third_order") or []) if isinstance(t, str)]

    corpus = [x for x in raw if x["copy_kind"] == "corpus"]
    # ---------------------------------------------------------------- 3.1 screen
    mlk = collections.defaultdict(list)
    for r in ml:
        mlk[(r["batch"], r["position"])].append(r)
    defects, reduce_ = [], []
    readv = collections.Counter(x.get("read") for x in raw)
    for x in raw:
        s = S(x)
        where = {"batch": x["batch"], "agent": x["agent"], "replicate": x["replicate"], "position": x["position"],
                 "item": key(x), "copy_kind": x["copy_kind"], "third_order": s}
        if x.get("read") == "label-only":
            defects.append(dict(where, kind="read label-only")); reduce_.append(where)
        if x.get("read") is None or x.get("families_opened") is None:
            defects.append(dict(where, kind="read or families_opened missing"))
        if len(s) > 1:
            recs = mlk.get((x["batch"], x["position"]), [])
            adds = {r.get("additional") for r in recs}
            if not set(s[1:]) <= adds:
                defects.append(dict(where, kind="multi placement without its multiplacement record",
                                    missing=sorted(set(s[1:]) - adds))); reduce_.append(where)
            elif any(not str(r.get("why_not_one") or "").strip() for r in recs if r.get("additional") in s[1:]):
                defects.append(dict(where, kind="multiplacement record with an empty why_not_one")); reduce_.append(where)
            if any(r.get("dispensable") in (None, "") for r in recs if r.get("additional") in s[1:]):
                defects.append(dict(where, kind="multiplacement record with dispensable null"))
        if len(s) > 3:
            defects.append(dict(where, kind="more than three themes on a line")); reduce_.append(where)
        if not s:
            defects.append(dict(where, kind="empty placement"))
        apx = x.get("also_present") or {}
        if isinstance(apx, dict) and (len(apx) > 20 or any(len(v or []) < 3 for v in apx.values())):
            defects.append(dict(where, kind="also_present over twenty themes or under three concepts"))
    undecided = []
    for x in raw:
        for t, v in (x.get("why") or {}).items() if isinstance(x.get("why"), dict) else []:
            if UNDECIDED.search(str(v)):
                undecided.append((x["batch"], x["position"], key(x), "why " + t, str(v)))
    for x in p2:
        if UNDECIDED.search(str(x.get("why_changed") or "")):
            undecided.append((x["batch"], x["position"], key(x), "why_changed", str(x["why_changed"])))
    for r in ml:
        for f in ("why_not_one", "why_this_one"):
            if UNDECIDED.search(str(r.get(f) or "")):
                undecided.append((r["batch"], r["position"], r["key"], f, str(r[f])))
    pos_ok = sum(sorted(x["position"] for x in raw + [] if x["batch"] == b) == list(range(1, batches[b]["n_items"] + 1))
                 for b in {x["batch"] for x in raw}) if False else None
    byb = collections.defaultdict(list)
    for x in raw:
        byb[x["batch"]].append(x["position"])
    perm_bad = sorted(b for b, ps in byb.items() if sorted(ps) != list(range(1, batches[b]["n_items"] + 1)))
    R["screen"] = {"lines": len(raw), "corpus": len(corpus), "read_values": dict(readv),
                   "defects_by_kind": dict(collections.Counter(d["kind"] for d in defects)),
                   "reduced_to_primary": len(reduce_), "undecided_texts": len(undecided),
                   "batches_positions_not_permutation": perm_bad}
    # connectivity, from the batches that returned
    adj = collections.defaultdict(set)
    for b in {x["batch"] for x in corpus}:
        for it in {key(x) for x in corpus if False}:
            pass
    rooms_of = collections.defaultdict(set)
    for x in corpus:
        rooms_of[x["batch"]].add(x["sub"])
    parent = {}

    def find(u):
        while parent.setdefault(u, u) != u:
            parent[u] = parent[parent[u]]; u = parent[u]
        return u
    for b, rs in rooms_of.items():
        for r in rs:
            parent[find("b:" + b)] = find("r:" + r)
    R["connectivity_components"] = len({find(u) for u in list(parent)})
    # ---------------------------------------------------------------- 3.2 gold
    b2 = {}
    for i, ln in enumerate(open(os.path.join(AN, "b2_gold_items.tsv"), encoding="utf-8")):
        c = ln.rstrip("\n").split("\t")
        if i:
            b2[c[0]] = {"rech": c[2].split(","), "nine": [s.split(",") for col in c[3:6] for s in col.split(" | ")]}
    gl = []
    for x in raw:
        if x["copy_kind"] != "gold":
            continue
        it, s = key(x), S(x)
        gl.append({"batch": x["batch"], "agent": x["agent"], "reader": x.get("reader"), "replicate": x["replicate"],
                   "group": 1 if x["batch"] in g1 else 2, "position": x["position"], "n": batches[x["batch"]]["n_items"],
                   "item": it, "mine": gold[it], "set": s, "fid": jac(s, gold[it]) if s else 0.0,
                   "fid_r": jac(s, b2[it]["rech"]) if s else 0.0, "exact": set(s) == set(gold[it]),
                   "prim": bool(s) and s[0] == gold[it][0], "missed": sorted(set(gold[it]) - set(s)),
                   "extra": sorted(set(s) - set(gold[it])),
                   "b2_fid": mean(jac(y, gold[it]) for y in b2[it]["nine"]),
                   "b2_prim": mean(y[0] == gold[it][0] for y in b2[it]["nine"])})
    gcorp = [x for x in corpus if key(x) in gold]

    def gfig(cs):
        return {"copies": len(cs), "fidelity": mean(c["fid"] for c in cs), "rechecked": mean(c["fid_r"] for c in cs),
                "primary": mean(c["prim"] for c in cs), "exact": mean(c["exact"] for c in cs),
                "b2_same": mean(c["b2_fid"] for c in cs), "b2_primary_same": mean(c["b2_prim"] for c in cs)}
    R["gold"] = {"all": gfig(gl), "group1": gfig([c for c in gl if c["group"] == 1]),
                 "group2": gfig([c for c in gl if c["group"] == 2]),
                 "corpus_readings_of_gold_items": {"lines": len(gcorp),
                                                    "fidelity": mean(jac(S(x), gold[key(x)]) if S(x) else 0 for x in gcorp),
                                                    "primary": mean(bool(S(x)) and S(x)[0] == gold[key(x)][0] for x in gcorp)},
                 "missed": dict(collections.Counter(t for c in gl for t in c["missed"]).most_common()),
                 "extra": dict(collections.Counter(t for c in gl for t in c["extra"]).most_common())}
    byi = collections.defaultdict(list)
    for c in gl:
        byi[c["item"]].append(c)
    R["gold"]["items"] = {it: dict(gfig(cs), fall=mean(c["b2_fid"] for c in cs) - mean(c["fid"] for c in cs))
                          for it, cs in sorted(byi.items())}
    R["gold"]["copies"] = gl
    rng = random.Random(SEED)
    bk = sorted({c["batch"] for c in gl})
    gb = collections.defaultdict(list)
    for c in gl:
        gb[c["batch"]].append(c)
    boot = []
    for _ in range(4000):
        cs = [c for k in (rng.choice(bk) for _ in bk) for c in gb[k]]
        boot.append(mean(c["b2_fid"] for c in cs) - mean(c["fid"] for c in cs))
    boot.sort()
    R["gold"]["fall"] = R["gold"]["all"]["b2_same"] - R["gold"]["all"]["fidelity"]
    R["gold"]["fall_ci"] = [boot[int(.025 * len(boot))], boot[int(.975 * len(boot)) - 1]]
    # ---------------------------------------------------------------- agreement (3.5)
    both = {it: c for it, c in classes.items() if c.get("r1") is not None and c.get("r2") is not None
            and not c["flags"].get("missing_replicate")}
    jj = {it: jac(c["r1"], c["r2"]) if (c["r1"] or c["r2"]) else 1.0 for it, c in both.items()}
    R["agreement"] = {"items_both": len(both), "jaccard": mean(jj.values()),
                      "exact": mean(set(c["r1"]) == set(c["r2"]) for c in both.values()),
                      "exact_list": mean(c["r1"] == c["r2"] for c in both.values()),
                      "primary": mean(bool(c["r1"]) and bool(c["r2"]) and c["r1"][0] == c["r2"][0] for c in both.values()),
                      "alpha": alpha_fast([[c["r1"], c["r2"]] for c in both.values()])}
    perfam = collections.defaultdict(list)
    for it, c in both.items():
        for g in {fam.get(c["r1"][0]) if c["r1"] else None, fam.get(c["r2"][0]) if c["r2"] else None} - {None}:
            perfam[g].append(it)
    R["agreement"]["families"] = {g: {"n": len(v), "jaccard": mean(jj[i] for i in v),
                                      "exact": mean(set(both[i]["r1"]) == set(both[i]["r2"]) for i in v),
                                      "primary": mean(bool(both[i]["r1"]) and bool(both[i]["r2"]) and both[i]["r1"][0] == both[i]["r2"][0] for i in v)}
                                  for g, v in sorted(perfam.items())}
    themes = sorted(fam)
    N = len(both)
    pt = {}
    for t in themes:
        a11 = a10 = a01 = 0
        for c in both.values():
            x, y = t in c["r1"], t in c["r2"]
            a11 += x and y; a10 += x and not y; a01 += y and not x
        a00 = N - a11 - a10 - a01
        either = a11 + a10 + a01
        po = (a11 + a00) / N
        pe = ((a11 + a10) * (a11 + a01) + (a00 + a01) * (a00 + a10)) / N ** 2
        pt[t] = {"either": either, "both": a11, "positive": a11 / either if either else None,
                 "kappa": (po - pe) / (1 - pe) if pe < 1 else None,
                 "jaccard_items": mean(jj[i] for i, c in both.items() if t in c["r1"] or t in c["r2"])}
    R["agreement"]["themes"] = pt
    # per-theme by primary: items where either primary is t
    # duplicates: within-reader
    dup = []
    byk = collections.defaultdict(dict)
    for x in raw:
        if x["copy_kind"] in ("corpus", "duplicate"):
            byk[(x["batch"], key(x))][x["copy_kind"]] = x
    for (b, it), d in byk.items():
        if "duplicate" in d and "corpus" in d:
            dup.append({"batch": b, "item": it, "jaccard": jac(S(d["corpus"]), S(d["duplicate"])) if S(d["corpus"]) or S(d["duplicate"]) else 1.0,
                        "exact": set(S(d["corpus"])) == set(S(d["duplicate"])),
                        "primary": bool(S(d["corpus"])) and bool(S(d["duplicate"])) and S(d["corpus"])[0] == S(d["duplicate"])[0],
                        "gap": abs(d["corpus"]["position"] - d["duplicate"]["position"])})
    R["duplicates"] = {"n": len(dup), "jaccard": mean(d["jaccard"] for d in dup), "exact": mean(d["exact"] for d in dup),
                       "primary": mean(d["primary"] for d in dup), "disagree_rate": mean(not d["exact"] for d in dup)}
    # ---------------------------------------------------------------- inventory
    inv = {"alike": 0, "split": 0, "split_primary": 0, "split_additional_only": 0, "split_order_only": 0}
    invf, invt = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
    for it, c in both.items():
        r1, r2 = c["r1"], c["r2"]
        fams = {fam.get(t) for t in r1[:1] + r2[:1]} - {None}
        if set(r1) == set(r2) and r1[:1] == r2[:1]:
            inv["alike"] += 1; k = "alike"
        else:
            inv["split"] += 1
            if r1[:1] != r2[:1]:
                k = "split_primary" if set(r1) != set(r2) else "split_order_only"
            else:
                k = "split_additional_only"
            inv[k] += 1
        for g in fams:
            invf[g][k] += 1
        for t in set(r1) | set(r2):
            invt[t][k] += 1
    inv["multi_lines"] = sum(len(S(x)) > 1 for x in corpus)
    inv["bag_lines"] = sum(bool(x.get("bag")) for x in corpus)
    inv["classes"] = dict(collections.Counter(c["class"] for c in classes.values()))
    R["inventory"] = inv
    R["inventory_families"] = {g: dict(v) for g, v in sorted(invf.items())}
    R["inventory_themes"] = {t: dict(v) for t, v in sorted(invt.items())}
    # ---------------------------------------------------------------- position (3.3)
    other = {}
    for it, c in both.items():
        other[(it, 1)], other[(it, 2)] = c["r2"], c["r1"]
    rows = []
    for x in corpus:
        it = key(x)
        if it not in both:
            continue
        s, o = S(x), other[(it, x["replicate"])]
        n = batches[x["batch"]]["n_items"]
        rows.append({"b": x["batch"], "p": x["position"], "n": n, "rel": (x["position"] - 1) / (n - 1) if n > 1 else 0.0,
                     "agree": jac(s, o) if (s or o) else 1.0, "multi": float(len(s) > 1),
                     "arg": float(x.get("confidence") == "arguable")})
    pos = {}
    for k in ("agree", "multi", "arg"):
        b, se = ols_fe([r[k] for r in rows], [r["p"] for r in rows], [r["b"] for r in rows])
        dec = collections.defaultdict(list)
        for r in rows:
            dec[min(9, int(r["rel"] * 10))].append(r[k])
        pos[k] = {"slope": b, "se": se, "ci": [b - 1.96 * se, b + 1.96 * se], "change14": b * STEPS,
                  "change14_ci": [(b - 1.96 * se) * STEPS, (b + 1.96 * se) * STEPS],
                  "sensitivity14": 2.80 * se * STEPS, "deciles": {d: [len(v), mean(v)] for d, v in sorted(dec.items())}}
    R["position"] = pos
    # per-reader multi rate distribution
    mr = collections.defaultdict(list)
    for x in corpus:
        mr[x["batch"]].append(len(S(x)) > 1)
    mrs = sorted(mean(v) for v in mr.values())
    R["position"]["multi_rate_readers"] = {"readers": len(mrs), "q": [mrs[int(q * (len(mrs) - 1))] for q in (0, .1, .25, .5, .75, .9, 1)]}
    # pass 1 -> pass 2
    p1k = {(x["batch"], x["position"]): S(x) for x in raw}
    rev = [(x["batch"], set(S(x)) != set(p1k.get((x["batch"], x["position"]), [])) or S(x)[:1] != p1k.get((x["batch"], x["position"]), [])[:1],
            bool(x.get("changed"))) for x in p2 if x.get("copy_kind") == "corpus"]
    R["revision"] = {"pass2_corpus_lines": len(rev), "set_or_primary_changed": mean(r[1] for r in rev),
                     "flag_changed": mean(r[2] for r in rev),
                     "readers_revising_any": mean(any(r[1] for r in rev if r[0] == b) for b in {r[0] for r in rev})}
    # formation: first five vs last five, batches of 10+
    fa, fl = collections.defaultdict(list), collections.defaultdict(list)
    for r in rows:
        if r["n"] >= 10:
            if r["p"] <= 5:
                fa[r["b"]].append(r)
            elif r["p"] > r["n"] - 5:
                fl[r["b"]].append(r)
    bs = [b for b in fa if b in fl]
    R["formation"] = {"readers": len(bs),
                      "arguable_first5": mean(mean(r["arg"] for r in fa[b]) for b in bs),
                      "arguable_last5": mean(mean(r["arg"] for r in fl[b]) for b in bs),
                      "agree_first5": mean(mean(r["agree"] for r in fa[b]) for b in bs),
                      "agree_last5": mean(mean(r["agree"] for r in fl[b]) for b in bs),
                      "readers_agree_drop_over_tol": sum(mean(r["agree"] for r in fa[b]) - mean(r["agree"] for r in fl[b]) > TOL for b in bs),
                      "readers_agree_rise_over_tol": sum(mean(r["agree"] for r in fl[b]) - mean(r["agree"] for r in fa[b]) > TOL for b in bs)}
    # duplicates: how the second copy was answered
    dup_why = [d for d in byk.values() if "duplicate" in d and "corpus" in d]
    R["duplicates"]["why_identical"] = sum(d["corpus"].get("why") == d["duplicate"].get("why") for d in dup_why)
    R["duplicates"]["why_names_repeat"] = sum(bool(re.search(r"(?i)same (item|theme) as|duplicate|repeat|again|identical|as (at|in) position",
                                                             json.dumps(d["duplicate"].get("why")))) for d in dup_why)
    R["duplicates"]["gap_median"] = statistics.median(d["gap"] for d in dup)
    # ---------------------------------------------------------------- multiplacement register (3.4)
    mlc = [r for r in ml if r.get("copy_kind") == "corpus"]
    pairs = collections.Counter((r["primary"], r["additional"]) for r in mlc)
    prd = collections.defaultdict(set)
    for r in mlc:
        prd[(r["primary"], r["additional"])].add(r["agent"])
    prm = collections.defaultdict(set)
    for r in mlc:
        prm[(r["primary"], r["additional"])].add(r["sub"])
    predicted = collections.Counter(frozenset(p.get("predicted_confusion") or []) for p in pred
                                    if isinstance(p.get("predicted_confusion"), list) and len(p["predicted_confusion"]) == 2)
    top = [{"primary": a, "additional": b, "count": n, "readers": len(prd[(a, b)]), "rooms": len(prm[(a, b)]),
            "predicted_by": predicted.get(frozenset((a, b)), 0)} for (a, b), n in pairs.most_common(20)]
    asadd = collections.Counter(r["additional"] for r in mlc)
    asprim = collections.Counter(S(x)[0] for x in corpus if S(x))
    load = sorted(({"theme": t, "additional": asadd[t], "primary": asprim.get(t, 0),
                    "ratio": asadd[t] / max(1, asprim.get(t, 0))} for t in asadd if asadd[t] >= 10), key=lambda d: -d["ratio"])
    rate = mean(len(S(x)) > 1 for x in corpus)
    R["register"] = {"multi_rate": rate, "records": len(mlc), "pairs_distinct": len(pairs), "top20": top,
                     "empties": sum(not S(x) for x in corpus), "three_theme_lines": sum(len(S(x)) == 3 for x in corpus),
                     "exception_load": load[:25],
                     "predicted_top": [[sorted(k), v] for k, v in predicted.most_common(15)]}
    # funnel per reader
    fun = {}
    for name, f in (("multi", lambda x: len(S(x)) > 1), ("empty", lambda x: not S(x))):
        p = mean(f(x) for x in corpus)
        out_ = []
        for b, xs in collections.defaultdict(list, {}).items():
            pass
        grp = collections.defaultdict(list)
        for x in corpus:
            grp[x["batch"]].append(f(x))
        for b, v in grp.items():
            n = len(v); lim = 3 * math.sqrt(p * (1 - p) / n) if 0 < p < 1 else 0
            if abs(mean(v) - p) > lim and (p > 0):
                out_.append([b, n, mean(v)])
        fun[name] = {"fleet": p, "outside": sorted(out_)}
    grp = collections.defaultdict(list)
    for x in corpus:
        grp[x["batch"]].append(len(S(x)))
    mth = mean(len(S(x)) for x in corpus)
    sd = statistics.pstdev([len(S(x)) for x in corpus])
    fun["themes_per_line"] = {"fleet": mth, "outside": sorted([b, len(v), mean(v)] for b, v in grp.items()
                                                              if abs(mean(v) - mth) > 3 * sd / math.sqrt(len(v)))}
    R["funnel"] = fun
    # what the readers above the multi limits share: batch size, item bytes, arguable rate, elapsed, and the
    # multi rate of the other replicate on the same items (how far the items, not the reader, carry it)
    up = {o[0] for o in fun["multi"]["outside"] if o[2] > fun["multi"]["fleet"]}
    rep = {(key(x), x["replicate"]): len(S(x)) > 1 for x in corpus}

    def prof(bs):
        xs = [x for x in corpus if x["batch"] in bs]
        oth = [rep[(key(x), 3 - x["replicate"])] for x in xs if (key(x), 3 - x["replicate"]) in rep]
        return {"readers": len(bs), "items": mean(batches[b]["n_items"] for b in bs),
                "item_bytes": mean(batches[b].get("item_bytes", 0) for b in bs),
                "arguable": mean(x.get("confidence") == "arguable" for x in xs),
                "elapsed_s": mean(x.get("packet_elapsed_s") or 0 for x in xs),
                "multi": mean(len(S(x)) > 1 for x in xs), "multi_other_replicate_same_items": mean(oth)}
    R["funnel"]["multi_above_profile"] = prof(up)
    R["funnel"]["fleet_profile"] = prof({x["batch"] for x in corpus})
    # families_opened
    fo = [len(x.get("families_opened") or []) for x in corpus]
    unopened = sum(1 for x in corpus for t in S(x) if fam.get(t) not in (x.get("families_opened") or []))
    R["families_opened"] = {"median": statistics.median(fo), "mean": mean(fo), "dist": dict(sorted(collections.Counter(fo).items())),
                            "placements": sum(len(S(x)) for x in corpus), "into_unopened_family": unopened,
                            "zero_opened_lines": sum(f == 0 for f in fo)}
    # predicted confusions against what divided the readers, and against confusions.md
    cpairs = set()
    for m in re.finditer(r"^(\d+)\. \*\*(T3-\d{3}) [^/]*/ (T3-\d{3})", open(os.path.join(OUT, "confusions.md"), encoding="utf-8").read(), re.M):
        cpairs.add(frozenset((m.group(2), m.group(3))))
    split_pairs = collections.Counter()
    for c in both.values():
        if c["r1"][:1] != c["r2"][:1] and c["r1"] and c["r2"]:
            split_pairs[frozenset((c["r1"][0], c["r2"][0]))] += 1
    pb = {}
    for p in pred:
        pc = p.get("predicted_confusion")
        if not (isinstance(pc, list) and len(pc) == 2):
            continue
        b = p["batch"]
        hit = False
        for x in corpus:
            pass
        pb[b] = frozenset(pc)
    divided_in_batch = 0
    items_of = collections.defaultdict(set)
    for x in corpus:
        items_of[x["batch"]].add(key(x))
    for b, pc in pb.items():
        if any(it in both and both[it]["r1"][:1] != both[it]["r2"][:1] and {both[it]["r1"][0], both[it]["r2"][0]} == set(pc)
               for it in items_of[b] if both.get(it) and both[it]["r1"] and both[it]["r2"]):
            divided_in_batch += 1
    R["predictions"] = {"lines": len(pred), "valid_pairs": len(pb), "in_confusions_md": sum(pc in cpairs for pc in pb.values()),
                        "pair_split_readers_on_an_item_of_the_batch": divided_in_batch,
                        "top_observed_primary_splits": [[sorted(k), v, predicted.get(k, 0), k in cpairs] for k, v in split_pairs.most_common(15)]}
    # coverage
    R["coverage"] = {"items": len(classes), "both": len(both),
                     "missing": sorted(it for it, c in classes.items() if c["flags"].get("missing_replicate"))}
    # worst theme: lowest positive agreement among themes on 30+ items
    w = sorted((v["positive"], t) for t, v in pt.items() if v["either"] >= 30 and v["positive"] is not None)
    R["worst_themes"] = [[t, pt[t]["either"], pt[t]["positive"], pt[t]["kappa"]] for _, t in w[:10]]
    # variance components
    try:
        import pandas as pd
        import statsmodels.formula.api as smf
        df = pd.DataFrame([{"room": x["sub"], "reader": x["batch"], "multi": float(len(S(x)) > 1), "empty": float(not S(x)),
                            "nthemes": float(len(S(x))), "one": 1} for x in corpus])
        vc = {}
        for y in ("multi", "nthemes"):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                m = smf.mixedlm("%s ~ 1" % y, df, groups="one", re_formula="0",
                                vc_formula={"room": "0 + C(room)", "reader": "0 + C(reader)"}).fit(method="lbfgs")
            names = list(m.model.exog_vc.names)
            vc[y] = {n: float(v) for n, v in zip(names, m.vcomp)}
            vc[y]["residual"] = float(m.scale)
        R["variance_components"] = vc
    except Exception as e:
        R["variance_components"] = {"error": repr(e)[:300]}
    # justifications sample
    rng = random.Random(SEED)
    pool = [r for r in mlc if str(r.get("why_not_one") or "").strip()]
    rng.shuffle(pool)
    seen, sample = set(), []
    for r in pool:
        if r["agent"] in seen:
            continue
        seen.add(r["agent"]); sample.append(r)
        if len(sample) == 40:
            break
    with open(os.path.join(AN, "b3_why_not_one_sample_%s.tsv" % a.tag), "w", encoding="utf-8") as fh:
        fh.write("n\tbatch\tagent\titem\tprimary\tadditional\twhy_not_one\n")
        for i, r in enumerate(sample, 1):
            fh.write("\t".join([str(i), r["batch"], r["agent"], r["key"], r["primary"], r["additional"],
                                str(r["why_not_one"]).replace("\t", " ").replace("\n", " ")]) + "\n")
    with open(os.path.join(AN, "b3_scheme_undecided_%s.tsv" % a.tag), "w", encoding="utf-8") as fh:
        for u in undecided:
            fh.write("\t".join(str(v).replace("\t", " ").replace("\n", " ") for v in u) + "\n")
    # returns with no prediction line (QB3-004), and detected position trends (section 3.3: unresolved diagnostics)
    with_pred = {p["batch"] for p in pred}
    for b in sorted({x["batch"] for x in raw} - with_pred):
        defects.append({"batch": b, "agent": batches[b]["agent"], "kind": "return without a prediction line",
                        "note": "item lines whole and valid; QB3-004"})
    for k, v in pos.items():
        if isinstance(v, dict) and "slope" in v and (v["ci"][0] > 0 or v["ci"][1] < 0):
            defects.append({"kind": "position trend (unresolved diagnostic)", "outcome": k, "slope": v["slope"], "se": v["se"],
                            "change_over_14": v["change14"], "change_ci": v["change14_ci"], "tolerance": TOL,
                            "evidence_needed": "whether the rise follows harder items placed late (item difficulty by position "
                                               "within room spreads), context length (item bytes before the line), or prior "
                                               "answers in the batch (the share of earlier lines on the same family); the "
                                               "position-by-room interaction and a reshuffled re-read of a sample would separate them"})
    R["defects"] = defects
    R["reduced"] = reduce_
    json.dump(R, open(os.path.join(AN, "b3_check_%s.json" % a.tag), "w", encoding="utf-8"), indent=1, default=str)
    if a.write_defects:
        p = os.path.join(OUT, "defects.jsonl")       # the run's ledger (A1's lines stand): append, once
        if os.path.exists(p) and any(json.loads(x).get("stage") == "B3" for x in open(p, encoding="utf-8") if x.strip()):
            raise SystemExit("out/defects.jsonl already holds stage B3 lines")
        with open(p, "a", encoding="utf-8") as fh:
            for d in defects:
                fh.write(json.dumps(dict(d, stage="B3", leg="B3b"), ensure_ascii=False) + "\n")
    # summary
    s = R["screen"]
    print("screen: %d lines (%d corpus); read %s; defects %s; reduced to primary %d; undecided texts %d; positions not 1..n: %s"
          % (s["lines"], s["corpus"], s["read_values"], s["defects_by_kind"], s["reduced_to_primary"], s["undecided_texts"], perm_bad))
    print("connectivity components (rooms x batches, corpus lines): %d" % R["connectivity_components"])
    g = R["gold"]
    print("gold all %s" % {k: round(v, 3) for k, v in g["all"].items()})
    print("gold group 1 %s; group 2 %s" % ({k: round(v, 3) for k, v in g["group1"].items()}, {k: round(v, 3) for k, v in g["group2"].items()}))
    print("gold fall %.3f CI %s; corpus readings of gold items %s" % (g["fall"], [round(v, 3) for v in g["fall_ci"]], g["corpus_readings_of_gold_items"]))
    print("gold items with own fall > floor: %s" % [(it, v["copies"], round(v["fall"], 2)) for it, v in g["items"].items() if v["fall"] > FLOOR])
    print("agreement %s" % {k: (round(v, 3) if isinstance(v, float) else v) for k, v in R["agreement"].items() if k not in ("families", "themes")})
    print("duplicates %s" % {k: round(v, 3) for k, v in R["duplicates"].items()})
    print("inventory %s" % R["inventory"])
    for k, v in pos.items():
        if k == "multi_rate_readers":
            continue
        print("position %s: slope %.4f se %.4f change14 %.3f [%.3f, %.3f] sensitivity14 %.3f deciles %s" % (
            k, v["slope"], v["se"], v["change14"], v["change14_ci"][0], v["change14_ci"][1], v["sensitivity14"],
            [round(d[1], 3) for d in v["deciles"].values()]))
    print("multi rate per reader quantiles %s" % R["position"]["multi_rate_readers"])
    print("revision %s" % R["revision"])
    print("formation %s" % R["formation"])
    r = R["register"]
    print("register: rate %.3f records %d distinct pairs %d empties %d three-theme lines %d" % (r["multi_rate"], r["records"], r["pairs_distinct"], r["empties"], r["three_theme_lines"]))
    for t in r["top20"]:
        print("  pair %s" % t)
    print("exception load %s" % r["exception_load"][:12])
    print("predicted top %s" % r["predicted_top"][:10])
    print("funnel %s" % {k: (round(v["fleet"], 3), len(v["outside"])) for k, v in R["funnel"].items() if "outside" in v})
    print("families_opened %s" % {k: v for k, v in R["families_opened"].items()})
    print("predictions %s" % {k: v for k, v in R["predictions"].items() if k != "top_observed_primary_splits"})
    print("top observed primary splits %s" % R["predictions"]["top_observed_primary_splits"][:10])
    print("coverage both %d of %d; missing %d" % (R["coverage"]["both"], R["coverage"]["items"], len(R["coverage"]["missing"])))
    print("worst themes %s" % R["worst_themes"][:6])
    print("variance components %s" % R["variance_components"])
    print("families agreement %s" % {g: round(v["jaccard"], 3) for g, v in R["agreement"]["families"].items()})


if __name__ == "__main__":
    main()
