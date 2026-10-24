#!/usr/bin/env python3
"""D3c, J's drift check before the freeze (16 October, 19:08 Berlin): draw the blind re-rule sample by the rules
logged at D3c before the draw. Population A: first-return lines whose last ruling was written at D3a-10 to D3a-54.
Population B: re-check lines whose last ruling is a D3b reading (not a G61 (1) repeat) written before --cutoff.
Both exclude propose lines and NONPORTABLE lines. Each --take POP:OP=N draws N lines of that population and op,
sorted by (op, sub, id), with random.Random(seed + index of the take). --force ID adds a line flagged 'forced'.
Prints only ids, elements, ops and populations: never a decision, a kind or a reason. Writes --out; never overwrites.

    python3 out/_analysis/d3c_blind_sample.py --seed 2026102310 --cutoff 2026-10-23T06:20 \
        --take A:instantiate=8 ... --force anaheimducks-066 ... --out out/_analysis/d3c_blind/sample-D3c.json
"""
import argparse, json, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--seed", type=int, required=True)
ap.add_argument("--cutoff", required=True)
ap.add_argument("--take", action="append", required=True)
ap.add_argument("--force", action="append", default=[])
ap.add_argument("--out", required=True)
a = ap.parse_args()
if os.path.exists(a.out):
    raise SystemExit("refusing to overwrite %s (never overwrite; supersede with a new name)" % a.out)


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


old = jl(os.path.join(OUT, "adaptations.jsonl"))
new = jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r


def legnum(leg):
    m = re.match(r"D3a-(\d+)$", leg or "")
    return int(m.group(1)) if m else None


def ok(l):
    return l.get("op") != "propose" and l.get("portable") is not False


popA = [l for l in old if ok(l) and legnum(last.get(l["id"], {}).get("leg")) is not None
        and 10 <= legnum(last[l["id"]]["leg"]) <= 54]
popB = [l for l in new if ok(l) and last.get(l["id"], {}).get("leg") == "D3b"
        and not (last[l["id"]].get("reason") or "").startswith("G61 (1)")
        and (last[l["id"]].get("t") or "") < a.cutoff]
pops = {"A": popA, "B": popB}
print("population A %d lines; population B %d lines" % (len(popA), len(popB)))
sample, seen = [], set()
for i, t in enumerate(a.take):
    pop, _, rest = t.partition(":")
    op, _, n = rest.partition("=")
    sel = sorted((l for l in pops[pop] if l["op"] == op), key=lambda l: (l["op"], l["sub"], l["id"]))
    drawn = random.Random(a.seed + i).sample([l["id"] for l in sel], int(n))
    byid = {l["id"]: l for l in sel}
    for d in drawn:
        seen.add(d)
        sample.append({"adaptation": d, "element": byid[d]["element"], "op": op, "population": pop, "forced": False})
    print("%s %s: %d lines; drew %s" % (pop, op, len(sel), ", ".join(drawn)))
byall = {l["id"]: l for l in old + new}
for f in a.force:
    l = byall.get(f)
    if l is None:
        raise SystemExit("forced id %s is in no ledger" % f)
    if f in seen:
        raise SystemExit("forced id %s was also drawn" % f)
    sample.append({"adaptation": f, "element": l["element"], "op": l["op"],
                   "population": "A" if f in {x["id"] for x in old} else "B", "forced": True})
    print("forced %s (%s, %s)" % (f, l["element"], l["op"]))
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
json.dump({"seed": a.seed, "cutoff": a.cutoff, "take": a.take, "force": a.force, "sample": sample},
          open(a.out, "w", encoding="utf-8"), indent=1)
print("wrote %d ids to %s" % (len(sample), a.out))
