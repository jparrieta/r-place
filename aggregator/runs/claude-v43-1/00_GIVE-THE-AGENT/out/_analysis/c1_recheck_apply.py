#!/usr/bin/env python3
"""C1: record the rechecks one gate change owes from a decisions file, one `mem.py recheck` call per item, so each
recheck is written and logged by the tool itself. The decisions file is a JSON list of
{"item": "<sub>:<tNN>", "reason": "...", "theme": "T3-a,T3-b", "codes": "T3-a=c1,c2;T3-b=c3"}; an entry without
"theme" is recorded unchanged, its themes and concepts copied from its line of assignments_final.jsonl in the
line's order (so nothing is typed twice). Refuses an item the change does not owe or has already rechecked. Stops at
the first refusal. Dry run without --write.

    python3 out/_analysis/c1_recheck_apply.py --change gate:2 --decisions out/_analysis/c1_rechecks/gate-2-decisions.json [--write]
"""
import argparse, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--change", required=True); ap.add_argument("--decisions", required=True)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true", help="run each recheck through mem.py --dry-run (validates the concepts, writes nothing)")
    a = ap.parse_args()
    o = next((x for x in vlib.owed_rechecks(OUT, "C1") if x["ref"] == a.change), None)
    if o is None:
        sys.exit("no change %s" % a.change)
    missing = {tuple(k) for k in o["missing"]}
    fin = {(r["sub"], r["theme_id"]): r for r in jl("assignments_final.jsonl")}
    dec = json.load(open(os.path.join(ROOT, a.decisions), encoding="utf-8"))
    calls, seen = [], set()
    for d in dec:
        sub, _, t = d["item"].partition(":")
        k = (sub, t)
        if k not in missing:
            sys.exit("%s is not owed by %s or is already rechecked" % (d["item"], a.change))
        if k in seen:
            sys.exit("%s twice in the decisions file" % d["item"])
        seen.add(k)
        if d.get("theme"):
            theme, codes = d["theme"], d["codes"]
        else:
            r = fin[k]
            ths = r.get("third_order") or []
            sup = r.get("support_by_theme") or {}
            theme = ",".join(ths)
            codes = ";".join("%s=%s" % (x, ",".join(sup.get(x) or [])) for x in ths)
        calls.append((d["item"], theme, codes, d["reason"]))
    left = sorted("%s:%s" % k for k in missing - seen)
    print("%s: %d decisions, %d owed items left without one%s" % (a.change, len(calls), len(left),
                                                                  (": " + ", ".join(left)) if left else ""))
    bad = 0
    for item, theme, codes, why in calls:
        if not a.write and not a.check:
            print("  would recheck %s --theme %s --codes %s" % (item, theme, codes))
            continue
        cmd = [sys.executable, "-W", "ignore", os.path.join(ROOT, "tools", "mem.py"), "recheck", item,
               "--change", a.change, "--theme", theme, "--codes", codes, "--reason", why]
        if a.check:
            cmd.append("--dry-run")
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        out = (p.stdout or "").strip().splitlines()
        ok = p.returncode == 0 and out and ("rechecked for" in out[0] or "dry run" in out[0])
        if a.check:
            if not ok:
                bad += 1
                print("  REFUSED %s: %s" % (item, " ".join(out)[:300] or (p.stderr or "").strip()[-300:]))
            continue
        print("  " + (out[0] if out else "(no output)"))
        if not ok:
            sys.exit("stopped at %s: %s" % (item, (p.stderr or "").strip()[-400:]))
    if a.check:
        print("checked %d: %d refused" % (len(calls), bad))


if __name__ == "__main__":
    main()
