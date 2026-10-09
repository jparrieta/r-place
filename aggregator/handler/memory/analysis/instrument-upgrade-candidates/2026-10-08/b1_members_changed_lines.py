"""Append members_changed lines to tier_history.jsonl for a review that changed members of existing
kinds without splitting one, read after the moves from scheme_current.jsonl. Each --gained or --lost
names one kind and its members; the script checks each gained member is in the kind and each lost
member is not, then writes was/now for the kind. Refuses a kind that already has a tier_history line
in this leg. Dry run unless --write.

usage: python3 out/_analysis/b1_members_changed_lines.py --leg B1b-20 --prompted "..."
         --gained "T3-152=kilian:t03,bangtan:t04" --lost "T3-014=bitcoin:t11"
         --why "T3-152=..." --why "T3-014=..." [--move "T3-014=dropping"] [--write]
"""
import datetime, json, sys

a = sys.argv[1:]
args = lambda k: [a[i + 1] for i, x in enumerate(a) if x == k]
arg = lambda k: a[a.index(k) + 1]
leg, prompted, write = arg("--leg"), arg("--prompted"), "--write" in a
whys = dict(w.split("=", 1) for w in args("--why"))
moves = dict(m.split("=", 1) for m in args("--move"))
rows = {}
for l in open("out/scheme/scheme_current.jsonl", encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        rows[r["theme"]] = r
mem = lambda t: ["%s:%s" % (m["sub"], m["theme_id"]) for m in rows[t]["members"]]
done = {json.loads(l)["id"] for l in open("out/tier_history.jsonl", encoding="utf-8")
        if l.strip() and json.loads(l).get("leg") == leg}
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
lines = []
for spec, gained in [(s, True) for s in args("--gained")] + [(s, False) for s in args("--lost")]:
    tid, ms = spec.split("=", 1)
    ms = ms.split(",")
    for x in ms:
        if (x in mem(tid)) != gained:
            sys.exit("PROBLEM: %s %s %s" % (x, "is not in" if gained else "is still in", tid))
    if tid in done:
        sys.exit("PROBLEM: %s already has a tier_history line in %s" % (tid, leg))
    was = [x for x in mem(tid) if x not in ms] if gained else mem(tid) + ms
    lines.append({"t": t, "stage": "B1", "leg": leg, "tier": "third", "id": tid,
                  "move": moves.get(tid, "relating or contrasting" if gained else "dropping"),
                  "event": "members_changed", "was": {"label": rows[tid]["label"], "members": was},
                  "now": [{"id": tid, "members": mem(tid)}], "prompted_by": prompted,
                  "why": whys.get(tid, "")})
    print("%s %s: was %d, now %d (%s %s)" % (tid, "gained" if gained else "lost", len(was), len(mem(tid)),
                                            "added" if gained else "removed", ", ".join(ms)))
if write:
    with open("out/tier_history.jsonl", "a", encoding="utf-8") as f:
        for d in lines:
            f.write(json.dumps(d) + "\n")
    print("written: %d tier_history lines" % len(lines))
else:
    print("dry run: %d lines" % len(lines))
