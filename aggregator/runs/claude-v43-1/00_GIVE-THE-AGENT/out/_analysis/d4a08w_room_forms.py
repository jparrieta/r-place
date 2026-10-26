#!/usr/bin/env python3
"""D4a-08, the reweighted variant: the D4a-08 blocks with the change block at a weight W of the total variance
(default two thirds) and the code block at 1 - W. The count by the merge-height gap (4 to 8); real matched-subsample
stability reported without a null; placement by the whole mix; the split-half check as at D4a-08. The rule is in
the diary, logged before this ran. Prints one JSON object.

    python3 out/_analysis/d4a08w_room_forms.py --w 0.6667 > out/_analysis/d4a08w_forms.json
"""
import argparse, collections, json, math, os, sys
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics import adjusted_rand_score, silhouette_samples

ap = argparse.ArgumentParser()
ap.add_argument("--w", type=float, default=2 / 3)
a = ap.parse_args()
W = a.w
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
sys.argv = [sys.argv[0]]
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
PLACE = {}
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    v = r.get("third_order") or []
    PLACE[(r["sub"], r["theme_id"])] = [v] if isinstance(v, str) else list(v)
CODES = jl(os.path.join(ROOT, "package", "store", "codes.jsonl"))
NCODES = collections.Counter(r["sub"] for r in CODES)
HALF = np.random.default_rng(7).integers(0, 2, len(CODES))


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


def code_counts(rooms, which=None):
    rs = set(rooms)
    out = {s: {lv: collections.Counter() for lv in LV} for s in rooms}
    for i, r in enumerate(CODES):
        s = r["sub"]
        if s not in rs or (which is not None and HALF[i] != which):
            continue
        t3 = PLACE.get((s, r.get("theme_id")), [])
        for x in t3:
            w = 1.0 / len(t3)
            out[s]["T3"][x] += w
            t4 = F.T4OF3.get(x)
            if t4:
                out[s]["T4"][t4] += w
                d = F.DOF4.get(t4)
                if d:
                    out[s]["dim"][d] += w
    return out


def columns(cd):
    cols = {}
    for lv in LV:
        held = collections.Counter()
        for c in cd.values():
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
        for i, s in enumerate(rooms):
            for k, v in counts[s][lv].items():
                if k in ci:
                    m[i, ci[k]] += v
        out[lv] = m
    return out


def shares(m):
    t = m.sum(axis=1, keepdims=True)
    return np.divide(m, t, out=np.zeros_like(m), where=t > 0)


def tv(X):
    return float(((X - X.mean(axis=0)) ** 2).sum(axis=1).mean())


def blocks(Mc, Mk, mean, ref=None):
    ec = np.hstack([np.sqrt(shares(Mc[lv])) / math.sqrt(6) for lv in LV])
    dv = {lv: shares(Mk[lv]) - mean[lv] for lv in LV}
    sc = ref or {"c": tv(ec), **{lv: tv(dv[lv]) for lv in LV}}
    kc = np.hstack([dv[lv] / math.sqrt(3 * sc[lv]) for lv in LV])
    return np.hstack([ec / math.sqrt(sc["c"]) * math.sqrt(W), kc * math.sqrt(1 - W)]), sc, ec.shape[1]


CC, KC = change_counts(CH), code_counts(ALL)
CCOLS, KCOLS = columns({s: CC[s] for s in DEF}), columns({s: KC[s] for s in DEF})
MEAN = {lv: shares(mats(KC, ALL, KCOLS)[lv]).mean(axis=0) for lv in LV}
MCD = mats(CC, DEF, CCOLS)
XD, SC, nch = blocks(MCD, mats(KC, DEF, KCOLS), MEAN)
XT, _, _ = blocks(mats(CC, THIN, CCOLS), mats(KC, THIN, KCOLS), MEAN, SC)
# both blocks at their own unit total variance, whatever W: used only to read each block's between-form share
_ec = np.hstack([np.sqrt(shares(MCD[lv])) / math.sqrt(6) for lv in LV]) / math.sqrt(SC["c"])
_mk = mats(KC, DEF, KCOLS)
_kc = np.hstack([(shares(_mk[lv]) - MEAN[lv]) / math.sqrt(3 * SC[lv]) for lv in LV])
RAW = np.hstack([_ec, _kc])
Z = linkage(XD, method="ward")
H = Z[:, 2]
gap = {k: round(float(H[-(k - 1)] - H[-k]), 4) for k in KS}
k_gap = max(KS, key=lambda k: (gap[k], -k))
rg = np.random.default_rng(0)
stab = {k: [] for k in KS}
n, m = len(XD), int(round(0.8 * len(XD)))
for _ in range(100):
    x1, x2 = np.sort(rg.choice(n, m, replace=False)), np.sort(rg.choice(n, m, replace=False))
    Z1, Z2 = linkage(XD[x1], method="ward"), linkage(XD[x2], method="ward")
    com = np.intersect1d(x1, x2)
    p1, p2 = {int(v): i for i, v in enumerate(x1)}, {int(v): i for i, v in enumerate(x2)}
    for k in KS:
        l1, l2 = fcluster(Z1, k, criterion="maxclust"), fcluster(Z2, k, criterion="maxclust")
        stab[k].append(adjusted_rand_score([l1[p1[int(c)]] for c in com], [l2[p2[int(c)]] for c in com]))
