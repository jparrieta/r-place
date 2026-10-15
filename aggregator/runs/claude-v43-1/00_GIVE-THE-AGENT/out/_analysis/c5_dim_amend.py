#!/usr/bin/env python3
"""C5a-02, the declaration prose rule extended to the dimensions (notes-C5.md): apply one dimension's amended construct
fields (`changed`, `mistaken_for`) from c5_dim_amend.json to dimensions.jsonl, in place, and append one
tier_history.jsonl line (tier dimension) with the old line as `was`. Names and members do not change. Refuses if the
dimension already has a C5a-02 construct_amended line, or if the spec names another field.

    python3 out/_analysis/c5_dim_amend.py D0n
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
DP, TH = os.path.join(OUT, "dimensions.jsonl"), os.path.join(OUT, "tier_history.jsonl")
spec = json.load(open(os.path.join(OUT, "_analysis", "c5_dim_amend.json"), encoding="utf-8"))
did = sys.argv[1]
s = spec[did]
if set(s["now"]) - {"changed", "mistaken_for"}:
    sys.exit("%s: the spec names fields outside changed and mistaken_for" % did)
hist = [json.loads(l) for l in open(TH, encoding="utf-8") if l.strip()]
if any(h.get("leg") == LEG and h.get("id") == did and h.get("event") == "construct_amended" for h in hist):
    sys.exit("%s already has a %s construct_amended line" % (did, LEG))
rows = [json.loads(l) for l in open(DP, encoding="utf-8") if l.strip()]
row = [r for r in rows if r["id"] == did]
if len(row) != 1:
    sys.exit("%s not found once" % did)
row = row[0]
was = json.loads(json.dumps(row))
for f, v in s["now"].items():
    if f not in row["construct"]:
        sys.exit("%s has no construct field %s" % (did, f))
    row["construct"][f] = v
with open(DP, "w", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
with open(TH, "a", encoding="utf-8") as f:
    f.write(json.dumps({"t": T, "stage": "C5", "leg": LEG, "tier": "dimension", "id": did, "move": s["move"],
                        "event": "construct_amended", "was": was,
                        "now": [{"id": did, "construct": dict((k, row["construct"][k]) for k in s["now"])}],
                        "why": s["why"], "rule": "notes-C5.md, the declaration prose rule, extended at C5a-02",
                        "rests_on": s.get("rests_on", [])}, ensure_ascii=False) + "\n")
print("%s amended (%s); tier_history line appended" % (did, ", ".join(s["now"])))
