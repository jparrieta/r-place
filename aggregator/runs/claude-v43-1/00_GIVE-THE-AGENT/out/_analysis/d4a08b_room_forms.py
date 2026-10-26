#!/usr/bin/env python3
"""D4a-08 (amended): room forms on two blocks, the D4a-07 change block (arrows and link ops as links; 0 is the
global model) and a code block of deviations: for each level, a room's share of its coded concepts on each node
minus the mean share over all 705 rooms (0 is the average room; J, 26 October 2026, 21:09 Berlin). Levels and
blocks count equally by total variance over the defining rooms. The rule is in the diary, logged before this ran.
No canvas field, no verdict. Prints one JSON object.

    python3 out/_analysis/d4a08b_room_forms.py > out/_analysis/d4a08b_forms.json
"""
import collections, json, math, os, sys
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist, squareform
from scipy.stats import kruskal
from sklearn.metrics import adjusted_rand_score, silhouette_samples

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
sys.path.insert(0, AN)
import d4a07_features as F  # noqa: E402
import adaptation_ledger as al  # noqa: E402

LV = ("T3", "T4", "dim")
FLOOR = 5
KS = list(range(4, 9))


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


ALL = sorted(al.effective_rooms(OUT), key=str.lower)
NCH = collections.Counter(r["sub"] for r in F.PLACED)
CH = sorted(NCH, key=str.lower)
CORE = sorted(set(ALL) - set(CH), key=str.lower)
DEF = [s for s in CH if NCH[s] >= FLOOR]
THIN = [s for s in CH if NCH[s] < FLOOR]


def change_counts(rooms):
    out = {}
    for s in rooms:
        c = {lv: collections.Counter() for lv in LV}
        for r in F.BY.get(s, []):
            for lv in LV:
                for col, w in F.features(r, lv):
                    c[lv][col] += w
        out[s] = c
    return out


T4OF3, DOF4 = F.T4OF3, F.DOF4
PLACE = {}
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    v = r.get("third_order") or []
    PLACE[(r["sub"], r["theme_id"])] = [v] if isinstance(v, str) else list(v)
CODES = jl(os.path.join(ROOT, "package", "store", "codes.jsonl"))
NCODES = collections.Counter(r["sub"] for r in CODES)
HALF = np.random.default_rng(7).integers(0, 2, len(CODES))


def code_counts(rooms, which=None):
    rs = set(rooms)
    out = {s: {lv: collections.Counter() for lv in LV} for s in rooms}
    for i, r in enumerate(CODES):
        s = r["sub"]
        if s not in rs or (which is not None and HALF[i] != which):
            continue
        t3 = PLACE.get((s, r.get("theme_id")), [])
        if not t3:
            continue
        w = 1.0 / len(t3)
        for x in t3:
            out[s]["T3"][x] += w
            t4 = T4OF3.get(x)
            if t4:
                out[s]["T4"][t4] += w
                d = DOF4.get(t4)
                if d:
                    out[s]["dim"][d] += w
    return out


def columns(counts_def):
    cols = {}
    for lv in LV:
        held = collections.defaultdict(int)
        for c in counts_def.values():
            for k, v in c[lv].items():
                if v > 0:
                    held[k] += 1
        cols[lv] = sorted(k for k, n in held.items() if n > 1)
    return cols


def mats(counts, rooms, cols):
    out = {}
    for lv in LV:
        ci = {k: j for j, k in enumerate(cols[lv])}
        m = np.zeros((len(rooms), len(cols[lv])))
        for a, s in enumerate(rooms):
            for k, v in counts[s][lv].items():
                if k in ci:
                    m[a, ci[k]] += v
        out[lv] = m
    return out


def shares(m):
    t = m.sum(axis=1, keepdims=True)
    return np.divide(m, t, out=np.zeros_like(m), where=t > 0)


def embed_change(M):
    return np.hstack([np.sqrt(shares(M[lv])) / math.sqrt(2 * len(LV)) for lv in LV])


def code_dev(M, mean):
    return {lv: shares(M[lv]) - mean[lv] for lv in LV}


def total_var(X):
    return float(((X - X.mean(axis=0)) ** 2).sum(axis=1).mean())


def scales(Mc_def, Mk_def, mean):
    dv = code_dev(Mk_def, mean)
    return {"change": total_var(embed_change(Mc_def)), **{lv: total_var(dv[lv]) for lv in LV}}


