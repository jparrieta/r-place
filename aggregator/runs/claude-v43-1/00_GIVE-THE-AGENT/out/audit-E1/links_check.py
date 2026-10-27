#!/usr/bin/env python3
"""E1 section 1, logs against claims: every id in the head, the questions and the views resolves through links.py.

    python3 out/audit-E1/links_check.py > out/audit-E1/links_check.txt

Runs tools/links.py over the folder as it stands (the head, _questions/*.md and _views/), then validate.py --links,
and prints both outputs whole with their exit codes. Nothing is written elsewhere.
"""
import os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for cmd in (["tools/links.py", "--root", ".", "--out", "out"], ["tools/validate.py", "--links"]):
    r = subprocess.run([sys.executable] + cmd, cwd=ROOT, capture_output=True, text=True)
    print("$ python3 %s\nexit %d" % (" ".join(cmd), r.returncode))
    print(r.stdout.strip())
    err = "\n".join(l for l in r.stderr.splitlines() if "Deprecation" not in l and "utcnow" not in l)
    if err.strip():
        print("stderr:", err.strip())
    print()
