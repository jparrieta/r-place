#!/usr/bin/env python3
"""C5a-03, stage C5 sections 4 and 5: reverse a C5 cut, setting one element back from 'candidate' to 'standing' when the
criterion written before pass 1 rejects the cut. The element keeps every field; `restored_at` and `restored_why` are
added, and one model/history.jsonl line records the old row as `was`. Refuses unless the element was cut at C5 and is
a candidate now.

    python3 out/_analysis/c5_restore.py ID "why the cut is reversed"
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
M = os.path.join(ROOT, "out", "model")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
eid, why = sys.argv[1], sys.argv[2]
ef, hf = os.path.join(M, "elements.jsonl"), os.path.join(M, "history.jsonl")
rows = [json.loads(l) for l in open(ef, encoding="utf-8") if l.strip()]
e = [r for r in rows if r["id"] == eid]
if len(e) != 1 or e[0].get("status") != "candidate" or not str(e[0].get("cut_at") or "").startswith("C5"):
    sys.exit("%s not found once, or not a candidate cut at C5" % eid)
was = dict(e[0])
e[0].update(status="standing", restored_at=LEG, restored_why=why)
with open(ef, "w", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
with open(hf, "a", encoding="utf-8") as f:
    f.write(json.dumps({"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "stage": "C5", "leg": LEG, "id": eid, "event": "restored (status candidate to standing)",
                        "move": "developing or dropping working hypotheses", "why": why, "was": was},
                       ensure_ascii=False) + "\n")
print("%s restored to standing; history line appended" % eid)
