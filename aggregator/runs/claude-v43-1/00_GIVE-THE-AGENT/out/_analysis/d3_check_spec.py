#!/usr/bin/env python3
"""D3a-48: run the four checks and the counts on one spec or rows file, in the order the legs run them by hand:
d3_spec_quotes.py and d3_spec_hours.py and d3_trunc_check.py against all the quote files given, d3_a16_seg_gap.py
against the first (it takes one), then d3_spec_counts.py with the tag file if one is given. Prints each helper's output
as it is. Writes nothing.

  python3 out/_analysis/d3_check_spec.py --spec S --quotes WQ [CITES ...] [--tags T]
"""
import argparse
import subprocess
import sys

A = "out/_analysis/"
ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("--quotes", nargs="+", required=True)
ap.add_argument("--tags", default="")
ap.add_argument("--window", default="", help="a reading window (d3_rw_*): its line ids must equal the spec's ids")
a = ap.parse_args()
if a.window:
    import re
    win = re.findall(r"^\[\d+\] (\S+-\d{3})\s", open(a.window, encoding="utf-8").read(), re.M)
    rows = [l.split("|", 1)[0] for l in open(a.spec, encoding="utf-8") if l.strip()]
    print("window lines %d; spec rows %d; missing from the spec: %s; not in the window: %s" % (
        len(win), len(rows), [i for i in win if i not in rows] or "none", [i for i in rows if i not in win] or "none"))
runs = [["d3_spec_quotes.py", "--spec", a.spec, "--quotes"] + a.quotes,
        ["d3_spec_hours.py", "--spec", a.spec, "--quotes"] + a.quotes,
        ["d3_trunc_check.py", "--spec", a.spec, "--quotes"] + a.quotes,
        ["d3_a16_seg_gap.py", "--spec", a.spec, "--quotes", a.quotes[0]],
        ["d3_spec_counts.py", "--spec", a.spec] + (["--tags", a.tags] if a.tags else [])]
for r in runs:
    out = subprocess.run([sys.executable, A + r[0]] + r[1:], capture_output=True, text=True)
    sys.stdout.write(out.stdout)
    if out.returncode:
        sys.stdout.write(out.stderr)
        sys.exit("%s failed" % r[0])
