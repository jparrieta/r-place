#!/usr/bin/env python3
"""C1: amend one entry of a theme's discriminators without retyping the rest. Reads the theme's current list from
scheme_v2.jsonl, replaces the question of the entry against --vs (or adds the entry when absent), and records the
change through `mem.py gate T3-NNN --field discriminators --now <the whole list> --reason ...`, so gate_history.jsonl
and the rechecks are the tool's own. Dry run (prints the old and new entry) without --write.

    python3 out/_analysis/c1_gate_disc.py --theme T3-002 --vs T3-084 --question "..." --reason "..." [--write]
"""
import argparse, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def main():
    ap = argparse.ArgumentParser()
    for x in ("--theme", "--vs", "--question", "--reason"):
        ap.add_argument(x, required=True)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    row = next((json.loads(x) for x in open(os.path.join(OUT, "scheme_v2.jsonl"), encoding="utf-8")
                if x.strip() and json.loads(x)["id"] == a.theme), None)
    if row is None:
        sys.exit("no %s in scheme_v2.jsonl" % a.theme)
    lst = [dict(d) for d in (row.get("discriminators") or [])]
    hit = [d for d in lst if d.get("vs") == a.vs]
    print("%s against %s, was: %s" % (a.theme, a.vs, hit[0]["question"] if hit else "(none)"))
    if hit:
        hit[0]["question"] = a.question
    else:
        lst.append({"vs": a.vs, "question": a.question})
    print("%s against %s, now: %s" % (a.theme, a.vs, a.question))
    if not a.write:
        return
    p = subprocess.run([sys.executable, "-W", "ignore", os.path.join(ROOT, "tools", "mem.py"), "gate", a.theme,
                        "--field", "discriminators", "--now", json.dumps(lst, ensure_ascii=False), "--reason", a.reason],
                       cwd=ROOT, capture_output=True, text=True)
    print((p.stdout or "").strip())
    if p.returncode != 0:
        sys.exit((p.stderr or "").strip()[-400:])


if __name__ == "__main__":
    main()
