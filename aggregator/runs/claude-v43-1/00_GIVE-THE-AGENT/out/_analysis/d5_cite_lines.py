#!/usr/bin/env python3
"""D5: run cite.py on every evidence code of a branch's key lines (a file from the keylines dump). Prints the quotes.

    python3 out/_analysis/d5_cite_lines.py out/_analysis/d5a11_F11_keylines.json [--subs a,b]
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
lines = json.load(open(sys.argv[1], encoding="utf-8"))
only = set(sys.argv[3].split(",")) if len(sys.argv) > 3 and sys.argv[2] == "--subs" else None
for l in sorted(lines, key=lambda x: x["sub"].lower()):
    if only and l["sub"] not in only:
        continue
    for c in l["evidence"].get("codes", []):
        r = subprocess.run([sys.executable, "-W", "ignore", os.path.join(ROOT, "tools", "cite.py"), "--room", l["sub"], "--code", c],
                           capture_output=True, text=True, cwd=ROOT)
        print("\n".join(x for x in r.stdout.splitlines() if x.startswith('"') or x.startswith("no ")))
