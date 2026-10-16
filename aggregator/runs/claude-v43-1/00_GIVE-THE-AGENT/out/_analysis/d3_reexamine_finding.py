#!/usr/bin/env python3
"""D3: re-examine a finding under rule 14 when an element it touches is revised (stage D3 section 2). Appends to
out/findings.jsonl a new line for the finding: the latest line for the id copied whole, with stage D3, the leg, a new
time, supersedes the bare id, and the re-examination's result added to why. Optionally replaces the statement or the
bound when the re-examination changes them. Never edits an existing line.

    python3 out/_analysis/d3_reexamine_finding.py --id F-017 --leg D3a-01 --note "..." [--statement "..."] \
        [--bound "..."] [--write]
"""
import argparse, datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, "out", "findings.jsonl")

ap = argparse.ArgumentParser()
ap.add_argument("--id", required=True)
ap.add_argument("--leg", required=True)
ap.add_argument("--note", required=True)
ap.add_argument("--statement")
ap.add_argument("--bound")
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
rows = [json.loads(l) for l in open(P, encoding="utf-8") if l.strip()]
hit = [r for r in rows if r.get("id") == a.id]
if not hit:
    sys.exit("no finding %s" % a.id)
new = json.loads(json.dumps(hit[-1]))
new.update({"stage": "D3", "leg": a.leg, "t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "supersedes": a.id})
new["why"] = "%s Re-examined at %s (rule 14): %s" % (new.get("why") or "", a.leg, a.note)
if a.statement:
    new["statement"] = a.statement
if a.bound:
    new["bound"] = a.bound
print(json.dumps({k: new[k] for k in ("id", "stage", "leg", "supersedes", "status")}, ensure_ascii=False))
print("why ends: ..." + new["why"][-400:])
if a.write:
    with open(P, "a", encoding="utf-8") as f:
        f.write(json.dumps(new, ensure_ascii=False) + "\n")
    print("appended; findings.jsonl holds %d lines" % (len(rows) + 1))
else:
    print("dry run: nothing written")
