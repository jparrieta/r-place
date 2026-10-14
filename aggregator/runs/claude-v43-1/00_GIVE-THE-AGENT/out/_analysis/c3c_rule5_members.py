#!/usr/bin/env python3
"""C3c: for each fourth-order theme mapped to one of the four universal problems in mapping-C3.jsonl, its members' rule
5 gate and carrier count (from structure-C3.md), one compact line per member, so part 2 of the four-problems section
reads the gates rather than types them. Members come from fourth/fourth.jsonl. Writes nothing.

    python3 out/_analysis/c3c_rule5_members.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
txt = open(os.path.join(OUT, "structure-C3.md"), encoding="utf-8").read()
t4 = {r["id"]: r for r in (json.loads(l) for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"), encoding="utf-8"))}
mp = [json.loads(l) for l in open(os.path.join(OUT, "mapping-C3.jsonl"), encoding="utf-8") if l.strip()]
for m in mp:
    if m["problem"] == "none":
        continue
    print("%s %s (%s)" % (m["fourth"], t4[m["fourth"]]["name"], m["problem"]))
    for t in t4[m["fourth"]]["members"]:
        s = re.search(r"^### %s (.+)$" % t, txt, re.M)
        j = txt.find("\n### ", s.end())
        g = re.search(r"Three numbers \(rule 5\), gate (\w+):\*\* carries (\d+); had the opportunity and does not (\d+); "
                      r"had no opportunity (\d+)", txt[s.end():j])
        print("   %s %-45s gate %-6s carries %3s, could and does not %3s, no opportunity %3s" % (
            t, s.group(1), g.group(1), g.group(2), g.group(3), g.group(4)))
