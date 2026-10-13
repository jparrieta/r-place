#!/usr/bin/env python3
"""C1: turn an item-keyed decisions file ({"<sub>:<tNN>": {"reason": ...[, "theme", "codes"]}}) into the change-keyed
special file c1_decisions_common.py reads ({"gate:N": [{"item", "reason"[, "theme", "codes"]}]}), putting each item
under every named change that owes it and has not rechecked it. Refuses an item no named change owes.

    python3 out/_analysis/c1_special_by_change.py --items in.json --changes gate:15,gate:16 --out out.json
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", required=True); ap.add_argument("--changes", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    items = json.load(open(os.path.join(ROOT, a.items), encoding="utf-8"))
    res, seen = {}, set()
    for o in vlib.owed_rechecks(OUT, "C1"):
        if o["ref"] not in a.changes.split(","):
            continue
        todo = {"%s:%s" % tuple(k) for k in o["owed"] if k not in o["done"]}
        res[o["ref"]] = [dict({"item": i}, **items[i]) for i in sorted(todo) if i in items]
        seen |= todo & set(items)
    miss = sorted(set(items) - seen)
    if miss:
        sys.exit("owed by none of the changes: %s" % ", ".join(miss))
    p = os.path.join(ROOT, a.out)
    if os.path.exists(p):
        sys.exit("%s exists" % a.out)
    json.dump(res, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote %s: %s" % (a.out, ", ".join("%s %d" % (k, len(v)) for k, v in res.items())))


if __name__ == "__main__":
    main()
