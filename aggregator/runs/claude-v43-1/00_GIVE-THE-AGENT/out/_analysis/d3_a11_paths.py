#!/usr/bin/env python3
"""D3a-38: print, for named A11 lines, each cited concept's thread, hour, forest path and author, read from the quote
files and `mem.py forest` as d3_a11_reply_check3.py reads them. Writes nothing.

  python3 out/_analysis/d3_a11_paths.py giantbomb-013 drugs-010
"""
import importlib.util
import re
import sys

spec = importlib.util.spec_from_file_location("rc3", "out/_analysis/d3_a11_reply_check3.py")
sys.argv, args = sys.argv[:1], sys.argv[1:]
src = open("out/_analysis/d3_a11_reply_check3.py", encoding="utf-8").read()
src = src.split("flag, how = ")[0]
ns = {}
exec(compile(src, "d3_a11_reply_check3.py", "exec"), ns)
for aid in args:
    room = aid.rsplit("-", 1)[0]
    ev = ns["text"].get(aid)
    if ev is None:
        print(aid, "not a transition line")
        continue
    cited = sorted(set(re.findall(r"\bc\d{4}\b", ev)))
    ans, how = ns["answer_of"](ev, cited, room)
    print("%s answer %s (%s)" % (aid, ans, how))
    for c in cited:
        if (room, c) not in ns["pos"]:
            print("  %s not placed" % c)
            continue
        th, h = ns["pos"][(room, c)]
        t = ns["tree"](room, th)
        d, u = t.get(c, ("?", "?"))
        print("  %s thread %s h+%.2f path %s author %s" % (c, th, h, d, u))
