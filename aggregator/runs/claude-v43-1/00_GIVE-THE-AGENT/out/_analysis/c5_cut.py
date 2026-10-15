#!/usr/bin/env python3
"""C5a-02, stage C5 section 4 (simplify, and say what it cost): cut one standing element from the model by changing
its status to 'candidate', the status the model gives an element with no grounded arrow (K03, K04, P19). The element
keeps its id and its fields; `cut_at` and `cut_cost` are added, and one model/history.jsonl line records the old row
as `was`. Refuses unless the element is standing and carries no arrow in the model.

    python3 out/_analysis/c5_cut.py ID "what it was doing and what the model can no longer account for"
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
M = os.path.join(ROOT, "out", "model")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
eid, cost = sys.argv[1], sys.argv[2]
ef, af, hf = (os.path.join(M, f) for f in ("elements.jsonl", "arrows.jsonl", "history.jsonl"))
arrows = [json.loads(l) for l in open(af, encoding="utf-8") if l.strip()]
if any(eid in (a.get("from"), a.get("to")) and a.get("status") != "tentative" for a in arrows):
    sys.exit("%s carries an arrow; not cut" % eid)
rows = [json.loads(l) for l in open(ef, encoding="utf-8") if l.strip()]
e = [r for r in rows if r["id"] == eid]
if len(e) != 1 or e[0].get("status") != "standing":
    sys.exit("%s not found once, or not standing" % eid)
was = dict(e[0])
e[0].update(status="candidate", cut_at=LEG, cut_cost=cost)
with open(ef, "w", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
with open(hf, "a", encoding="utf-8") as f:
    f.write(json.dumps({"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "stage": "C5", "leg": LEG, "id": eid, "event": "cut (status standing to candidate)",
                        "move": "dropping", "why": "stage C5 section 4: a standing element with no grounded arrow, "
                        "against the model's own rule that a process or condition enters only with one; " + cost,
                        "was": was}, ensure_ascii=False) + "\n")
print("%s cut to candidate; history line appended" % eid)
