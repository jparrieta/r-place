"""Before writing, check every concept id cited in a bag file's why against the second-order theme
the line is for, through b1_room_codes.py (as b1_check_bags.py does after writing), and check that
the kept kind is where the theme is placed now and that no listed kind repeats the kept one. Read-only.
usage: python3 out/_analysis/b1_precheck_bagfile.py <bagfile>"""
import collections, json, re, subprocess, sys

lines = [l.strip() for l in open(sys.argv[1]) if l.strip()]
where = collections.defaultdict(set)
for l in open("out/scheme/scheme_current.jsonl", encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        for m in r["members"]:
            where[(m["sub"], m["theme_id"])].add(r["theme"])
theme_of = {}
for sub in sorted({l.split(":")[0] for l in lines}):
    out = subprocess.run(["python3", "out/_analysis/b1_room_codes.py", sub], capture_output=True, text=True).stdout
    for row in out.splitlines():
        p = row.split()
        if len(p) >= 3 and re.match(r"^c\d{4}$", p[0]):
            theme_of[(sub, p[0])] = p[2]
bad = 0
for l in lines:
    sub, tid, kept, wanted, why = l.split(":", 4)
    now = where.get((sub, tid), set())
    if now != {kept}:
        print("PLACEMENT %s:%s kept %s but placed %s" % (sub, tid, kept, sorted(now)))
        bad += 1
    if kept in wanted.split(","):
        print("REPEAT %s:%s lists its kept kind %s" % (sub, tid, kept))
        bad += 1
    for c in re.findall(r"c\d{4}", why):
        if theme_of.get((sub, c)) != tid:
            print("CODE %s:%s cites %s, which sits under %s" % (sub, tid, c, theme_of.get((sub, c))))
            bad += 1
print("%d bag lines checked, %d problems" % (len(lines), bad))
