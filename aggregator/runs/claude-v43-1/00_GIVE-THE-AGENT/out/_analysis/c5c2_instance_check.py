#!/usr/bin/env python3
"""C5c-02: after Stigmergy's recut, do the instances of A01, A03, A07 and A11 still sit inside their elements? An
element stands for the concepts cited under its third-order themes (support_by_theme in assignments_final.jsonl), as
c2_arrow_evidence.py reads it; the themes are those of c2_elements_c5c2.json. Prints, for each support and
support_transition code, the third-order themes that cite it and whether the element at that end still holds it.

    python3 out/_analysis/c5c2_instance_check.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
cites = collections.defaultdict(set)
for l in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        for t3, codes in (r.get("support_by_theme") or {}).items():
            for c in codes:
                cites[(r["sub"], c)].add(t3)
els = {e["id"]: set(e["themes"]) for e in json.load(open(os.path.join(OUT, "_analysis", "c2_elements_c5c2.json"),
                                                          encoding="utf-8"))["elements"]}
arrows = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "model", "arrows.jsonl"), encoding="utf-8")
          if l.strip()}
for aid in ("A01", "A03", "A07", "A11"):
    a = arrows[aid]
    for t in a.get("support_transition") or []:
        ends = [(t["codes"][0], a["from"]), (t["codes"][-1], a["to"])]
        for code, el in ends:
            ts = sorted(cites.get((t["sub"], code), set()))
            print("%s transition %s/%s -> %s: cited under %s; %s holds it: %s" % (
                aid, t["sub"], code, el, ts, el, bool(set(ts) & els[el])))
    for s in a.get("support") or []:
        ts = sorted(cites.get((s["sub"], s["code"]), set()))
        hold = [el for el in (a["from"], a["to"]) if set(ts) & els[el]]
        print("%s support %s/%s: cited under %s; held by %s" % (aid, s["sub"], s["code"], ts, hold or "neither"))