stab = {k: round(float(np.mean(v)), 4) for k, v in stab.items()}

names4 = {r["id"]: r.get("name") for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
dimn = {r["id"]: r.get("label") for r in jl(os.path.join(OUT, "dimensions.jsonl"))}
third = {r["id"]: r.get("name") for r in jl(os.path.join(OUT, "scheme_final.jsonl"))}


def label(c):
    def one(x):
        return names4.get(x) or third.get(x) or dimn.get(x) or x
    return " > ".join(one(x) for x in c.split(">")) if ">" in c else one(c)


IDX = {s: i for i, s in enumerate(DEF)}
SCH = shares(MCD["T4"])
PCH = SCH.mean(axis=0)
SK4 = shares(mats(KC, DEF, KCOLS)["T4"])
XALL = {s: XD[IDX[s]] for s in DEF}
XALL.update({s: XT[i] for i, s in enumerate(THIN)})
prev = {}
for f, key in (("room-forms-D4a07.jsonl", "D4a07"), ("room-forms-D4a08.jsonl", "D4a08")):
    for r in jl(os.path.join(OUT, f)):
        if r.get("level") == "form":
            for s in r["members"]:
                prev.setdefault(s, {})[key] = r["id"]
attack = {s: sum(1 for r in F.BY[s] if r["lift"][1] == "T3-006" or r["lift"][2] == "T4-020") / NCH[s] for s in CH}
raid = [s for s in DEF if attack[s] >= 0.25]
B = {b["id"]: b for b in jl(os.path.join(OUT, "branches.jsonl"))}


def describe(k):
    lab = fcluster(Z, k, criterion="maxclust")
    order = [c for c, _ in collections.Counter(lab).most_common()]
    letter = {c: "ABCDEFGH"[i] for i, c in enumerate(order)}
    ward = {s: letter[lab[IDX[s]]] for s in DEF}
    forms = sorted(set(ward.values()))
    cent = {f: XD[[IDX[s] for s in DEF if ward[s] == f]].mean(axis=0) for f in forms}
    rooms = {s: (ward[s] if s in ward else min(forms, key=lambda f: float(np.linalg.norm(XALL[s] - cent[f])))) for s in CH}
    info = {}
    for f in forms:
        idx = [IDX[s] for s in DEF if ward[s] == f]
        sh, pres = SCH[idx].mean(axis=0), (MCD["T4"][idx] > 0).mean(axis=0)
        sig = sorted([{"name": label(c), "ratio": round(float(sh[j] / PCH[j]), 2), "presence": round(float(pres[j]), 3), "share": round(float(sh[j]), 4)}
                      for j, c in enumerate(CCOLS["T4"]) if PCH[j] > 0 and sh[j] / PCH[j] >= 1.5 and pres[j] >= 1 / 3], key=lambda r: -r["share"])
        ks = SK4[idx].mean(axis=0)
        kover = sorted(({"name": label(c), "share": round(float(ks[j]), 4), "mean": round(float(MEAN["T4"][j]), 4)}
                        for j, c in enumerate(KCOLS["T4"])), key=lambda r: -(r["share"] - r["mean"]))[:3]
        info[f] = {"ward_n": len(idx), "placed": sum(1 for s in CH if rooms[s] == f), "sig": sig[:4], "codes_over": kover,
                   "median_codes": float(np.median([NCODES[s] for s in CH if rooms[s] == f])),
                   "median_changes": float(np.median([NCH[s] for s in CH if rooms[s] == f]))}
    labs = np.array([forms.index(ward[s]) for s in DEF])
    between = {}
    for name, Xb in (("changes", RAW[:, :nch]), ("codes", RAW[:, nch:])):
        sst = ((Xb - Xb.mean(axis=0)) ** 2).sum()
        ssw = sum(((Xb[labs == q] - Xb[labs == q].mean(axis=0)) ** 2).sum() for q in set(labs))
        between[name] = round(float(1 - ssw / sst), 4)
    cross = collections.defaultdict(collections.Counter)
    for s in CH:
        cross[prev[s]["D4a07"]][rooms[s]] += 1
    sizes = collections.Counter(rooms.values())
    return {"k": k, "forms": info, "between_share": between, "ratio": round(max(sizes.values()) / min(sizes.values()), 2),
            "ari_D4a07": round(adjusted_rand_score([prev[s]["D4a07"] for s in CH], [rooms[s] for s in CH]), 3),
            "ari_D4a08": round(adjusted_rand_score([prev[s]["D4a08"] for s in CH], [rooms[s] for s in CH]), 3),
            "cross_D4a07": {x: dict(v) for x, v in sorted(cross.items())},
            "raiding_by_form": dict(collections.Counter(rooms[s] for s in raid)),
            "takeover_by_form": dict(collections.Counter(rooms.get(s, "K") for s in B["F02"]["members"])),
            "rooms": rooms}


cuts = {str(k): describe(k) for k in KS}
print(json.dumps({"w_changes": round(W, 4), "gap": gap, "k_gap": k_gap, "stability_real": stab, "cuts": cuts}, ensure_ascii=False))
