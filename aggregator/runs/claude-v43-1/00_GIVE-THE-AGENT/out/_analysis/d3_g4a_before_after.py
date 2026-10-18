#!/usr/bin/env python3
"""D3a-11: the add-condition, add-step and link lines of each group, ruled before a leg and after it, as a
markdown table for the notes. 'Before' is each line's latest ruling written outside the leg; 'after' is its
latest ruling. Columns are counted as d3_opkind.py counts them (a reject under 'reject', an accept of kind
none an evidence limit), so the 'after' figures match its tables.

  python3 out/_analysis/d3_g4a_before_after.py --leg D3a-11 --elements R01,P01,P02 [--ops add-condition,add-step,link]
"""
import argparse
import json
from collections import Counter

COLS = ["specification", "elaboration", "correction", "evidence limit", "particular", "reject"]


def col(r, adaptation_kind):
    dec = r.get("decision")
    kind = r.get("kind") or adaptation_kind or "-"
    if dec == "reject":
        return "reject"
    if dec == "particular":
        return "particular"
    if dec == "accept" and kind == "none":
        return "evidence limit"
    if dec == "accept":
        return kind
    return str(dec)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--leg", required=True)
    ap.add_argument("--elements", required=True)
    ap.add_argument("--ops", default="add-condition,add-step,link")
    a = ap.parse_args()
    els = [e for e in a.elements.split(",") if e]
    ops = [o for o in a.ops.split(",") if o]
    meta = {}
    for ln in open("out/adaptations.jsonl", encoding="utf-8"):
        if ln.strip():
            x = json.loads(ln)
            meta[x["id"]] = x
    before, after = {}, {}
    for ln in open("out/adjudications.jsonl", encoding="utf-8"):
        if ln.strip():
            r = json.loads(ln)
            after[r["adaptation"]] = r
            if r.get("leg") != a.leg:
                before[r["adaptation"]] = r
    print("| group | op | lines | " + " | ".join(COLS) + " |")
    print("|---|---|---|" + "---|" * len(COLS))
    tb, ta, tn = Counter(), Counter(), 0
    for el in els:
        for op in ops:
            ids = [i for i, x in meta.items() if x.get("element") == el and x.get("op") == op and i in after]
            if not ids:
                continue
            cb = Counter(col(before[i], meta[i].get("kind")) for i in ids if i in before)
            ca = Counter(col(after[i], meta[i].get("kind")) for i in ids)
            tb.update(cb)
            ta.update(ca)
            tn += len(ids)
            cells = []
            for c in COLS:
                b, n = cb.get(c, 0), ca.get(c, 0)
                cells.append(str(n) if b == n else f"{b} → {n}")
            print(f"| {el} | {op} | {len(ids)} | " + " | ".join(cells) + " |")
    cells = []
    for c in COLS:
        b, n = tb.get(c, 0), ta.get(c, 0)
        cells.append(str(n) if b == n else f"{b} → {n}")
    print(f"| all | | {tn} | " + " | ".join(cells) + " |")
    extra = sorted((set(tb) | set(ta)) - set(COLS))
    if extra:
        print("other columns: " + ", ".join(f"{c} {tb.get(c, 0)} -> {ta.get(c, 0)}" for c in extra))


if __name__ == "__main__":
    main()
