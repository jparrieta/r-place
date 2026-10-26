#!/usr/bin/env python3
"""D5b: print the held proposals (QD4-001) in full, copied from tree-D4.md's section, for appending
to a D5b file with >>. The text is copied, not retyped.

    python3 out/_analysis/d5b_held.py >> out/waterfall-D5.md
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
lines = open(os.path.join(ROOT, "out", "tree-D4.md"), encoding="utf-8").read().split("\n")
start = next(i for i, l in enumerate(lines) if l.startswith("## The held proposals"))
end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("## "))
body = lines[start + 1:end]
print("## The held proposals (QD4-001; never served, not re-checked)")
print()
print("Copied in full from `tree-D4.md`, section \"The held proposals\". Neither proposal is part of the model the walk used.")
print("\n".join(body).rstrip())
