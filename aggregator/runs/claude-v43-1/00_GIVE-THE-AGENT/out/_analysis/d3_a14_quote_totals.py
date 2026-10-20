#!/usr/bin/env python3
"""D3a-41: totals of quoted segments and checked hours for A14's spec and row files, by running d3_spec_quotes.py,
d3_spec_hours.py and d3_trunc_check.py over each file with its quote files, and the number of record posts fetched
through cite.py (blocks in d3_cites_A14_record_*.txt). Writes nothing.

  python3 out/_analysis/d3_a14_quote_totals.py
"""
import glob
import subprocess
import sys

A = "out/_analysis/"
R = A + "d3_rulings/"
CITES = sorted(glob.glob(A + "d3_cites_A14_record_*.txt"))
SETS = {
    "instantiate": (R + "A14-inst-spec.txt", sorted(glob.glob(A + "d3_wq_A14_i*.txt")) + CITES),
    "restrict": (R + "A14-restrict-spec.txt", sorted(glob.glob(A + "d3_wq_A14_r*.txt")) + CITES),
    "add-condition": (R + "A14-addc-spec.txt", [A + "d3_wq_A14_ac323.txt", A + "d3_wq_A14_i442_000.txt",
                                                 A + "d3_wq_A14_i442_060.txt"]),
    "add-step": (R + "A14-adds-spec.txt", [A + "d3_wq_A14_as339.txt"]),
    "absent rows": (R + "A14-absent-rows.txt", sorted(glob.glob(A + "d3_wq_A14_ab*.txt"))),
}


def run(script, spec, quotes):
    out = subprocess.run([sys.executable, A + script, "--spec", spec, "--quotes"] + quotes, capture_output=True,
                         text=True).stdout.strip().splitlines()
    return out[0] if out else "(no output)"


for name, (spec, quotes) in SETS.items():
    print("%-13s | %s | %s | %s" % (name, run("d3_spec_quotes.py", spec, quotes), run("d3_spec_hours.py", spec, quotes),
                                   run("d3_trunc_check.py", spec, quotes)))
posts = sum(open(f, encoding="utf-8").read().count('"  [') for f in CITES)
print("record posts fetched through cite.py: %d in %d files" % (posts, len(CITES)))
