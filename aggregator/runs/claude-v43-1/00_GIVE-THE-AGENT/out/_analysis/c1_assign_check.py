#!/usr/bin/env python3
"""C1, read-only: assignments_final.jsonl against assign_final.jsonl and the overlay. Keys equal and one line each;
every line whose placement differs from the settled line is in assign_revisions_only.jsonl with the same placement, and
the overlay holds nothing else; every C1 move names its concepts; empties counted; moves by kind of reason.

    python3 out/_analysis/c1_assign_check.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def pl(r):
    return sorted(t for t in (r.get("third_order") or []) if t and t != "unresolved")


def main():
    old = {(r["sub"], r["theme_id"]): r for r in jl("assign_final.jsonl")}
    new_rows = jl("assignments_final.jsonl")
    new = {(r["sub"], r["theme_id"]): r for r in new_rows}
    ov = {(r["sub"], r["theme_id"]): r for r in jl("assign_revisions_only.jsonl")}
    errs = []
    if len(new_rows) != len(new) or set(new) != set(old):
        errs.append("keys differ or a key repeats")
    moved = {k for k in new if pl(new[k]) != pl(old[k])}
    if moved - set(ov):
        errs.append("moved lines missing from the overlay: %s" % sorted(moved - set(ov))[:5])
    if any(pl(ov[k]) != pl(new[k]) for k in ov if k in new):
        errs.append("overlay and final disagree")
    if set(ov) - moved:
        errs.append("overlay lines that do not move: %s" % sorted(set(ov) - moved)[:5])
    nosup = [k for k, r in new.items() for m in r.get("moves") or [] if m.get("stage") == "C1" and not m.get("support")]
    if nosup:
        errs.append("C1 moves without concepts: %s" % nosup[:5])
    kinds = collections.Counter()
    for k, r in new.items():
        for m in r.get("moves") or []:
            if m.get("stage") == "C1":
                kinds["class 2 ruling" if str(m.get("why", "")).startswith("J, 13 October") else "re-read" if "re-read" in str(m.get("why", "")) else "other"] += 1
    empt = sum(1 for r in new.values() if not pl(r))
    print("lines %d; moved against assign_final %d; overlay %d; C1 moves %s; empties %d (assign_final %d)" % (
        len(new_rows), len(moved), len(ov), dict(kinds), empt, sum(1 for r in old.values() if not pl(r))))
    for e in errs:
        print("ERROR " + e)
    print("%d errors" % len(errs))


if __name__ == "__main__":
    main()
