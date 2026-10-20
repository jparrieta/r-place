#!/usr/bin/env python3
"""D3a-46: totals of quoted segments and checked hours for A19's current spec and row files (the instantiate spec, the
restrict spec v4 and the add-condition spec v2, which carry the re-rulings, and the joined absent rows), each run with
d3_spec_quotes.py, d3_spec_hours.py, d3_trunc_check.py and d3_a16_seg_gap.py against its own windows' quote files and
A19's cites files (posts above a line's concepts, fetched with d3_cite_many.py). Writes nothing.

  python3 out/_analysis/d3_a19_quote_totals.py
"""
import glob
import re
import subprocess
import sys

A = "out/_analysis/"
R = A + "d3_rulings/"
CITES = sorted(glob.glob(A + "d3_cites_A19_*.txt"))
SETS = {
    "instantiate": ("A19-inst-spec.txt", "d3_wq_A19_i487_*.txt"),
    "restrict": ("A19-restrict-spec-v4.txt", "d3_wq_A19_r556_*.txt"),
    "add-condition": ("A19-addcond-spec-v2.txt", "d3_wq_A19_ac478*.txt"),
    "absent rows": ("A19-absent-rows.txt", "d3_wq_A19_ab*.txt"),
}


def run(script, spec, quotes):
    return subprocess.run([sys.executable, A + script, "--spec", spec, "--quotes"] + quotes, capture_output=True,
                          text=True).stdout


print("cites files:", len(CITES))
for name, (spec, pat) in SETS.items():
    wins = sorted(glob.glob(A + pat))
    q = wins + CITES
    o1 = run("d3_spec_quotes.py", R + spec, q)
    m1 = re.search(r"(\d+) lines, (\d+) quoted segments, (\d+) not found", o1)
    o2 = run("d3_spec_hours.py", R + spec, q)
    m2 = re.search(r"matching: (\d+); mismatches: (\d+); hours for concepts not in the quote files: (\d+)", o2)
    o3 = run("d3_trunc_check.py", R + spec, q)
    m3 = re.search(r"followed by a letter: (\d+)", o3)
    # d3_a16_seg_gap.py takes one quote file; its count of segments the quote check does not read is the spec's own
    o4 = run("d3_a16_seg_gap.py", R + spec, wins[:1])
    m4 = re.search(r"segments the quote check does not read: (\d+)", o4)
    print("%-13s | %d windows | %s rows | %s segments, %s not found | %s hours matching, %s mismatches, %s not in the "
          "files | cuts %s | segments the quote check does not read %s" % (
              name, len(wins), m1.group(1), m1.group(2), m1.group(3), m2.group(1), m2.group(2), m2.group(3),
              m3.group(1), m4.group(1) if m4 else "?"))
