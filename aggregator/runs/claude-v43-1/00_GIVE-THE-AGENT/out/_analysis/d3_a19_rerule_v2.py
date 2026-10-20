#!/usr/bin/env python3
"""D3a-46: version 2 of d3_a19_rerule.py, with the file names as arguments. Reads a rows file ('id|CLASS|evidence')
and a tags file for those ids ('id|TAG,TAG', empty for none), and writes, as superseding files with new names (the
earlier versions stay): the spec file with those rows replaced, the tag file with those ids' tags replaced, and a
rulings file in the restrict build's format ('G51 and G9: <evidence>; <clause>') with the decision and kind of the
class in A19-restrict-clauses.json. Refuses an id the spec file lacks, or a class the clause file lacks.

  python3 out/_analysis/d3_a19_rerule_v2.py --rows R --rows-tags T --spec-in S1 --spec-out S2 --tags-in T1 \
      --tags-out T2 --out J
"""
import argparse
import json

D = "out/_analysis/d3_rulings/"
ap = argparse.ArgumentParser()
for k in ("rows", "rows-tags", "spec-in", "spec-out", "tags-in", "tags-out", "out"):
    ap.add_argument("--" + k, required=True)
a = ap.parse_args()
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
clauses = json.load(open(D + "A19-restrict-clauses.json", encoding="utf-8"))
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
assert found == set(rows), set(rows) - found
open(D + a.spec_out, "w", encoding="utf-8").write("".join(out))
print("wrote", len(out), "rows to", D + a.spec_out)
keep = [l if l.endswith("\n") else l + "\n" for l in open(D + a.tags_in, encoding="utf-8")
        if l.strip() and l.split("|", 1)[0] not in rows]
keep += ["%s|%s\n" % (i, t) for i, t in newtags.items()]
open(D + a.tags_out, "w", encoding="utf-8").write("".join(keep))
print("wrote", len(keep), "tag rows to", D + a.tags_out)
with open(D + a.out, "w", encoding="utf-8") as f:
    for i, (c, ev) in rows.items():
        d, k, clause = clauses[c]
        rec = {"adaptation": i, "decision": d}
        if k:
            rec["kind"] = k
        rec["reason"] = "G51 and G9: %s; %s" % (ev, clause.replace("{el}", "A19"))
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
print("wrote", len(rows), "re-rulings to", D + a.out)
