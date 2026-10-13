#!/usr/bin/env python3
"""C1: write a gate change's decisions file for c1_recheck_apply.py when most owed items share one reading. Every owed,
not yet rechecked item gets --reason (recorded unchanged, its themes and concepts copied from its line); items named in
--special (a JSON list of {"item", "reason"[, "theme", "codes"]}) take their own entry instead. Refuses a special item the
change does not owe. Writes out/_analysis/c1_rechecks/<ref>-decisions.json, refusing to overwrite.

    python3 out/_analysis/c1_decisions_common.py --change gate:8 --reason "..." [--special path.json]
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--change", required=True); ap.add_argument("--reason", required=True); ap.add_argument("--special")
    a = ap.parse_args()
    o = next((x for x in vlib.owed_rechecks(OUT, "C1") if x["ref"] == a.change), None)
    if o is None:
        sys.exit("no change %s" % a.change)
    todo = ["%s:%s" % k for k in o["owed"] if k not in o["done"]]
    spec = {}
    if a.special:
        sp = json.load(open(os.path.join(ROOT, a.special), encoding="utf-8"))
        if isinstance(sp, dict):                 # a file keyed by change: take this change's list
            sp = sp.get(a.change) or []
        for d in sp:
            if d["item"] not in todo:
                sys.exit("%s is not owed by %s" % (d["item"], a.change))
            spec[d["item"]] = d
    dec = [spec.get(i) or {"item": i, "reason": a.reason} for i in todo]
    p = os.path.join(OUT, "_analysis", "c1_rechecks", a.change.replace(":", "-") + "-decisions.json")
    if os.path.exists(p):
        sys.exit("%s exists" % p)
    json.dump(dec, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote %s: %d decisions, %d with their own entry" % (os.path.relpath(p, ROOT), len(dec), len(spec)))


if __name__ == "__main__":
    main()
