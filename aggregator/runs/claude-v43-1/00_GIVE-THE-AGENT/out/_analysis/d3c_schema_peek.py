#!/usr/bin/env python3
"""D3c: print the keys and one example per kind of line in verdicts-D.jsonl, verdicts-recheck-D.jsonl and
recheck-scope.json, the local_status lines of rooms/<sub>/model-D-recheck.md (counted), and the distinct values of
the last rulings' decision and kind. Read-only; for d3c_exception_report.py's field names.

    python3 out/_analysis/d3c_schema_peek.py
"""
import collections, glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


for name in ("verdicts-D.jsonl", "verdicts-recheck-D.jsonl"):
    L = jl(os.path.join(OUT, name))
    kinds = collections.Counter((r.get("ruled_by"), bool(r.get("recheck")), tuple(sorted(r.keys()))) for r in L)
    print("==", name, len(L))
    for k, n in kinds.items():
        print("  ", n, k)
    seen = set()
    for r in L:
        key = (r.get("ruled_by"), tuple(sorted(r.keys())))
        if key in seen:
            continue
        seen.add(key)
        print("   e.g.", json.dumps(r, ensure_ascii=False)[:700])
sc = json.load(open(os.path.join(OUT, "recheck-scope.json"), encoding="utf-8"))
print("== recheck-scope.json keys", sorted(sc.keys()), "affected", len(sc.get("affected_rooms", [])),
      "unaffected", len(sc.get("unaffected_rooms", {})))
st = collections.Counter()
ex = {}
for p in glob.glob(os.path.join(OUT, "rooms", "*", "model-D-recheck.md")):
    t = open(p, encoding="utf-8").read()
    m = re.findall(r".*local[_ ]status.*", t)
    k = m[0].strip()[:120] if m else "(no local_status line)"
    st[re.sub(r"\s+", " ", k)] += 1
    ex.setdefault(re.sub(r"\s+", " ", k), p)
print("== model-D-recheck.md files", sum(st.values()))
for k, n in st.most_common(12):
    print("  ", n, k, "|", os.path.relpath(ex[k], OUT))
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
print("== last rulings", len(last), collections.Counter((r.get("decision"), r.get("kind")) for r in last.values()))
pr = collections.Counter()
for name in ("adaptations.jsonl", "adaptations-recheck.jsonl"):
    for l in jl(os.path.join(OUT, name)):
        pr[(name, l.get("op"), l.get("portable"))] += 1
print("== op and portable by ledger", sorted(pr.items(), key=str))
