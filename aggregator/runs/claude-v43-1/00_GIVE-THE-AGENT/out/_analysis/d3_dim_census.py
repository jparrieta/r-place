#!/usr/bin/env python3
"""D3a-54: the dimension lines' census under its rules (logged before this ran). Reads the 13 spec files of the 122
lines for each line's class, the eight dimension packets (d3_pk_D0N_000.txt) for each line's op, lift and link kind,
and D07's window quote files for the earliest cited hour of each D07 line. Prints lines by target and class; link
lines by source dimension and target dimension, with the paired elaborations and particulars apart; the ids that
other-held specifications name; the link kinds; and D07's specifications by the earliest hour against hour 73.
Writes nothing.

  python3 out/_analysis/d3_dim_census.py
"""
import re
from collections import Counter, defaultdict

R = "out/_analysis/d3_rulings/"
SPECS = ["D07-link-spec.txt", "D02-link-spec.txt", "D02-addcond-spec.txt", "D02-addstep-spec.txt",
         "D02-restrict-spec.txt", "D01-link-spec.txt", "D01-addcond-spec.txt", "D01-restrict-spec.txt",
         "D05-link-spec.txt", "D03-link-spec.txt", "D06-link-spec.txt", "D04-link-spec.txt", "D08-link-spec.txt"]
rows = {}
for f in SPECS:
    target = f[:3]
    for l in open(R + f, encoding="utf-8"):
        if l.strip():
            p = l.rstrip("\n").split("|")
            assert p[0] not in rows, p[0]
            rows[p[0]] = {"target": target, "class": p[1], "ev": p[2], "pair": p[3] if len(p) > 3 else None}
pk = {}
for d in ("D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08"):
    txt = open("out/_analysis/d3_pk_%s_000.txt" % d, encoding="utf-8").read()
    for blk in txt.split("\n== ")[1:]:
        head = blk.split("\n", 1)[0].split()
        lift = re.search(r"lift \S+ > (\S+) > (\S+) > (\S+)", blk)
        kind = re.search(r"link_kind: (\S+)", blk)
        pk[head[0]] = {"op": head[1], "t3": lift.group(1) if lift else None,
                       "src": lift.group(3) if lift and lift.group(3) != "None" else "none",
                       "kind": kind.group(1) if kind else None}
assert set(rows) == set(pk), (sorted(set(rows) ^ set(pk)))
print("lines: %d" % len(rows))
by_t = defaultdict(Counter)
for i, x in rows.items():
    by_t[x["target"]][x["class"]] += 1
for t in sorted(by_t):
    print("  %s %3d %s" % (t, sum(by_t[t].values()), dict(sorted(by_t[t].items()))))
print("by op:", dict(Counter(pk[i]["op"] for i in rows)))
print("by class:", dict(Counter(x["class"] for x in rows.values())))

links = [i for i in rows if pk[i]["op"] == "link"]
print("\nlink lines %d by source dimension -> target (all classes):" % len(links))
pairs = Counter((pk[i]["src"], rows[i]["target"]) for i in links)
for (s, t), n in sorted(pairs.items(), key=lambda z: (-z[1], z[0])):
    same = " (same)" if s == t else ""
    print("  %-4s -> %s  %2d%s" % (s, t, n, same))
print("link lines whose source lifts into the target itself: %d; to another dimension: %d; unplaced source: %d"
      % (sum(1 for i in links if pk[i]["src"] == rows[i]["target"]),
         sum(1 for i in links if pk[i]["src"] not in (rows[i]["target"], "none")),
         sum(1 for i in links if pk[i]["src"] == "none")))
print("\nnew dependences (paired elaborations and particulars):")
for i in sorted(links, key=lambda z: (rows[z]["target"], rows[z]["class"], z)):
    if rows[i]["class"] in ("E-PAIR", "PART"):
        print("  %-5s %-24s %s -> %s  kind %s  pair %s" % (rows[i]["class"], i, pk[i]["src"], rows[i]["target"],
                                                          pk[i]["kind"], rows[i]["pair"]))
named = Counter()
for i, x in rows.items():
    if x["class"] == "S-OTHER":
        ids = set(re.findall(r"\b(P\d\d|A\d\d|C0\d|K0\d|D0\d)\b", x["ev"]))
        for n in ids:
            named[n] += 1
print("\nspecifications held elsewhere (S-OTHER %d), ids named in their evidence: %s"
      % (sum(1 for x in rows.values() if x["class"] == "S-OTHER"), dict(sorted(named.items()))))
print("specifications held by the target itself (S-SHOW, S-PRED): %d"
      % sum(1 for x in rows.values() if x["class"] in ("S-SHOW", "S-PRED")))
print("link kinds:", dict(Counter(pk[i]["kind"] for i in links)))

hours = defaultdict(list)
for f in ("out/_analysis/d3_wq_D07_l001_000.txt", "out/_analysis/d3_wq_D07_l001_026.txt"):
    cur = None
    for l in open(f, encoding="utf-8"):
        m = re.match(r"\[\d+\] (\S+-\d{3}) ", l)
        if m:
            cur = m.group(1)
            continue
        h = re.search(r"\]  item \S+  thread \S+  h\+(\d+\.\d+)", l)
        if cur and h:
            hours[cur].append(float(h.group(1)))
d7 = [i for i, x in rows.items() if x["target"] == "D07" and x["class"] in ("S-SHOW", "S-PRED")]
early = sorted(i for i in d7 if hours[i] and min(hours[i]) < 73)
print("\nD07 specifications: %d; earliest cited hour before 73: %d; at or after 73: %d"
      % (len(d7), len(early), sum(1 for i in d7 if hours[i] and min(hours[i]) >= 73)))
print("  S-SHOW only: before 73 %d of %d" % (sum(1 for i in early if rows[i]["class"] == "S-SHOW"),
                                           sum(1 for i in d7 if rows[i]["class"] == "S-SHOW")))
