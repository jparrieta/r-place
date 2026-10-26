#!/usr/bin/env python3
"""D5, room-form accounts (D5a-36 to D5a-41): the facts of one form of the six-form cut, by the rules logged at D5a-36.
Thin and core rooms weigh less: shares, signatures, themes, representatives and the split are read on the defining
rooms; thin and core members are listed apart. Prints one JSON object.

    python3 out/_analysis/d5f_facts.py --form A > out/_analysis/d5a36_facts.json
"""
import argparse, collections, json, os, re, statistics, sys
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
a = ap.parse_args()
sys.argv = [sys.argv[0]]
AN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402
import d4a07_features as F  # noqa: E402

ROOT, OUT = E.ROOT, E.OUT
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib  # noqa: E402
from adaptation_ledger import shared_lines  # noqa: E402

jl = E.jl
FORM = E.FORMS[a.form]
MEM = sorted(FORM["members"], key=str.lower)
n = len(MEM)
DEFS = [s for s in MEM if s in E.IDX]
THIN = [s for s in MEM if s in E.THIN]
CORE = [s for s in MEM if s in E.CORE]
ALLDEF = E.DEF
CHANGE = {"add-step", "add-condition", "link", "restrict", "contradict"}

# (3) element and arrow by element and arrow: defining members with a selected line of each op, against the 558
sel = collections.defaultdict(lambda: collections.defaultdict(set))
for l in shared_lines(OUT):
    if l.get("op") in CHANGE and len(l.get("lift") or []) >= 4:
        sel[l["element"]][l["op"]].add(l["sub"])
els = {r["id"]: r for r in jl(os.path.join(OUT, "model", "elements.jsonl"))}
arrows = {r["id"]: r for r in jl(os.path.join(OUT, "model", "arrows.jsonl"))}
dset, aset, tset, cset = set(DEFS), set(ALLDEF), set(THIN), set(CORE)
eltab = []
for e in sorted(sel):
    for op, rooms in sorted(sel[e].items()):
        f, p = len(rooms & dset), len(rooms & aset)
        eltab.append({"element": e, "op": op, "form_def": f, "form_share": round(f / len(DEFS), 3), "pop_def": p,
                      "pop_share": round(p / len(ALLDEF), 3), "ratio": round((f / len(DEFS)) / (p / len(ALLDEF)), 2) if p else None,
                      "thin": sorted(rooms & tset, key=str.lower)})

# (1) rule 6
rooms705 = {r["sub"] for r in jl(os.path.join(ROOT, "package", "store", "rooms.jsonl"))}
arx = []
for r in arrows.values():
    subs = set(r.get("subs") or []) & rooms705
    arx.append({"arrow": r["id"], "from": r.get("from"), "to": r.get("to"), "subs": len(subs),
                "expected": round(len(subs) / len(rooms705) * n, 3), "members_in_subs": sorted(subs & set(MEM), key=str.lower)})
expd = {x["arrow"]: x["expected"] for x in arx}
props = [{"id": p["id"], "rests_on": p.get("rests_on"), "max_expected": max(expd.get(x, 0) for x in p.get("rests_on") or [])}
         for p in jl(os.path.join(OUT, "propositions.jsonl"))]

# the change columns at the fourth-order level (nodes and links), as the allocation built them
cols = E.CCOLS["T4"]
S = E.shares(E.MCD["T4"])
P = E.MCD["T4"] > 0
fi = [E.IDX[s] for s in DEFS]
pop_sh, form_sh, form_pr, pop_pr = S.mean(axis=0), S[fi].mean(axis=0), P[fi].mean(axis=0), P.mean(axis=0)
names4 = {r["id"]: r.get("name") for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}


def lab(c):
    return " > ".join(names4.get(x) or els.get(x, {}).get("id") or x for x in c.split(">"))


sig = sorted([{"col": c, "name": lab(c), "ratio": round(float(form_sh[j] / pop_sh[j]), 2), "presence": round(float(form_pr[j]), 3),
               "pop_presence": round(float(pop_pr[j]), 3), "form_share": round(float(form_sh[j]), 4)}
              for j, c in enumerate(cols) if pop_sh[j] > 0 and form_sh[j] / pop_sh[j] >= 1.5 and form_pr[j] >= 1 / 3],
             key=lambda r: -r["presence"])
top_links = sorted([{"col": c, "name": lab(c), "ratio": round(float(form_sh[j] / pop_sh[j]), 2) if pop_sh[j] else None,
                     "presence": round(float(form_pr[j]), 3), "pop_presence": round(float(pop_pr[j]), 3)}
                    for j, c in enumerate(cols) if ">" in c and form_pr[j] >= 0.15], key=lambda r: -r["presence"])[:15]

# (7) branches
B = jl(os.path.join(OUT, "branches.jsonl"))
base = n / len(E.ALL)
btab = []
inb = collections.Counter()
for b in B:
    ms = set(b["members"])
    for s in ms & set(MEM):
        inb[s] += 1
    k = len(ms & set(MEM))
    btab.append({"branch": b["id"], "parent": b.get("parent"), "name": b["name"], "n": len(ms), "in_form": k,
                 "def": len(ms & dset), "thin": len(ms & tset), "core": len(ms & cset),
                 "share_in_form": round(k / len(ms), 3), "ratio": round(k / len(ms) / base, 2)})
nobranch = sorted([s for s in MEM if not inb[s]], key=str.lower)

# composition: verdicts and local statuses
byv = collections.defaultdict(list)
for r in jl(os.path.join(OUT, "verdicts-D.jsonl")):
    byv[r["sub"]].append(r)
