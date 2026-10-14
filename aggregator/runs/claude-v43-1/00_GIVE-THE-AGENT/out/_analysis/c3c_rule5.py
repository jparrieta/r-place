#!/usr/bin/env python3
"""C3c: rule 5's three numbers and gate for given themes (third or fourth order), read from each theme's section in
structure-C3.md, so part 2 of the four-problems section quotes them rather than types them. Writes nothing.

    python3 out/_analysis/c3c_rule5.py T4-xxx [T3-yyy ...]
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
txt = open(os.path.join(ROOT, "out", "structure-C3.md"), encoding="utf-8").read()
for t in sys.argv[1:]:
    m = re.search(r"^### %s (.+)$" % t, txt, re.M)
    if not m:
        print("%s: no section" % t)
        continue
    j = txt.find("\n### ", m.end())
    sec = txt[m.end():j if j > 0 else len(txt)]
    lines = [l for l in sec.splitlines() if "rule 5" in l or "Three numbers" in l]
    print("%s %s: %s" % (t, m.group(1), " | ".join(lines) if lines else "no rule 5 line"))
