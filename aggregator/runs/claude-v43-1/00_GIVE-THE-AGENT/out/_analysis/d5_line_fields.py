#!/usr/bin/env python3
"""D5: the fields of a branches-D5.jsonl line that must match the files, for one branch. Prints JSON.

    python3 out/_analysis/d5_line_fields.py --branch F01
"""
import argparse, collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--branch", required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


b = next(x for x in jl(os.path.join(OUT, "branches.jsonl")) if x["id"] == a.branch)
members = b["members"]
n = len(members)
# verdicts as the check reads them
by = collections.defaultdict(list)
for r in jl(os.path.join(OUT, "verdicts-D.jsonl")):
    by[r["sub"]].append(r)
verdict = {}
for s in members:
    rs = by.get(s, [])
    ruled = [r for r in rs if r.get("ruled_by") == "analyst"]
    if ruled:
        verdict[s] = ruled[-1]["verdict"]
        continue
    vs = {e["verdict"] for r in rs for e in (r.get("readers") or [])}
    verdict[s] = vs.pop() if len(vs) == 1 else None
vc = collections.Counter(v for v in verdict.values() if v)
local = vlib.local_return_states(OUT)
statuses = {s: local.get(s, {}).get("local_status", "unresolved") for s in members}
oe = {r["sub"]: r for r in jl(os.path.join(OUT, "organizing_end-A1.jsonl"))}
hrs = sorted(oe[s]["organizing_end_hour"] for s in members if isinstance(oe.get(s, {}).get("organizing_end_hour"), (int, float)))
med = hrs[len(hrs) // 2] if len(hrs) % 2 else (hrs[len(hrs) // 2 - 1] + hrs[len(hrs) // 2]) / 2.0
aft = [oe[s]["aftermath_share"] for s in members if isinstance(oe.get(s, {}).get("aftermath_share"), (int, float))]
wr = collections.Counter(oe.get(s, {}).get("work_remained", "silent") for s in members)
proj = next(p for p in jl(os.path.join(OUT, "projections-D4.jsonl")) if p.get("branch") == a.branch)
out = {"branch": a.branch, "name": b["name"], "n": n,
       "verdicts": {k: vc.get(k, 0) for k in ("composes", "composes-with-residue", "does-not-compose", "cannot-tell")},
       "unruled": sorted(s for s, v in verdict.items() if v is None),
       "uncomposed_members": sorted(s for s, v in verdict.items() if v == "does-not-compose"),
       "global_model_version": open(os.path.join(OUT, "handoff-D", "VERSION"), encoding="utf-8").read().strip().removeprefix("sha256:"),
       "local_model_version": vlib.model_hash(OUT),
       "local_statuses": statuses,
       "unresolved_members": sorted(s for s, st in statuses.items() if st != "validated"),
       "survival": {"median_organizing_end_hour": med, "aftermath_share": round(sum(aft) / len(aft), 4),
                    "work_remained": {k: wr.get(k, 0) for k in ("kept", "lost", "silent")}},
       "canvas": {"median_area_px": proj["canvas"]["median_area_px"],
                  "rooms_with_artwork": proj["canvas"]["rooms_with_artwork"]},
       "percentile_median_area": proj["canvas"]["percentile_median_area"]}
print(json.dumps(out, ensure_ascii=False))
