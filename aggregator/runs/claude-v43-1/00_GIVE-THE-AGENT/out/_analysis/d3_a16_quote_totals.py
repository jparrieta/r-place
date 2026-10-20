#!/usr/bin/env python3
"""D3a-43: totals of quoted segments and checked hours for A16's spec and row files, each run against its own window's
quote file with d3_spec_quotes.py, d3_spec_hours.py and d3_trunc_check.py. Quotes and hours taken from posts above a
line's concepts (fetched with d3_cite_many.py and checked by eye against its output) show here as 'not found' and
'not in the quote files'. Writes nothing.

  python3 out/_analysis/d3_a16_quote_totals.py
"""
import re
import subprocess
import sys

A = "out/_analysis/"
R = A + "d3_rulings/"
SETS = {
    "instantiate": [("A16-inst-spec-%d.txt" % (n + 1), w) for n, w in enumerate(
        ("i357_000", "i357_026", "i357_052", "i357_078", "i457_000", "i457_026", "i457_052", "i457_078", "i557_000",
         "i557_019"))],
    "restrict": [("A16-restrict-spec-%d.txt" % (n + 1), w) for n, w in enumerate(
        ("r594_000", "r594_020", "r594_040", "r594_060", "r594_080", "r694_000"))],
    "add-condition": [("A16-addcond-spec.txt", "ac330")],
    "add-step": [("A16-addstep-spec.txt", "as347")],
    "absent rows": [("A16-absent-rows-%d.txt" % (n + 1), w) for n, w in enumerate(
        ("ab001_000", "ab001_034", "ab001_067", "ab101_000", "ab101_034", "ab101_067", "ab201_000", "ab201_034",
         "ab201_067", "ab301_000"))],
}


def nums(script, spec, quotes):
    out = subprocess.run([sys.executable, A + script, "--spec", spec, "--quotes", quotes], capture_output=True,
                         text=True).stdout
    return out


for name, parts in SETS.items():
    rows = seg = nf = hrs = mis = outside = cuts = 0
    for spec, w in parts:
        q = A + "d3_wq_A16_%s.txt" % w
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
