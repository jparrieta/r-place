#!/usr/bin/env python3
"""D5b, section 4: the dated changes in each branch's narrative (section 1 of forms/<id>-account.md).

Prints, per branch, every sentence of section 1 that names an hour by number, with the
rooms it names (r/<name>). Used to check each dated change against prior.md section 4's
brackets and the members' placements by hour.

    python3 out/_analysis/d5b_dated.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
B = [json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8") if l.strip()]
HOUR = re.compile(r"\b(hours?|h)\s?(\d{1,2}(\.\d+)?)\b", re.I)
for b in B:
    text = open(os.path.join(OUT, "forms", b["id"] + "-account.md"), encoding="utf-8").read()
    m = re.search(r"^## 1\..*?$(.*?)^## 2\.", text, re.S | re.M)
    sec = m.group(1) if m else ""
    sec = re.sub(r"\s+", " ", sec)
    sents = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'])", sec)
    hits = [s for s in sents if HOUR.search(s)]
    print("== %s (%d sentences with an hour)" % (b["id"], len(hits)))
    for s in hits:
        rooms = sorted(set(re.findall(r"r/([A-Za-z0-9_]+)", s)))
        print("- %s | rooms: %s" % (s.strip(), ", ".join(rooms)))
