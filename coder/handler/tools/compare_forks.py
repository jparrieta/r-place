#!/usr/bin/env python3
"""compare_forks.py — set a room's run and its forks side by side.

    python3 _tools/compare_forks.py --room rooms/<sub> [names...]

Forks of a branch-B room share the pool (the fleet's codes are fixed at the snapshot), so what
differs is the lead's work: the themes, the verdict, the step-5 codes, the case. The table
prints, per run: verdict, codes (pool and step 5), themes, case.md words, sections present,
relations marked [crosses], and the theme labels. It does not say which fork is better; that is
a reading, and the carry rule (which fork the record keeps) is J's, declared before the forks
run, not chosen after.
"""
import argparse, glob, json, os, re, sys


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


def describe(run):
    d = {"run": run}
    rj = os.path.join(run, "out", "_run.json")
    r = json.load(open(rj)) if os.path.exists(rj) else {}
    d["verdict"] = r.get("verdict")
    codes = jl(os.path.join(run, "out", "codes.jsonl"))
    d["codes"] = len(codes)
    d["step5_codes"] = sum(1 for c in codes if c.get("minted_in_stage") == "step5_counter")
    themes = jl(os.path.join(run, "out", "themes.jsonl"))
    d["themes"] = len(themes)
    d["theme_labels"] = [t.get("second_order") for t in themes]
    case = os.path.join(run, "out", "case.md")
    s = open(case, encoding="utf-8").read() if os.path.exists(case) else ""
    d["case_words"] = len(s.split())
    d["crosses"] = len(re.findall(r"\[crosses", s))
    d["sections"] = [h for h in re.findall(r"^## (.+)$", s, re.M)]
    fj = os.path.join(os.path.dirname(run), "FORK.json")
    d["lineage"] = json.load(open(fj)) if os.path.exists(fj) else None
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--room", default=".")
    ap.add_argument("names", nargs="*")
    a = ap.parse_args()
    room = os.path.abspath(a.room)
    runs = [("run", os.path.join(room, "run"))]
    names = a.names or sorted(os.path.basename(p) for p in glob.glob(os.path.join(room, "forks", "*")))
    for n in names:
        runs.append((n, os.path.join(room, "forks", n, "run")))
    rows = [(n, describe(p)) for n, p in runs if os.path.exists(p)]
    keys = ["verdict", "codes", "step5_codes", "themes", "case_words", "crosses"]
    print("%-14s" % "" + "".join("%-14s" % n for n, _ in rows))
    for k in keys:
        print("%-14s" % k + "".join("%-14s" % str(d.get(k)) for _, d in rows))
    print()
    for n, d in rows:
        print("== %s: themes" % n)
        for t in d["theme_labels"]:
            print("   -", t)
    return 0


if __name__ == "__main__":
    sys.exit(main())
