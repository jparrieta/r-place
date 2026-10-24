#!/usr/bin/env python3
"""D4: an amendment to the model after the D3 freeze (rule 11; J after the D3c interview, 24 Oct 13:39 Berlin).
One element or arrow, one or more field changes. The spec is a JSON file:
  {"id", "file": "elements"|"arrows", "move", "adaptations", "rooms",
   "changes": [{"field", "now", "event", "why", "new": true|false}, ...]}
Before writing it checks that the model hash is the version D3 froze (out/_closes/model-D3.sha256), or that every
history line since the freeze is a D4 amendment of this tool, so no other change rides along. Without --write it
prints each field before and after and writes nothing. With --write it replaces only that line of the model file
(every other line byte for byte) and appends one history line per change, in the form d3_revise_element.py and
d3_revise_arrow.py write (t, stage, leg, id, event, move, why, field, now, was, adaptations), plus "rooms",
"rechecked": false and "frozen_version" (the D3 hash). A field the record lacks is added only when the change says
"new": true. It prints the model hash before and after.

    python3 out/_analysis/d4_amend.py --spec out/_analysis/d4a01_amend_P05.json --leg D4a-01 [--write]
"""
import argparse, copy, datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib  # noqa: E402

HISTORY = os.path.join(OUT, "model", "history.jsonl")
MOVES = {"asking questions", "focusing on puzzles", "dropping", "merging", "splitting", "relating", "contrasting",
         "sequencing", "developing working hypotheses", "dropping working hypotheses"}
ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("--leg", required=True)
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
spec = json.load(open(a.spec, encoding="utf-8"))
for key in ("id", "file", "move", "adaptations", "rooms", "changes"):
    if key not in spec:
        sys.exit("spec lacks %s" % key)
if spec["move"] not in MOVES:
    sys.exit("move %r is not one of Grodal, Anteby and Holm's eight" % spec["move"])
if spec["file"] not in ("elements", "arrows"):
    sys.exit("file must be elements or arrows")
frozen = open(os.path.join(OUT, "_closes", "model-D3.sha256"), encoding="utf-8").read().strip()
h0 = vlib.model_hash(OUT)
hist = [json.loads(l) for l in open(HISTORY, encoding="utf-8") if l.strip()]
since = [h for h in hist if h.get("stage") == "D4"]
if h0 != frozen and not since:
    sys.exit("the model hash %s is not the D3 freeze %s, and no D4 amendment explains it" % (h0[:12], frozen[:12]))
if any(h.get("rechecked") is not False for h in since):
    sys.exit("a D4 history line is not an amendment of this tool")
path = os.path.join(OUT, "model", spec["file"] + ".jsonl")
lines = open(path, encoding="utf-8").read().splitlines()
hits = [i for i, ln in enumerate(lines) if ln.strip() and json.loads(ln).get("id") == spec["id"]]
if len(hits) != 1:
    sys.exit("%s: %d lines in %s" % (spec["id"], len(hits), path))
i = hits[0]
rec = json.loads(lines[i])
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
out_hist = []
for c in spec["changes"]:
    for key in ("field", "now", "event", "why"):
        if key not in c:
            sys.exit("change lacks %s" % key)
    if c["field"] not in rec and not c.get("new"):
        sys.exit("%s has no field %s, and the change does not say new" % (spec["id"], c["field"]))
    if c["field"] in rec and c.get("new"):
        sys.exit("%s already has field %s" % (spec["id"], c["field"]))
    was = copy.deepcopy(rec)
    print("%s.%s was: %s" % (spec["id"], c["field"], json.dumps(rec.get(c["field"]), ensure_ascii=False)))
    rec[c["field"]] = c["now"]
    print("%s.%s now: %s" % (spec["id"], c["field"], json.dumps(c["now"], ensure_ascii=False)))
    out_hist.append({"t": t, "stage": "D4", "leg": a.leg, "id": spec["id"], "event": c["event"],
                     "move": spec["move"], "why": c["why"], "field": c["field"], "now": c["now"], "was": was,
                     "adaptations": spec["adaptations"], "rooms": spec["rooms"], "rechecked": False,
                     "frozen_version": frozen})
if not a.write:
    print("dry run: nothing written; model hash %s (D3 freeze %s)" % (h0[:12], frozen[:12]))
    raise SystemExit(0)
lines[i] = json.dumps(rec, ensure_ascii=False)
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
with open(HISTORY, "a", encoding="utf-8") as f:
    for h in out_hist:
        f.write(json.dumps(h, ensure_ascii=False) + "\n")
h1 = vlib.model_hash(OUT)
n = sum(1 for l in open(HISTORY, encoding="utf-8") if l.strip())
print("rewrote %s in %s; appended %d history lines (history now %d); model hash %s -> %s; D3 freeze %s" % (
    spec["id"], os.path.relpath(path, ROOT), len(out_hist), n, h0[:12], h1[:12], frozen[:12]))
