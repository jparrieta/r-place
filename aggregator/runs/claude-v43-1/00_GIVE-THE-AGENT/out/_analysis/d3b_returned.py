"""D3b: which rooms of the re-check scope came back, in the labelers' ledger and in the verdict fleet's.
Counts only; nothing is written."""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


subs = collections.Counter(r["sub"] for r in jl(os.path.join(OUT, "adaptations-recheck.jsonl")))
keys = set()
for r in jl(os.path.join(OUT, "adaptations-recheck.jsonl"))[:50]:
    keys |= set(r)
v = jl(os.path.join(OUT, "verdicts-recheck-D.jsonl"))
scope = json.load(open(os.path.join(OUT, "recheck-scope.json"), encoding="utf-8"))
aff = scope["affected_rooms"]
contrast = set(scope.get("contrasting_cases", []))
print("rooms in the labelers' re-check ledger: %d (lines %d)" % (len(subs), sum(subs.values())))
print("ledger fields:", sorted(keys))
vs = {r["sub"] for r in v}
print("verdict re-check lines: %d, rooms %d; fields: %s" % (len(v), len(vs), sorted(set(k for r in v for k in r))))
miss_l = [s for s in aff if s not in subs]
miss_v = [s for s in aff if s not in vs]
print("affected rooms with no labeler return: %d; of them contrasting cases: %d" % (len(miss_l), len(set(miss_l) & contrast)))
print("affected rooms with no verdict return: %d" % len(miss_v))
mr = [s for s in aff if os.path.exists(os.path.join(OUT, "rooms", s, "model-D-recheck.md"))]
print("model-D-recheck.md present: %d" % len(mr))
print("contrasting cases returned by labelers: %d of %d" % (len(contrast & set(subs)), len(contrast)))
print("first 40 rooms with no labeler return:", miss_l[:40])
print("rooms with no verdict return:", miss_v)
