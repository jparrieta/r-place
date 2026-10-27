#!/usr/bin/env python3
"""D6a-04: run tools/cite.py on every evidence code of the given fractal lines (jsonl files) and print one line per
room:code, the quote line found or NOT FOUND, then a count. cite.py logs each read as usual.

    python3 out/_analysis/d6a04_codes_check.py out/_analysis/d6a04_D04_formlines.jsonl out/_analysis/d6a04_D04_branchlines.jsonl
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
pairs = []
for path in sys.argv[1:]:
    for raw in open(path, encoding="utf-8"):
        line = json.loads(raw)
        for c in line["evidence"].get("codes", []):
            room, code = c.split(":")
            if (room, code) not in pairs:
                pairs.append((room, code))
found = 0
for room, code in pairs:
    r = subprocess.run([sys.executable, "-W", "ignore", os.path.join(ROOT, "tools", "cite.py"), "--room", room, "--code", code],
                       capture_output=True, text=True, cwd=ROOT)
    hits = [l for l in r.stdout.splitlines() if "[%s/%s]" % (room, code) in l]
    if hits:
        found += 1
        print("OK %s:%s %s" % (room, code, hits[0]))
    else:
        print("NOT FOUND %s:%s %s" % (room, code, r.stdout.strip()[-200:]))
print("END %d of %d codes resolve" % (found, len(pairs)))
