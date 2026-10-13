#!/usr/bin/env python3
"""C1, J's guard on QC1-001, for every move written in a leg (the `moves` entries of assignments_final.jsonl with that
leg, rechecks and re-reads alike): the themes each move added, and which of them neither reader (b3_classes r1, r2) nor
my B1 grouping (b1) placed. Prints; --write records out/_analysis/c1_guard_<leg>.json.

    python3 out/_analysis/c1_guard_moves.py --leg C1a-03 [--write]
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--leg", required=True); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    b3 = {(r["sub"], r["theme_id"]): r for r in jl("b3_classes.jsonl")}
    rows = []
    for r in jl("assignments_final.jsonl"):
        for m in r.get("moves") or []:
            if m.get("leg") != a.leg:
                continue
            k = (r["sub"], r["theme_id"])
            c = b3.get(k) or {}
            known = set(c.get("r1") or []) | set(c.get("r2") or []) | set(c.get("b1") or [])
            added = [t for t in m["to"] if t not in (m.get("from") or [])]
            rows.append({"item": "%s/%s" % k, "class": c.get("class"), "from": m.get("from"), "to": m["to"], "added": added,
                         "outside": [t for t in added if t not in known], "in_b1": [t for t in added if t in (c.get("b1") or [])]})
    out = [x for x in rows if x["outside"]]
    print("moves in %s: %d; adding a theme: %d; adding a theme neither reader nor my B1 placed: %d"
          % (a.leg, len(rows), sum(1 for x in rows if x["added"]), len(out)))
    for x in rows:
        print("  %s (class %s): %s -> %s; added %s; outside %s; from my B1 %s" % (
            x["item"], x["class"], ",".join(x["from"] or []), ",".join(x["to"]), ",".join(x["added"]) or "-",
            ",".join(x["outside"]) or "-", ",".join(x["in_b1"]) or "-"))
    if a.write:
        json.dump({"guard": "QC1-001", "leg": a.leg, "moves": rows},
                  open(os.path.join(OUT, "_analysis", "c1_guard_%s.json" % a.leg), "w"), indent=1, ensure_ascii=False)
        print("wrote out/_analysis/c1_guard_%s.json" % a.leg)


if __name__ == "__main__":
    main()
