#!/usr/bin/env python3
"""B2b-r3-p3: the items the freeze edits (scheme_edits 296 to 302) owe rechecks on, from
out/_analysis/b2_rechecks_owed_freeze.txt: per item, the edits, its file, my placement, my why per theme, the
size of its support and of each also_present theme. With item names on the command line, only those. Reads only."""
import collections, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
placed = {}
for name in ("author_items.jsonl", "gold_items.jsonl"):
    for r in (json.loads(x) for x in open(os.path.join(OUT, name), encoding="utf-8") if x.strip()):
        placed[r["item"]] = (name, r)
owed, edit = collections.defaultdict(list), None
for line in open(os.path.join(OUT, "_analysis", "b2_rechecks_owed_freeze.txt"), encoding="utf-8"):
    m = re.match(r"^(edit:\d+)\s", line)
    if m:
        edit = m.group(1)
    m = re.match(r"^\s+owed: ([^:]+):(t\d+)\s+on (\S+)", line)
    if m and edit and int(edit.split(":")[1]) >= 296:
        owed["%s/%s" % (m.group(1), m.group(2))].append(edit)
want = set(sys.argv[1:])
print("%d items, %d (edit, item) pairs" % (len(owed), sum(len(v) for v in owed.values())))
for it in sorted(owed):
    if want and it not in want:
        continue
    f, r = placed[it]
    ap = r.get("also_present") or {}
    print("%s [%s] on %s; edits %s; support %d; also_present %s" % (
        it, f.split("_")[0], ",".join(r["third_order"]), ",".join(e.split(":")[1] for e in owed[it]), len(r.get("support") or []),
        ", ".join("%s:%d" % (k, len(v)) for k, v in ap.items()) or "-"))
    if want:
        for k, v in (r.get("why") or {}).items():
            print("    why %s: %s" % (k, v))
        if r.get("support_by_theme"):
            print("    support_by_theme: %s" % json.dumps(r["support_by_theme"]))
