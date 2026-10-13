#!/usr/bin/env python3
"""C1, QC1-003 (handler's ruling under J's delegation, 13 October): the revision-rate errors the C1 tools could not
apply, one line each in out/_analysis/c1_unapplied.jsonl: the item, the placement as it is, the change the C1 tools
could not make (empty the line, or swap the placed theme with also_present), and the concepts that decide it.
Read from c1_revision/classes.json (rows carried) and my decisions (dec-*.json). Refuses to overwrite.

    python3 out/_analysis/c1_unapplied.py [--write]
"""
import argparse, glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DIR = os.path.join(OUT, "_analysis", "c1_revision")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    rows = [r for r in json.load(open(os.path.join(DIR, "classes.json"), encoding="utf-8"))["rows"] if r["carried"]]
    dec = {d["item"]: d for p in sorted(glob.glob(os.path.join(DIR, "dec-*.json"))) for d in json.load(open(p, encoding="utf-8"))}
    cur = {"%s:%s" % (r["sub"], r["theme_id"]): r for r in map(json.loads, open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8"))}
    out = []
    for r in rows:
        it, d, c = r["item"], dec[r["item"]], cur[r["item"]]
        now = {"third_order": c.get("third_order") or [], "support_by_theme": c.get("support_by_theme") or {},
               "also_present": c.get("also_present") or {}}
        if not d["codes"]:
            change = "empty the line"
            decides = {"line_concepts": now["support_by_theme"], "why": d.get("note")}
        else:
            prim = list(d["codes"])[0]
            change = "swap the placed theme with also_present: place %s; list %s under also_present" % (
                prim, ", ".join(d.get("bag") or []))
            decides = {"placed": {prim: d["codes"][prim]}, "also_present_themes": d.get("bag") or [], "why": d.get("note")}
        out.append({"item": it, "placement_now": now, "change": change, "decides": decides,
                    "source": "C1a-05 revision rate (seed 20261013); QC1-003"})
        print("%-24s now %-20s -> %s" % (it, ",".join(now["third_order"]) or "-", change))
    if a.write:
        p = os.path.join(OUT, "_analysis", "c1_unapplied.jsonl")
        if os.path.exists(p):
            sys.exit("c1_unapplied.jsonl exists; supersede it with a new name")
        with open(p, "w", encoding="utf-8") as f:
            for x in out:
                f.write(json.dumps(x, ensure_ascii=False) + "\n")
        print("wrote out/_analysis/c1_unapplied.jsonl (%d)" % len(out))


if __name__ == "__main__":
    main()
