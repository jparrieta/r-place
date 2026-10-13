#!/usr/bin/env python3
"""C1: confirm gate pairs already read side by side, one `mem.py gates T3-a T3-b --confirm --reason ...` call each, so
gate_checks.jsonl is the tool's own. --pairs "T3-a|T3-b;T3-c|T3-d"; --reason the shared reason; --special a JSON object
{"T3-a|T3-b": "own reason"}. The tool refuses a pair with a one-way discriminator or an unanswered must_not_show; the
script stops at the first refusal.

    python3 out/_analysis/c1_confirm_pairs.py --pairs "..." --reason "..." [--special path.json]
"""
import argparse, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True); ap.add_argument("--reason", required=True); ap.add_argument("--special")
    a = ap.parse_args()
    spec = json.load(open(os.path.join(ROOT, a.special), encoding="utf-8")) if a.special else {}
    pairs = [p.strip() for p in a.pairs.split(";") if p.strip()]
    for p in spec:
        if p not in pairs:
            sys.exit("special pair %s is not in --pairs" % p)
    for p in pairs:
        x, y = p.split("|")
        r = subprocess.run([sys.executable, "-W", "ignore", os.path.join(ROOT, "tools", "mem.py"), "gates", x, y, "--confirm",
                            "--reason", spec.get(p, a.reason)], cwd=ROOT, capture_output=True, text=True)
        out = (r.stdout or "").strip().splitlines()
        if r.returncode != 0 or not out or not out[0].startswith("confirmed"):
            sys.exit("stopped at %s: %s %s" % (p, " ".join(out)[:300], (r.stderr or "").strip()[-300:]))
    print("confirmed %d pairs (%d with their own reason)" % (len(pairs), len(spec)))


if __name__ == "__main__":
    main()
