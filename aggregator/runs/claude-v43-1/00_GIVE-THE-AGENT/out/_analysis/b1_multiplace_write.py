"""Rule 0 record for B1: check a TSV of second placements against scheme_current.jsonl, verify that
every cited concept belongs to that second-order theme (through mem.py), and, with --write, append
the multiplacement_log.jsonl lines, the item-is-a-bag lines, and one tier_history.jsonl line per
third-order theme whose members the unplacements of this leg changed.

usage: python3 out/_analysis/b1_multiplace_write.py <tsv> --leg B1b-01 [--bag sub:tNN:T3-kept:T3-a,T3-b ...] [--write]
"""
import collections
import datetime
import json
import re
import subprocess
import sys

argv = sys.argv[1:]
tsv = argv[0]
leg = argv[argv.index("--leg") + 1]
write = "--write" in argv
bags = [argv[i + 1] for i, a in enumerate(argv) if a == "--bag"]


def mem(*a):
    return subprocess.run(["python3", "tools/mem.py", *a, "--stage", "B1"], capture_output=True, text=True).stdout


rows = [json.loads(l) for l in open("out/scheme/scheme_current.jsonl")]
label = {r["theme"]: r["label"] for r in rows}
placed = collections.defaultdict(set)
members = {}
for r in rows:
    members[r["theme"]] = [(m["sub"], m["theme_id"]) for m in r["members"]]
    for m in r["members"]:
        placed[(m["sub"], m["theme_id"])].add(r["theme"])

lines = open(tsv).read().splitlines()
head = lines[0].split("\t")
recs = [dict(zip(head, l.split("\t"))) for l in lines[1:] if l.strip()]

problems = []
seen = set()
for r in recs:
    k = (r["sub"], r["theme_id"])
    have = placed.get(k, set())
    if r["primary"] not in have or r["additional"] not in have:
        problems.append("not in scheme as written: %s:%s %s + %s (has %s)" % (k[0], k[1], r["primary"], r["additional"], sorted(have)))
    seen.add((k, r["additional"]))
    seen.add((k, r["primary"]))
for k, v in placed.items():
    if len(v) > 1:
        for t in v:
            if (k, t) not in seen:
                problems.append("placement with no line: %s:%s %s (all %s)" % (k[0], k[1], t, sorted(v)))

cache = {}
for r in recs:
    k = (r["sub"], r["theme_id"])
    if k not in cache:
        out = mem("codes", "--sub", r["sub"], "--second", r["theme_id"], "--limit", "3000")
        cache[k] = set(re.findall(r"^(c\d{4})", out, re.M))
    for c in r["codes"].split(","):
        if c not in cache[k]:
            problems.append("concept %s is not under %s:%s" % (c, k[0], k[1]))

for p in problems:
    print("PROBLEM", p)
print("%d lines, %d problems" % (len(recs), len(problems)))
if problems or not write:
    sys.exit(0 if not problems else 1)

t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
with open("out/multiplacement_log.jsonl", "a") as f:
    for r in recs:
        f.write(json.dumps({"t": t, "stage": "B1", "leg": leg, "sub": r["sub"], "theme_id": r["theme_id"],
                            "primary": r["primary"], "additional": r["additional"],
                            "codes": r["codes"].split(","), "why_not_one": r["why_not_one"],
                            "dispensable": r["additional"]}) + "\n")
    for b in bags:
        sub, tid, kept, wanted = b.split(":")
        f.write(json.dumps({"t": t, "stage": "B1", "leg": leg, "sub": sub, "theme_id": tid, "primary": kept,
                            "item_is_a_bag": True, "would_need": wanted.split(","),
                            "why_not_one": "the theme holds five doings (deals, help sent, room granted, a hub sub, "
                                           "messages to placers); beyond three, rule 0 places it once"}) + "\n")

# tier_history: the unplacements of this leg, from the diary
diary = mem("diary", "--grep", "unplaced", "--limit", "500")
removed = collections.defaultdict(list)
for line in diary.splitlines():
    m = re.search(r"\b%s\b.*unplaced (\S+):(t\d+) from (T3-\d+)" % re.escape(leg), line)
    if m:
        removed[m.group(3)].append((m.group(1), m.group(2)))
added = collections.defaultdict(list)
for line in mem("diary", "--grep", "lithuania:t05", "--limit", "50").splitlines():
    m = re.search(r"\b%s\b.*placed lithuania:t05 in (T3-083)" % re.escape(leg), line)
    if m:
        added[m.group(1)].append(("lithuania", "t05"))
with open("out/tier_history.jsonl", "a") as f:
    for tid in sorted(set(removed) | set(added)):
        now = members.get(tid, [])
        was = [x for x in now if x not in added[tid]] + removed[tid]
        f.write(json.dumps({"t": t, "stage": "B1", "leg": leg, "tier": "third", "id": tid, "move": "dropping",
                            "event": "members_changed",
                            "was": {"label": label.get(tid), "members": ["%s:%s" % x for x in was]},
                            "now": [{"id": tid, "members": ["%s:%s" % x for x in now]}],
                            "prompted_by": "a check: validate.py warned that 88 second-order themes sat under two to five "
                                           "third-order themes without the rule 0 record",
                            "why": "single placement by rule 0; a second or third placement kept only where a concept of "
                                   "its own supports it and the primary cannot carry it, logged in multiplacement_log.jsonl"}) + "\n")
print("written: %d multiplacement lines, %d bag lines, %d tier_history lines"
      % (len(recs), len(bags), len(set(removed) | set(added))))
