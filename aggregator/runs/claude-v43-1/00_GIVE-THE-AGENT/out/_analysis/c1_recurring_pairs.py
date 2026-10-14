#!/usr/bin/env python3
"""C1 section 1, read-only: what each recurring (primary, additional) pair of stage B3's pair table became at C1.
Reads the 20 rows of multiplacement_register-B3.md's table, and for each unordered pair gives: the pair-test call
(c1_pair_calls-*.json), the lines of assignments_final.jsonl now carrying both themes (and with which first), and the
gates amended at C1 on either theme whose old or new sentence names the other. Then the two modifier candidates of
the table (a theme placed as an addition far more than as a primary): their counts as first and as later theme, on
the settled line (assign_final.jsonl) and now.

    python3 out/_analysis/c1_recurring_pairs.py
"""
import collections, glob, json, os, re

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jl(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


txt = open(os.path.join(OUT, "multiplacement_register-B3.md"), encoding="utf-8").read()
rows = [(int(m.group(1)), m.group(2), m.group(3), int(m.group(4)))
        for m in re.finditer(r"^\| (\d+) \| (T3-\d{3}) \| (T3-\d{3}) \| (\d+) \|", txt, re.M)][:20]
calls = {}
for p in sorted(glob.glob(os.path.join(OUT, "_analysis", "c1_pair_calls-*.json"))):
    for c in json.load(open(p, encoding="utf-8"))["calls"]:
        calls[tuple(sorted(c["pair"]))] = c
pt = json.load(open(os.path.join(OUT, "_analysis", "c1_pair_test.json"), encoding="utf-8"))
tested = dict((tuple(sorted(q["pair"])), q) for q in pt["pairs"])
now = jl("assignments_final.jsonl")
gh = jl("gate_history.jsonl")
names = dict((t["id"], t["name"]) for t in jl("scheme_v2.jsonl"))
seen = set()
print("n | B3 pair (primary, additional) | B3 lines | pair test | now: lines with both (first a / first b) | gates naming the other")
for n, a, b, k in rows:
    key = tuple(sorted((a, b)))
    both = [r for r in now if a in (r.get("third_order") or []) and b in (r.get("third_order") or [])]
    fa = sum(1 for r in both if r["third_order"][0] == a)
    fb = sum(1 for r in both if r["third_order"][0] == b)
    gates = [g["ref"] for g in gh if g["theme"] in key and (set(key) - {g["theme"]}).pop() in json.dumps([g.get("was"), g.get("now")])]
    c = calls.get(key)
    q = tested.get(key)
    if c:
        call = "#%d %s" % (c["n"], c["call"])
    elif q:
        call = "no call owed: arguable rate %.3f, under the bar %.3f" % (q["rate"], pt["threshold"])
    else:
        call = "not in the pair test (fewer than ten lines at pass 6)"
    print("%d | %s %s, %s %s | %d | %s | %d (%d / %d) | %s%s" % (
        n, a, names.get(a, "")[:30], b, names.get(b, "")[:30], k, call,
        len(both), fa, fb, ", ".join(gates) or "-", "  [same pair as an earlier row]" if key in seen else ""))
    seen.add(key)
settled = jl("assign_final.jsonl")
for t in ("T3-089", "T3-152"):
    def cnt(rs):
        first = sum(1 for r in rs if (r.get("third_order") or [None])[0] == t)
        later = sum(1 for r in rs if t in (r.get("third_order") or [])[1:])
        return first, later
    print("%s %s: settled line first %d, later %d; now first %d, later %d" % ((t, names.get(t, "")) + cnt(settled) + cnt(now)))
