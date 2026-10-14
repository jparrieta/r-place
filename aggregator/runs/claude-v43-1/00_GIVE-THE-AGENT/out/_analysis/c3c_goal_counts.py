#!/usr/bin/env python3
"""C3c, part 5 (the goal; Felin and Zenger's chosen problem): rooms carrying third-order themes I place, by their names,
in four modes of having a goal: inherited (the mark is the sub's own sign, or someone else's start), negotiated (the
room argues its design or votes), contested (members argue the room should not be on the canvas at all,
or should stop), changed (the room moves, shrinks, quits or turns to upkeep). A fifth set holds the goals made after
the clock, and a sixth the proposal by one member (T3-033), kept apart because a proposal others join is a start, not
a negotiation, unless the room then argues it. The placement is mine, from the themes' names and their members' records as read in stages B and C; the theme
a reply sits under does not track its stance (C3b), so the counts are of rooms whose coded records sit under a theme,
not of rooms whose stance was read. Prints the names from structure-C3.md, the rooms per theme and per mode (unions,
`mem.py rooms --with`), the overlaps between modes, and the rooms with no mode. Writes nothing.

    python3 out/_analysis/c3c_goal_counts.py
"""
import os, re, subprocess, sys
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
txt = open(os.path.join(ROOT, "out", "structure-C3.md"), encoding="utf-8").read()
names = {}
for line in re.findall(r"- \*\*Members:\*\* (.*?)\. Rooms carrying any member", txt):
    names.update(re.findall(r"(T3-\d{3}) ([^,]+)", line))

MODES = [
    ("inherited", ["T3-065", "T3-113", "T3-082", "T3-175", "T3-197"]),
    ("negotiated", ["T3-004", "T3-066"]),
    ("contested", ["T3-037", "T3-075", "T3-140", "T3-059", "T3-098"]),
    ("changed", ["T3-124", "T3-022", "T3-181", "T3-042", "T3-069"]),
    ("after the clock", ["T3-054", "T3-111"]),
    ("proposed by one", ["T3-033"]),
]


def rooms_with(tid):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "rooms", "--with", tid,
                        "--limit", "2000"], cwd=ROOT, capture_output=True, text=True)
    n = int(re.search(r"rooms with \S+: (\d+) of (\d+)", p.stdout).group(1))
    got = set(re.findall(r"^  (\S+)\s*$", p.stdout, re.M))
    if len(got) != n:
        sys.exit("%s: header says %d rooms, parsed %d" % (tid, n, len(got)))
    return got


union = {}
for mode, ids in MODES:
    u = set()
    for t in ids:
        r = rooms_with(t)
        u |= r
        print("  %-15s %s %-40s %3d rooms" % (mode, t, names.get(t, "?"), len(r)))
    union[mode] = u
    print("%s: rooms carrying any: %d" % (mode, len(u)))
four = [m for m, _ in MODES[:4]]
for a, b in combinations(four, 2):
    print("both %s and %s: %d" % (a, b, len(union[a] & union[b])))
anyg = set().union(*(union[m] for m in four))
print("rooms with any of the four modes: %d of 705" % len(anyg))
print("inherited only, of the four: %d" % len(union["inherited"] - union["negotiated"] - union["contested"]
                                            - union["changed"]))
print("negotiated and not inherited: %d" % len(union["negotiated"] - union["inherited"]))
print("changed and also inherited or negotiated: %d" % len(union["changed"] & (union["inherited"] | union["negotiated"])))
p1 = union["proposed by one"]
print("proposed by one and negotiated: %d; proposed by one and not negotiated: %d; proposed by one and inherited: %d"
      % (len(p1 & union["negotiated"]), len(p1 - union["negotiated"]), len(p1 & union["inherited"])))
print("rooms with any of the four modes or a proposal: %d of 705" % len(anyg | p1))
