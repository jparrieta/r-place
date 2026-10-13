#!/usr/bin/env python3
"""C1, read-only: J's floor (QC1-002) against my own C1 re-placements. For every line of assignments_final.jsonl that a
C1 move rewrote, the themes now on the line that no line before C1 held (assign_final.jsonl's third_order) and that
sit second or third with fewer than three concepts. Those rest on rule 0's old 'alone at its level', which the floor
replaced. Prints each with the leg of the move that added it.

    python3 out/_analysis/c1_floor_scan.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def main():
    settled = {(r["sub"], r["theme_id"]): r for r in jl("assign_final.jsonl")}
    n = 0
    for r in jl("assignments_final.jsonl"):
        mv = [m for m in r.get("moves") or [] if m.get("stage") == "C1"]
        if not mv:
            continue
        k = (r["sub"], r["theme_id"])
        th, sup = r.get("third_order") or [], r.get("support_by_theme") or {}
        before = set(settled[k].get("third_order") or [])
        for i, t in enumerate(th):
            if i == 0 or t in before or len(sup.get(t) or []) >= 3:
                continue
            leg = next((m.get("leg") for m in reversed(mv) if t in m.get("to", []) and t not in (m.get("from") or [])), "?")
            n += 1
            print("%s/%s: %s; %s at position %d on %d concept%s (%s), added at %s" % (
                k[0], k[1], ",".join("%s(%d)" % (x, len(sup.get(x) or [])) for x in th), t, i + 1, len(sup.get(t) or []),
                "" if len(sup.get(t) or []) == 1 else "s", ",".join(sup.get(t) or []), leg))
    print("%d themes below the floor that a C1 move added" % n)


if __name__ == "__main__":
    main()
