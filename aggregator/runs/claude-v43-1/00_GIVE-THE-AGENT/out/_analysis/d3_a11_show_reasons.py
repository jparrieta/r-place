#!/usr/bin/env python3
"""D3a-38: print the class and reason (or evidence) of named A11 transition lines, from the spec files and the absent
rulings, as d3_a11_reply_check3.py reads them. Writes nothing.

  python3 out/_analysis/d3_a11_show_reasons.py Okami-008 aoe2-055
"""
import json
import sys

R = "out/_analysis/d3_rulings/"
want = set(sys.argv[1:])
for name in ("A11-inst-spec.txt", "A11-restrict-spec.txt"):
    for l in open(R + name, encoding="utf-8"):
        if l.strip():
            aid, cls, ev = l.rstrip("\n").split("|", 2)
            if aid in want:
                print("%s %s: %s" % (aid, cls, ev))
for l in open(R + "A11-absent.jsonl"):
    r = json.loads(l)
    if r["adaptation"] in want:
        print("%s absent %s: %s" % (r["adaptation"], r["decision"], r["reason"]))
