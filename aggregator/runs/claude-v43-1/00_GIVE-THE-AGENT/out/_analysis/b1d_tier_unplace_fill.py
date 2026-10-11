"""Fill tier_history lines for unplacements that b1_multiplace_write4.py skipped.

write4 writes one members_changed line per T3 id per leg, from the leg's unplacements in the
diary, and skips an id that already has a line in the leg. A second unplacement from the same id
in the same leg is then not recorded. This script finds, for the leg, every unplacement in the
diary whose sub:theme does not appear as removed (in "was" but not in "now") in any of the leg's
lines for that id, and writes one line for it in write4's format.

Usage: python3 out/_analysis/b1d_tier_unplace_fill.py --leg B1d-06 [--write]
"""
import collections
import datetime
import json
import re
import subprocess
import sys

args = sys.argv[1:]
leg = args[args.index("--leg") + 1]
write = "--write" in args


def mem(*a):
    return subprocess.run(["python3", "tools/mem.py", *a, "--stage", "B1"], capture_output=True, text=True).stdout


members = {}
label = {}
for l in open("out/scheme/scheme_current.jsonl", encoding="utf-8"):
    d = json.loads(l)
    members[d["theme"]] = ["%s:%s" % (m["sub"], m["theme_id"]) for m in d.get("members", [])]
    label[d["theme"]] = d.get("label")

diary = mem("diary", "--grep", "unplaced", "--limit", "500")
removed = collections.defaultdict(list)
for line in diary.splitlines():
    m = re.search(r"\b%s\b.*unplaced (\S+):(t\d+) from (T3-\d+)" % re.escape(leg), line)
    if m:
        removed[m.group(3)].append("%s:%s" % (m.group(1), m.group(2)))

recorded = collections.defaultdict(set)
for l in open("out/tier_history.jsonl", encoding="utf-8"):
    d = json.loads(l)
    if d.get("leg") != leg or d.get("event") != "members_changed":
        continue
    was = set(d.get("was", {}).get("members", []))
    now = set()
    for n in d.get("now", []):
        now |= set(n.get("members", []))
    recorded[d["id"]] |= (was - now)

todo = []
for tid, items in sorted(removed.items()):
    for it in items:
        if it not in recorded[tid]:
            todo.append((tid, it))

t = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds")
for tid, it in todo:
    print("missing tier line: %s %s" % (tid, it))
if write and todo:
    with open("out/tier_history.jsonl", "a", encoding="utf-8") as f:
        for tid, it in todo:
            now = members.get(tid, [])
            f.write(json.dumps({"t": t, "stage": "B1", "leg": leg, "tier": "third", "id": tid, "move": "dropping",
                                "event": "members_changed",
                                "was": {"label": label.get(tid), "members": now + [it]},
                                "now": [{"id": tid, "members": now}],
                                "prompted_by": "rule 0, while placing the room",
                                "why": "single placement by rule 0; the second-order theme stays where its gate is met best"}) + "\n")
print("%d unplacements without a tier line%s" % (len(todo), "; written" if write and todo else ""))
