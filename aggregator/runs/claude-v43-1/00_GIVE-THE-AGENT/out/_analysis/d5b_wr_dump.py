#!/usr/bin/env python3
"""D5b: dump, for every room in at least one branch, the work_remained field and the code(s) it cites, with hour,
first-order label and text, so that the field can be re-read by hand. One line per cited code; silent rooms get one
line. Prints text, sorted by room (case ignored). Optional --part N --of M to page the output.

    python3 out/_analysis/d5b_wr_dump.py --part 1 --of 4
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--part", type=int, default=1)
ap.add_argument("--of", type=int, default=1)
a = ap.parse_args()
B = [json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8") if l.strip()]
rooms = sorted({s for b in B for s in b["members"]}, key=str.lower)
oe = {json.loads(l)["sub"]: json.loads(l) for l in open(os.path.join(OUT, "organizing_end-A1.jsonl"), encoding="utf-8") if l.strip()}
codes = {}
want = {(s, c) for s in rooms for c in (oe.get(s, {}).get("work_remained_codes") or [])}
for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"):
    d = json.loads(l)
    if (d["sub"], d["code_id"]) in want:
        codes[(d["sub"], d["code_id"])] = d
n = len(rooms)
lo, hi = (a.part - 1) * n // a.of, a.part * n // a.of
print("rooms in a branch", n, "part", a.part, "of", a.of, "rooms", lo + 1, "to", hi)
for s in rooms[lo:hi]:
    r = oe.get(s, {})
    f = r.get("work_remained", "silent")
    cs = r.get("work_remained_codes") or []
    if not cs:
        print("%s | %s | - |" % (s, f))
    for c in cs:
        d = codes.get((s, c), {})
        print("%s | %s | %s | h%s | %s | %s" % (s, f, c, d.get("hour"), d.get("first_order", ""), d.get("text", "")))
