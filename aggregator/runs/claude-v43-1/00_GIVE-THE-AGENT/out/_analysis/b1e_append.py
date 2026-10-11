#!/usr/bin/env python3
"""B1e: append files, in order, to a target file; print the target's lines before and after.

Usage: python3 out/_analysis/b1e_append.py <target> <source> [<source> ...]
"""
import sys

target, sources = sys.argv[1], sys.argv[2:]
with open(target, encoding="utf-8") as f:
    before = f.read()
add = ""
for s in sources:
    with open(s, encoding="utf-8") as f:
        t = f.read()
    add += t if t.endswith("\n") else t + "\n"
with open(target, "a", encoding="utf-8") as f:
    if not before.endswith("\n"):
        f.write("\n")
    f.write(add)
with open(target, encoding="utf-8") as f:
    after = f.read()
print("%s: %d lines before, %d after (%d bytes added)" % (target, before.count("\n"), after.count("\n"), len(after.encode()) - len(before.encode())))
