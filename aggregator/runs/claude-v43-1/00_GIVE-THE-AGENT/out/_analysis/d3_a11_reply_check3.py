#!/usr/bin/env python3
"""D3a-38: G43 reading 4's check, version 3. Version 1 passed a line when any pair of its cited concepts was
reply-linked, so a talk-to-talk pair could pass a line whose layout answered another post (giantbomb-013). Version 2
sorted talk from layout by words in the labels, which misreads many labels (Okami-008's revised layout). This version
takes the answer from each ruling's own words: the last concept code before ' answers' or ' answer', or the first
after 'answered by' or 'answer is'; with none, the cited concept latest in hour. The talk is every other cited concept
earlier in hour in the answer's thread. The line is linked when the answer's item replies under a talk item, is the
same item, has the same author, or a talk item is the submission. Forests are read by `mem.py forest`, each line by
its last '-> [' so a flair holding '>' does not break the parse. Lines not linked are listed with their answer's and
talk's paths, for a reading in the forest. Writes nothing.

  python3 out/_analysis/d3_a11_reply_check3.py
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

text = {}
for name, keep in (("A11-inst-spec.txt", ("T", "TO")), ("A11-restrict-spec.txt", ("S-T", "S-TO"))):
    for l in open(R + name, encoding="utf-8"):
        if l.strip():
            aid, cls, ev = l.rstrip("\n").split("|", 2)
            if cls in keep:
                text[aid] = ev
for l in open(R + "A11-absent.jsonl"):
    r = json.loads(l)
    if r["decision"] == "reject":
        text[r["adaptation"]] = r["reason"]

CODE = re.compile(r"\bc\d{4}\b")


def answer_of(ev, cited, room):
    m = re.search(r"answered by (c\d{4})|answer is (c\d{4})", ev)
    if m:
        return m.group(1) or m.group(2), "words"
    k = ev.find(" answer")
    if k >= 0:
        before = CODE.findall(ev[:k])
        if before:
            return before[-1], "words"
    hs = [(pos[(room, c)][1], c) for c in cited if (room, c) in pos]
    return (max(hs)[1], "latest") if hs else (None, "none")


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
                for c in CODE.findall(line[k:]):
                    t[c] = (m.group(1), m.group(3))
        trees[(room, thread)] = t
    return trees[(room, thread)]


flag, how = [], {"words": 0, "latest": 0, "none": 0}
for aid in sorted(text):
    room = aid.rsplit("-", 1)[0]
    cited = sorted(set(CODE.findall(text[aid])))
    ans, src = answer_of(text[aid], cited, room)
    how[src] += 1
    if ans is None or (room, ans) not in pos:
        flag.append((aid, src, ans, "answer not placed"))
        continue
    ta, ha = pos[(room, ans)]
    t = tree(room, ta)
    talk = [c for c in cited if c != ans and (room, c) in pos and pos[(room, c)][0] == ta and pos[(room, c)][1] <= ha]
    if ans not in t:
        flag.append((aid, src, ans, "answer not in its forest"))
        continue
    da, ua = t[ans]
    ok, seen = False, []
    for c in talk:
        if c not in t:
            continue
        dc, uc = t[c]
        seen.append("%s@%s" % (c, dc))
        if dc == "0" or da == dc or da.startswith(dc + ".") or ua == uc:
            ok = True
    if not ok:
        flag.append((aid, src, ans, "answer %s@%s; talk %s" % (ans, da, " ".join(seen) or "none in thread")))
print("transition lines: %d; answer found by words %d, by latest hour %d, none %d; not linked: %d" % (
    len(text), how["words"], how["latest"], how["none"], len(flag)))
for aid, src, ans, why in flag:
    print("  %s (%s) %s" % (aid, src, why))
