"""For each sub:tNN given, print its current kinds (scheme_current.jsonl), whether a bag record exists
(multiplacement_log.jsonl, item_is_a_bag) and the bag's kept and listed kinds, and the latest
rule 0 line's primary. Read-only.
usage: python3 out/_analysis/b1_member_status.py greenlattice:t03 ainbowroad:t05"""
import collections, json, sys

where = collections.defaultdict(set)
for l in open("out/scheme/scheme_current.jsonl", encoding="utf-8"):
    if not l.strip():
        continue
    r = json.loads(l)
    for m in r["members"]:
        where[(m["sub"], m["theme_id"])].add(r["theme"])
bag, last = {}, {}
for l in open("out/multiplacement_log.jsonl", encoding="utf-8"):
    if not l.strip():
        continue
    r = json.loads(l)
    k = (r["sub"], r["theme_id"])
    if r.get("item_is_a_bag"):
        bag[k] = r
    else:
        last[k] = r
for a in sys.argv[1:]:
    s, t = a.split(":")
    k = (s, t)
    b = bag.get(k)
    bs = ("bag kept %s, would need %s (%s)" % (b.get("primary"), ",".join(b.get("would_need") or []), b.get("leg"))) if b else "no bag"
    p = last.get(k)
    ps = ("rule0 primary %s (%s)" % (p.get("primary"), p.get("leg"))) if p else "no rule0 line"
    print("%-26s now %-28s %s; %s" % (a, ",".join(sorted(where.get(k, []))), bs, ps))