def combine(Mc, Mk, mean, sc):
    ec = embed_change(Mc) / math.sqrt(sc["change"])
    dv = code_dev(Mk, mean)
    kc = np.hstack([dv[lv] / math.sqrt(len(LV) * sc[lv]) for lv in LV])
    return np.hstack([ec, kc]) / math.sqrt(2), ec.shape[1]


CC = change_counts(CH)
KC = code_counts(ALL)
CCOLS = columns({s: CC[s] for s in DEF})
KCOLS = columns({s: KC[s] for s in DEF})
MKALL = mats(KC, ALL, KCOLS)
MEAN = {lv: shares(MKALL[lv]).mean(axis=0) for lv in LV}
MCD, MKD = mats(CC, DEF, CCOLS), mats(KC, DEF, KCOLS)
SCALE = scales(MCD, MKD, MEAN)
XD, nch = combine(MCD, MKD, MEAN, SCALE)
XT, _ = combine(mats(CC, THIN, CCOLS), mats(KC, THIN, KCOLS), MEAN, SCALE)
Z = linkage(XD, method="ward")
H = Z[:, 2]
gap = {k: {"begins": round(float(H[-k]), 4), "ends": round(float(H[-(k - 1)]), 4),
           "lifetime": round(float(H[-(k - 1)] - H[-k]), 4)} for k in KS}
k_gap = max(KS, key=lambda k: (gap[k]["lifetime"], -k))


def pair_aris(X, rg, npairs):
    n, m = len(X), int(round(0.8 * len(X)))
    res = {k: [] for k in KS}
    for _ in range(npairs):
        a = np.sort(rg.choice(n, m, replace=False))
        b = np.sort(rg.choice(n, m, replace=False))
        Za, Zb = linkage(X[a], method="ward"), linkage(X[b], method="ward")
        common = np.intersect1d(a, b)
        pa = {int(x): i for i, x in enumerate(a)}
        pb = {int(x): i for i, x in enumerate(b)}
        for k in KS:
            la, lb = fcluster(Za, k, criterion="maxclust"), fcluster(Zb, k, criterion="maxclust")
            res[k].append(adjusted_rand_score([la[pa[int(c)]] for c in common], [lb[pb[int(c)]] for c in common]))
    return res


def shuffled(M, rg):
    out = {}
    for lv in LV:
        m = M[lv].copy()
        for j in range(m.shape[1]):
            m[:, j] = rg.permutation(m[:, j])
        out[lv] = m
    return out


real = pair_aris(XD, np.random.default_rng(0), 100)
nrg = np.random.default_rng(1)
null = {k: [] for k in KS}
DVD = code_dev(MKD, MEAN)
for _ in range(20):
    # amended null: change counts shuffled as at D4a-07; code deviations permuted node by node
    mc = shuffled(MCD, nrg)
    dvs = {lv: DVD[lv][:, [0]] * 0 + np.column_stack([nrg.permutation(DVD[lv][:, j]) for j in range(DVD[lv].shape[1])]) for lv in LV}
    ec = embed_change(mc)
    ec = ec / math.sqrt(total_var(ec))
    kc = np.hstack([dvs[lv] / math.sqrt(len(LV) * total_var(dvs[lv])) for lv in LV])
    Xn = np.hstack([ec, kc]) / math.sqrt(2)
    if not null.get("sizes"):
        Zn = linkage(Xn, method="ward")
        null["sizes"] = {k: sorted(collections.Counter(fcluster(Zn, k, criterion="maxclust")).values(), reverse=True) for k in KS}
        Zr = linkage(XD, method="ward")
        null["real_sizes"] = {k: sorted(collections.Counter(fcluster(Zr, k, criterion="maxclust")).values(), reverse=True) for k in KS}
    r = pair_aris(Xn, nrg, 20)
    for k in KS:
        null[k].extend(r[k])
stab = {k: {"real_mean": round(float(np.mean(real[k])), 4), "null_mean": round(float(np.mean(null[k])), 4),
            "null_p95": round(float(np.percentile(null[k], 95)), 4),
            "margin": round(float(np.mean(real[k]) - np.mean(null[k])), 4)} for k in KS}
bm = max(stab[k]["margin"] for k in KS)
k_stab = min(k for k in KS if stab[k]["margin"] >= bm - 0.005)

