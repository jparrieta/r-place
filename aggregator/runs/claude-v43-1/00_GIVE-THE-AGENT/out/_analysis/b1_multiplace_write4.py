"""Rule 0 record for B1, from B1b-29 on (supersedes b1_multiplace_write3.py, which slowed within a leg:
it started one mem.py process for every room and theme of the leg's whole table, on every run, and the
bag write ran it again). Records and checks are the same as write3. What changes:

- the concept check (does every cited code belong to that second-order theme) runs only on the rows not
  yet in the log; rows already logged were checked when they were written;
- it asks mem.py once per room among those rows (codes --sub <room>, every code with its theme), not once
  per room and theme, so a normal write, one room's rows, makes one mem.py call for the check;
- a bag already in the log for the same room, theme and kept kind is not written twice.

The in-memory checks still cover the whole table: every row's primary and additional are placed as
written, and every theme placed in more than one kind has a line or a bag.

usage: python3 out/_analysis/b1_multiplace_write4.py <tsv> --leg B1b-29 [--bag sub:tNN:T3-kept:T3-a,T3-b:"why"] [--write]
       [--check-all]   run the concept check on every row of the table, one mem.py call per room (a test)
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

logged = set()
triples = set()
bagged = set()
for l in open("out/multiplacement_log.jsonl"):
    d = json.loads(l)
    k = (d["sub"], d["theme_id"])
    logged.add((k, d["primary"]))
    if "additional" in d:
        logged.add((k, d["additional"]))
        triples.add((k, d["primary"], d["additional"]))
    for t in d.get("would_need", []):
        logged.add((k, t))
    if d.get("item_is_a_bag"):
        bagged.add((k, d["primary"]))

lines = open(tsv).read().splitlines()
head = lines[0].split("\t")
recs = [dict(zip(head, l.split("\t"))) for l in lines[1:] if l.strip()]
new = [r for r in recs if ((r["sub"], r["theme_id"]), r["primary"], r["additional"]) not in triples]

problems = []
seen = set(logged)
for r in recs:
    k = (r["sub"], r["theme_id"])
    have = placed.get(k, set())
    if r["primary"] not in have or r["additional"] not in have:
        problems.append("not in scheme as written: %s:%s %s + %s (has %s)" % (k[0], k[1], r["primary"], r["additional"], sorted(have)))
    seen.add((k, r["additional"]))
    seen.add((k, r["primary"]))
for b in bags:
    sub, tid, kept, wanted, why = b.split(":", 4)
    for t in [kept] + wanted.split(","):
        seen.add(((sub, tid), t))
for k, v in placed.items():
    if len(v) > 1:
        for t in v:
            if (k, t) not in seen:
                problems.append("placement with no line: %s:%s %s (all %s)" % (k[0], k[1], t, sorted(v)))

# concept check: new rows only (every row with --check-all), one mem.py call per room
checked = recs if "--check-all" in argv else new
codes_of = {}
for sub in sorted({r["sub"] for r in checked}):
    out = mem("codes", "--sub", sub, "--limit", "20000")
    m = collections.defaultdict(set)
    for c, tid in re.findall(r"^(c\d{4})\s+\S+\s+(t\d+)", out, re.M):
        m[tid].add(c)
    codes_of[sub] = m
for r in checked:
    have = codes_of[r["sub"]].get(r["theme_id"], set())
    for c in r["codes"].split(","):
        if c not in have:
            problems.append("concept %s is not under %s:%s" % (c, r["sub"], r["theme_id"]))

new_bags = []
for b in bags:
    sub, tid, kept, wanted, why = b.split(":", 4)
    if ((sub, tid), kept) in bagged:
        print("bag already in the log, not written again: %s:%s %s" % (sub, tid, kept))
    else:
        new_bags.append(b)

for p in problems:
    print("PROBLEM", p)
print("%d lines in the table, %d not yet in the log, %d bags new, %d mem.py calls for the concept check, %d problems"
      % (len(recs), len(new), len(new_bags), len(codes_of), len(problems)))
if problems or not write:
    sys.exit(0 if not problems else 1)

t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
with open("out/multiplacement_log.jsonl", "a") as f:
    for r in new:
        f.write(json.dumps({"t": t, "stage": "B1", "leg": leg, "sub": r["sub"], "theme_id": r["theme_id"],
                            "primary": r["primary"], "additional": r["additional"],
                            "codes": r["codes"].split(","), "why_not_one": r["why_not_one"],
                            "dispensable": r["additional"]}) + "\n")
    for b in new_bags:
        sub, tid, kept, wanted, why = b.split(":", 4)
        f.write(json.dumps({"t": t, "stage": "B1", "leg": leg, "sub": sub, "theme_id": tid, "primary": kept,
                            "item_is_a_bag": True, "would_need": wanted.split(","), "why_not_one": why}) + "\n")

# tier_history: this leg's unplacements, from the diary
diary = mem("diary", "--grep", "unplaced", "--limit", "500")
removed = collections.defaultdict(list)
for line in diary.splitlines():
    m = re.search(r"\b%s\b.*unplaced (\S+):(t\d+) from (T3-\d+)" % re.escape(leg), line)
    if m:
        removed[m.group(3)].append((m.group(1), m.group(2)))
done = set()
for l in open("out/tier_history.jsonl"):
    d = json.loads(l)
    if d.get("leg") == leg:
        done.add(d["id"])
n = 0
with open("out/tier_history.jsonl", "a") as f:
    for tid in sorted(set(removed) - done):
        now = members.get(tid, [])
        was = now + removed[tid]
        f.write(json.dumps({"t": t, "stage": "B1", "leg": leg, "tier": "third", "id": tid, "move": "dropping",
                            "event": "members_changed",
                            "was": {"label": label.get(tid), "members": ["%s:%s" % x for x in was]},
                            "now": [{"id": tid, "members": ["%s:%s" % x for x in now]}],
                            "prompted_by": "rule 0, while placing the room",
                            "why": "single placement by rule 0; the second-order theme stays where its gate is met best"}) + "\n")
        n += 1
print("written: %d multiplacement lines, %d bag lines, %d tier_history lines" % (len(new), len(new_bags), n))
