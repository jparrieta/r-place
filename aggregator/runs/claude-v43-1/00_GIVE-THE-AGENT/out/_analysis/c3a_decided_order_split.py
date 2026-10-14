#!/usr/bin/env python3
"""C3a, abductive read prompted by O'Mahony and Ferraro (2007): does decided order (rooms placed on T4-011 Decided
order) gather in rooms that rule on other rooms' works (hosts vetting guests' requests to build, T3-162; colour factions,
T4-023 Neo-tribes) more than in other rooms, held to room size?

Room sets come from `mem.py rooms --with <id>` (placed themes over the 705 analysed rooms); size from `mem.py facts
--field items_in_window`. The null shuffles which rooms carry decided order within each items_in_window quartile
(2000 shuffles, seed 20261014), keeping each quartile's count, and counts how many decided-order rooms fall in the
ruling set. Reads the store through mem.py only; writes nothing.

    python3 out/_analysis/c3a_decided_order_split.py
"""
import json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def mem(args):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py")] + args, cwd=ROOT, capture_output=True,
                       text=True)
    return p.stdout


def rooms_with(tid):
    out = mem(["rooms", "--with", tid, "--limit", "10000"])
    return set(l.strip() for l in out.splitlines() if l.startswith("  ") and l.strip())


facts = mem(["facts", "--field", "items_in_window", "--json", "--limit", "10000"])
items = dict((r["sub"], r["items_in_window"]) for r in (json.loads(l) for l in facts.splitlines() if l.startswith("{")))
if len(items) != 705:
    sys.exit("expected 705 rooms, got %d" % len(items))
order = sorted(items, key=lambda s: (items[s], s))
n = len(order)
quart = dict((s, i * 4 // n) for i, s in enumerate(order))
D = rooms_with("T4-011")
H = rooms_with("T3-162")
F = rooms_with("T4-023")
G = rooms_with("T3-035") | rooms_with("T3-099")
A = rooms_with("T3-094")
R = H | F
print("decided order (T4-011): %d rooms; hosts vetting guests (T3-162): %d; colour factions (T4-023): %d; "
      "ruling set (either): %d; guests asking a host (T3-035 or T3-099): %d; disputing who approves (T3-094): %d"
      % (len(D), len(H), len(F), len(R), len(G), len(A)))


def rate(group, name):
    k = len(D & group)
    print("  %-34s %3d rooms, %3d with decided order (%.3f)" % (name, len(group), k, k / len(group) if group else 0))


rate(H, "hosts vetting guests")
rate(F, "colour factions")
rate(R, "ruling set")
rate(G, "guests asking a host")
rate(A, "disputing who approves a spot")
rate(set(items) - R, "all other rooms")
print("by items_in_window quartile (decided order in ruling set / ruling set; in others / others):")
for q in range(4):
    qs = set(s for s in items if quart[s] == q)
    r, o = qs & R, qs - R
    print("  quartile %d (%d to %d items): %d of %d (%.3f) against %d of %d (%.3f)" % (
        q + 1, items[min(qs, key=lambda s: items[s])], items[max(qs, key=lambda s: items[s])], len(D & r), len(r),
        len(D & r) / len(r) if r else 0, len(D & o), len(o), len(D & o) / len(o) if o else 0))
obs = len(D & R)
rnd = random.Random(20261014)
byq = [sorted(s for s in items if quart[s] == q) for q in range(4)]
kq = [len(D & set(b)) for b in byq]
hits = 0
null = []
for _ in range(2000):
    d = set()
    [d.update(rnd.sample(b, k)) for b, k in zip(byq, kq)]
    v = len(d & R)
    null.append(v)
    hits += v >= obs
null.sort()
print("decided-order rooms in the ruling set: %d; null mean %.1f, 95th percentile %d, p (one-sided) %.4f" % (
    obs, sum(null) / len(null), null[int(0.95 * len(null))], (hits + 1) / (len(null) + 1)))
print("decided order and hosts vetting guests: %s" % ", ".join(sorted(D & H, key=str.lower)))
print("decided order and colour factions: %s" % ", ".join(sorted(D & F, key=str.lower)))
print("decided order, neither: %s" % ", ".join(sorted(D - R, key=str.lower)))
