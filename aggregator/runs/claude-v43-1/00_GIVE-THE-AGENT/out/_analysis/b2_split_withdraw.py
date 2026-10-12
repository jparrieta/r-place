#!/usr/bin/env python3
"""B2a-r3-p2: withdraw the split's placements from author_items.jsonl and gold_items.jsonl (J, 2026-10-12).

The children's lines (source "split") move, unchanged and in order, to
out/_analysis/author_items_split_withdrawn.jsonl and gold_items_split_withdrawn.jsonl; each items file
keeps the lines it held before the split, in their order. Refuses to run twice (the withdrawn files must not
exist) and checks that every moved line is a child of out/recut/themes.jsonl. Dry run unless --write.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    kids = {"%s/%s" % (r["sub"], r["theme_id"]) for r in jl(os.path.join(OUT, "recut", "themes.jsonl"))}
    plan = []
    for name, wname in (("author_items.jsonl", "author_items_split_withdrawn.jsonl"),
                        ("gold_items.jsonl", "gold_items_split_withdrawn.jsonl")):
        p, wp = os.path.join(OUT, name), os.path.join(OUT, "_analysis", wname)
        if os.path.exists(wp):
            sys.exit("%s exists; the withdrawal ran already" % wp)
        raw = [x for x in open(p, encoding="utf-8") if x.strip()]
        keep = [x for x in raw if json.loads(x).get("source") != "split"]
        move = [x for x in raw if json.loads(x).get("source") == "split"]
        bad = [json.loads(x)["item"] for x in move if json.loads(x)["item"] not in kids]
        if bad:
            sys.exit("lines marked split that are no child of out/recut: %s" % bad)
        print("%s: %d lines; keep %d, move %d to %s" % (name, len(raw), len(keep), len(move), wname))
        plan.append((p, wp, keep, move))
    if "--write" not in sys.argv:
        return
    for p, wp, keep, move in plan:
        with open(wp, "w", encoding="utf-8") as f:
            f.writelines(move)
        with open(p, "w", encoding="utf-8") as f:
            f.writelines(keep)
    print("written")


if __name__ == "__main__":
    main()
