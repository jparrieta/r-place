#!/usr/bin/env python3
"""D5, room-form accounts: one line of room-forms-D5.jsonl, modelled on branches-D5.jsonl. Counts come from the leg's
files; the judgements (status, bindings, result) are passed in. Prints the line.

    python3 out/_analysis/d5f_line.py --form A --judgement out/_analysis/d5a36_judgement.json >> out/room-forms-D5.jsonl
"""
import argparse, json, os, sys

ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
ap.add_argument("--judgement", required=True)
a = ap.parse_args()
sys.argv = [sys.argv[0]]
AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
sys.path.insert(0, os.path.join(os.path.dirname(OUT), "tools"))
import vlib  # noqa: E402

tag = {"A": "d5a36", "B": "d5a37", "C": "d5a38", "D": "d5a39", "E": "d5a40", "F": "d5a41"}[a.form]
J = lambda n: json.load(open(os.path.join(AN, "%s_%s.json" % (tag, n)), encoding="utf-8"))  # noqa: E731
facts, split, rs = J("facts"), J("split"), J("restrict_sorted")
jd = json.load(open(a.judgement, encoding="utf-8"))
form = {r["id"]: r for r in map(json.loads, open(os.path.join(OUT, "room-forms-D4a08c.jsonl"), encoding="utf-8"))}[a.form]
local = vlib.local_return_states(OUT)
statuses = {s: local.get(s, {}).get("local_status", "unresolved") for s in form["members"]}
over = [b["branch"] for b in facts["branches"] if b["ratio"] >= 1.5]
line = {
    "form": a.form, "leg": "D5a-%d" % (36 + "ABCDEF".index(a.form)), "name": facts["name"], "n": facts["n"],
    "n_defining": facts["n_def"], "thin": [x["sub"] for x in facts["thin"]], "core": [x["sub"] for x in facts["core"]],
    "account": "room-form-%s-account.md" % a.form,
    "verdicts": {k: facts["verdicts_all"].get(k, 0) for k in ("composes", "composes-with-residue", "does-not-compose", "cannot-tell")},
    "verdicts_defining": {k: facts["verdicts_def"].get(k, 0) for k in ("composes", "composes-with-residue", "does-not-compose", "cannot-tell")},
    "global_model_version": open(os.path.join(OUT, "handoff-D", "VERSION"), encoding="utf-8").read().strip().removeprefix("sha256:"),
    "local_model_version": vlib.model_hash(OUT), "local_statuses": statuses,
    "unresolved_members": sorted((s for s, st in statuses.items() if st != "validated"), key=str.lower),
    "change_signature_T4": facts["signature_T4"],
    "over": [r["t4"] for r in facts["themes_over"]], "under": [r["t4"] for r in facts["themes_under"]],
    "arrows_present": [], "arrows_absent": [],
    "arrows_not_testable": [{"arrow": x["arrow"], "expected": x["expected"]} for x in facts["arrows"] if x["expected"] < 1],
    "propositions_hold": [], "propositions_fail": [], "propositions_not_testable": [p["id"] for p in facts["propositions"]],
    "restrict_lines_on_arrows": {"lines": rs["lines"], "arrow_fails_here": rs["total"].get("F", 0),
                                 "record_cannot_show": rs["total"].get("R", 0), "both": rs["total"].get("B", 0),
                                 "neither": rs["total"].get("N", 0), "by_arrow": rs["by_arrow"]},
    "branches_leaning_here": over, "branches_none_here": [b["branch"] for b in facts["branches"] if b["in_form"] == 0],
    "rooms_in_no_branch": len(facts["no_branch"]),
    "split": [{"group": w["group"], "k": w["splits_at_k"], "reads": w["reads_as_split"],
               "parts": {p: v["defining"] for p, v in w["parts"].items()}} for w in split["walk"]],
    "representatives": {"best": [r["sub"] for r in facts["best"]], "least": facts["least"]["sub"], "read_at_length": facts["length"]["sub"]},
    "survival": {"median_organizing_end_hour": facts["survival"]["median_organizing_end_hour"],
                 "aftermath_share": facts["survival"]["aftermath_share"], "work_remained": facts["survival"]["work_remained"]},
    "canvas": {"used": False, "read": "not used in the room-form accounts; the canvas only where declared (rule 7)"},
}
line.update(jd)
print(json.dumps(line, ensure_ascii=False))
