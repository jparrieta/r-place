#!/usr/bin/env python3
"""C4: coded records whose words or label match a pattern, inside an hour window, from the store through
`mem.py codes --grep <re> --json`. Prints the count of records and rooms in the window and, for up to N records drawn
with seed 20261015, room/code, hour, the first-order label, the third-order theme where `mem.py` gives it, and the
words whole. For checking whether my rooms could answer a field mechanism, and for choosing quotes to serve through
cite.py. Writes nothing.

    python3 out/_analysis/c4_grep_hours.py "<re>" [--from H] [--to H] [--n N]
"""
import argparse, json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser()
ap.add_argument("pattern")
ap.add_argument("--from", dest="lo", type=float, default=-1e9)
ap.add_argument("--to", dest="hi", type=float, default=1e9)
ap.add_argument("--n", type=int, default=12)
a = ap.parse_args()
recs, off = [], 0
while True:
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", a.pattern, "--json",
                        "--offset", str(off), "--limit", "1000"], cwd=ROOT, capture_output=True, text=True)
    got = [json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")]
    recs += got
    if len(got) < 1000:
        break
    off += 1000
inw = [r for r in recs if r.get("hour") is not None and a.lo <= r["hour"] < a.hi]
print("matches %d records; in window [%s, %s): %d records in %d rooms" % (
    len(recs), a.lo, a.hi, len(inw), len({r["sub"] for r in inw})))
for r in random.Random(20261015).sample(inw, min(a.n, len(inw))):
    print("  %s/%s h%.2f [%s] %s" % (r["sub"], r["code_id"], r["hour"], r["first_order"], r["text"].replace("\n", " ")))
