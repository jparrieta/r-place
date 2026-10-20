#!/usr/bin/env python3
"""D3a-46: apply G51's reading 69 backwards to three A19 lines already written. Reads A19-rerule-rows.txt
('id|CLASS|evidence'), and writes, as superseding files with new names (the first versions stay):
  - A19-restrict-spec-v2.txt and A19-addcond-spec-v2.txt, the spec files with those rows replaced;
  - A19-tags-restrict-v2.txt and A19-tags-add-v2.txt, the tag files without those ids;
  - A19-rerule.jsonl, one ruling per id in the restrict build's format ('G51 and G9: <evidence>; <clause>'), with the
    decision and kind of the class in A19-restrict-clauses.json.
Refuses an id that neither spec file holds, or a class the clause file lacks. Prints what it wrote.

  python3 out/_analysis/d3_a19_rerule.py
"""
import json

R = "out/_analysis/d3_rulings/"
rows = {}
for l in open(R + "A19-rerule-rows.txt", encoding="utf-8"):
    if l.strip():
        i, c, ev = l.rstrip("\n").split("|", 2)
        rows[i] = (c, ev)
clauses = json.load(open(R + "A19-restrict-clauses.json", encoding="utf-8"))
found = set()
for old, new in (("A19-restrict-spec.txt", "A19-restrict-spec-v2.txt"), ("A19-addcond-spec.txt", "A19-addcond-spec-v2.txt")):
    out = []
    for l in open(R + old, encoding="utf-8"):
        if not l.strip():
            continue
        i = l.split("|", 1)[0]
        if i in rows:
            found.add(i)
            out.append("%s|%s|%s\n" % (i, rows[i][0], rows[i][1]))
        else:
            out.append(l if l.endswith("\n") else l + "\n")
    open(R + new, "w", encoding="utf-8").write("".join(out))
    print("wrote", len(out), "rows to", R + new)
assert found == set(rows), set(rows) - found
for old, new in (("A19-tags-restrict.txt", "A19-tags-restrict-v2.txt"), ("A19-tags-add.txt", "A19-tags-add-v2.txt")):
    keep = [l for l in open(R + old, encoding="utf-8") if l.strip() and l.split("|", 1)[0] not in rows]
    open(R + new, "w", encoding="utf-8").write("".join(keep))
    print("wrote", len(keep), "tag rows to", R + new)
with open(R + "A19-rerule.jsonl", "w", encoding="utf-8") as f:
    for i, (c, ev) in rows.items():
        d, k, clause = clauses[c]
        rec = {"adaptation": i, "decision": d}
        if k:
            rec["kind"] = k
        rec["reason"] = "G51 and G9: %s; %s" % (ev, clause.replace("{el}", "A19"))
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
print("wrote", len(rows), "re-rulings to", R + "A19-rerule.jsonl")
