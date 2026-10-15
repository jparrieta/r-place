#!/usr/bin/env python3
"""C5a-01, rule 14: append a line superseding F-016, after the declaration prose pass removed the sentence on which
Completion ritual's by-construction mapping to reward rested. The mapping stays reward, by reading; the counts do not
change. Copies the last F-016 line, replaces the two words of the statement that changed, and records why. Refuses if
a C5a-01 line for F-016 exists.

    python3 out/_analysis/c5_f016_supersede.py
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = os.path.join(ROOT, "out", "findings.jsonl")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
if any(r["id"] == "F-016" and r.get("leg") == LEG for r in rows):
    sys.exit("a %s line for F-016 exists" % LEG)
last = [r for r in rows if r["id"] == "F-016"][-1]
old = "Reward provision: 2 (Completion ritual, by construction; Visibility returns)"
if old not in last["statement"]:
    sys.exit("the passage to change is not in F-016's statement")
new = dict(last)
new.update({
    "stage": "C5", "leg": LEG, "t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "statement": last["statement"].replace(old, "Reward provision: 2 (Completion ritual, by my reading of its credit "
                                                "acts since C5a-01, by construction before; Visibility returns)"),
    "supersedes": "F-016",
    "why": "rule 14: the declaration prose pass at C5a-01 removed 'the ritual pays the members whom no one could pay' "
           "from Completion ritual's declaration, on which its by-construction mapping to reward rested; the mapping "
           "line in mapping-C3.jsonl is amended to a mapping by reading (credit, own parts and prizes map nonmonetary "
           "rewards to members; celebration maps nothing), and no count changes",
})
with open(path, "a", encoding="utf-8") as f:
    f.write(json.dumps(new, ensure_ascii=False) + "\n")
print("F-016 superseded at %s" % LEG)
