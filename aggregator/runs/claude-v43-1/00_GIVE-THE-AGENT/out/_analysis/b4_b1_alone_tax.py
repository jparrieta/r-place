#!/usr/bin/env python3
"""Read-only. Taxonomy of past rulings that hold no reader's theme, and of unresolved rulings, by class.

Prints counts and up to three examples per (kind, class, taxonomy), so a new ruling can follow precedent.
"""
import json
import collections

rows = [json.loads(x) for x in open("out/disagreements.jsonl")]
tab = collections.defaultdict(list)
for d in rows:
    readers = set(d["readers"][0]) | set(d["readers"][1])
    rul = set(d["ruling"])
    if d.get("unresolved"):
        kind = "unresolved"
    elif rul and not (rul & readers):
        kind = "no-reader-theme"
    else:
        continue
    tab[(kind, d.get("class"), d["taxonomy"])].append(d)
for key in sorted(tab, key=lambda k: (k[0], str(k[1]), k[2])):
    items = tab[key]
    print(key[0], "class", key[1], key[2], len(items))
    for d in items[:3]:
        print("   ", d["sub"], d["theme_id"], "packet", d.get("packet"), "field", d.get("field"), "theme", d.get("theme"), "|", d["why"][:300])
