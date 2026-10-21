#!/usr/bin/env python3
"""D3a-57: which rooms' adapted accounts rely on an element that D3 rewrote, bounded, moved to standing or
entered (stage section 5). Counts only, unless --write, which writes out/recheck-scope.json.

A room relies on an element when its ledger holds a line on that element whose last ruling is accept or modify
(an instantiate, restrict, add or link line the account carries), or, for the candidates entered at D3a-55, an
accepted propose line in the candidate's group, or a verdict ruling whose residue reason names the candidate.
The elements, from model/history.jsonl at stage D3: R01 and P05 revised (moves 172, 173); P22 and P21
reworded and A21 bounded (moves 174 to 176, the field's entries); P06, R02, K03, K04 and P19 moved from
candidate to standing (moves 177 to 181); P23 to P34 and K05 to K07 entered as candidates (moves 182 to 196).

    python3 out/_analysis/d3_recheck_scope.py [--write]
"""
import argparse, collections, glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


REVISED = ["R01", "P05"]
FIELD = ["P22", "P21", "A21"]
STATUS = ["P06", "R02", "K03", "K04", "P19"]
CAND = ["P%d" % n for n in range(23, 35)] + ["K05", "K06", "K07"]
rooms = sorted(r["sub"] for r in jl(os.path.join(ROOT, "package", "store", "rooms.jsonl")))
dropped = {r.get("sub") for r in (jl(os.path.join(OUT, "dropped.jsonl")) if os.path.exists(os.path.join(OUT, "dropped.jsonl")) else [])}
rooms = [s for s in rooms if s not in dropped]
led = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations.jsonl"))}
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
why = collections.defaultdict(set)
for i, l in led.items():
    d = last.get(i, {}).get("decision")
    if d not in ("accept", "modify"):
        continue
    e = l.get("element")
    if l.get("op") == "absent":
        continue
    if e in REVISED:
        why[l["sub"]].add("revised " + e)
    elif e in FIELD:
        why[l["sub"]].add("field entry " + e)
    elif e in STATUS:
        why[l["sub"]].add("now standing " + e)
cands = {c["class"]: c["id"] for c in json.load(open(os.path.join(OUT, "_analysis", "d3_rulings", "propose-candidates.json")))}
for s in glob.glob(os.path.join(OUT, "_analysis", "d3_rulings", "propose-spec-*.txt")):
    for line in open(s, encoding="utf-8"):
        line = line.rstrip("\n")
        if line:
            i, c = line.split("|")[:2]
            if c in cands and last.get(i, {}).get("decision") == "accept":
                why[led[i]["sub"]].add("candidate " + cands[c])
for r in jl(os.path.join(OUT, "verdicts-D.jsonl")):
    if r.get("ruled_by") == "analyst" and r.get("verdict") == "composes-with-residue":
        for c in set(re.findall(r"\b(P2[3-9]|P3[0-4]|K0[5-7])\b", r.get("reason", ""))):
            why[r["sub"]].add("verdict residue " + c)
aff = [s for s in rooms if why.get(s)]
un = [s for s in rooms if not why.get(s)]
by = collections.Counter(w.split(" ")[0] + (" " + w.split(" ")[1] if w.startswith(("verdict", "now", "field")) else "") for s in aff for w in why[s])
print("analysed rooms %d; affected %d; unaffected %d" % (len(rooms), len(aff), len(un)))
for k in ("revised R01", "revised P05"):
    print("  %s: %d rooms" % (k, sum(1 for s in aff if k in why[s])))
print("  field entries: %d rooms; now standing: %d rooms; candidates (accepted propose): %d rooms; verdict residue: %d rooms"
      % (sum(1 for s in aff if any(w.startswith("field") for w in why[s])),
         sum(1 for s in aff if any(w.startswith("now") for w in why[s])),
         sum(1 for s in aff if any(w.startswith("candidate") for w in why[s])),
         sum(1 for s in aff if any(w.startswith("verdict") for w in why[s]))))
print("  rooms relying on R01 or P05 alone counted:", sum(1 for s in rooms if any(w in why[s] for w in ("revised R01", "revised P05"))))
print("unaffected:", un)
