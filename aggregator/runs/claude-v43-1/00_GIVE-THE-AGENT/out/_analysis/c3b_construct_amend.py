#!/usr/bin/env python3
"""C3b, stage C3 section 6: amend two fourth-order construct blocks where the shelf shows a construct each may be
mistaken for. fourth/fourth.jsonl is edited in place (its `mistaken_for` field only); each superseded line goes to
tier_history.jsonl as `was`, with the move, the work and one clause of reason. The third-order tier does not change.
Refuses to run if either theme already has a C3b tier_history line.

    python3 out/_analysis/c3b_construct_amend.py
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
FP = os.path.join(OUT, "fourth", "fourth.jsonl")
TH = os.path.join(OUT, "tier_history.jsonl")
ADD = {
    "T4-007": ("Puranam, Alexy and Reitzig 2014",
               " Also the transparent task architecture of open source and Wikipedia (Puranam, Alexy and Reitzig 2014, "
               "verified, pp. 172-173), where the final product 'is its own representation' and a visible task structure "
               "lets contributors choose their part. There a founder or a core lays out the architecture; here no one "
               "does, and the half-built picture itself shows what is missing.",
               "the shelf names coordination through the visible work as transparency of task architecture, a construct "
               "this one could be mistaken for"),
    "T4-011": ("O'Mahony and Ferraro 2007",
               " Also a shared basis of authority (O'Mahony and Ferraro 2007, verified, p. 1081), which a community must "
               "establish before it can govern itself. A decided element here is a leader named or a vote taken for one "
               "work within hours; a shared basis of authority is a lasting consensus on who may decide. Only the small "
               "canvas-born factions come near one (F-006, bounded at C3a).",
               "the shelf names a shared basis of authority, a construct this one could be mistaken for, and C3a bounded "
               "its finding"),
}
hist = [json.loads(l) for l in open(TH, encoding="utf-8") if l.strip()]
if any(h.get("leg") == LEG and h.get("id") in ADD for h in hist):
    sys.exit("a %s tier_history line exists for %s; not written again" % (LEG, ", ".join(ADD)))
rows = [json.loads(l) for l in open(FP, encoding="utf-8") if l.strip()]
new_hist = []
for r in rows:
    if r["id"] in ADD:
        work, add, why = ADD[r["id"]]
        was = dict(r)
        r["mistaken_for"] = (r.get("mistaken_for") or "").rstrip() + add
        new_hist.append({"t": T, "stage": "C3", "leg": LEG, "tier": "fourth", "id": r["id"],
                         "move": "relating or contrasting", "event": "construct_amended", "was": was,
                         "now": [{"id": r["id"], "mistaken_for": r["mistaken_for"]}], "why": why,
                         "literature": [work], "prompted_by": work})
if len(new_hist) != len(ADD):
    sys.exit("not every theme was found")
with open(FP, "w", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
with open(TH, "a", encoding="utf-8") as f:
    f.write("".join(json.dumps(h, ensure_ascii=False) + "\n" for h in new_hist))
print("amended: %s; tier_history lines appended: %d" % (", ".join(h["id"] for h in new_hist), len(new_hist)))
