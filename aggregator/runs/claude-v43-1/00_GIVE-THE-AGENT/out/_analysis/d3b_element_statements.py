#!/usr/bin/env python3
"""Print the current statement and range of the named elements (read-only).

Reads out/model/elements.jsonl and keeps the last line per id, so a revised
element shows its revised words. Used while ruling propose lines, to check
that an element or candidate states the act before a line is held by it.

usage: python3 out/_analysis/d3b_element_statements.py --ids P14,P20,P32
"""
import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", required=True)
    args = ap.parse_args()
    want = [x.strip() for x in args.ids.split(",") if x.strip()]
    last = {}
    with open(ROOT / "out" / "model" / "elements.jsonl", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("id") in want:
                last[rec["id"]] = rec
    for eid in want:
        rec = last.get(eid)
        if rec is None:
            print(f"== {eid}: not in elements.jsonl")
            continue
        print(f"== {eid}  status={rec.get('status')}  name={rec.get('name')}")
        for key in ("statement", "range", "scope", "bound"):
            if rec.get(key):
                print(f"   {key}: {rec[key]}")
        print()


if __name__ == "__main__":
    main()
