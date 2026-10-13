#!/usr/bin/env python3
"""C1: record one change to the third-order tier in the two places it lives: an op in out/_analysis/c1_tier_ops.jsonl,
which c1_scheme_v2_sync.py applies to scheme_v2.jsonl, and its event line in out/tier_history.jsonl (section 4). For now
one kind: --rare moves a theme to the rare tier (tier "rare", floor null; event moved_to_rare). Refuses a theme already
rare or missing. Dry run without --write.

    python3 out/_analysis/c1_tier_op.py --rare T3-140 --leg C1a-04 --move "relating or contrasting" \
        --prompted "..." --why "..." [--write]
"""
import argparse, datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rare", required=True); ap.add_argument("--leg", required=True); ap.add_argument("--move", required=True)
    ap.add_argument("--prompted", required=True); ap.add_argument("--why", required=True); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    rows = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "scheme_v2.jsonl"), encoding="utf-8") if l.strip()}
    r = rows.get(a.rare)
    if r is None or r.get("tier") == "rare":
        sys.exit("%s missing or already rare" % a.rare)
    n = 0
    for l in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8"):
        if a.rare in (json.loads(l).get("third_order") or []):
            n += 1
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ops = [{"op": "set", "id": a.rare, "field": "tier", "value": "rare", "leg": a.leg, "t": t},
           {"op": "set", "id": a.rare, "field": "floor", "value": None, "leg": a.leg, "t": t}]
    hist = {"t": t, "stage": "C1", "leg": a.leg, "tier": "third", "id": a.rare, "move": a.move, "event": "moved_to_rare",
            "was": {"label": r.get("name"), "tier": r.get("tier"), "floor": r.get("floor")},
            "now": [{"id": a.rare, "tier": "rare", "members": n}], "prompted_by": a.prompted, "why": a.why}
    print(json.dumps(ops, ensure_ascii=False)); print(json.dumps(hist, ensure_ascii=False))
    if not a.write:
        return
    with open(os.path.join(OUT, "_analysis", "c1_tier_ops.jsonl"), "a", encoding="utf-8") as f:
        for o in ops:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    with open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(hist, ensure_ascii=False) + "\n")
    print("wrote 2 ops and 1 tier_history line for %s" % a.rare)


if __name__ == "__main__":
    main()
