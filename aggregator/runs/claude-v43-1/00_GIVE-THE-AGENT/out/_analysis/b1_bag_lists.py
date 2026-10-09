"""Print the latest bag record of each sub:tNN as 'sub:tNN:kept:would_need (leg)'. Read-only.
usage: python3 out/_analysis/b1_bag_lists.py greenlattice:t03 ..."""
import json, sys

bag = {}
for l in open("out/multiplacement_log.jsonl", encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        if r.get("item_is_a_bag"):
            bag[(r["sub"], r["theme_id"])] = r
for a in sys.argv[1:]:
    s, t = a.split(":")
    b = bag.get((s, t))
    print("%s:%s:%s:%s (%s)" % (s, t, b["primary"], ",".join(b["would_need"]), b["leg"]) if b else "%s NO BAG" % a)
