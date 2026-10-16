#!/usr/bin/env python3
"""D3, ruling rule G1b: the seeded check of a packet of instantiate lines. Runs the verbs itself (mem.py adaptations
--element <id> --offset --limit for the packet; cite.py --room --code for each cited concept of the drawn lines), so
every read is logged as the verbs log it. Draws K instantiate lines of the packet by random.Random(SEED + offset) over
their ids in the verb's order and prints each line with its cited concepts whole. Writes nothing.

    python3 out/_analysis/d3_sample_packet.py --element R01 --offset 113 --limit 100 [--k 10] [--seed 20261016]
"""
import argparse, os, random, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--offset", type=int, required=True)
ap.add_argument("--limit", type=int, required=True)
ap.add_argument("--k", type=int, default=10)
ap.add_argument("--seed", type=int, default=20261016)
a = ap.parse_args()


def run(*args):
    r = subprocess.run([sys.executable] + list(args), cwd=ROOT, capture_output=True, text=True)
    return r.stdout.splitlines()


page = run(os.path.join(ROOT, "tools", "mem.py"), "adaptations", "--element", a.element, "--offset", str(a.offset),
           "--limit", str(a.limit))
inst = [l for l in page if " instantiate " in l]
rng = random.Random(a.seed + a.offset)
draw = rng.sample(inst, min(a.k, len(inst)))
print("%s packet offset %d: %d instantiate lines; drawn %d by seed %d+%d" % (
    a.element, a.offset, len(inst), len(draw), a.seed, a.offset))
for l in draw:
    lid = l.split()[0]
    sub = lid.rsplit("-", 1)[0]
    codes = re.findall(r"c\d{4}", l.rsplit("[", 1)[-1])
    print("\n" + l)
    for c in codes:
        q = run(os.path.join(ROOT, "tools", "cite.py"), "--room", sub, "--code", c)
        print("   " + (q[0] if q else "(no quote) %s/%s" % (sub, c)))
