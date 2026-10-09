"""Print each member of the named third-order themes as one line: sub, theme id, second-order label,
and the member's other kinds, from scheme_current.jsonl. Read-only.
usage: python3 out/_analysis/b1_kind_labels.py T3-056 T3-012"""
import collections, json, sys

ids = sys.argv[1:]
label, members, where = {}, {}, collections.defaultdict(set)
for l in open("out/scheme/scheme_current.jsonl", encoding="utf-8"):
    if not l.strip():
        continue
    r = json.loads(l)
    label[r["theme"]] = r["label"]
    members[r["theme"]] = [(m["sub"], m["theme_id"], m["second_order"]) for m in r["members"]]
    for m in r["members"]:
        where[(m["sub"], m["theme_id"])].add(r["theme"])
for t in ids:
    print("%s %s: %d members" % (t, label[t], len(members[t])))
    for s, tid, so in members[t]:
        others = ",".join(sorted(o for o in where[(s, tid)] if o != t))
        print("  %-22s %-4s %-70s %s" % (s, tid, so[:70], others))
