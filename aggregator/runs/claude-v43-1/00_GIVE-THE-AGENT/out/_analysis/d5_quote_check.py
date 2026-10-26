#!/usr/bin/env python3
"""D5: check an account's parts before assembly: every r/ name is an analysed room (case-sensitive, 'place' excepted),
and every quote directly before a [sub/cNNNN] citation is a substring of that code's words, read through cite.py.

    python3 out/_analysis/d5_quote_check.py part1.md part2.md ...
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
subs = {json.loads(l)["sub"] for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8")}
text = "".join(open(p, encoding="utf-8").read() for p in sys.argv[1:])
bad_rooms = sorted({m for m in re.findall(r"\br/([A-Za-z0-9_]+)", text) if m != "place" and m not in subs})
print("rooms not analysed:", bad_rooms)
cache, bad, n = {}, [], 0
for q, s, c in re.findall(r'"([^"]+)"\s*\[([A-Za-z0-9_]+)/(c\d{3,5})\]', text):
    n += 1
    if (s, c) not in cache:
        r = subprocess.run([sys.executable, "-W", "ignore", os.path.join(ROOT, "tools", "cite.py"), "--room", s, "--code", c],
                           capture_output=True, text=True, cwd=ROOT)
        line = next((x for x in r.stdout.splitlines() if x.startswith('"')), "")
        cache[(s, c)] = line[1:line.rfind('"  [')] if line else None
    words = cache[(s, c)]
    if words is None or q not in words:
        bad.append((s, c, q[:60], (words or "NO CODE")[:80]))
print("quotes checked:", n, "not verbatim:", len(bad))
for b in bad:
    print(b)
