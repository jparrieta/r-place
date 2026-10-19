#!/usr/bin/env python3
"""Count the rooms where C01 is shown, by side, from D3a-24's ruling files.

A room shows C01 where an instantiate line is accepted, or where an absent line is rejected because
its concepts show the element (G29). A line is counted on the lower end when its reason names
"lower end" or "lower side"; otherwise on the decided side. A room with lines on both sides counts
on both.

  python3 out/_analysis/d3_c01_sides.py
"""
import json
import re

FILES = {
    "instantiate": ["out/_analysis/d3_rulings/C01-inst-000.jsonl", "out/_analysis/d3_rulings/C01-inst-100.jsonl"],
    "absent": ["out/_analysis/d3_rulings/C01-absent.jsonl"],
}


def room(aid):
    return re.sub(r"-\d+$", "", aid)


def main():
    shown = {}
    for op, files in FILES.items():
        for f in files:
            for line in open(f):
                r = json.loads(line)
                if (op == "instantiate" and r["decision"] == "accept") or (op == "absent" and r["decision"] == "reject"):
                    lower = bool(re.search(r"lower (end|side)", r["reason"]))
                    sides = shown.setdefault(room(r["adaptation"]), set())
                    sides.add("lower" if lower else "decided")
                    if lower and re.search(r"poll|vote|team|office|leader|officer|ban|handover|handed|division|assign", r["reason"].split("lower")[0]):
                        sides.add("decided")
    by_op = {}
    for op, files in FILES.items():
        rooms = set()
        for f in files:
            for line in open(f):
                r = json.loads(line)
                if (op == "instantiate" and r["decision"] == "accept") or (op == "absent" and r["decision"] == "reject"):
                    rooms.add(room(r["adaptation"]))
        by_op[op] = rooms
    print(f"rooms shown by accepted instantiate lines: {len(by_op['instantiate'])}")
    print(f"rooms shown by rejected absent lines: {len(by_op['absent'])}")
    print(f"overlap: {len(by_op['instantiate'] & by_op['absent'])}")
    print(f"rooms where C01 is shown, either op: {len(shown)}")
    print(f"  with a line on the decided side: {sum(1 for s in shown.values() if 'decided' in s)}")
    print(f"  with a line naming the lower end: {sum(1 for s in shown.values() if 'lower' in s)}")
    print(f"  lower end only: {sum(1 for s in shown.values() if s == {'lower'})}")
    print(f"  both sides: {sum(1 for s in shown.values() if s == {'lower', 'decided'})}")


if __name__ == "__main__":
    main()
