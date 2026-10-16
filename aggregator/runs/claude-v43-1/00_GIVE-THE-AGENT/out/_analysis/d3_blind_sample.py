#!/usr/bin/env python3
"""D3, J's drift check (16 October, 19:08 Berlin): draw a blind re-rule sample from closed element groups.
For each --take ELEMENT=N, draws N of the element's portable ledger lines (the lines `mem.py adaptations --element`
selects, in the verb's order) by random.Random(SEED + index of the element in the order given), and writes the ids,
element and op to --out. Prints only ids, elements and ops: never a decision, a kind or a reason, so the re-rule stays
blind. Writes nothing else.

    python3 out/_analysis/d3_blind_sample.py --seed 2026101610 --take R01=7 --take P01=7 --out out/_analysis/d3_blind/sample.json
"""
import argparse, json, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--seed", type=int, required=True)
ap.add_argument("--take", action="append", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()

lines = [json.loads(l) for l in open(os.path.join(OUT, "adaptations.jsonl"), encoding="utf-8") if l.strip()]
sample = []
for i, t in enumerate(a.take):
    el, _, n = t.partition("=")
    sel = [l for l in lines if l.get("element") == el and l.get("portable", True)]
    sel.sort(key=lambda l: (l["op"], l["sub"]))
    ids = [l["id"] for l in sel]
    drawn = random.Random(a.seed + i).sample(ids, int(n))
    byid = {l["id"]: l for l in sel}
    for d in drawn:
        sample.append({"adaptation": d, "element": el, "op": byid[d]["op"]})
    print("%s: %d portable lines; drew %s" % (el, len(sel), ", ".join(drawn)))
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
if os.path.exists(a.out):
    raise SystemExit("refusing to overwrite %s (never overwrite; supersede with a new name)" % a.out)
json.dump({"seed": a.seed, "take": a.take, "sample": sample}, open(a.out, "w", encoding="utf-8"), indent=1)
print("wrote %d ids to %s" % (len(sample), a.out))
