#!/usr/bin/env python3
"""Run b1_multiplace_write4.py with one --bag argument per line of a bag file (supersedes
b1_bags_from_file.py, which ran write3 and so repeated its per-row mem.py calls).

usage: b1_bags_from_file2.py <tsv> <leg> <bagfile> [--write]
Each non-empty line of <bagfile> is one bag spec, "sub:tNN:T3-kept:T3-a,T3-b:why".
"""
import os
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
tsv, leg, bagfile = sys.argv[1], sys.argv[2], sys.argv[3]
cmd = [sys.executable, os.path.join(here, "b1_multiplace_write4.py"), tsv, "--leg", leg]
with open(bagfile) as f:
    for line in f:
        line = line.strip()
        if line:
            cmd += ["--bag", line]
cmd += sys.argv[4:]
sys.exit(subprocess.call(cmd))
