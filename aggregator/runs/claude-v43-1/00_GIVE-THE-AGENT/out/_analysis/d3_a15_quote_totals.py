#!/usr/bin/env python3
"""D3a-42: totals of quoted segments and checked hours for A15's spec and row files, by running d3_spec_quotes.py,
d3_spec_hours.py and d3_trunc_check.py over each file with its quote files, the number of record posts fetched
through cite.py (blocks in d3_cites_A15_record_*.txt), and the census tags by kind across the A15-tags files.
Spec files that do not exist yet are skipped. Writes nothing.

  python3 out/_analysis/d3_a15_quote_totals.py
"""
import collections
import glob
import os
import subprocess
import sys

A = "out/_analysis/"
R = A + "d3_rulings/"
CITES = sorted(glob.glob(A + "d3_cites_A15_record_*.txt"))
SETS = {
    "instantiate": (R + "A15-inst-spec.txt", sorted(glob.glob(A + "d3_wq_A15_i*.txt")) + CITES),
    "re-rulings": (R + "A15-rerule-spec.txt", sorted(glob.glob(A + "d3_wq_A15_i*.txt")) + CITES),
    "restrict": (R + "A15-restrict-spec.txt", sorted(glob.glob(A + "d3_wq_A15_r*.txt")) + CITES),
    "add-condition": (R + "A15-addc-spec.txt", sorted(glob.glob(A + "d3_wq_A15_ac*.txt")) + CITES),
    "add-step": (R + "A15-adds-spec.txt", sorted(glob.glob(A + "d3_wq_A15_as*.txt")) + CITES),
    "absent rows": (R + "A15-absent-rows.txt", sorted(glob.glob(A + "d3_wq_A15_ab*.txt")) + CITES),
}


def run(script, spec, quotes):
    out = subprocess.run([sys.executable, A + script, "--spec", spec, "--quotes"] + quotes, capture_output=True,
                         text=True).stdout.strip().splitlines()
    return out[0] if out else "(no output)"


for name, (spec, quotes) in SETS.items():
    if not os.path.exists(spec):
        print("%-13s | not written yet" % name)
        continue
    print("%-13s | %s | %s | %s" % (name, run("d3_spec_quotes.py", spec, quotes), run("d3_spec_hours.py", spec, quotes),
                                   run("d3_trunc_check.py", spec, quotes)))
posts = sum(open(f, encoding="utf-8").read().count('"  [') for f in CITES)
print("record posts fetched through cite.py: %d in %d files" % (posts, len(CITES)))
tags = collections.defaultdict(set)
for f in glob.glob(R + "A15-tags-*.txt"):
    for l in open(f, encoding="utf-8"):
        if l.strip():
            i, t = l.strip().split("|")
            for k in t.split(","):
                tags[k].add(i)
print("tags: " + ", ".join("%s %d" % (k, len(v)) for k, v in sorted(tags.items())))
for k, v in sorted(tags.items()):
    print("  %s: %s" % (k, " ".join(sorted(v))))
