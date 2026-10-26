#!/usr/bin/env python3
"""D4a-08c: the D4a-08b weighting (changes two thirds, codes one third) cut at 4, 6 and 8, with the 21 rooms that
hold no selected change placed by their codes (J, 26 October 2026, 22:00 Berlin; the rule is in the diary, logged
before this ran). Prints one JSON object.

    python3 out/_analysis/d4a08c_room_forms.py > out/_analysis/d4a08c_forms.json
"""
import collections, json, math, os, sys
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster

W = 2 / 3
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
sys.argv = [sys.argv[0]]
sys.path.insert(0, AN)
import d4a07_features as F  # noqa: E402
import adaptation_ledger as al  # noqa: E402

LV = ("T3", "T4", "dim")
FLOOR = 5


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


def code_counts(rooms):
    rs = set(rooms)
    out = {s: {lv: collections.Counter() for lv in LV} for s in rooms}
    for r in CODES:
        s = r["sub"]
        if s not in rs:
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


CC, KC = change_counts(CH), code_counts(ALL)
CCOLS, KCOLS = columns({s: CC[s] for s in DEF}), columns({s: KC[s] for s in DEF})
MEAN = {lv: shares(mats(KC, ALL, KCOLS)[lv]).mean(axis=0) for lv in LV}
MCD, MKD = mats(CC, DEF, CCOLS), mats(KC, DEF, KCOLS)
ECD = np.hstack([np.sqrt(shares(MCD[lv])) / math.sqrt(6) for lv in LV])
SC = {"c": tv(ECD), **{lv: tv(shares(MKD[lv]) - MEAN[lv]) for lv in LV}}


def code_part(rooms):
    mk = mats(KC, rooms, KCOLS)
    return np.hstack([(shares(mk[lv]) - MEAN[lv]) / math.sqrt(3 * SC[lv]) for lv in LV]) * math.sqrt(1 - W)


def change_part(rooms):
    mc = mats(CC, rooms, CCOLS)
    return np.hstack([np.sqrt(shares(mc[lv])) / math.sqrt(6) for lv in LV]) / math.sqrt(SC["c"]) * math.sqrt(W)


XD = np.hstack([change_part(DEF), code_part(DEF)])
XT = np.hstack([change_part(THIN), code_part(THIN)])
KCORE = code_part(CORE)
nch = ECD.shape[1]
Z = linkage(XD, method="ward")
IDX = {s: i for i, s in enumerate(DEF)}

names4 = {r["id"]: r.get("name") for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
dimn = {r["id"]: r.get("label") for r in jl(os.path.join(OUT, "dimensions.jsonl"))}
third = {r["id"]: r.get("name") for r in jl(os.path.join(OUT, "scheme_final.jsonl"))}


def label(c):
    def one(x):
        return names4.get(x) or third.get(x) or dimn.get(x) or x
    return " > ".join(one(x) for x in c.split(">")) if ">" in c else one(c)


SCH, PCH = shares(MCD["T4"]), shares(MCD["T4"]).mean(axis=0)
SK4 = shares(MKD["T4"])
OPS = {s: collections.Counter(r["op"] for r in F.BY[s]) for s in CH}
attack = {s: sum(1 for r in F.BY[s] if r["lift"][1] == "T3-006" or r["lift"][2] == "T4-020") / NCH[s] for s in CH}
RAID = [s for s in DEF if attack[s] >= 0.25]
B = {b["id"]: b for b in jl(os.path.join(OUT, "branches.jsonl"))}
TAKE = B["F02"]["members"]
# the D4a-08b letters, from the eight-form cut of the same tree
lab8 = fcluster(Z, 8, criterion="maxclust")
order8 = [c for c, _ in collections.Counter(lab8).most_common()]
L8 = {c: "ABCDEFGH"[i] for i, c in enumerate(order8)}
WARD8 = {s: L8[lab8[IDX[s]]] for s in DEF}


def cut(k):
    lab = fcluster(Z, k, criterion="maxclust")
    order = [c for c, _ in collections.Counter(lab).most_common()]
    letter = {c: "ABCDEFGH"[i] for i, c in enumerate(order)}
    ward = {s: letter[lab[IDX[s]]] for s in DEF}
    forms = sorted(set(ward.values()))
    cent = {f: XD[[IDX[s] for s in DEF if ward[s] == f]].mean(axis=0) for f in forms}
    rooms = dict(ward)
    for i, s in enumerate(THIN):
        rooms[s] = min(forms, key=lambda f: float(np.linalg.norm(XT[i] - cent[f])))
    core_codes, core_full = {}, {}
    for i, s in enumerate(CORE):
        core_codes[s] = min(forms, key=lambda f: float(np.linalg.norm(KCORE[i] - cent[f][nch:])))
        full = np.concatenate([np.zeros(nch), KCORE[i]])
        core_full[s] = min(forms, key=lambda f: float(np.linalg.norm(full - cent[f])))
        rooms[s] = core_codes[s]
    info = {}
    for f in forms:
        idx = [IDX[s] for s in DEF if ward[s] == f]
        sh, pres = SCH[idx].mean(axis=0), (MCD["T4"][idx] > 0).mean(axis=0)
        sig = sorted([{"name": label(c), "ratio": round(float(sh[j] / PCH[j]), 2), "presence": round(float(pres[j]), 3)}
                      for j, c in enumerate(CCOLS["T4"]) if PCH[j] > 0 and sh[j] / PCH[j] >= 1.5 and pres[j] >= 1 / 3], key=lambda r: -r["presence"])
        ks = SK4[idx].mean(axis=0)
        kover = sorted(({"name": label(c), "share": round(float(ks[j]), 4), "mean": round(float(MEAN["T4"][j]), 4)}
                        for j, c in enumerate(KCOLS["T4"])), key=lambda r: -(r["share"] - r["mean"]))[:3]
        mem = [s for s, x in rooms.items() if x == f]
        ops = collections.Counter()
        for s in mem:
            ops.update(OPS.get(s, {}))
        nops = sum(ops.values()) or 1
        info[f] = {"of_the_eight": sorted({WARD8[s] for s in DEF if ward[s] == f}), "ward_n": len(idx), "n": len(mem),
                   "thin": sum(1 for s in mem if s in THIN), "core": sum(1 for s in mem if s in CORE), "sig": sig[:4],
                   "mixture": bool(sig) and all(r["presence"] < 0.5 for r in sig), "codes_over": kover,
                   "median_codes": float(np.median([NCODES[s] for s in mem])), "restrict_share": round(ops["restrict"] / nops, 3),
                   "raiding": sum(1 for s in RAID if rooms[s] == f), "takeover": sum(1 for s in TAKE if rooms.get(s) == f)}
    sizes = [v["n"] for v in info.values()]
    return {"k": k, "forms": info, "ratio": round(max(sizes) / min(sizes), 2), "rooms": rooms,
            "core_by_codes": core_codes, "core_by_full_distance": core_full}


H = Z[:, 2]
out = {"w_changes": round(W, 4), "gap": {k: round(float(H[-(k - 1)] - H[-k]), 4) for k in range(4, 9)},
       "n_defining": len(DEF), "n_thin": len(THIN), "n_core": len(CORE),
       "core_codes": {s: NCODES[s] for s in CORE}, "cuts": {str(k): cut(k) for k in (4, 5, 6, 7, 8)}}
print(json.dumps(out, ensure_ascii=False))
