#!/usr/bin/env python3
"""C2, pass 3, read-only: tally the coded grounds of the hosts' rulings (c2_vetting_grounds-p3.json) by concepts and by
rooms, check that the coding covers every concept listed in c2_vetting_concepts-p3.txt and nothing else, and apply the
declared statement: "a host admits guests by fit with the body it carried in" holds if ground a is the commonest among
concepts that give one (a, b or c), by concepts and by rooms.

    python3 out/_analysis/c2_vetting_tally.py
"""
import collections, json, os, re, sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
g = json.load(open(os.path.join(OUT, "_analysis", "c2_vetting_grounds-p3.json"), encoding="utf-8"))
listed, sub = set(), None
for line in open(os.path.join(OUT, "_analysis", "c2_vetting_concepts-p3.txt"), encoding="utf-8"):
    m = re.match(r"^== (\S+)", line)
    if m:
        sub = m.group(1)
        continue
    m = re.match(r"^    (c\d+) h", line)
    if m:
        listed.add("%s:%s" % (sub, m.group(1)))
coded = set(g["coded"])
if listed != coded:
    sys.exit("coding and list differ: missing %s; extra %s" % (sorted(listed - coded), sorted(coded - listed)))
by_c = collections.Counter(g["coded"].values())
by_r = collections.defaultdict(set)
for k, v in g["coded"].items():
    by_r[v].add(k.split(":")[0])
print("concepts coded: %d in %d rooms" % (len(coded), len(set(k.split(":")[0] for k in coded))))
for k in "abcde":
    print("  %s %-90s concepts %2d, rooms %d (%s)" % (k, g["grounds"][k][:90], by_c[k], len(by_r[k]), ", ".join(sorted(by_r[k]))))
gc = dict((k, by_c[k]) for k in "abc")
gr = dict((k, len(by_r[k])) for k in "abc")
print("concepts giving a ground (a, b or c): %d" % sum(gc.values()))
held = all(gc["a"] > gc[k] for k in "bc") and all(gr["a"] > gr[k] for k in "bc")
print("statement 'a host admits guests by fit with the body it carried in': %s (by concepts a %d, b %d, c %d; by rooms a %d, b %d, c %d)"
      % ("holds" if held else "fails", gc["a"], gc["b"], gc["c"], gr["a"], gr["b"], gr["c"]))
