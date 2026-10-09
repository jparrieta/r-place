"""Append tier_history.jsonl lines for one review of an oversized kind, read after the moves: the
leg's unplacements come from the diary ("unplaced <sub>:<tNN> from <T3>" in this leg), the members
from scheme_current.jsonl. One split line for the source (was = now + removed; now = the source and
each new kind with its members), one members_changed line for every other kind that lost members,
and one for every kind named with --gained (was = now minus the named members).
Refuses if a kind already has a tier_history line in this leg. Dry run unless --write.

usage: python3 out/_analysis/b1_review_tier_lines.py --leg B1b-19-p2 --source T3-010 --new T3-194,T3-195
         --gained T3-056=h3h3productions:t38,batman:t06 --moves "T3-122=splitting" --prompted "..."
         --why-split "..." --why-dropped "..." --why "T3-122=..." --why "T3-056=..." [--write]
"""
import collections, datetime, json, re, subprocess, sys

a = sys.argv[1:]


def arg(k, d=None):
    return a[a.index(k) + 1] if k in a else d


def args(k):
    return [a[i + 1] for i, x in enumerate(a) if x == k]


leg, src = arg("--leg"), arg("--source")
new = arg("--new").split(",")
gained = {}
for g in args("--gained"):
    t, ms = g.split("=", 1)
    gained[t] = ms.split(",")
moves = dict(m.split("=", 1) for m in args("--moves"))
whys = dict(w.split("=", 1) for w in args("--why"))
write = "--write" in a

rows = {}
for l in open("out/scheme/scheme_current.jsonl", encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        rows[r["theme"]] = r
mem = lambda t: ["%s:%s" % (m["sub"], m["theme_id"]) for m in rows[t]["members"]]

out = subprocess.run(["python3", "tools/mem.py", "diary", "--grep", "unplaced", "--limit", "2000"],
                     capture_output=True, text=True).stdout
removed = collections.defaultdict(list)
for line in out.splitlines():
    m = re.search(r"\b%s\b.*unplaced (\S+):(t\d+) from (T3-\d+)" % re.escape(leg), line)
    if m:
        x = "%s:%s" % (m.group(1), m.group(2))
        if x not in removed[m.group(3)]:
            removed[m.group(3)].append(x)

done = set()
for l in open("out/tier_history.jsonl", encoding="utf-8"):
    d = json.loads(l)
    if d.get("leg") == leg:
        done.add(d["id"])
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
lines = []
prompted = arg("--prompted")
for x in removed[src]:
    if x in mem(src):
        sys.exit("PROBLEM: %s is still in %s" % (x, src))
lines.append({"t": t, "stage": "B1", "leg": leg, "tier": "third", "id": src, "move": "splitting", "event": "split",
              "was": {"label": rows[src]["label"], "members": mem(src) + removed[src]},
              "now": [{"id": src, "members": mem(src)}] +
                     [{"id": n, "label": rows[n]["label"], "members": mem(n)} for n in new],
              "prompted_by": prompted, "why": arg("--why-split")})
for tid in sorted(removed):
    if tid == src:
        continue
    for x in removed[tid]:
        if x in mem(tid):
            sys.exit("PROBLEM: %s is still in %s" % (x, tid))
    lines.append({"t": t, "stage": "B1", "leg": leg, "tier": "third", "id": tid, "move": moves.get(tid, "dropping"),
                  "event": "members_changed",
                  "was": {"label": rows[tid]["label"], "members": mem(tid) + removed[tid]},
                  "now": [{"id": tid, "members": mem(tid)}],
                  "prompted_by": prompted, "why": whys.get(tid, arg("--why-dropped"))})
for tid, ms in gained.items():
    for x in ms:
        if x not in mem(tid):
            sys.exit("PROBLEM: %s is not in %s" % (x, tid))
    lines.append({"t": t, "stage": "B1", "leg": leg, "tier": "third", "id": tid, "move": "relating or contrasting",
                  "event": "members_changed",
                  "was": {"label": rows[tid]["label"], "members": [x for x in mem(tid) if x not in ms]},
                  "now": [{"id": tid, "members": mem(tid)}],
                  "prompted_by": prompted, "why": whys.get(tid, "")})
clash = [d["id"] for d in lines if d["id"] in done]
if clash:
    sys.exit("PROBLEM: already a tier_history line in %s for %s" % (leg, ", ".join(clash)))
for d in lines:
    gone = len(d["was"]["members"]) - len(d["now"][0]["members"])
    print("%s %s %s: was %d, now %d%s" % (d["id"], d["event"], d["move"], len(d["was"]["members"]),
                                          len(d["now"][0]["members"]),
                                          (" (removed %s)" % ", ".join(removed.get(d["id"], []))) if gone > 0 else ""))
if write:
    with open("out/tier_history.jsonl", "a", encoding="utf-8") as f:
        for d in lines:
            f.write(json.dumps(d) + "\n")
    print("written: %d tier_history lines" % len(lines))
else:
    print("dry run: %d lines" % len(lines))
