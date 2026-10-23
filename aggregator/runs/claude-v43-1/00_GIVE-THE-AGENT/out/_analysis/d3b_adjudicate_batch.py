#!/usr/bin/env python3
"""D3b: write one rulings file's lines to adjudications.jsonl (QD3-001), with the same checks as
d3_adjudicate_batch.py: the id is a ledger line (first return or re-check); the decision is one of DECISIONS; the
reason is not empty; the pair is a ledger id of another room; revised only with modify; kind one of the stage
check's kinds; no id twice in the file; no id already ruled (a re-ruling is written only by a file named
re-rule-*). Appends the verb's line format and logs one diary note with the file's name and its counts by decision
(the ids stay in the file and the ledger).

    python3 out/_analysis/d3b_adjudicate_batch.py --file out/_analysis/d3_rulings/recheck-repeat-01.jsonl [--write]
"""
import argparse, collections, datetime, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DECISIONS = ("accept", "modify", "reject", "particular", "pending")
KINDS = ("specification", "elaboration", "correction", "proposal", "particular", "none")
ap = argparse.ArgumentParser()
ap.add_argument("--file", required=True)
ap.add_argument("--write", action="store_true")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


led = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations.jsonl")) + jl(os.path.join(OUT, "adaptations-recheck.jsonl"))}
ruled = {r["adaptation"] for r in jl(os.path.join(OUT, "adjudications.jsonl"))}
rows = jl(a.file)
rerule = os.path.basename(a.file).startswith("re-rule-")
errs, seen = [], collections.Counter(r.get("adaptation") for r in rows)
for n, r in enumerate(rows, 1):
    i = r.get("adaptation")
    extra = set(r) - {"adaptation", "decision", "reason", "kind", "pair", "revised"}
    if extra:
        errs.append("line %d: fields beyond the ruling: %s" % (n, sorted(extra)))
    if i not in led:
        errs.append("line %d: no adaptation %r in the ledger" % (n, i))
    if seen[i] > 1:
        errs.append("line %d: %s ruled more than once in the file" % (n, i))
    if i in ruled and not rerule:
        errs.append("line %d: %s is already ruled; a re-ruling goes in a re-rule-* file" % (n, i))
    if r.get("decision") not in DECISIONS:
        errs.append("line %d (%s): no decision, or not one of %s" % (n, i, DECISIONS))
    if not str(r.get("reason") or "").strip():
        errs.append("line %d (%s): no reason" % (n, i))
    if r.get("kind") not in (None, "") and r["kind"] not in KINDS:
        errs.append("line %d (%s): kind %r is not one of %s" % (n, i, r["kind"], KINDS))
    p = r.get("pair")
    if p not in (None, ""):
        if p not in led:
            errs.append("line %d (%s): pair %r is not a ledger id" % (n, i, p))
        elif i in led and led[p]["sub"] == led[i]["sub"]:
            errs.append("line %d (%s): pair %s is a line of the same room" % (n, i, p))
    if r.get("revised") and r.get("decision") != "modify":
        errs.append("line %d (%s): revised on a decision that is not modify" % (n, i))
    if r.get("decision") == "modify" and not str(r.get("revised") or "").strip():
        errs.append("line %d (%s): modify without revised" % (n, i))
    if r.get("decision") == "accept" and i in led and led[i].get("portable") is False:
        errs.append("line %d (%s): accept on a line ingest marked portable false" % (n, i))
if errs or not rows:
    print("\n".join(errs[:40] or ["the file holds no ruling"]))
    sys.exit("refused: nothing written")
leg = open(os.path.join(ROOT, ".leg")).read().strip() if os.path.exists(os.path.join(ROOT, ".leg")) else "?"
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
out = [{"adaptation": r["adaptation"], "decision": r["decision"], "reason": r["reason"], "revised": r.get("revised"),
        "pair": r.get("pair"), "kind": r.get("kind"), "t": t, "stage": "D3", "leg": leg} for r in rows]
counts = collections.Counter(r["decision"] for r in rows)
print("%s: %d rulings checked; %s; leg %s" % (os.path.basename(a.file), len(rows), dict(counts), leg))
if not a.write:
    print("dry run: nothing written")
    sys.exit(0)
with open(os.path.join(OUT, "adjudications.jsonl"), "a", encoding="utf-8") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
note = "adjudicated %d re-check lines from %s: %s (ids in the file and the ledger)" % (
    len(rows), os.path.relpath(a.file, OUT), ", ".join("%s %d" % kv for kv in sorted(counts.items())))
subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "log", note, "--kind", "note"], cwd=ROOT,
               check=True, capture_output=True)
n = sum(1 for _ in open(os.path.join(OUT, "adjudications.jsonl"), encoding="utf-8"))
print("appended %d lines; adjudications.jsonl now %d lines; one diary note" % (len(rows), n))
