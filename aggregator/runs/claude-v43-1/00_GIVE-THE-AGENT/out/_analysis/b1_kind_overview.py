"""For each third-order theme named, print its members' count, rooms, and how often its members
are also placed in each other theme (co-placement), from scheme_current.jsonl. Read-only.
usage: python3 out/_analysis/b1_kind_overview.py T3-009 T3-010 [--top 15]"""
import collections, json, sys

a = sys.argv[1:]
top = int(a[a.index("--top") + 1]) if "--top" in a else 15
ids = [x for x in a if x.startswith("T3-")]
label, members, where = {}, {}, collections.defaultdict(set)
for l in open("out/scheme/scheme_current.jsonl", encoding="utf-8"):
    if not l.strip():
        continue
    r = json.loads(l)
    label[r["theme"]] = r["label"]
    members[r["theme"]] = [(m["sub"], m["theme_id"]) for m in r["members"]]
    for m in r["members"]:
        where[(m["sub"], m["theme_id"])].add(r["theme"])
total = len(where)
for t in ids:
    mem = members[t]
    rooms = len(set(s for s, _ in mem))
    alone = sum(1 for k in mem if len(where[k]) == 1)
    co = collections.Counter(o for k in mem for o in where[k] if o != t)
    print("%s %s: %d members (%.1f%% of %d), %d rooms, %d placed here only" %
          (t, label[t], len(mem), 100.0 * len(mem) / total, total, rooms, alone))
    for o, n in co.most_common(top):
        print("   with %s %-45s %d" % (o, label[o][:45], n))
