#!/usr/bin/env python3
"""D3, J's drift check: join the blind re-rule file to the original rulings, one pair per line, for the handler's
kappa. The original is the line's last adjudication written before the blind file. Each pair carries both decisions,
kinds, pairs and reasons, the original's leg and time, and whether the original was written before the element's
last revision in history.jsonl (statement or range changed later). Refuses unless the blind file covers the sample
exactly, in order. Prints counts of raw agreement (not kappa) and writes --out; never overwrites.

    python3 out/_analysis/d3_blind_pairs.py --sample S.json --blind B.jsonl --out P.jsonl
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--sample", required=True)
ap.add_argument("--blind", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


S = json.load(open(a.sample, encoding="utf-8"))["sample"]
B = jl(a.blind)
if [s["adaptation"] for s in S] != [b["adaptation"] for b in B]:
    raise SystemExit("the blind file does not cover the sample exactly, in order")
orig = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    orig[r["adaptation"]] = r
rev = {}
for h in jl(os.path.join(OUT, "model", "history.jsonl")):
    if h.get("stage") == "D3" and h.get("field") in ("statement", "range", "status"):
        rev[h["id"]] = max(rev.get(h["id"], ""), h.get("t", ""))
if os.path.exists(a.out):
    raise SystemExit("refusing to overwrite %s" % a.out)
pairs, same_d, same_dk = [], 0, 0
for s, b in zip(S, B):
    o = orig.get(s["adaptation"])
    if not o:
        raise SystemExit("no original ruling for %s" % s["adaptation"])
    ok = o.get("kind") if o.get("decision") != "reject" else None
    bk = b.get("kind") if b.get("decision") != "reject" else None
    p = {"adaptation": s["adaptation"], "element": s["element"], "op": s["op"],
         "original": {"decision": o.get("decision"), "kind": ok, "pair": o.get("pair"), "leg": o.get("leg"),
                      "t": o.get("t"), "reason": o.get("reason")},
         "blind": {"decision": b["decision"], "kind": bk, "pair": b.get("pair"), "leg": "D3a-10", "reason": b["reason"]},
         "original_before_revision": bool(rev.get(s["element"]) and o.get("t", "") < rev[s["element"]])}
    pairs.append(p)
    same_d += o.get("decision") == b["decision"]
    same_dk += (o.get("decision"), ok) == (b["decision"], bk)
with open(a.out, "w", encoding="utf-8") as f:
    for p in pairs:
        f.write(json.dumps(p, ensure_ascii=False) + "\n")
print("wrote %d pairs to %s" % (len(pairs), a.out))
print("raw agreement (not kappa): decision %d of %d; decision and kind %d of %d; originals written before their element's revision: %d"
      % (same_d, len(pairs), same_dk, len(pairs), sum(p["original_before_revision"] for p in pairs)))
