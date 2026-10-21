#!/usr/bin/env python3
"""D3a-47: re-rule instantiate lines already in the ledger, by appended lines. Reads a rows file ('id|CLASS|evidence')
and a tags file for those ids ('id|TAG,TAG'; an id with no row loses its tags), and writes, as superseding files
with new names (the earlier versions stay): the spec file with those rows replaced, the tag file with those ids' tags
replaced, and a rulings file in the instantiate build's format ('<rule>: <evidence>; <clause>'), with the decision of
the class in the instantiate clause file and kind 'specification' for an accepted class. Refuses an id the spec file
lacks, a class the clause file lacks, or an output path that already exists.

  python3 out/_analysis/d3_rerule_inst.py --element A20 --rule G52 --clauses A20-inst-clauses.json --rows R \
      --rows-tags T --spec-in S1 --spec-out S2 --tags-in T1 --tags-out T2 --out J
"""
import argparse
import json
import os
import sys

D = "out/_analysis/d3_rulings/"
ap = argparse.ArgumentParser()
for k in ("element", "rule", "clauses", "rows", "rows-tags", "spec-in", "spec-out", "tags-in", "tags-out", "out"):
    ap.add_argument("--" + k, required=True)
a = ap.parse_args()
for p in (a.spec_out, a.tags_out, a.out):
    if os.path.exists(D + p):
        sys.exit("refused: %s exists" % p)
rows = {}
for l in open(D + a.rows, encoding="utf-8"):
    if l.strip():
        i, c, ev = l.rstrip("\n").split("|", 2)
        rows[i] = (c, ev)
newtags = {}
for l in open(D + a.rows_tags, encoding="utf-8"):
    if l.strip():
        i, t = l.strip().split("|")
        newtags[i] = t
clauses = json.load(open(D + a.clauses, encoding="utf-8"))
for i, (c, _) in rows.items():
    if c not in clauses:
        sys.exit("refused: class %s not in the clause file" % c)
out, found = [], set()
for l in open(D + a.spec_in, encoding="utf-8"):
    if not l.strip():
        continue
    i = l.split("|", 1)[0]
    if i in rows:
        found.add(i)
        out.append("%s|%s|%s\n" % (i, rows[i][0], rows[i][1]))
    else:
        out.append(l if l.endswith("\n") else l + "\n")
if found != set(rows):
    sys.exit("refused: ids not in the spec file: %s" % sorted(set(rows) - found))
open(D + a.spec_out, "w", encoding="utf-8").write("".join(out))
tags = [l for l in open(D + a.tags_in, encoding="utf-8") if l.strip() and l.split("|", 1)[0] not in rows]
tags += ["%s|%s\n" % (i, t) for i, t in newtags.items()]
open(D + a.tags_out, "w", encoding="utf-8").write("".join(t if t.endswith("\n") else t + "\n" for t in tags))
with open(D + a.out, "w", encoding="utf-8") as f:
    for i, (c, ev) in rows.items():
        d, clause = clauses[c]
        r = {"adaptation": i, "decision": d,
             "reason": "%s: %s; %s" % (a.rule, ev, clause.replace("{el}", a.element))}
        if d == "accept":
            r["kind"] = "specification"
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("re-ruled %d rows: %s; wrote %s, %s and %s" % (len(rows), {i: rows[i][0] for i in rows}, a.spec_out,
                                                     a.tags_out, a.out))
