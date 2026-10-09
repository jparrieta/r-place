"""List second-order themes whose label names both acts of a kind pair (two regexes) but which are
placed in only one of the two kinds. Read-only.
usage: python3 out/_analysis/b1_both_acts.py T3-005 T3-021 "defen|attack|fight" "repair|maint|keep|fix|watch"
"""
import collections, json, re, sys

a, b, ra, rb = sys.argv[1], sys.argv[2], re.compile(sys.argv[3], re.I), re.compile(sys.argv[4], re.I)
where, label = collections.defaultdict(set), {}
for l in open("out/scheme/scheme_current.jsonl", encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        for m in r["members"]:
            k = (m["sub"], m["theme_id"])
            where[k].add(r["theme"])
            label[k] = m["second_order"]
rows = []
for k, kinds in where.items():
    if (a in kinds) != (b in kinds) and ra.search(label[k]) and rb.search(label[k]):
        rows.append((k, "only " + (a if a in kinds else b), ",".join(sorted(kinds))))
for (s, t), only, kinds in sorted(rows):
    print("%-22s %-4s %-12s %-30s %s" % (s, t, only, kinds, label[(s, t)][:70]))
print("%d themes name both acts but hold one of %s, %s" % (len(rows), a, b))