names4 = {r["id"]: r.get("name") for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
dimn = {r["id"]: r.get("label") for r in jl(os.path.join(OUT, "dimensions.jsonl"))}
third = {r["id"]: r.get("name") for r in jl(os.path.join(OUT, "scheme_final.jsonl"))}


def label(c):
    def one(n):
        return names4.get(n) or third.get(n) or dimn.get(n) or n
    return " > ".join(one(x) for x in c.split(">")) if ">" in c else one(c)


SC = {lv: shares(MCD[lv]) for lv in LV}
SK = {lv: shares(MKD[lv]) for lv in LV}
PC = {lv: SC[lv].mean(axis=0) for lv in LV}
IDX = {s: i for i, s in enumerate(DEF)}
XALL = {s: XD[IDX[s]] for s in DEF}
XALL.update({s: XT[i] for i, s in enumerate(THIN)})
OPS = {s: collections.Counter(r["op"] for r in F.BY[s]) for s in CH}
T4W = {s: CC[s]["T4"] for s in CH}


def describe(labels):
    order = [c for c, _ in collections.Counter(labels).most_common()]
    letter = {c: "ABCDEFGH"[i] for i, c in enumerate(order)}
    ward = {s: letter[labels[IDX[s]]] for s in DEF}
    forms = sorted(set(ward.values()))
    cent = {f: XD[[IDX[s] for s in DEF if ward[s] == f]].mean(axis=0) for f in forms}
    info, sig = {}, {}
    for f in forms:
        idx = [IDX[s] for s in DEF if ward[s] == f]
        sh, pres = SC["T4"][idx].mean(axis=0), (MCD["T4"][idx] > 0).mean(axis=0)
        rows = [{"col": c, "name": label(c), "link": ">" in c, "share": round(float(sh[j]), 4),
                 "ratio": round(float(sh[j] / PC["T4"][j]), 2) if PC["T4"][j] > 0 else 0.0,
                 "presence": round(float(pres[j]), 3)} for j, c in enumerate(CCOLS["T4"])]
        s4 = sorted([r for r in rows if r["ratio"] >= 1.5 and r["presence"] >= 1 / 3], key=lambda r: -r["share"])
        ksh = SK["T4"][idx].mean(axis=0)
        krows = [{"col": c, "name": label(c), "share": round(float(ksh[j]), 4), "mean_share": round(float(MEAN["T4"][j]), 4),
                  "deviation": round(float(ksh[j] - MEAN["T4"][j]), 4)} for j, c in enumerate(KCOLS["T4"])]
        kover = sorted(krows, key=lambda r: -r["deviation"])[:4]
        kunder = sorted(krows, key=lambda r: r["deviation"])[:3]
        kd = SK["dim"][idx].mean(axis=0)
        kdims = sorted(({"col": c, "name": label(c), "share": round(float(kd[j]), 4), "mean_share": round(float(MEAN["dim"][j]), 4),
                         "deviation": round(float(kd[j] - MEAN["dim"][j]), 4)} for j, c in enumerate(KCOLS["dim"])), key=lambda r: -r["deviation"])[:3]
        sig[f] = {r["col"] for r in s4}
        info[f] = {"ward_n": len(idx), "sig_T4": s4, "code_over": kover, "code_under": kunder, "code_dims": kdims,
                   "mixture": bool(s4) and all(r["presence"] < 0.5 for r in s4), "no_signature": not s4}
    rooms = {}
    for s in CH:
        d = {f: float(np.linalg.norm(XALL[s] - cent[f])) for f in forms}
        form = ward[s] if s in ward else min(forms, key=lambda f: d[f])
        tot = sum(T4W[s].values())
        on = {f: sum(w for c, w in T4W[s].items() if c in sig[f]) for f in forms}
        rooms[s] = {"form": form, "defining": s in ward, "changes": NCH[s], "codes": NCODES[s],
                    "share_own": round(on[form] / tot, 3) if tot else 0.0,
                    "secondary": sorted(f for f in forms if f != form and tot and on[f] / tot >= 0.25),
                    "near_equal_centre": sorted(f for f in forms if f != form and d[f] <= 1.05 * d[form])}
    sizes = collections.Counter(r["form"] for r in rooms.values())
    opmix = {}
    for f in forms:
        c, n = collections.Counter(), 0
        for s, r in rooms.items():
            if r["form"] == f:
                c.update(OPS[s])
                n += NCH[s]
        opmix[f] = {k: round(c[k] / n, 3) for k in ("restrict", "add-step", "add-condition", "link")}
    core_place = {}
    if CORE:
        dv = code_dev(mats(KC, CORE, KCOLS), MEAN)
        kc = np.hstack([dv[lv] / math.sqrt(len(LV) * SCALE[lv]) for lv in LV]) / math.sqrt(2)
        for i, s in enumerate(CORE):
            core_place[s] = min(forms, key=lambda f: float(np.linalg.norm(kc[i] - cent[f][nch:])))
    return {"sizes": dict(sorted(sizes.items())), "ward_sizes": dict(sorted(collections.Counter(ward.values()).items())),
            "ratio": round(max(sizes.values()) / min(sizes.values()), 2), "forms": info, "rooms": rooms,
            "op_mix": opmix, "core_by_codes": core_place, "ward": ward}


cuts = {}
for k in sorted({k_stab, k_gap}):
    cuts[k] = describe(fcluster(Z, k, criterion="maxclust"))
K0 = k_gap  # amended at D4a-08 (diary): the shuffled null cannot choose the count for this distance; the gap carries it
C0 = cuts[K0]


# ---- the split-half check ----
def half_inputs(which):
    kc_def = code_counts(DEF, which)
    cols = columns(kc_def)
    kc_all = code_counts(ALL, which)
    mean = {lv: shares(mats(kc_all, ALL, cols)[lv]).mean(axis=0) for lv in LV}
    mk = mats(kc_def, DEF, cols)
    return mk, mean


mkA, meanA = half_inputs(0)
mkB, meanB = half_inputs(1)
XA, _ = combine(MCD, mkA, meanA, scales(MCD, mkA, meanA))
XB, _ = combine(MCD, mkB, meanB, scales(MCD, mkB, meanB))
la = fcluster(linkage(XA, method="ward"), K0, criterion="maxclust")
lb = fcluster(linkage(XB, method="ward"), K0, criterion="maxclust")
scB = scales(MCD, mkB, meanB)
dvB = code_dev(mkB, meanB)
MB = np.hstack([dvB[lv] / math.sqrt(len(LV) * scB[lv]) for lv in LV])


def pseudo_f(M, lab):
    g = M.mean(axis=0)
    sst = ((M - g) ** 2).sum()
    ssw = sum(((M[lab == c] - M[lab == c].mean(axis=0)) ** 2).sum() for c in set(lab))
    kk, n = len(set(lab)), len(lab)
    return ((sst - ssw) / (kk - 1)) / (ssw / (n - kk)), 1 - ssw / sst


def nearest_acc(M, lab):
    hit = 0
    for i in range(len(lab)):
        best, bd = None, None
        for c in set(lab):
            sel = lab == c
            sel[i] = False
            if not sel.any():
                continue
            dd = np.linalg.norm(M[i] - M[sel].mean(axis=0))
            if bd is None or dd < bd:
                best, bd = c, dd
        hit += best == lab[i]
    return hit / len(lab)


rg8 = np.random.default_rng(8)
Fa, R2a = pseudo_f(MB, la)
Fn = [pseudo_f(MB, rg8.permutation(la))[0] for _ in range(999)]
acc = nearest_acc(MB, la)
accn = [nearest_acc(MB, rg8.permutation(la)) for _ in range(20)]
prev7 = {}
for r in jl(os.path.join(OUT, "room-forms-D4a07.jsonl")):
    if r.get("level") == "form":
        for s in r["members"]:
            prev7[s] = r["id"]
main_lab = fcluster(Z, K0, criterion="maxclust")
d7 = [prev7[s] for s in DEF]
split = {"pseudo_F_halfB": round(float(Fa), 3), "r2_halfB": round(float(R2a), 4),
         "null_F_p95": round(float(np.percentile(Fn, 95)), 3), "perm_p": round((1 + sum(1 for x in Fn if x >= Fa)) / 1000, 4),
         "nearest_acc_halfB": round(acc, 3), "nearest_null_mean": round(float(np.mean(accn)), 3), "nearest_null_max": round(float(np.max(accn)), 3),
         "ari_halfA_halfB": round(adjusted_rand_score(la, lb), 3), "ari_halfA_main": round(adjusted_rand_score(la, main_lab), 3),
         "ari_halfA_D4a07": round(adjusted_rand_score(la, d7), 3), "ari_halfB_D4a07": round(adjusted_rand_score(lb, d7), 3),
         "ari_main_D4a07_defining": round(adjusted_rand_score(main_lab, d7), 3)}

# ---- named sets, agreement, sizes ----
attack = {s: sum(1 for r in F.BY[s] if r["lift"][1] == "T3-006" or r["lift"][2] == "T4-020") / NCH[s] for s in CH}
core_r = sorted((s for s in DEF if attack[s] >= 0.25), key=str.lower)
Dm = squareform(pdist(XD))


def group_sil(members):
    lab = np.array([1 if s in members else 0 for s in DEF])
    return float(silhouette_samples(Dm, lab, metric="precomputed")[lab == 1].mean())


rs = group_sil(set(core_r))
rg6 = np.random.default_rng(6)
ns = [group_sil(set(rg6.choice(DEF, len(core_r), replace=False))) for _ in range(999)]
raid = {"n": len(core_r), "core": core_r, "silhouette": round(rs, 4), "null_mean": round(float(np.mean(ns)), 4),
        "null_p95": round(float(np.percentile(ns, 95)), 4), "p": round((1 + sum(1 for x in ns if x >= rs)) / 1000, 4),
        "by_form": dict(collections.Counter(C0["rooms"][s]["form"] for s in core_r))}
B = {b["id"]: b for b in jl(os.path.join(OUT, "branches.jsonl"))}
takeover = sorted(B["F02"]["members"], key=str.lower)
ari7 = round(adjusted_rand_score([prev7[s] for s in CH], [C0["rooms"][s]["form"] for s in CH]), 3)
cross7 = collections.defaultdict(collections.Counter)
for s in CH:
    cross7[prev7[s]][C0["rooms"][s]["form"]] += 1
kw = kruskal(*[[NCODES[s] for s in CH if C0["rooms"][s]["form"] == f] for f in sorted(C0["sizes"])])
code_share_of_spread = None
for k, c in cuts.items():
    c["median_codes"] = {f: float(np.median([NCODES[s] for s in CH if c["rooms"][s]["form"] == f])) for f in sorted(c["sizes"])}
    c["median_changes"] = {f: float(np.median([NCH[s] for s in CH if c["rooms"][s]["form"] == f])) for f in sorted(c["sizes"])}
    c["takeover_by_form"] = dict(collections.Counter(c["rooms"][s]["form"] if s in c["rooms"] else "K" for s in takeover))
    for f in c["forms"]:
        if c["forms"][f]["mixture"] or c["forms"][f]["no_signature"]:
            mem = [s for s in DEF if c["ward"][s] == f]
            l2 = fcluster(linkage(XD[[IDX[s] for s in mem]], method="ward"), 2, criterion="maxclust")
            halves = []
            for h in (1, 2):
                idx = [IDX[s] for s, l in zip(mem, l2) if l == h]
                sh, pres = SC["T4"][idx].mean(axis=0), (MCD["T4"][idx] > 0).mean(axis=0)
                top = sorted(range(len(CCOLS["T4"])), key=lambda j: -((sh[j] / PC["T4"][j] if PC["T4"][j] > 0 else 0) * (pres[j] >= 1 / 3)))[:3]
                halves.append({"n": len(idx), "leading": [(label(CCOLS["T4"][j]), round(float(sh[j] / PC["T4"][j]), 2), round(float(pres[j]), 3)) for j in top]})
            c["forms"][f]["ward_split"] = halves
    # how much of each form's separation comes from each block: between-form share of each block's variance
    lab = np.array([sorted(c["sizes"]).index(c["ward"][s]) for s in DEF])
    blocks = {"changes": XD[:, :nch], "codes": XD[:, nch:]}
    c["between_share"] = {}
    for name, Xb in blocks.items():
        g = Xb.mean(axis=0)
        sst = ((Xb - g) ** 2).sum()
        ssw = sum(((Xb[lab == q] - Xb[lab == q].mean(axis=0)) ** 2).sum() for q in set(lab))
        c["between_share"][name] = round(float(1 - ssw / sst), 4)
    del c["ward"]

print(json.dumps({"floor": FLOOR, "n_defining": len(DEF), "n_thin": len(THIN), "n_core": len(CORE), "core": CORE,
                  "cols": {"changes": {lv: len(CCOLS[lv]) for lv in LV}, "codes": {lv: len(KCOLS[lv]) for lv in LV}},
                  "scale": {k: round(v, 6) for k, v in SCALE.items()},
                  "gap": gap, "k_gap": k_gap, "stability": stab, "k_stab": k_stab, "agree": k_gap == k_stab,
                  "null_cut_sizes": null.get("sizes"), "real_cut_sizes": null.get("real_sizes"),
                  "cuts": {str(k): v for k, v in cuts.items()}, "split_half": split, "raiding_core": raid,
                  "ari_vs_D4a07": ari7, "D4a07_to_D4a08": {k: dict(v) for k, v in sorted(cross7.items())},
                  "kruskal_codes": [round(float(kw.statistic), 2), float(kw.pvalue)], "takeover": takeover},
                 ensure_ascii=False))
