#!/usr/bin/env python3
"""D3a-39: one reading window for an arrow's lines: runs d3_window_quotes2.py (the verb's page, each line with its
cited concepts whole, every read logged by the verbs) and d3_reply_context.py on its output, and writes one file that
gives each line's block followed by its reply context. The quote window is kept too, for the quote and hour checks.

  python3 out/_analysis/d3_read_window.py --element A12 --op instantiate --offset 190 --limit 100 --start 0 --stop 50 \
      --tag i190_000
writes out/_analysis/d3_wq_A12_i190_000.txt and out/_analysis/d3_rw_A12_i190_000.txt
"""
import argparse
import re
import subprocess
import sys

ap = argparse.ArgumentParser()
for k in ("--element", "--op", "--tag"):
    ap.add_argument(k, required=True)
for k in ("--offset", "--limit", "--start", "--stop"):
    ap.add_argument(k, type=int, required=True)
a = ap.parse_args()
wq = "out/_analysis/d3_wq_%s_%s.txt" % (a.element, a.tag)
rw = "out/_analysis/d3_rw_%s_%s.txt" % (a.element, a.tag)
out = subprocess.run([sys.executable, "out/_analysis/d3_window_quotes2.py", "--element", a.element, "--op", a.op,
                      "--offset", str(a.offset), "--limit", str(a.limit), "--start", str(a.start), "--stop",
                      str(a.stop)], capture_output=True, text=True).stdout
open(wq, "w", encoding="utf-8").write(out)
ctx = subprocess.run([sys.executable, "out/_analysis/d3_reply_context.py", wq], capture_output=True, text=True).stdout
blocks = {}
for blk in ctx.split("== ")[1:]:
    aid = blk.split("\n", 1)[0].strip()
    blocks[aid] = blk.split("\n", 1)[1] if "\n" in blk else ""
HEAD = re.compile(r"^(?:\[\d+\] )?(\S+-\d{3})\s+%s\s" % re.escape(a.op))
res, cur, n = [], None, 0
for l in out.splitlines():
    m = HEAD.match(l)
    if m:
        if cur:
            res.append("  -- reply context\n" + blocks.get(cur, "  (none)\n"))
        cur = m.group(1)
        n += 1
    res.append(l)
if cur:
    res.append("  -- reply context\n" + blocks.get(cur, "  (none)\n"))
open(rw, "w", encoding="utf-8").write("\n".join(res) + "\n")
print("%s: %d lines; wrote %s and %s" % (a.tag, n, wq, rw))
