#!/usr/bin/env python3
"""C5c-12: check that every quoted citation in a file ([sub/cNNNN], with optional more codes as 'cNNNN') resolves through
cite.py, and that the quoted words just before it occur in the cited passage (spaces and escapes ignored). Writes
nothing.

    python3 out/_analysis/c5c12_cite_check.py out/account.md
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
t = open(os.path.join(ROOT, sys.argv[1]), encoding="utf-8").read()
norm = lambda s: re.sub(r"[\s\\]+", " ", s).strip().lower()
bad, n = [], 0
for m in re.finditer(r'"([^"]{3,})" \[([A-Za-z0-9_]+)/(c\d{4})', t):
    words, sub, code = m.group(1), m.group(2), m.group(3)
    n += 1
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", sub, "--code", code, "--json"],
                       capture_output=True, text=True, cwd=ROOT)
    try:
        q = json.loads(p.stdout)["quotes"][0]["text"]
    except (ValueError, KeyError, IndexError):
        bad.append("%s/%s does not resolve" % (sub, code))
        continue
    if norm(words) not in norm(q):
        bad.append("%s/%s: %r not in %r" % (sub, code, words[:60], q[:80]))
print("quoted citations checked: %d; problems: %d" % (n, len(bad)))
for b in bad:
    print("  " + b)
