#!/usr/bin/env python3
"""C3a: plan whole-work reads of one shelf work in pages under the output limit. Serves the work once through mem.py
(logged there) with --limit 100000, measures each line's bytes, and prints offset/limit pairs whose pages stay under
--max bytes (default 26000). Prints no text of the work.

    python3 out/_analysis/c3a_shelf_pages.py felin-zenger-2017 [--max 26000]
"""
import argparse, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser()
ap.add_argument("name")
ap.add_argument("--max", type=int, default=26000)
a = ap.parse_args()
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "shelf", a.name, "--limit", "100000"],
                   cwd=ROOT, capture_output=True, text=True)
lines = [l for l in p.stdout.splitlines() if not l.startswith("[end:")]
pages, start, size = [], 0, 0
for i, l in enumerate(lines):
    b = len(l.encode()) + 1
    if size + b > a.max and i > start:
        pages.append((start, i - start, size))
        start, size = i, 0
    size += b
pages.append((start, len(lines) - start, size))
print("%s: %d lines, %d bytes, %d pages" % (a.name, len(lines), sum(s for _, _, s in pages), len(pages)))
print(" ".join("%d:%d" % (o, n) for o, n, _ in pages))
