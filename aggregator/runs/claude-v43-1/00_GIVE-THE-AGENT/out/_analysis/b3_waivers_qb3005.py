#!/usr/bin/env python3
"""B3b: J's waiver at QB3-005 (23:09 Berlin): the 22 readers' record slips, placements kept as given, one line each in
out/return_waivers.jsonl keyed by batch and position, in the form J gave. Found with checks/stage_B3.py's own tests:
  support_overlap  a multiplacement record whose support_additional is empty or shares a concept with
                   support_primary (the record's batch and position; one line per position)
  support_count    a multi line whose support holds fewer distinct concepts than themes
  no_multi         a line with no multi field
Refuses unless they are the 10 + 8 + 4 named in the question. Dry run unless --write."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
REASON = {"support_overlap": "the multiplacement record's support_additional shares a concept with support_primary; "
                             "the added theme also has a concept of its own (b3_support_defects.py); kept as given",
          "support_count": "the line's support lists the primary's concepts only; the multiplacement records carry a "
                           "concept of its own for each added theme; kept as given",
          "no_multi": "a single-theme line written without the multi field; one theme placed; kept as given"}
EXPECT = {"support_overlap": 10, "support_count": 8, "no_multi": 4}


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    raw = jl(os.path.join(OUT, "assign_raw.jsonl"))
    keys = set()
    for m in jl(os.path.join(OUT, "multiplacement_log.jsonl")):
        sp, sa = set(m.get("support_primary") or []), set(m.get("support_additional") or [])
        if not sa or sa & sp:
            keys.add(("support_overlap", m["batch"], m["position"]))
    for x in raw:
        if "multi" not in x:
            keys.add(("no_multi", x["batch"], x["position"]))
        elif x.get("multi") and len(set(x.get("support") or [])) < len(set(x.get("third_order") or [])):
            keys.add(("support_count", x["batch"], x["position"]))
    got = {c: sum(1 for k in keys if k[0] == c) for c in EXPECT}
    if got != EXPECT:
        sys.exit("not the 22 named: %s" % got)
    p = os.path.join(OUT, "return_waivers.jsonl")
    have = {(w.get("check"), w.get("batch"), w.get("position")) for w in jl(p) if w.get("stage") == "B3"}
    rows = [{"stage": "B3", "check": c, "batch": b, "position": pos, "reason": REASON[c], "ruled_by": "J, 2026-10-12, QB3-005"}
            for c, b, pos in sorted(keys) if (c, b, pos) not in have]
    for r in rows:
        print(r["check"], r["batch"], r["position"])
    print("%d waivers to write" % len(rows))
    if "--write" in sys.argv:
        with open(p, "a", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("return_waivers.jsonl now %d lines" % len(jl(p)))


if __name__ == "__main__":
    main()
