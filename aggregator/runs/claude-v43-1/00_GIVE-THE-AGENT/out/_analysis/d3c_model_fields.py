#!/usr/bin/env python3
"""D3c: print the field names the model's elements and arrows carry, the fields of one element in full, and
the number of lines in findings.jsonl. Read-only.

    python3 out/_analysis/d3c_model_fields.py --id P05
"""
import argparse
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--id", required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


last = {}
for r in jl(os.path.join(OUT, "model", "elements.jsonl")):
    last[r["id"]] = r
keys = set()
for r in last.values():
    keys |= set(r)
print("element fields:", sorted(keys))
arrows = jl(os.path.join(OUT, "model", "arrows.jsonl"))
akeys = set()
for r in arrows:
    akeys |= set(r)
print("arrow fields:", sorted(akeys))
rec = last.get(a.id)
if rec is None:
    print("%s is not an element id" % a.id)
else:
    for k in sorted(rec):
        print("%s.%s: %s" % (a.id, k, json.dumps(rec[k], ensure_ascii=False)))
print("findings.jsonl lines:", len(jl(os.path.join(OUT, "findings.jsonl"))))
