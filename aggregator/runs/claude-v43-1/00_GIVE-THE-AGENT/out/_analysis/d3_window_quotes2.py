#!/usr/bin/env python3
"""D3: version 2 of d3_window_quotes.py (D3a-31), with --op, so restrict, contradict and add lines can be read with
their cited concepts whole. Runs the verbs itself (mem.py adaptations --element <id> --offset --limit for the packet;
cite.py --room --code for each cited concept), so every read is logged as the verbs log it. Prints the page's lines of
the given op in the verb's order, from index --start to --stop within them, each with its cited concepts whole.
Writes nothing.

    python3 out/_analysis/d3_window_quotes2.py --element A04 --op restrict --offset 498 --limit 100 --start 0 --stop 25
"""
import argparse, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--op", required=True)
ap.add_argument("--offset", type=int, required=True)
ap.add_argument("--limit", type=int, required=True)
ap.add_argument("--start", type=int, default=0)
ap.add_argument("--stop", type=int, default=20)
a = ap.parse_args()


def run(*args):
    r = subprocess.run([sys.executable] + list(args), cwd=ROOT, capture_output=True, text=True)
    return r.stdout.splitlines()


page = run(os.path.join(ROOT, "tools", "mem.py"), "adaptations", "--element", a.element, "--offset", str(a.offset),
           "--limit", str(a.limit))
rows = [l for l in page if (" %s " % a.op) in l]
part = rows[a.start:a.stop]
print("%s page offset %d: %d %s lines; printing %d to %d in the verb's order" % (
    a.element, a.offset, len(rows), a.op, a.start, a.start + len(part)))
for i, l in enumerate(part, a.start):
    lid = l.split()[0]
    sub = lid.rsplit("-", 1)[0]
    codes = re.findall(r"c\d{4}", l.rsplit("[", 1)[-1])
    print("\n[%d] %s" % (i, l))
    for c in codes:
        q = run(os.path.join(ROOT, "tools", "cite.py"), "--room", sub, "--code", c)
        print("   " + (q[0] if q else "(no quote) %s/%s" % (sub, c)))
