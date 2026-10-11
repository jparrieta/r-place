#!/usr/bin/env python3
"""Wait until out/rechecks-B2.jsonl has at least N lines, or until M seconds pass; print the count.

Usage: python3 out/_analysis/b2_wait.py N [M]
"""
import os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
p = os.path.join(ROOT, "out", "rechecks-B2.jsonl")
n, m = int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 540
t0 = time.time()
while True:
    c = sum(1 for _ in open(p, encoding="utf-8"))
    if c >= n or time.time() - t0 > m:
        print("%d lines after %d s" % (c, time.time() - t0))
        break
    time.sleep(15)
