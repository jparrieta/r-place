#!/usr/bin/env python3
"""D3: counts for closing one element group (stage D3, moments to log: each group closed with its counts by
decision). Selects the element's lines as `mem.py adaptations --element <id>` does and reads each line's last
adjudication. Prints counts only, never a line: lines by op and decision; the kind of every ruled line (the
adjudication's kind where I reclassified, else the labeler's); the lines still unruled or pending; absent lines split
by observation (J, 12:59); accepted corrections by lifted node at the third and fourth order with their rooms (the §2
trigger); and the repairs comparison (J, 12:59): decisions in rooms with and without same-session repairs
(DROPS/D/REPAIRS.tsv). Writes nothing.

    python3 out/_analysis/d3_group_close.py --element P01
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


sel = [l for l in jl(os.path.join(OUT, "adaptations.jsonl")) if l.get("element") == a.element]
adj = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    adj[r.get("adaptation")] = r
rep = {}
rp = os.path.join(ROOT, "DROPS", "D", "REPAIRS.tsv")
if os.path.exists(rp):
    for l in open(rp, encoding="utf-8"):
        c = l.rstrip("\n").split("\t")
        if len(c) >= 2 and not l.startswith(("#", "sub\t")):
            rep[c[0]] = c[1]


def repaired(sub):
    v = rep.get(sub)
    try:
        return int(v) > 0
    except (TypeError, ValueError):
        return None


by_op = collections.defaultdict(collections.Counter)
kinds = collections.defaultdict(collections.Counter)
unruled = collections.Counter()
absent_obs = collections.defaultdict(collections.Counter)
corr = collections.defaultdict(set)
reps = collections.defaultdict(collections.Counter)
rooms = set()
for l in sel:
    r = adj.get(l["id"])
    d = r.get("decision") if r else None
    rooms.add(l["sub"])
    if d is None or d == "pending":
        unruled[l["op"]] += 1
    by_op[l["op"]][d or "unruled"] += 1
    k = (r or {}).get("kind") or l.get("kind") or "-"
    kinds[d or "unruled"][k] += 1
    if l["op"] == "absent":
        absent_obs[l.get("observation") or "-"][d or "unruled"] += 1
    if d in ("accept", "modify") and k == "correction":
        lift = [str(x) for x in (l.get("lift") or [])]
        for node in lift:
            if node.startswith(("T3-", "T4-")):
                corr[node].add(l["sub"])
    rp_ = repaired(l["sub"])
    reps["repaired" if rp_ else ("unrepaired" if rp_ is False else "no entry")][d or "unruled"] += 1

print("%s: %d lines in %d rooms" % (a.element, len(sel), len(rooms)))
dec = sorted({d for c in by_op.values() for d in c})
print("%-15s %s %7s" % ("op", " ".join("%10s" % d for d in dec), "total"))
for op in sorted(by_op):
    print("%-15s %s %7d" % (op, " ".join("%10d" % by_op[op][d] for d in dec), sum(by_op[op].values())))
tot = collections.Counter()
for c in by_op.values():
    tot.update(c)
print("%-15s %s %7d" % ("all", " ".join("%10d" % tot[d] for d in dec), sum(tot.values())))
print("\nunruled or pending: %d %s" % (sum(unruled.values()), dict(unruled)))
print("\nkind by decision:")
for d in sorted(kinds):
    print("  %-11s %s" % (d, dict(sorted(kinds[d].items()))))
print("\nabsent lines by observation:")
for o in sorted(absent_obs):
    print("  %-16s %s" % (o, dict(absent_obs[o])))
print("\naccepted corrections by lifted node (third and fourth order), rooms:")
if not corr:
    print("  none")
for node in sorted(corr):
    print("  %-8s %d rooms: %s" % (node, len(corr[node]), ", ".join(sorted(corr[node]))))
print("\nrepairs comparison (lines by decision):")
for g in ("repaired", "unrepaired", "no entry"):
    c = reps.get(g)
    if c:
        n = sum(c.values())
        print("  %-10s %4d lines: %s; accept share %.3f" % (g, n, dict(sorted(c.items())), c["accept"] / n))
