#!/usr/bin/env python3
"""C5c-02: carry Stigmergy's recut (C5-move-merging-93, C5-move-splitting-94, C5-move-relating-95) into account.md.
Each replacement must match exactly once; the counts are read from model/arrows.jsonl, not typed. Refuses unless
account-p5.md exists (the pass 5 text kept).

    python3 out/_analysis/c5c2_account_recut.py [--write]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
if not os.path.exists(os.path.join(OUT, "account-p5.md")):
    sys.exit("keep the pass 5 text as account-p5.md first")
A = {r["id"]: r for r in (json.loads(l) for l in open(os.path.join(OUT, "model", "arrows.jsonl"), encoding="utf-8")
                          if l.strip())}


def c(a):
    return "%d of %d" % (A[a]["counts"]["holds"], A[a]["counts"]["both"])


p = os.path.join(OUT, "account.md")
t = open(p, encoding="utf-8").read()
R = [
    ("# The account, pass 5 (C5c-01)", "# The account, pass 6 (C5c-02)"),
    ("Pass 5 answers the three readers; their disagreements are printed beside it in `account-readers-C5.md`.",
     "Pass 5 answered the three readers; their disagreements are printed beside it in `account-readers-C5.md`. Pass 6 "
     "carries Stigmergy's recut after a third coding and answers the field analyst's second reading."),
    ("Passes 1, 3 and 4 are kept as `account-p1.md`, `account-p3.md` and `account-p4.md`.",
     "Passes 1, 3, 4 and 5 are kept as `account-p1.md`, `account-p3.md`, `account-p4.md` and `account-p5.md`."),
    ('"137 of 190" counts the rooms', '"%s" counts the rooms' % c("A01")),
    ("members report what they built in 137 of 190 rooms [A01]", "members report what they built in %s rooms [A01]" % c("A01")),
    ("members turn to keeping it in 182 of 291 rooms [A03]", "members turn to keeping it in %s rooms [A03]" % c("A03")),
    ("after the first build report in 182 of 282 rooms [A07, P11]", "after the first build report in %s rooms [A07, P11]" % c("A07")),
    ("They argue its design in 281 rooms and build their homeland's flag in 96 (the rooms carrying each theme; F-017).",
     "They argue its design in 281 rooms and build their homeland's flag in 96 (the rooms carrying each theme; F-017). "
     "They add to the mark or enlarge it in 168 rooms, mostly by proposing what to add, and add personal pieces to a "
     "shared mark in 7."),
]
old_para_start = "**The mark tells what is missing.**"
i = t.index(old_para_start)
j = t.index("\n\n", i)
new_para = (
    "**The mark tells what is missing.** Members report the state of the half-built mark to the thread [P03]: \"It "
    "looks like the gridref (600,456) is wrong. It should be (600,482).\" [starcitizen/c0330, h69.84]. Three coders read "
    "a seeded sample of 24 records of building and reporting the mark. By the code at least two of them gave, 10 of the "
    "14 records that bear on the work report what is placed, done or missing, or say a member acted on what the canvas "
    "showed; 4 propose or ask (F-018). This is a reading of a sample, not an order test. The theme is named Stigmergy: "
    "coordination through the work itself, where what is already placed shows the next person what to add (Grassé "
    "1959; Heylighen 2016). Since the third coding it holds this one theme. Two themes that stood with it, extending "
    "the work and adding a personal piece, mostly propose what to add, so they moved to what members settle the mark "
    "will show [P02]. Stigmergy differs from imitation, because members name what the work lacks, not who else is "
    "placing. It differs from an open-source project, where a founder lays out the tasks for all to see; here any "
    "member may post a template.")
t = t[:i] + new_para + t[j:]
for old, new in R:
    n = t.count(old)
    if n != 1:
        sys.exit("%r matches %d times" % (old[:60], n))
    t = t.replace(old, new)
print(new_para)
print("%d words" % len(t.split()))
if "--write" in sys.argv:
    open(p, "w", encoding="utf-8").write(t)
    print("account.md written")
