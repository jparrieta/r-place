#!/usr/bin/env python3
"""D3a-48: print one or more elements whole from out/model/elements.jsonl, with their history.jsonl lines, so that a
candidate group is read with its record before any line is ruled. Writes nothing.

  python3 out/_analysis/d3_element_record.py --ids P06 R02
"""
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("--ids", nargs="+", required=True)
a = ap.parse_args()
els = {}
for l in open("out/model/elements.jsonl", encoding="utf-8"):
    if l.strip():
        e = json.loads(l)
        els[e["id"]] = e
print("elements: %d; candidates: %s" % (len(els), " ".join(sorted(i for i, e in els.items()
                                                                   if e.get("status") == "candidate"))))
hist = [json.loads(l) for l in open("out/model/history.jsonl", encoding="utf-8") if l.strip()]
for i in a.ids:
    print("\n== %s" % i)
    for k, v in els[i].items():
        print("  %s: %s" % (k, v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)))
    n = 0
    for h in hist:
        if i in json.dumps(h, ensure_ascii=False):
            n += 1
            print("  -- history: %s" % json.dumps(h, ensure_ascii=False))
    print("  history lines naming %s: %d" % (i, n))
