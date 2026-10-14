#!/usr/bin/env python3
"""C2d-02: the size of each pass 5 story room's page (--no-canvas) and forest, in lines and bytes, so each read can be
paged under the output limit. Reads story_rooms-p5.jsonl line 1; reads no verdicts.

    python3 out/_analysis/c2d2_room_sizes.py
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
draw = json.loads(open(os.path.join(ROOT, "out", "story_rooms-p5.jsonl"), encoding="utf-8").readline())["draw"]


def run(args):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py")] + args + ["--limit", "100000"], cwd=ROOT,
                       capture_output=True, text=True)
    return p.stdout


tot = 0
for d in draw:
    s = d["sub"]
    r = run(["room", s, "--no-canvas"])
    f = run(["forest", s])
    tot += len(f.encode())
    print("%-22s room %5d lines %7d bytes | forest %5d lines %8d bytes" % (s, len(r.splitlines()), len(r.encode()),
                                                                          len(f.splitlines()), len(f.encode())))
print("forest bytes in all: %d" % tot)
