"""Rule 0 record for B1, from leg B1b-02 on (supersedes b1_multiplace_write.py, whose bag text and
lithuania block were B1b-01's). Check a TSV of second placements against scheme_current.jsonl and
the lines already in multiplacement_log.jsonl, verify every cited concept belongs to that
second-order theme (through mem.py), and, with --write, append only the TSV lines not yet in the log,
plus one tier_history.jsonl line per third-order theme whose members this leg's unplacements changed.

usage: python3 out/_analysis/b1_multiplace_write2.py <tsv> --leg B1b-02 [--bag sub:tNN:T3-kept:T3-a,T3-b:"why"] [--write]
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
for l in open("out/multiplacement_log.jsonl"):
    d = json.loads(l)
    k = (d["sub"], d["theme_id"])
    logged.add((k, d["primary"]))
    if "additional" in d:
        logged.add((k, d["additional"]))
    for t in d.get("would_need", []):
        logged.add((k, t))

lines = open(tsv).read().splitlines()
head = lines[0].split("\t")
recs = [dict(zip(head, l.split("\t"))) for l in lines[1:] if l.strip()]
new = [r for r in recs if ((r["sub"], r["theme_id"]), r["additional"]) not in logged]

problems = []
seen = set(logged)
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
print("%d lines in the table, %d not yet in the log, %d problems" % (len(recs), len(new), len(problems)))
if problems or not write:
    sys.exit(0 if not problems else 1)

t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
with open("out/multiplacement_log.jsonl", "a") as f:
    for r in new:
        f.write(json.dumps({"t": t, "stage": "B1", "leg": leg, "sub": r["sub"], "theme_id": r["theme_id"],
                            "primary": r["primary"], "additional": r["additional"],
                            "codes": r["codes"].split(","), "why_not_one": r["why_not_one"],
                            "dispensable": r["additional"]}) + "\n")
    for b in bags:
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
print("written: %d multiplacement lines, %d bag lines, %d tier_history lines" % (len(new), len(bags), n))
