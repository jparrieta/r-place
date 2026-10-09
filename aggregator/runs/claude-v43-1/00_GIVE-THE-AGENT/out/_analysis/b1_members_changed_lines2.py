"""Append members_changed lines to tier_history.jsonl for a review that changed members of existing
kinds without splitting one, read after the moves from scheme_current.jsonl. Supersedes
b1_members_changed_lines.py, which wrote one line per --gained or --lost and so could not record a
kind that both gained and lost members in one leg. Here --gained and --lost may name the same kind;
the script writes one line per kind, with was = now minus the gained plus the lost. It checks each
gained member is in the kind and each lost member is not. Refuses a kind that already has a
tier_history line in this leg. Dry run unless --write.

usage: python3 out/_analysis/b1_members_changed_lines2.py --leg B1b-20 --prompted "..."
         --gained "T3-095=scotland:t04,bitcoin:t06" --lost "T3-095=halo:t09"
         --why "T3-095=..." [--move "T3-095=relating or contrasting"] [--write]
"""
import collections, datetime, json, sys

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
gained, lost, order = collections.defaultdict(list), collections.defaultdict(list), []
for key, store in (("--gained", gained), ("--lost", lost)):
    for spec in args(key):
        tid, ms = spec.split("=", 1)
        store[tid] += ms.split(",")
        if tid not in order:
            order.append(tid)
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
lines = []
for tid in order:
    now = mem(tid)
    for x in gained[tid]:
        if x not in now:
            sys.exit("PROBLEM: %s is not in %s" % (x, tid))
    for x in lost[tid]:
        if x in now:
            sys.exit("PROBLEM: %s is still in %s" % (x, tid))
    if tid in done:
        sys.exit("PROBLEM: %s already has a tier_history line in %s" % (tid, leg))
    was = [x for x in now if x not in gained[tid]] + lost[tid]
    move = moves.get(tid, "relating or contrasting" if gained[tid] else "dropping")
    lines.append({"t": t, "stage": "B1", "leg": leg, "tier": "third", "id": tid, "move": move,
                  "event": "members_changed", "was": {"label": rows[tid]["label"], "members": was},
                  "now": [{"id": tid, "members": now}], "prompted_by": prompted, "why": whys.get(tid, "")})
    print("%s: was %d, now %d (gained %d, lost %d), move %s" % (tid, len(was), len(now), len(gained[tid]),
                                                                len(lost[tid]), move))
if write:
    with open("out/tier_history.jsonl", "a", encoding="utf-8") as f:
        for d in lines:
            f.write(json.dumps(d) + "\n")
    print("written: %d tier_history lines" % len(lines))
else:
    print("dry run: %d lines" % len(lines))
