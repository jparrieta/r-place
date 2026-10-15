#!/usr/bin/env python3
"""C5a-01, the declaration prose pass (rule in notes-C5.md): apply one theme's amended `prose`, `changed` and
`mistaken_for` from c5_prose_amend.json to fourth/fourth.jsonl, in place, and append one tier_history.jsonl line with
the old line as `was`, the move, the reason and the quotes the new text rests on. Names, members and the cut do not
change. Refuses if the theme already has a C5a-01 construct_amended line, if a field named in the spec is not in the
theme, or if the spec carries any other field.

    python3 out/_analysis/c5_prose_amend.py T4-xxx
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
FP, TH = os.path.join(OUT, "fourth", "fourth.jsonl"), os.path.join(OUT, "tier_history.jsonl")
spec = json.load(open(os.path.join(OUT, "_analysis", "c5_prose_amend.json"), encoding="utf-8"))
tid = sys.argv[1]
s = spec[tid]
FIELDS = ("prose", "changed", "mistaken_for")
if set(s["now"]) - set(FIELDS):
    sys.exit("%s: the spec names fields outside %s" % (tid, FIELDS))
hist = [json.loads(l) for l in open(TH, encoding="utf-8") if l.strip()]
if any(h.get("leg") == LEG and h.get("id") == tid and h.get("event") == "construct_amended" for h in hist):
    sys.exit("%s already has a %s construct_amended line" % (tid, LEG))
rows = [json.loads(l) for l in open(FP, encoding="utf-8") if l.strip()]
row = [r for r in rows if r["id"] == tid]
if len(row) != 1:
    sys.exit("%s not found once" % tid)
row = row[0]
was = dict(row)
for f, v in s["now"].items():
    if f not in row:
        sys.exit("%s has no field %s" % (tid, f))
    row[f] = v
with open(FP, "w", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
line = {"t": T, "stage": "C5", "leg": LEG, "tier": "fourth", "id": tid, "move": s["move"], "event": "construct_amended",
        "was": was, "now": [dict({"id": tid}, **s["now"])], "why": s["why"], "rule": "notes-C5.md, the declaration prose rule",
        "rests_on": s.get("rests_on", [])}
for k in ("literature", "abductive", "prompted_by"):
    if k in s:
        line[k] = s[k]
with open(TH, "a", encoding="utf-8") as f:
    f.write(json.dumps(line, ensure_ascii=False) + "\n")
print("%s amended (%s); tier_history line appended" % (tid, ", ".join(s["now"])))
