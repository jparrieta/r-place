"""B1e: a digest of third-order themes, for writing their gates.

For each T3 id given: its label, trigger and leg (theme_discovery.jsonl); its members and rooms (through
`mem.py scheme <T3>`); its rule 0 partners (multiplacement_log.jsonl: lines where it is primary or additional,
and bag lines naming it); its tier_history.jsonl events; and a seeded sample of its members' second-order
labels (seed "b1e:<T3>", so the sample is the same on every run).

usage: python3 out/_analysis/b1e_digest.py T3-001 T3-023 ... [--k 40]
"""
import collections
import json
import random
import subprocess
import sys

argv = sys.argv[1:]
k = 40
if "--k" in argv:
    i = argv.index("--k")
    k = int(argv[i + 1])
    del argv[i:i + 2]


def mem(*a):
    return subprocess.run(["python3", "tools/mem.py", *a, "--stage", "B1"], capture_output=True, text=True).stdout


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


disc = {d["theme"]: d for d in jl("out/theme_discovery.jsonl")}
mp = jl("out/multiplacement_log.jsonl")
th = jl("out/tier_history.jsonl")

for t in argv:
    out = mem("scheme", t, "--limit", "100000")
    lines = out.splitlines()
    head = lines[0] if lines else t
    members = []
    for x in lines[1:]:
        if x.startswith("  ") and not x.startswith("   "):
            parts = x.strip().split("  ", 1)
            if len(parts) == 2:
                members.append((parts[0].strip(), parts[1].strip()))
    rooms = collections.Counter(s for s, _ in members)
    d = disc.get(t, {})
    print("== %s" % head)
    print("   trigger %s (leg %s); members %d; rooms %d" % (d.get("trigger"), d.get("leg"), len(members), len(rooms)))
    print("   rooms with most members: %s" % ", ".join("%s %d" % (s, n) for s, n in rooms.most_common(8)))
    part = collections.Counter()
    for r in mp:
        if r.get("item_is_a_bag"):
            if r.get("primary") == t:
                for x in r.get("would_need") or []:
                    part["bag with " + x] += 1
            elif t in (r.get("would_need") or []):
                part["in bag kept " + r.get("primary", "?")] += 1
        else:
            if r.get("primary") == t and r.get("additional"):
                part["+" + r["additional"]] += 1
            elif r.get("additional") == t:
                part["beside " + r.get("primary", "?")] += 1
    print("   rule 0 partners: %s" % (", ".join("%s %d" % (p, n) for p, n in part.most_common(10)) or "none"))
    for r in th:
        if r.get("id") == t:
            print("   tier %s %s %s: %s" % (r.get("leg"), r.get("event"), r.get("move"), str(r.get("why") or "")[:260]))
    rng = random.Random("b1e:" + t)
    sample = members if len(members) <= k else rng.sample(members, k)
    for s, lab in sample:
        print("   - %s: %s" % (s, lab[:110]))
    print()