verdict = {}
for s in MEM:
    rs = byv.get(s, [])
    ruled = [r for r in rs if r.get("ruled_by") == "analyst"]
    if ruled:
        verdict[s] = ruled[-1]["verdict"]
        continue
    vs = {e["verdict"] for r in rs for e in (r.get("readers") or [])}
    verdict[s] = vs.pop() if len(vs) == 1 else None
local = vlib.local_return_states(OUT)
status = {s: local.get(s, {}).get("local_status", "unresolved") for s in MEM}

# survival from the record
oe = {r["sub"]: r for r in jl(os.path.join(OUT, "organizing_end-A1.jsonl"))}
hrs = [oe[s]["organizing_end_hour"] for s in MEM if isinstance(oe.get(s, {}).get("organizing_end_hour"), (int, float))]
aft = [oe[s]["aftermath_share"] for s in MEM if isinstance(oe.get(s, {}).get("aftermath_share"), (int, float))]
wr = collections.Counter(oe.get(s, {}).get("work_remained", "silent") for s in MEM)

# (9) themes on the defining members' codes
t4 = {m: r["id"] for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl")) for m in r.get("members") or []}
room = collections.defaultdict(collections.Counter)
for r in E.CODES:
    nodes = [t4[x] for x in E.PLACE.get((r["sub"], r.get("theme_id")), []) if x in t4]
    for nd in nodes:
        room[r["sub"]][nd] += 1 / len(nodes)
pop, fr, carry = collections.Counter(), collections.Counter(), collections.Counter()
for s, c in room.items():
    pop.update(c)
    if s in dset:
        fr.update(c)
        carry.update({k for k, v in c.items() if v > 0})
pt, ft = sum(pop.values()), sum(fr.values())
trows = [{"t4": k, "name": names4.get(k), "pop_share": round(pop[k] / pt, 4), "form_share": round(fr.get(k, 0) / ft, 4),
          "ratio": round(fr.get(k, 0) / ft / (pop[k] / pt), 3), "members": carry.get(k, 0)} for k in sorted(pop)]
over = [r for r in trows if r["ratio"] >= 1.5 and r["members"] >= 5]
under = [r for r in trows if r["ratio"] <= 0.67 and r["pop_share"] >= 0.01]

# (5) representatives and (8) the room between forms
C = E.CENTRE
dist = {s: float(np.linalg.norm(E.XD[E.IDX[s]] - C[a.form])) for s in DEFS}
margin = {s: min(float(np.linalg.norm(E.XD[E.IDX[s]] - C[g])) for g in C if g != a.form) - dist[s] for s in DEFS}
nearer = {s: min((g for g in C if g != a.form), key=lambda g: float(np.linalg.norm(E.XD[E.IDX[s]] - C[g]))) for s in DEFS}
medch = statistics.median(E.NCH[s] for s in DEFS)
medco = statistics.median(E.NCODES[s] for s in DEFS)
earlier = set()
for f in sorted(os.listdir(os.path.join(OUT, "forms"))):
    if f.endswith("-account.md"):
        earlier.update(re.findall(r"\*\*Read at length: r/([A-Za-z0-9_]+)", open(os.path.join(OUT, "forms", f), encoding="utf-8").read()))
order = sorted(DEFS, key=lambda s: dist[s])
best = [s for s in order if E.NCH[s] >= medch and E.NCODES[s] >= medco][:2]
least = order[-1]
ten = order[:10]
length = max([s for s in ten if s not in earlier], key=lambda s: (E.NCH[s], E.NCODES[s]))
centres = {g: round(float(np.linalg.norm(C[a.form] - C[g])), 4) for g in C if g != a.form}


def row(s):
    return {"sub": s, "dist": round(dist[s], 4), "margin": round(margin[s], 4), "nearer_other": nearer[s], "changes": E.NCH[s],
            "codes": E.NCODES[s], "verdict": verdict[s], "branches": inb[s]}


out = {"form": a.form, "name": FORM["name"], "n": n, "n_def": len(DEFS), "n_thin": len(THIN), "n_core": len(CORE),
       "thin": [{"sub": s, "changes": E.NCH[s], "codes": E.NCODES[s], "verdict": verdict[s]} for s in THIN],
       "core": [{"sub": s, "codes": E.NCODES[s], "verdict": verdict[s]} for s in CORE],
       "elements": eltab, "arrows": arx, "propositions": props, "signature_T4": sig, "links_held": top_links,
       "branches": btab, "no_branch": nobranch, "no_branch_def": sum(1 for s in nobranch if s in dset),
       "verdicts_all": dict(collections.Counter(v or "unruled" for v in verdict.values())),
       "verdicts_def": dict(collections.Counter(verdict[s] or "unruled" for s in DEFS)),
       "local_status": dict(collections.Counter(status.values())),
       "uncomposed": sorted(s for s in MEM if verdict[s] in ("does-not-compose", "cannot-tell")),
       "survival": {"median_organizing_end_hour": statistics.median(hrs) if hrs else None, "with_hour": len(hrs),
                    "aftermath_share": round(sum(aft) / len(aft), 4) if aft else None,
                    "work_remained": {k: wr.get(k, 0) for k in ("kept", "lost", "silent")}},
       "themes_over": over, "themes_under": under,
       "reps_rule": {"median_changes_def": medch, "median_codes_def": medco},
       "best": [row(s) for s in best], "least": row(least), "length": row(length), "ten_nearest": [row(s) for s in ten],
       "between": [row(s) for s in sorted(DEFS, key=lambda s: margin[s])[:8]], "centre_distances": centres,
       "read_at_length_earlier": len(earlier)}
print(json.dumps(out, ensure_ascii=False))
