#!/usr/bin/env python3
"""C1, J's guard on QC1-001 (21:12 Berlin): count and report the C1 recheck moves to a theme that neither the readers
(b3_classes r1, r2) nor my B1 grouping (b1) placed. For each moved recheck: the themes it added (in `now`, not in
`was`), and which of them no reader and not my B1 placed. Also lists the rechecks whose reason puts the item on the
visitor rule's sweep. Prints; --write records out/_analysis/c1_guard.json.

    python3 out/_analysis/c1_guard_report.py [--write]
"""
import collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def main():
    b3 = {(r["sub"], r["theme_id"]): r for r in jl("b3_classes.jsonl")}
    rows, sweep = [], []
    per = collections.Counter(); per_new = collections.Counter(); per_out = collections.Counter()
    for r in jl("rechecks-C1.jsonl"):
        k = (r["sub"], r["theme_id"])
        if "visitor rule's sweep" in (r.get("why") or ""):
            sweep.append("%s/%s" % k)
        if not r.get("changed"):
            continue
        c = b3.get(k) or {}
        known = set(c.get("r1") or []) | set(c.get("r2") or []) | set(c.get("b1") or [])
        added = [t for t in r["now"] if t not in (r.get("was") or [])]
        outside = [t for t in added if t not in known]
        per[r["change"]] += 1
        if added:
            per_new[r["change"]] += 1
        if outside:
            per_out[r["change"]] += 1
        rows.append({"change": r["change"], "item": "%s/%s" % k, "class": c.get("class"), "was": r.get("was"),
                     "now": r["now"], "added": added, "added_outside_readers_and_b1": outside})
    print("moved rechecks at C1: %d" % len(rows))
    for ch in sorted(per, key=lambda x: int(x.split(":")[1])):
        print("  %s: %d moved, %d adding a theme, %d adding a theme neither the readers nor my B1 placed"
              % (ch, per[ch], per_new[ch], per_out[ch]))
    print("moves to a theme no reader and not my B1 placed:")
    for x in rows:
        if x["added_outside_readers_and_b1"]:
            print("  %s %s (class %s): %s -> %s; outside: %s" % (x["change"], x["item"], x["class"], ",".join(x["was"] or []),
                                                               ",".join(x["now"]), ",".join(x["added_outside_readers_and_b1"])))
    sweep = sorted(set(sweep))
    print("listed for the visitor rule's sweep: %d: %s" % (len(sweep), ", ".join(sweep)))
    if "--write" in sys.argv:
        json.dump({"guard": "QC1-001, J 21:12 Berlin", "moves": rows, "sweep": sweep},
                  open(os.path.join(OUT, "_analysis", "c1_guard.json"), "w"), indent=1, ensure_ascii=False)
        print("wrote out/_analysis/c1_guard.json")


if __name__ == "__main__":
    main()
