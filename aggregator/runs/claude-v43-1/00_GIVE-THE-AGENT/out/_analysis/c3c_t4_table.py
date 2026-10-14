#!/usr/bin/env python3
"""C3c: for each fourth-order theme, print what the mapping to the four universal problems needs, read from
structure-C3.md (the question it answers, its members with their names, the rooms carrying any member) and from
fourth/fourth.jsonl (dimension, in_model, declared). Reads my own files only; writes nothing.

    python3 out/_analysis/c3c_t4_table.py
"""
import json, os, re

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "out")
txt = open(os.path.join(OUT, "structure-C3.md"), encoding="utf-8").read()
t4 = [json.loads(l) for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"), encoding="utf-8")]
for r in t4:
    head = "### %s %s\n" % (r["id"], r["name"])
    i = txt.find(head)
    j = txt.find("\n### ", i + len(head))
    sec = txt[i:j if j > 0 else len(txt)]
    q = re.search(r"- \*\*The question it answers:\*\* (.*)", sec)
    m = re.search(r"- \*\*Members:\*\* (.*?)\. Rooms carrying any member: (\d+) of 705", sec)
    print("%s %s | %s | in_model %s | %s rooms" % (r["id"], r["name"], ",".join(r.get("dimension") or []),
                                                  r.get("in_model"), m.group(2) if m else "?"))
    print("   Q: %s" % (q.group(1) if q else "?"))
    print("   M: %s" % (m.group(1) if m else "?"))
