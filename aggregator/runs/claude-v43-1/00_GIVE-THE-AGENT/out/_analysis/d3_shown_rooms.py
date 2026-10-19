#!/usr/bin/env python3
"""Count the rooms where an element is shown, from a leg's ruling files.

A room shows the element where one of its instantiate lines is accepted, or where one of its absent
lines is rejected because the concepts show the element. Restrict and add specifications are not
counted, since they mostly state conditions the element's statement already holds.

  python3 out/_analysis/d3_shown_rooms.py --inst out/_analysis/d3_rulings/C02-inst-000.jsonl \
      out/_analysis/d3_rulings/C02-inst-100.jsonl --absent out/_analysis/d3_rulings/C02-absent.jsonl
"""
import argparse
import json
import re


def room(aid):
    return re.sub(r"-\d+$", "", aid)


def rooms(files, decision):
    out = set()
    for f in files:
        for line in open(f):
            r = json.loads(line)
            if r["decision"] == decision:
                out.add(room(r["adaptation"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inst", nargs="+", required=True)
    ap.add_argument("--absent", nargs="+", required=True)
    a = ap.parse_args()
    inst = rooms(a.inst, "accept")
    absent = rooms(a.absent, "reject")
    print(f"rooms shown by accepted instantiate lines: {len(inst)}")
    print(f"rooms shown by rejected absent lines: {len(absent)}")
    print(f"overlap: {len(inst & absent)}")
    print(f"rooms where the element is shown, either op: {len(inst | absent)}")


if __name__ == "__main__":
    main()
