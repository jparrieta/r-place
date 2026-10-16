#!/usr/bin/env python3
"""D3: one revision of one element or arrow of the model (stage D3 section 2). Rewrites one field of the entry in
model/elements.jsonl or model/arrows.jsonl (every other line unchanged, order kept) and appends one line to
model/history.jsonl: t, stage, leg, id, event, move, why, was (the whole entry before), adaptations (the ledger ids
that caused it), field and now (the new value). Refuses an unknown id, an unknown field, a move outside Grodal, Anteby
and Holm's eight, or an adaptation id the ledger lacks.

    python3 out/_analysis/d3_revise.py --id R01 --field statement --new "..." --move splitting --why "..." \
        --adaptations a,b,c --leg D3a-01 --event "statement revised" [--write]

Without --write it prints the history line and changes nothing.
"""
import argparse, datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
MD = os.path.join(OUT, "model")
MOVES = ("asking questions", "focusing on puzzles", "dropping", "merging", "splitting", "relating",
         "relating or contrasting", "sequencing", "developing or dropping working hypotheses")
FIELDS = ("statement", "range", "mechanism", "status", "bounded_by")

ap = argparse.ArgumentParser()
for k in ("id", "field", "new", "move", "why", "adaptations", "leg", "event"):
    ap.add_argument("--" + k, required=True)
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
if a.field not in FIELDS:
    sys.exit("field %r is not one of %s" % (a.field, FIELDS))
if a.move not in MOVES:
    sys.exit("move %r is not one of %s" % (a.move, MOVES))
ids = {json.loads(l)["id"] for l in open(os.path.join(OUT, "adaptations.jsonl"), encoding="utf-8") if l.strip()}
causes = [x for x in a.adaptations.split(",") if x]
miss = [x for x in causes if x not in ids]
if miss or not causes:
    sys.exit("adaptation ids not in the ledger: %s" % (miss or "none given"))
path = os.path.join(MD, "arrows.jsonl" if a.id.startswith("A") else "elements.jsonl")
rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
hit = [r for r in rows if r.get("id") == a.id]
if len(hit) != 1:
    sys.exit("%s holds %d entries with id %s" % (os.path.basename(path), len(hit), a.id))
was = json.loads(json.dumps(hit[0]))
new = json.loads(a.new) if a.field == "bounded_by" else a.new
hist = {"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "stage": "D3", "leg": a.leg,
        "id": a.id, "event": a.event, "move": a.move, "why": a.why, "field": a.field, "now": new, "was": was,
        "adaptations": causes}
print(json.dumps(hist, ensure_ascii=False, indent=1))
if not a.write:
    print("dry run: nothing written")
    sys.exit(0)
hit[0][a.field] = new
tmp = path + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
os.replace(tmp, path)
with open(os.path.join(MD, "history.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(hist, ensure_ascii=False) + "\n")
print("wrote %s %s and one history line" % (os.path.relpath(path, OUT), a.id))
