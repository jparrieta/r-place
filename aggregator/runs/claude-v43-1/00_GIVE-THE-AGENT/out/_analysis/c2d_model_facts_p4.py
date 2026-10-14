#!/usr/bin/env python3
"""C2d-01, pass 4, read-only: print per arrow what model-p4.md must carry, from model/arrows.jsonl as pass 4 left it:
counts, the order-fails count (both minus holds), the failure clause counted (clause_holds), the count without joining
lines, the sides, sampled rooms that fail, the bound, every support transition with its audit, the instance note, and
A20's counts before hour 73. Also the support quotes, so the model text quotes the ledger and not memory.

    python3 out/_analysis/c2d_model_facts_p4.py > out/_analysis/c2d_model_facts-p4.txt
"""
import json, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = [json.loads(l) for l in open(os.path.join(OUT, "model", "arrows.jsonl"), encoding="utf-8") if l.strip()]
for a in rows:
    c = a.get("counts") or {}
    print("== %s %s -> %s, %s, %s" % (a["id"], a["from"], a["to"], a["kind"], a["strength"]))
    if c.get("both"):
        print("  counts: holds %s of %s (%.3f), null mean %.3f, p95 %.3f; order fails in %d" % (
            c["holds"], c["both"], c["share"], c["null_mean"], c["null_p95"], c["both"] - c["holds"]))
    el = a.get("early_late") or {}
    if el:
        print("  sides: early %s of %s, late %s of %s" % (el.get("early"), el.get("early_n"), el.get("late"), el.get("late_n")))
    if a.get("clause_holds"):
        print("  clause: no TO after the first FROM in %d of %d" % (a["clause_holds"]["rooms"], a["clause_holds"]["both"]))
    if a.get("without_joining"):
        w = a["without_joining"]
        print("  without joining: %s of %s (%.3f), p95 %.3f, beaten %s" % (w["holds"], w["both"], w["share"], w["null_p95"], w["beaten"]))
    if a.get("before_h73"):
        for k, v in a["before_h73"].items():
            print("  before h73 %s: %s" % (k, v if isinstance(v, str) else "%s of %s (%.3f), null mean %.3f, p95 %.3f" % (
                v["holds"], v["both"], v["share"], v["null_mean"], v["null_p95"])))
    print("  sampled fails: %s" % ", ".join(s["sub"] for s in a.get("sampled_against") or [] if s.get("found") != "holds"))
    print("  bound: %s" % a.get("bound"))
    for t in a.get("support_transition") or []:
        print("  transition %s %s -> %s (%s min): %s" % (t["sub"], t["codes"][0], t["codes"][1], t.get("interval_min"), t.get("audit")))
    for s in a.get("support") or []:
        print("  quote %s/%s: %s" % (s["sub"], s["code"], s["quote"][:300]))
    if a.get("instance_note"):
        print("  instance note: %s" % a["instance_note"])
