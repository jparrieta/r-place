#!/usr/bin/env python3
"""C1: move every placement a gate change's rechecks moved and assignments_final.jsonl does not yet carry, one
`mem.py reassign` call per item, with the recheck's own themes, concepts and reason (the reason names the gate and its
amended clause, as J's guard of 13 October asks). Dry run without --write.

    python3 out/_analysis/c1_reassign_from_rechecks.py --change gate:6 [--write]
"""
import argparse, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--change", required=True); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    fin = {(r["sub"], r["theme_id"]): r for r in jl("assignments_final.jsonl")}
    todo = []
    for r in jl("rechecks-C1.jsonl"):
        if r.get("change") != a.change or not r.get("changed"):
            continue
        k = (r["sub"], r["theme_id"])
        if list(fin[k].get("third_order") or []) == list(r["now"]):
            continue
        codes = ";".join("%s=%s" % (t, ",".join(r["support_by_theme"].get(t) or [])) for t in r["now"])
        why = r["why"] if r["why"].startswith(a.change) else "%s: %s" % (a.change, r["why"])
        todo.append(("%s:%s" % k, ",".join(r["now"]), codes, why, fin[k].get("third_order")))
    print("%s: %d moved rechecks not yet in assignments_final.jsonl" % (a.change, len(todo)))
    for item, theme, codes, why, was in todo:
        if not a.write:
            print("  would move %s from %s to %s" % (item, ",".join(was or []), theme))
            continue
        p = subprocess.run([sys.executable, "-W", "ignore", os.path.join(ROOT, "tools", "mem.py"), "reassign", item,
                            "--theme", theme, "--codes", codes, "--reason", why], cwd=ROOT, capture_output=True, text=True)
        out = (p.stdout or "").strip().splitlines()
        print("  " + (out[0] if out else "(no output)"))
        if p.returncode != 0 or not out or not out[0].startswith("moved"):
            sys.exit("stopped at %s: %s" % (item, (p.stderr or "").strip()[-400:]))


if __name__ == "__main__":
    main()
