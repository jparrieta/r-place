#!/usr/bin/env python3
"""D3a-38: G43 reading 4's check, version 2. Version 1 (d3_a11_reply_check.py) passed a line when any pair of its
cited concepts was reply-linked, so a line whose layout answered another post could pass (giantbomb-013), and it
lost items whose author flair holds a '>'. This version reads each forest line by its last '-> [' and pairs only an
earlier concept whose label does not read as a layout with a later concept whose label does (a layout, coordinates,
a pointer, a request for one), in one thread. A pair is linked when the later item replies under the earlier one,
one member wrote both, or the earlier one is the submission. A later item that is a top-level comment is listed apart,
since whether it does what the talk asked must be read. Labels come from the A11 packets and the absent cites.
Writes nothing.

  python3 out/_analysis/d3_a11_reply_check2.py
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
labels = {}
for f in glob.glob("out/_analysis/d3_pk_A11_*.txt"):
    for blk in open(f, encoding="utf-8").read().split("\n== ")[1:]:
        room = blk.split("\n", 1)[0].split()[0].rsplit("-", 1)[0]
        m = re.search(r"codes: (.*)", blk)
        if m:
            for c, lab in re.findall(r"(c\d{4}) (.*?)(?=; c\d{4} |$)", m.group(1)):
                labels[(room, c)] = lab
LAY = re.compile(r"template|layout|grid|mock|sketch|blueprint|schematic|overlay|pattern|guide|reference|plan\b|"
                 r"design (link|image)|image|picture|map|coordinat|location|link|draft|version|png|sprite|target|"
                 r"where to|the spot|chart", re.I)

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

trees = {}


def tree(room, thread):
    if (room, thread) not in trees:
        out = subprocess.run([sys.executable, "tools/mem.py", "forest", room, thread], capture_output=True,
                             text=True).stdout
        t = {}
        for line in out.splitlines():
            m = re.search(r"\[([0-9.]+)\] (OP )?\(([^ |)]+)", line)
            k = line.rfind("-> [")
            if m and k >= 0:
                for c in re.findall(r"c\d{4}", line[k:]):
                    t[c] = (m.group(1), m.group(3))
        trees[(room, thread)] = t
    return trees[(room, thread)]


none, toplevel = [], []
for aid in sorted(lines):
    room = aid.rsplit("-", 1)[0]
    cs = [(c, pos[(room, c)]) for c in lines[aid] if (room, c) in pos]
    linked_pair, top_pair = False, []
    for a, (ta, ha) in cs:
        if LAY.search(labels.get((room, a), "")):
            continue
        for b, (tb, hb) in cs:
            if b == a or tb != ta or hb < ha or not LAY.search(labels.get((room, b), "")):
                continue
            t = tree(room, ta)
            if a not in t or b not in t:
                continue
            (da, ua), (db, ub) = t[a], t[b]
            if da == "0" or db == da or db.startswith(da + ".") or ua == ub:
                linked_pair = True
            elif "." not in db:
                top_pair.append("%s->%s" % (a, b))
    if not linked_pair:
        (toplevel if top_pair else none).append((aid, top_pair))
print("transition lines checked: %d; no linked talk-to-layout pair: %d; of them with a top-level layout to read: %d"
      % (len(lines), len(none) + len(toplevel), len(toplevel)))
for aid, tp in toplevel:
    print("  top-level: %s %s" % (aid, " ".join(tp)))
for aid, tp in none:
    print("  not linked: %s" % aid)
