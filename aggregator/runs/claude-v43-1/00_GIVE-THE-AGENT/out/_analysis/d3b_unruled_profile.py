"""D3b: the re-check lines still unruled, by element and op (absent split by observation). Counts only."""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


new = jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
ruled = {r["adaptation"] for r in jl(os.path.join(OUT, "adjudications.jsonl"))}
un = [r for r in new if r["id"] not in ruled]
print("re-check lines %d; ruled %d; unruled %d" % (len(new), len(new) - len(un), len(un)))
by_el = collections.defaultdict(collections.Counter)
for r in un:
    op = r["op"] + (":" + str(r.get("observation")) if r["op"] == "absent" else "")
    by_el[r.get("element") or "-"][op] += 1
ops = sorted({k for c in by_el.values() for k in c})
print("element  total  " + "  ".join(ops))
for e in sorted(by_el, key=lambda e: -sum(by_el[e].values())):
    c = by_el[e]
    print("%-7s %6d  %s" % (e, sum(c.values()), "  ".join("%s=%d" % (k, c[k]) for k in ops if c[k])))
print("by op:", dict(collections.Counter(r["op"] for r in un)))
print("portable false among unruled:", sum(1 for r in un if r.get("portable") is False))
