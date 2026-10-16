#!/usr/bin/env python3
"""D3: check that a rulings file covers exactly one packet: the ids of one element's lines (optionally one op), in the
verb's order (op, room), sliced [offset, offset + limit), against the file's ids in order. Prints the counts, whether
they match, and any id missing or extra. Writes nothing.

    python3 out/_analysis/d3_check_file.py --element P01 --op add-condition --offset 0 --limit 53 --file <rulings>
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--op")
ap.add_argument("--offset", type=int, default=0)
ap.add_argument("--limit", type=int, required=True)
ap.add_argument("--file", required=True)
a = ap.parse_args()
sel = [json.loads(l) for l in open(os.path.join(ROOT, "out", "adaptations.jsonl"), encoding="utf-8") if l.strip()]
sel = [l for l in sel if l.get("element") == a.element and (not a.op or l.get("op") == a.op)]
sel.sort(key=lambda l: (l["op"], l["sub"]))
want = [l["id"] for l in sel[a.offset:a.offset + a.limit]]
got = [json.loads(l)["adaptation"] for l in open(a.file, encoding="utf-8") if l.strip()]
ok = want == got
print("packet %d ids, file %d ids, same ids in order: %s" % (len(want), len(got), ok))
if not ok:
    print("missing: %s" % [i for i in want if i not in got])
    print("extra: %s" % [i for i in got if i not in want])
    sys.exit(1)
