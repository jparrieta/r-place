#!/usr/bin/env python3
"""D3a-44: totals of quoted segments and checked hours for A17's spec and row files, each run against its own window's
quote file with d3_spec_quotes.py, d3_spec_hours.py and d3_trunc_check.py. Quotes and hours taken from posts above a
line's concepts, or from another window (fetched with d3_cite_many.py, or read in that window, and checked in their
own runs), show here as 'not found' and 'outside the window'. Writes nothing.

  python3 out/_analysis/d3_a17_quote_totals.py
"""
import re
import subprocess
import sys

A = "out/_analysis/"
R = A + "d3_rulings/"
SETS = {
    "instantiate": [("A17-inst-spec-%d.txt" % (n + 1), w) for n, w in enumerate(
        ("i432_000", "i432_026", "i432_052", "i432_078", "i532_000", "i532_028"))],
    "restrict": [("A17-restrict-spec-%d.txt" % (n + 1), w) for n, w in enumerate(
        ("r588_000", "r588_016", "r588_032", "r588_048"))],
    "add-condition": [("A17-addcond-spec.txt", "ac423")],
    "add-step": [("A17-addstep-spec.txt", "as430")],
    "absent rows": [("A17-absent-rows-%d.txt" % (n + 1), w) for n, w in enumerate(
        ("ab001_000", "ab001_034", "ab001_067", "ab101_000", "ab101_034", "ab101_067", "ab201_000", "ab201_034",
         "ab201_067", "ab301_000", "ab301_034", "ab301_067", "ab401_000"))],
}


def nums(script, spec, quotes):
    return subprocess.run([sys.executable, A + script, "--spec", spec, "--quotes", quotes], capture_output=True,
                          text=True).stdout


for name, parts in SETS.items():
    rows = seg = nf = hrs = mis = outside = cuts = 0
    for spec, w in parts:
        q = A + "d3_wq_A17_%s.txt" % w
        o1 = nums("d3_spec_quotes.py", R + spec, q)
        m = re.search(r"(\d+) lines, (\d+) quoted segments, (\d+) not found", o1)
        rows += int(m.group(1)); seg += int(m.group(2)); nf += int(m.group(3))
        o2 = nums("d3_spec_hours.py", R + spec, q)
        m = re.search(r"matching: (\d+); mismatches: (\d+); hours for concepts not in the quote files: (\d+)", o2)
        hrs += int(m.group(1)); mis += int(m.group(2)); outside += int(m.group(3))
        o3 = nums("d3_trunc_check.py", R + spec, q)
        m = re.search(r"followed by a letter: (\d+)", o3)
        cuts += int(m.group(1))
    print("%-13s | %d windows | %d rows | %d segments, %d not found in the window | %d hours matching, %d mismatches, "
          "%d outside the window | cuts %d" % (name, len(parts), rows, seg, nf, hrs, mis, outside, cuts))
