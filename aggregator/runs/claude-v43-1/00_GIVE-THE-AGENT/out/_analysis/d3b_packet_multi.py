#!/usr/bin/env python3
"""D3b: several small packets of flagged re-check absent lines in one file. For each element named, runs
d3b_packet.py (--op absent --ids recheck-absent-flagged2.jsonl --offset 0 --limit 100) into
d3b_pk_<element>_abs_000.txt and appends that packet to --out, so that a group of small elements is read whole in one
pass. Each element's packet keeps its own file name, which its rulings cite. Refuses an element with more than 100
unruled flagged lines (read it alone).

    python3 out/_analysis/d3b_packet_multi.py --elements P14,P29,P26 --out out/_analysis/d3b_pk_group_01.txt
"""
import argparse, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AN = os.path.join(ROOT, "out", "_analysis")
ap = argparse.ArgumentParser()
ap.add_argument("--elements", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--prefix", default="d3b_pk", help="packet name prefix; the second batch uses d3b2_pk")
ap.add_argument("--flagged", default="recheck-absent-flagged2.jsonl", help="the flagged list in d3_rulings/")
a = ap.parse_args()
if os.path.exists(a.out):
    sys.exit("refused: %s exists" % a.out)
parts = []
for e in a.elements.split(","):
    p = os.path.join(AN, "%s_%s_abs_000.txt" % (a.prefix, e))
    if os.path.exists(p):
        sys.exit("refused: %s exists; name the packet otherwise" % p)
    r = subprocess.run([sys.executable, os.path.join(AN, "d3b_packet.py"), "--element", e, "--op", "absent", "--ids",
                        os.path.join(AN, "d3_rulings", a.flagged), "--offset", "0", "--limit",
                        "100", "--out", p], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stdout + r.stderr)
    print(r.stdout.strip())
    if "(of " in r.stdout and int(r.stdout.rsplit("(of ", 1)[1].split(")")[0]) > 100:
        sys.exit("refused: %s has more than 100 lines; read it alone" % e)
    parts.append("######## %s (packet %s_%s_abs_000.txt)\n" % (e, a.prefix, e) + open(p, encoding="utf-8").read())
open(a.out, "w", encoding="utf-8").write("\n".join(parts))
print("wrote %s: %d packets" % (a.out, len(parts)))
