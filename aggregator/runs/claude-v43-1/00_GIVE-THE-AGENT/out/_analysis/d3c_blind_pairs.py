#!/usr/bin/env python3
"""D3c, J's drift check before the freeze: join the blind re-rule file to the original rulings, one pair per line,
for the handler's kappa, as d3_blind_pairs.py does for D3a-10. The original is the line's last adjudication in
adjudications.jsonl (the blind file is never appended there). Each pair carries both decisions, kinds, pairs and
reasons, the original's leg and time, the line's population and whether it was forced, and whether the original
was written before the element's last D3 revision in history.jsonl. Refuses unless the blind file covers the sample
exactly, in order. Prints raw agreement (not kappa) over all pairs and over the drawn pairs alone; writes --out;
never overwrites.

    python3 out/_analysis/d3c_blind_pairs.py --sample S.json --blind B.jsonl --out P.jsonl
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


def norm(k):
    return "none" if k in (None, "none", "None") else k


pairs = []
for s, b in zip(S, B):
    o = orig.get(s["adaptation"])
    if not o:
        raise SystemExit("no original ruling for %s" % s["adaptation"])
    ok = norm(o.get("kind")) if o.get("decision") != "reject" else None
    bk = norm(b.get("kind")) if b.get("decision") != "reject" else None
    if o.get("decision") == "particular":
        ok = "particular"
    if b.get("decision") == "particular":
        bk = "particular"
    pairs.append({"adaptation": s["adaptation"], "element": s["element"], "op": s["op"],
                  "population": s.get("population"), "forced": bool(s.get("forced")),
                  "original": {"decision": o.get("decision"), "kind": ok, "pair": o.get("pair"), "leg": o.get("leg"),
                               "t": o.get("t"), "reason": o.get("reason")},
                  "blind": {"decision": b["decision"], "kind": bk, "pair": b.get("pair"), "leg": "D3c",
                            "reason": b["reason"]},
                  "same_decision": o.get("decision") == b["decision"],
                  "same_decision_and_kind": (o.get("decision"), ok) == (b["decision"], bk),
                  "original_before_revision": bool(rev.get(s["element"]) and o.get("t", "") < rev[s["element"]])})
with open(a.out, "w", encoding="utf-8") as f:
    for p in pairs:
        f.write(json.dumps(p, ensure_ascii=False) + "\n")
drawn = [p for p in pairs if not p["forced"]]
print("wrote %d pairs to %s" % (len(pairs), a.out))
for name, ps in (("all", pairs), ("drawn", drawn), ("forced", [p for p in pairs if p["forced"]])):
    print("%s: %d pairs; decision agrees %d; decision and kind agree %d" % (
        name, len(ps), sum(p["same_decision"] for p in ps), sum(p["same_decision_and_kind"] for p in ps)))
for p in pairs:
    if not p["same_decision_and_kind"]:
        print("differs: %s (%s %s, %s%s): original %s/%s (%s) | blind %s/%s" % (
            p["adaptation"], p["element"], p["op"], p["population"], ", forced" if p["forced"] else "",
            p["original"]["decision"], p["original"]["kind"], p["original"]["leg"], p["blind"]["decision"],
            p["blind"]["kind"]))
