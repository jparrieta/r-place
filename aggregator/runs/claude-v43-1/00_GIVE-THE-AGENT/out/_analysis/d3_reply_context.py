#!/usr/bin/env python3
"""D3a-39: the reply context of each line in a quote window (d3_window_quotes2.py or d3_sample_packet.py output), so
G43 reading 4 and G44's pair can be read from the first ruling. For each line, each cited concept is printed with its
hour, its forest path and author, and its parent item (path, author, and the parent's codes with their labels, or
'na' where the parent carries no code); the submission's codes are printed once per thread. Forests come from
`mem.py forest <room> <thread>` (logged as the verb logs it), each forest line read by its last '-> [' so a flair
holding '>' does not break the parse. A cited concept that replies under another cited concept's item, by another
author, is marked 'replies under cNNNN'; one by the same author is marked 'same author as cNNNN'. Writes nothing.

  python3 out/_analysis/d3_reply_context.py out/_analysis/d3_wq_A12_i190_000.txt
"""
import re
import subprocess
import sys

HEAD = re.compile(r"^(?:\[\d+\] )?(\S+-\d{3})\s+(\S+)\s")
QL = re.compile(r'^\s+".*"  \[([^/\]]+)/(c\d{4})\]  item (\S+)  thread (\S+)  h\+(\d+\.\d+)')
lines, order = {}, []
for l in open(sys.argv[1], encoding="utf-8"):
    m = HEAD.match(l)
    if m and m.group(2) in ("instantiate", "restrict", "absent", "add-condition", "add-step", "contradict", "link"):
        cur = m.group(1)
        order.append(cur)
        lines[cur] = []
        continue
    q = QL.match(l)
    if q and order:
        lines[order[-1]].append((q.group(1), q.group(2), q.group(4), float(q.group(5))))

forests = {}


def forest(room, thread):
    if (room, thread) not in forests:
        # the verb pages at 80 lines by default; the whole thread is read here (D3a-39 fix), since a later page's
        # items would otherwise look absent from the forest
        out = subprocess.run([sys.executable, "tools/mem.py", "forest", room, thread, "--limit", "100000"],
                             capture_output=True, text=True).stdout
        by_code, by_path = {}, {}
        for fl in out.splitlines():
            m = re.search(r"\[([0-9.]+)\] (OP )?\(([^ |)]+)", fl)
            k = fl.rfind("-> [")
            if not (m and k >= 0):
                continue
            j = fl.find("]", k)
            codes = re.findall(r"c\d{4}", fl[k:j])
            labels = [x.strip() for x in fl[j + 1:].split(" | ")] if j > 0 else []
            path, author = m.group(1), m.group(3)
            by_path[path] = (author, list(zip(codes, labels)) if len(labels) == len(codes) else [(c, "") for c in codes])
            for c in codes:
                by_code[c] = (path, author)
        forests[(room, thread)] = (by_code, by_path)
    return forests[(room, thread)]


def parent(p):
    if p == "0":
        return None
    return p.rsplit(".", 1)[0] if "." in p else "0"


def show(path, by_path):
    if path is None or path not in by_path:
        return "none" if path is None else "%s (outside the coded record)" % path
    au, cl = by_path[path]
    return "%s (%s) %s" % (path, au, "; ".join("%s %s" % x for x in cl) or "na")


for aid in order:
    print("== " + aid)
    room = aid.rsplit("-", 1)[0]
    cited = lines[aid]
    seen_sub = set()
    for r, c, th, h in cited:
        by_code, by_path = forest(r, th)
        if c not in by_code:
            print("  %s h+%.2f thread %s: not in the forest" % (c, h, th))
            continue
        p, au = by_code[c]
        marks = []
        for r2, c2, th2, h2 in cited:
            if c2 == c or th2 != th or c2 not in by_code:
                continue
            p2, au2 = by_code[c2]
            if p != p2 and (p.startswith(p2 + ".") or (p2 == "0" and p != "0")):
                marks.append(("replies under %s" if au != au2 else "same author as %s (under)") % c2)
            elif au == au2 and p != p2:
                marks.append("same author as %s" % c2)
            elif p == p2:
                marks.append("one item with %s" % c2)
        print("  %s h+%.2f thread %s path %s (%s)%s" % (c, h, th, p, au, ("  [" + ", ".join(marks) + "]") if marks else ""))
        print("      parent: %s" % show(parent(p), by_path))
        if th not in seen_sub and p != "0" and "0" in by_path:
            seen_sub.add(th)
            print("      submission: %s" % show("0", by_path))
