#!/usr/bin/env python3
"""D3: print one arrow of the model whole (every field), the two elements it joins in brief, and every
model/history.jsonl line that names it, for the drift rule's re-orientation and an arrow's G rule. Writes nothing.

  python3 out/_analysis/d3_arrow_full.py A12
"""
import json
import sys

aid = sys.argv[1]
arrows = [json.loads(l) for l in open("out/model/arrows.jsonl", encoding="utf-8") if l.strip()]
els = {e["id"]: e for e in (json.loads(l) for l in open("out/model/elements.jsonl", encoding="utf-8") if l.strip())}
a = next(x for x in arrows if x["id"] == aid)
print(json.dumps(a, ensure_ascii=False, indent=1))
for k in ("from", "to"):
    e = els.get(a.get(k))
    if e:
        print("%s %s [%s, %s]: %s" % (k, e["id"], e.get("tier", e.get("kind", "")), e.get("status", ""),
                                     e.get("statement", e.get("name", ""))))
print("history lines naming %s:" % aid)
for n, l in enumerate(open("out/model/history.jsonl", encoding="utf-8"), 1):
    if aid in l:
        h = json.loads(l)
        print("  line %d: %s" % (n, json.dumps(h, ensure_ascii=False)))
