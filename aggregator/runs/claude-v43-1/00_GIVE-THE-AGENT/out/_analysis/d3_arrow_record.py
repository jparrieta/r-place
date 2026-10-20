#!/usr/bin/env python3
"""D3a-44, read-only: print one arrow's whole record from out/model/arrows.jsonl, every model history line that names
it (by its id in any field), and the names and glosses of its two elements from out/model/elements.jsonl.

  python3 out/_analysis/d3_arrow_record.py A17
"""
import json
import sys

aid = sys.argv[1]
arrows = {json.loads(l)["id"]: json.loads(l) for l in open("out/model/arrows.jsonl", encoding="utf-8") if l.strip()}
els = {json.loads(l)["id"]: json.loads(l) for l in open("out/model/elements.jsonl", encoding="utf-8") if l.strip()}
r = arrows[aid]
print("===== %s %s -> %s" % (aid, r.get("from"), r.get("to")))
for k, v in r.items():
    print("  %s: %s" % (k, v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)))
for e in (r.get("from"), r.get("to")):
    x = els.get(e, {})
    print("  element %s: name %s; status %s; gloss %s" % (e, x.get("name"), x.get("status"), x.get("gloss")))
print("history lines naming %s:" % aid)
for n, l in enumerate(open("out/model/history.jsonl", encoding="utf-8"), 1):
    h = json.loads(l)
    if aid in json.dumps(h, ensure_ascii=False):
        print("  line %d: %s" % (n, json.dumps(h, ensure_ascii=False)))
