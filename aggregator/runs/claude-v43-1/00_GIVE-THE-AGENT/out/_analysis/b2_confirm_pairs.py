#!/usr/bin/env python3
"""B2: run `mem.py gates A B --confirm --reason R` for a list of pairs read in the session.

Usage: python3 out/_analysis/b2_confirm_pairs.py FILE    (FILE: JSON list of [A, B, reason])
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
bad = 0
for a, b, r in json.load(open(sys.argv[1], encoding="utf-8")):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "gates", a, b, "--confirm", "--reason", r],
                       capture_output=True, text=True)
    out = [l for l in (p.stdout + p.stderr).splitlines() if "Deprecation" not in l and "utcnow" not in l]
    if p.returncode != 0:
        bad += 1
        print("FAILED %s|%s: %s" % (a, b, " ".join(out)))
print("pairs %d, failed %d" % (len(json.load(open(sys.argv[1], encoding="utf-8"))), bad))
