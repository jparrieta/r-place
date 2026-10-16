#!/usr/bin/env python3
"""D3, ruling rule G2: which absent lines on an element sit in rooms whose placements carry the element. Runs the
verbs themselves (mem.py rooms --with <T3> for each of the element's third-order themes, and mem.py adaptations
--element <id>), so every read is logged as the verbs log it; prints the absent lines in carrying rooms and the count
of the others. Writes nothing.

    python3 out/_analysis/d3_carried_absent.py --element R01 --themes T3-033,T3-092
"""
import argparse, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--themes", required=True)
a = ap.parse_args()


def verb(*args):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py")] + list(args), cwd=ROOT,
                       capture_output=True, text=True)
    return r.stdout.splitlines()


carry = set()
for t in a.themes.split(","):
    carry |= {l.strip() for l in verb("rooms", "--with", t, "--limit", "2000") if l.startswith("  ")}
lines = [l for l in verb("adaptations", "--element", a.element, "--limit", "5000") if " absent " in l]
hit = [l for l in lines if l.split()[0].rsplit("-", 1)[0] in carry]
print("%s: %d rooms carry it through %s; %d absent lines, %d of them in carrying rooms" % (
    a.element, len(carry), a.themes, len(lines), len(hit)))
for l in hit:
    print(l)
