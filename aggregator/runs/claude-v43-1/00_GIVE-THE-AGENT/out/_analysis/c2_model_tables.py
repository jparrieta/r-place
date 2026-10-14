#!/usr/bin/env python3
"""C2 section 4, read-only: print model.md's apparatus tables from model/elements.jsonl and model/arrows.jsonl.

    python3 out/_analysis/c2_model_tables.py
"""
import json, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jl(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


els = jl(os.path.join("model", "elements.jsonl"))
arr = jl(os.path.join("model", "arrows.jsonl"))
E = dict((e["id"], e) for e in els)
print("| id | kind | statement | tier | dimension | range |")
print("|---|---|---|---|---|---|")
for e in els:
    print("| %s | %s | %s | %s | %s | %s |" % (e["id"], e["kind"], e["statement"], ", ".join(e["tier"]), ", ".join(e["dimension"]) or "none (form pass)", e["range"]))
print()
print("| id | from -> to | kind | strength | rooms: holds of both (share) | null mean (p95) | early / late holds | base rate beaten |")
print("|---|---|---|---|---|---|---|---|")
for a in arr:
    c = a.get("counts") or {}
    el = a.get("early_late") or {}
    print("| %s | %s -> %s | %s | %s | %s | %s | %s | %s |" % (
        a["id"], a["from"], a["to"], a["kind"], a["strength"],
        ("%d of %d (%.3f)" % (c["holds"], c["both"], c["share"])) if c else "never counted",
        ("%.3f (%.3f)" % (c["null_mean"], c["null_p95"])) if c else "-",
        ("%d of %d / %d of %d" % (el["early"], el["early_n"], el["late"], el["late_n"])) if el else "-",
        a.get("base_rate_beaten")))
print()
for a in arr:
    print("- **%s, %s %s -> %s %s.** Mechanism: %s Fails if: %s Failure present: %s. Negative check: %s. Bound: %s Support: %s. Transitions: %s." % (
        a["id"], a["from"], E[a["from"]]["statement"].split(":")[0][:60], a["to"], E[a["to"]]["statement"].split(":")[0][:60],
        a["mechanism"], a["mechanism_fails_if"], a["mechanism_failure_present"], a["negative_check"], a["bound"],
        "; ".join("\"%s\" [%s/%s]" % (s["quote"][:120], s["sub"], s["code"]) for s in a["support"]),
        "; ".join("%s %s -> %s, %d min" % (t["sub"], t["codes"][0], t["codes"][1], t["interval_min"]) for t in a["support_transition"])))
