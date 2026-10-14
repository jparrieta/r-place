#!/usr/bin/env python3
"""C3c: for given third-order themes, each carrying room's first coded hour under the theme (from `mem.py codes --third
<id> --json`, field hour), with the quartiles and how many rooms first carry it before hour 24, 48 and 73. Tests
prior.md's "Votes and polls will be rare and late" and similar claims of timing. Writes nothing.

    python3 out/_analysis/c3c_hours.py T3-xxx [T3-yyy ...]
"""
import json, os, statistics, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
allfirst = []
for t in sys.argv[1:]:
    recs, off = [], 0
    while True:
        p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--third", t, "--json",
                            "--offset", str(off), "--limit", "500"], cwd=ROOT, capture_output=True, text=True)
        got = [json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")]
        recs += got
        if len(got) < 500:
            break
        off += 500
    first = {}
    [first.__setitem__(r["sub"], min(first.get(r["sub"], 1e9), r["hour"])) for r in recs if r.get("hour") is not None]
    h = sorted(first.values())
    allfirst += h
    if not h:
        print("%s: no records" % t)
        continue
    q = statistics.quantiles(h, n=4) if len(h) > 1 else [h[0]] * 3
    print("%s: %d records, %d rooms; first hour quartiles %.1f / %.1f / %.1f; first before h24 %d, h48 %d, h73 %d" % (
        t, len(recs), len(h), q[0], q[1], q[2], sum(x < 24 for x in h), sum(x < 48 for x in h),
        sum(x < 73 for x in h)))
