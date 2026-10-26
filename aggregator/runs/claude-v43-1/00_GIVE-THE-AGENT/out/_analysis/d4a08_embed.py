#!/usr/bin/env python3
"""The D4a-08c allocation's construction as a module (copied unchanged from d4a08c_room_forms.py and
d4a08d_room_tree.py): changes two thirds, codes one third, floor of 5. Exposes ALL, DEF, THIN, CORE, NCH, NCODES,
XD (defining rooms), XT (thin rooms, both blocks), KCORE (core rooms, code part), nch (change columns), CCOLS, KCOLS,
point(s) and the form centres of room-forms-D4a08c.jsonl. Read by the D5 room-form helpers (d5f_*.py)."""
import collections, json, math, os, sys
import numpy as np

W = 2 / 3
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
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
IDX = {s: i for i, s in enumerate(DEF)}
FORMS = {r["id"]: r for r in jl(os.path.join(OUT, "room-forms-D4a08c.jsonl"))}
FORM_OF = {s: f for f, r in FORMS.items() for s in r["members"]}
CENTRE = {f: XD[[IDX[s] for s in r["members"] if s in IDX]].mean(axis=0) for f, r in FORMS.items()}
