#!/usr/bin/env python3
"""D3a-38: a second look at A11's restrict spec. A concept's quote can omit the layout its code label names
(texas-042's c0062, 'posting a template'). For every row not classed as the transition (S-T, S-TO), list the
pairs of its concepts in one thread where an earlier concept's label reads as design talk and a later concept's
label reads as a layout, so each flagged row can be read again. Labels come from the restrict packets, hours and
threads from the quote windows. Writes nothing.

  python3 out/_analysis/d3_a11_label_check.py
"""
import glob
import re

LAY = re.compile(r"template|layout|grid|mock-?up|sketch|pixel (art|design|plan|map|guide)|guide|reference|blueprint|"
                 r"schematic|overlay|pattern|draft|new version|plan (image|picture)|posting (a|an|the) (design|image|"
                 r"picture|plan|version)|linking (a|an|the) (design|image|picture|plan)", re.I)
TALK = re.compile(r"propos|suggest|argu|debat|vot(e|ing)|objecting|asking (what|whether|how|for (a )?(change|"
                  r"colou?r))|questioning|preferring|deciding|choosing|wanting|wishing|doubting|criticis|disagree",
                  re.I)
labels = {}
for f in sorted(glob.glob("out/_analysis/d3_pk_A11_restrict_*.txt")):
    for blk in open(f, encoding="utf-8").read().split("\n== ")[1:]:
        aid = blk.split("\n", 1)[0].split()[0]
        m = re.search(r"codes: (.*)", blk)
        if m:
            for c, lab in re.findall(r"(c\d{4}) (.*?)(?=; c\d{4} |$)", m.group(1)):
                labels[(aid, c)] = lab
info = {}
QL = re.compile(r'^\s*".*"  \[[^/\]]+/(c\d{4})\]  item \S+  thread (\S+)  h\+(\d+\.\d+)')
for f in sorted(glob.glob("out/_analysis/d3_wq_A11_r348_*.txt")):
    cur = None
    for line in open(f, encoding="utf-8"):
        h = re.match(r"^\[\d+\] (\S+)\s+restrict", line)
        if h:
            cur = h.group(1)
            continue
        m = QL.match(line)
        if m and cur:
            info.setdefault(cur, []).append((m.group(1), m.group(2), float(m.group(3))))
rows = []
for f in sorted(glob.glob("out/_analysis/d3_rulings/A11-restrict-spec-[0-9]*.txt")):
    for line in open(f, encoding="utf-8"):
        if line.strip():
            aid, cls, _ = line.split("|", 2)
            rows.append((aid, cls))
flag = 0
for aid, cls in rows:
    if cls in ("S-T", "S-TO"):
        continue
    cs = info.get(aid, [])
    hits = []
    for a, ta, ha in cs:
        for b, tb, hb in cs:
            if ta == tb and ha < hb and TALK.search(labels.get((aid, a), "")) and LAY.search(labels.get((aid, b), "")):
                hits.append("%s (%s) -> %s (%s)" % (a, labels[(aid, a)][:60], b, labels[(aid, b)][:60]))
    if hits:
        flag += 1
        print("%s %s: %s" % (aid, cls, " | ".join(hits[:3])))
print("rows read: %d; flagged for a second look: %d" % (len(rows), flag))
