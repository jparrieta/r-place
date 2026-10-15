#!/usr/bin/env python3
"""C5, section 6: write out/propositions.jsonl from c5_propositions.json, carrying up from model/arrows.jsonl, for each
arrow a proposition rests on, its mechanism (and mechanism_source where stage C3 supplied it) and its order count, so
that no mechanism or count is typed. Checks that every arrow named exists. Refuses to overwrite unless --replace.

    python3 out/_analysis/c5_propositions.py [--replace]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(OUT, "propositions.jsonl")
if os.path.exists(DEST) and "--replace" not in sys.argv:
    sys.exit("propositions.jsonl exists; pass --replace")
spec = json.load(open(os.path.join(OUT, "_analysis", "c5_propositions.json"), encoding="utf-8"))
A = {r["id"]: r for r in (json.loads(l) for l in open(os.path.join(OUT, "model", "arrows.jsonl"), encoding="utf-8"))}
lines = []
for pid, s in spec.items():
    arrows = []
    for a in s["rests_on"]:
        if a not in A:
            sys.exit("%s rests on %s, which model/arrows.jsonl does not carry" % (pid, a))
        r, c = A[a], A[a].get("counts") or {}
        arrows.append({"arrow": a, "from": r["from"], "to": r["to"], "strength": r.get("strength"),
                       "mechanism": r.get("mechanism"), "mechanism_source": r.get("mechanism_source") or "C2",
                       "count": ("%d of %d rooms carrying both (%.3f; null mean %.3f, 95th percentile %.3f)" % (
                           c["holds"], c["both"], c["share"], c["null_mean"], c["null_p95"]) if c else
                                 "never counted as an order")})
    line = {"id": pid, "statement": s["statement"], "rests_on": s["rests_on"], "theorised": s["theorised"],
            "carried_by": s["carried_by"], "rival": s["rival"]}
    if s.get("finding"):
        line["finding"] = s["finding"]
    line.update({"primary": s.get("primary"), "thin": s["thin"], "level": s["level"],
                 "from_literature": any(x["mechanism_source"] == "from-literature" for x in arrows),
                 "mechanisms": arrows,
                 "evidence_gate": "rooms carrying both elements of each arrow; the order statement 'in a room carrying "
                                  "both, the first concept of FROM comes before the first concept of TO', against 500 "
                                  "shuffles within each room (seed 20261014)",
                 "decides": s["decides"], "falsify_elsewhere": s["falsify_elsewhere"], "boundary": s["boundary"]})
    lines.append(line)
with open(DEST, "w", encoding="utf-8") as f:
    f.write("".join(json.dumps(l, ensure_ascii=False) + "\n" for l in lines))
print("propositions.jsonl: %d lines; thin %d; wholly theorised %d; from-literature %d" % (
    len(lines), sum(l["thin"] for l in lines), sum(l["theorised"] for l in lines), sum(l["from_literature"] for l in lines)))
