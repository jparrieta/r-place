#!/usr/bin/env python3
"""D5: build one branches-D5.jsonl line from the computed files (d5_line_fields, d5_arrows, d5_themes) and the
prose file, and append it unless the branch already has a line.

    python3 out/_analysis/d5_line.py --fields f.json --arrows a.json --themes t.json --prose p.json [--dry]
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
for k in ("fields", "arrows", "themes", "prose"):
    ap.add_argument("--" + k, required=True)
ap.add_argument("--dry", action="store_true")
a = ap.parse_args()
f, ar, th, pr = (json.load(open(p, encoding="utf-8")) for p in (a.fields, a.arrows, a.themes, a.prose))
assert f["branch"] == ar["branch"] == th["branch"]
present = [{"arrow": x["arrow"], "expected": x["expected"]} for x in ar["arrows"] if x["expected"] >= 1 and x["members_in_subs"]]
absent = [{"arrow": x["arrow"], "expected": x["expected"]} for x in ar["arrows"] if x["expected"] >= 1 and not x["members_in_subs"]]
nt = [{"arrow": x["arrow"], "expected": x["expected"]} for x in ar["arrows"] if x["expected"] < 1]
line = {"branch": f["branch"], "name": f["name"], "n": f["n"], "verdicts": f["verdicts"],
        "global_model_version": f["global_model_version"], "local_model_version": f["local_model_version"],
        "local_statuses": f["local_statuses"], "unresolved_members": f["unresolved_members"],
        "shared_status": pr["shared_status"], "shared_warrant": pr["shared_warrant"],
        "construct_bindings": pr["construct_bindings"], "binding_account": pr["binding_account"],
        "binds": pr["binds"], "leaves_free": pr["leaves_free"], "over": th["over"], "under": th["under"],
        "arrows_present": present, "arrows_absent": absent, "arrows_not_testable": nt,
        "propositions_hold": [], "propositions_fail": [],
        "propositions_not_testable": [p["id"] for p in ar["propositions"]],
        "survival": f["survival"],
        "canvas": dict(f["canvas"], read=pr["canvas_read"]),
        "unmodelled": pr["unmodelled"], "form_or_grouping": pr["form_or_grouping"], "confidence": pr["confidence"]}
if any(p["max_expected"] >= 1 for p in ar["propositions"]):
    sys.exit("a proposition reaches an expectation of one; decide hold or fail by reading, not by this script")
dest = os.path.join(OUT, "branches-D5.jsonl")
have = [json.loads(l)["branch"] for l in open(dest, encoding="utf-8") if l.strip()] if os.path.exists(dest) else []
print("branch %s; present %d, absent %d, not testable %d; over %s; under %d; already there: %s" % (
    line["branch"], len(present), len(absent), len(nt), line["over"], len(line["under"]), line["branch"] in have))
if a.dry or line["branch"] in have:
    sys.exit(0)
with open(dest, "a", encoding="utf-8") as fh:
    fh.write(json.dumps(line, ensure_ascii=False) + "\n")
print("appended to", dest)
