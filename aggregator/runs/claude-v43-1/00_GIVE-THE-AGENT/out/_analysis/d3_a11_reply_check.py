#!/usr/bin/env python3
"""D3a-38: G43 reading 4's check on every A11 line ruled as the transition (instantiate T and TO, restrict S-T and
S-TO, absent rejects). For each line, the cited concepts' threads and hours come from the quote files; each thread's
reply tree comes from `mem.py forest <room> <thread>` (Dewey paths and authors). A pair of cited concepts, a earlier
and b later in one thread, is linked when b's item replies under a's item, when they are the same item, when one
member wrote both, or when a is the submission itself. The script lists the lines with no linked pair, for a second
reading. Writes nothing.

  python3 out/_analysis/d3_a11_reply_check.py
"""
import glob
import json
import re
import subprocess
import sys

R = "out/_analysis/d3_rulings/"
QL = re.compile(r'^\s*".*"  \[([^/\]]+)/(c\d{4})\]  item \S+  thread (\S+)  h\+(\d+\.\d+)')
pos = {}
for f in (glob.glob("out/_analysis/d3_wq_A11_*.txt") + glob.glob("out/_analysis/d3_absent_cites_A11_*.txt")):
    for line in open(f, encoding="utf-8"):
        m = QL.match(line)
        if m:
            pos[(m.group(1), m.group(2))] = (m.group(3), float(m.group(4)))

lines = {}
for name, keep in (("A11-inst-spec.txt", ("T", "TO")), ("A11-restrict-spec.txt", ("S-T", "S-TO"))):
    for l in open(R + name, encoding="utf-8"):
        if l.strip():
            aid, cls, ev = l.rstrip("\n").split("|", 2)
            if cls in keep:
                lines[aid] = sorted(set(re.findall(r"\b(c\d{4})\b", ev)))
for l in open(R + "A11-absent.jsonl"):
    r = json.loads(l)
    if r["decision"] == "reject":
        lines[r["adaptation"]] = sorted(set(re.findall(r"\b(c\d{4})\b", r["reason"])))

ITEM = re.compile(r"\[([0-9.]+)\] (?:OP )?\(([^ |)]+)[^>]*-> \[([^\]]*)\]")
trees = {}


def tree(room, thread):
    key = (room, thread)
    if key not in trees:
        out = subprocess.run([sys.executable, "tools/mem.py", "forest", room, thread], capture_output=True,
                             text=True).stdout
        t = {}
        for line in out.splitlines():
            m = ITEM.search(line)
            if m:
                for c in re.findall(r"c\d{4}", m.group(3)):
                    t[c] = (m.group(1), m.group(2))
        trees[key] = t
    return trees[key]


def linked(pa, pb):
    (da, ua), (db, ub) = pa, pb
    return da == "0" or db == da or db.startswith(da + ".") or ua == ub


flag = []
for aid in sorted(lines):
    room = aid.rsplit("-", 1)[0]
    cs = [(c, pos[(room, c)]) for c in lines[aid] if (room, c) in pos]
    ok = False
    for a, (ta, ha) in cs:
        for b, (tb, hb) in cs:
            if a != b and ta == tb and ha <= hb:
                t = tree(room, ta)
                if a in t and b in t and linked(t[a], t[b]):
                    ok = True
    if not ok:
        flag.append(aid)
print("transition lines checked: %d; with no linked pair of cited concepts: %d" % (len(lines), len(flag)))
for aid in flag:
    print("  " + aid)
