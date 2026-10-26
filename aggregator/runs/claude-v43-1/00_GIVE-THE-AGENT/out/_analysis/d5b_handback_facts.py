#!/usr/bin/env python3
"""D5b: the cross-branch facts the handback and the final message report, from branches-D5.jsonl,
findings.jsonl and verdicts-D.jsonl. Prints JSON.

    python3 out/_analysis/d5b_handback_facts.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


D = jl(os.path.join(OUT, "branches-D5.jsonl"))
F = jl(os.path.join(OUT, "findings.jsonl"))
V = jl(os.path.join(OUT, "verdicts-D.jsonl"))
B = {b["id"]: b for b in jl(os.path.join(OUT, "branches.jsonl"))}
inb = {s for b in B.values() for s in b["members"]}
first, recheck = {}, {}
for v in V:
    if v.get("recheck"):
        recheck[v["sub"]] = v.get("verdict")
    elif v.get("grade"):
        first[v["sub"]] = v.get("grade")
out = {"branches": len(D),
       "form_or_grouping": collections.Counter(d.get("form_or_grouping") for d in D),
       "forms": [d["branch"] for d in D if d.get("form_or_grouping") == "form"],
       "shared_status": collections.Counter(d.get("shared_status") for d in D),
       "arrows_present": sum(len(d.get("arrows_present") or []) for d in D),
       "arrows_absent": sum(len(d.get("arrows_absent") or []) for d in D),
       "arrows_not_testable": sum(len(d.get("arrows_not_testable") or []) for d in D),
       "propositions_fail": sorted({p if isinstance(p, str) else json.dumps(p) for d in D for p in (d.get("propositions_fail") or [])}),
       "propositions_hold": sorted({p if isinstance(p, str) else json.dumps(p) for d in D for p in (d.get("propositions_hold") or [])}),
       "verdicts_sum": dict(sum((collections.Counter(d.get("verdicts") or {}) for d in D), collections.Counter())),
       "cannot_tell_or_dnc_by_branch": {d["branch"]: {k: (d.get("verdicts") or {}).get(k, 0) for k in ("cannot-tell", "does-not-compose")}
                                        for d in D if (d.get("verdicts") or {}).get("cannot-tell") or (d.get("verdicts") or {}).get("does-not-compose")},
       "first_return_uncomposed": sorted([s for s, g in first.items() if g in ("does-not-compose", "cannot-tell")]),
       "first_return_uncomposed_in_branch": sorted([s for s, g in first.items() if g in ("does-not-compose", "cannot-tell") and s in inb]),
       "recheck_uncomposed": sorted([s for s, g in recheck.items() if g in ("does-not-compose", "cannot-tell")]),
       "recheck_uncomposed_in_branch": sorted([s for s, g in recheck.items() if g in ("does-not-compose", "cannot-tell") and s in inb]),
       "findings_lines": len(F),
       "findings_D5": [{k: f.get(k) for k in ("id", "stage", "leg", "supersedes", "status")} for f in F if f.get("stage") == "D5" or str(f.get("leg", "")).startswith("D5")],
       }
# verdicts as the branch lines read them (d5_line_fields.py): the analyst's last ruling, else the readers' one verdict
by = collections.defaultdict(list)
for r in V:
    by[r["sub"]].append(r)
vrule = {}
for s, rs in by.items():
    ruled = [r for r in rs if r.get("ruled_by") == "analyst"]
    if ruled:
        vrule[s] = ruled[-1]["verdict"]
        continue
    vs = {e["verdict"] for r in rs for e in (r.get("readers") or [])}
    vrule[s] = vs.pop() if len(vs) == 1 else None
out["uncomposed_in_branch_by_line_rule"] = {s: {"verdict": vrule.get(s), "branches": sorted(b for b in B if s in B[b]["members"])}
                                           for s in sorted(inb, key=str.lower) if vrule.get(s) in ("cannot-tell", "does-not-compose")}
out["uncomposed_all_by_line_rule"] = collections.Counter(v for v in vrule.values() if v in ("cannot-tell", "does-not-compose"))
out["unruled_in_branch"] = sorted(s for s in inb if vrule.get(s) is None)
print(json.dumps(out, ensure_ascii=False, default=str))
