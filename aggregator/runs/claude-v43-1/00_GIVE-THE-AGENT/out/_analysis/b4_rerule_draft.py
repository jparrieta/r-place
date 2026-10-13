#!/usr/bin/env python3
"""B4a-05: build a --replace draft for b4_rule_append.py from my re-ruling decisions and the old ledger lines.

    python3 out/_analysis/b4_rerule_draft.py --packet 1 --decisions out/_adjudication-B4/rerule-B4a-05/decisions-01.jsonl \
        --out out/_adjudication-B4/rerule-B4a-05/draft-01.jsonl

A decision line: {"n": 48, "r": [...], "w": "the new why", and optionally "sup": {theme: [ids]} (overrides the old
concepts for those themes), "t", "f", "th", "q", "br" (null clears it), "u", "ap" (replaces the old also_present),
"c"}. Fields not given carry over from the old ruled line; a placed theme with no sup given keeps its old concepts.
Read-only on the ledger; writes only the draft. Refuses a decision whose ruling holds a theme no placement held.
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", type=int, required=True)
    ap.add_argument("--decisions", required=True, nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    old = {d["n"]: d for d in jl(os.path.join(OUT, "disagreements.jsonl")) if d.get("packet") == a.packet}
    probs, rows = [], []
    for dc in [x for f in a.decisions for x in jl(f)]:
        n = dc["n"]
        d = old.get(n)
        if d is None:
            probs.append("item %d not ruled" % n)
            continue
        held = set(d["readers"][0]) | set(d["readers"][1]) | set(d.get("b1") or [])
        r = dc["r"]
        if set(r) - held:
            probs.append("item %d: %s held by no placement" % (n, sorted(set(r) - held)))
        sup = {}
        for t in r:
            v = (dc.get("sup") or {}).get(t) or d["support_by_theme"].get(t)
            if not v:
                probs.append("item %d: no concepts for %s" % (n, t))
            sup[t] = v
        row = {"n": n, "r": r, "t": dc.get("t", d["taxonomy"]), "c": dc.get("c", d["confidence"]), "w": dc["w"],
               "sup": sup}
        if dc.get("u"):
            row["u"] = True
            row["sup"] = {}
        tax = row["t"]
        if tax == "scheme-ambiguous":
            row["f"] = dc.get("f", d.get("field"))
            row["th"] = dc.get("th", d.get("theme"))
            row["q"] = dc.get("q", d.get("quote"))
        else:
            row["q"] = dc.get("q", d.get("quote") if d["taxonomy"] != "scheme-ambiguous" else None)
            if row["q"] is None:
                probs.append("item %d: taxonomy changed to %s; give q" % (n, tax))
        br = dc["br"] if "br" in dc else d.get("boundary_ruling")
        if br:
            row["br"] = br
        apv = dc["ap"] if "ap" in dc else d.get("also_present") or {}
        if apv:
            row["ap"] = apv
        rows.append(row)
    for p in probs:
        print("PROBLEM " + p)
    if probs:
        sys.exit(1)
    with open(a.out, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("wrote %d draft lines to %s" % (len(rows), os.path.relpath(a.out, ROOT)))


if __name__ == "__main__":
    main()
