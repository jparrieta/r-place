#!/usr/bin/env python3
"""E1 section 5 (E1d): the versioned judgments side by side for the thirty reconstruction rooms, and the seeded
sample of disagreements.

    python3 out/audit-E1/versioned_judgments.py > out/audit-E1/versioned_judgments.json

The rule, declared before the run (E1d):
- For each room of out/reconstruction-E1.jsonl, four judgments, each with its model version:
  the fixed-global verdict of the first return, ruled (both readers agreeing, else the analyst's D3 ruling without
  recheck), from verdicts-D.jsonl; the same at the re-check (the readers' lines in rooms/<folder>/verdict-D-recheck.jsonl
  agreeing, else the D3 ruling with recheck); the current adapted-local status and grade from the effective return
  manifest (tools/adaptation_ledger.effective_rooms, which reads adaptation-returns.jsonl); the shared-branch status
  of the room's branch (the sample's, its most specific) from branches-D5.jsonl, or none; and beside them the
  reconstruction's fidelity, unresolved and contradicted claims and the readers' stated version.
- Seen before this rule was written: the manifest gives all 705 rooms local status unresolved and grade
  composes-with-residue, and branches-D5.jsonl gives 33 of 35 branches shared status unresolved (F09 and F32
  supported). So neither can mark a room as disagreeing, and the rule below does not use them; the counts are
  reported.
- A room's judgments disagree where (a) its first-return and re-check verdicts differ, or (b) its first-return verdict
  is composes and its fidelity is below the thirty's median, or is cannot-tell or does-not-compose and its fidelity
  is at or above the median.
- The seeded sample: the disagreeing rooms sorted by name, shuffled with random.Random(int(out/seed.txt, 16)), the
  first five (all, if five or fewer). They are examined by reading each room's case account in its packet against
  its verdict lines.
"""
import collections, glob, json, os, random, statistics, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from adaptation_ledger import effective_rooms  # noqa: E402


def jl(p):
    return [json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip()]


def main():
    R = jl("reconstruction-E1.jsonl")
    subs = [r["sub"] for r in R]
    first, first_mv, re_, re_mv = {}, {}, {}, {}
    for v in jl("verdicts-D.jsonl"):
        if not v.get("stage") and v["sub"] in subs:
            rs = sorted({x.get("verdict") for x in v.get("readers") or []})
            first[v["sub"]] = rs[0] if len(rs) == 1 else "split"
            first_mv[v["sub"]] = sorted({(x.get("model_version") or "")[:12] for x in v.get("readers") or []})
    for s in subs:
        rows = [json.loads(l) for l in open(os.path.join(OUT, "rooms", s, "verdict-D-recheck.jsonl"), encoding="utf-8") if l.strip()]
        vs = sorted({x.get("verdict") for x in rows})
        re_[s] = vs[0] if len(vs) == 1 else "split"
        re_mv[s] = sorted({(x.get("model_version") or "")[:12] for x in rows})
    ruled_by = {}
    for v in jl("verdicts-D.jsonl"):
        if v.get("stage") == "D3" and v.get("verdict") and v["sub"] in subs:
            if v.get("recheck"):
                re_[v["sub"]] = v["verdict"]; ruled_by[(v["sub"], "recheck")] = (v.get("model_version") or "")[:12]
            else:
                first[v["sub"]] = v["verdict"]; ruled_by[(v["sub"], "first")] = (v.get("model_version") or "")[:12]
    E = effective_rooms(OUT)
    B = {b["branch"]: b for b in jl("branches-D5.jsonl")}
    causes = json.load(open(os.path.join(OUT, "audit-E1", "reconstruction_causes.json"), encoding="utf-8"))["by_room"]
    med = statistics.median(r["fidelity"] for r in R)
    table = []
    for r in R:
        s, e = r["sub"], E.get(r["sub"], {})
        b = B.get(r["branch"])
        f1, f2 = first[s], re_[s]
        why = []
        if f1 != f2:
            why.append("verdict changed at the re-check")
        if f1 == "composes" and r["fidelity"] < med:
            why.append("composes, fidelity below the median")
        if f1 in ("cannot-tell", "does-not-compose") and r["fidelity"] >= med:
            why.append(f1 + ", fidelity at or above the median")
        table.append({"sub": s, "branch": r["branch"],
                      "first_return": f1, "first_return_model": ruled_by.get((s, "first")) or first_mv.get(s),
                      "recheck": f2, "recheck_model": ruled_by.get((s, "recheck")) or re_mv.get(s),
                      "local_status": e.get("local_status"), "local_grade": e.get("local_grade"),
                      "manifest_model": (e.get("model_version") or "")[:12], "manifest_phase": e.get("phase"),
                      "shared_status": b.get("shared_status") if b else None,
                      "branch_local_status": (b.get("local_statuses") or {}).get(s) if b else None,
                      "fidelity": r["fidelity"], "unresolved": r["unresolved"], "contradicted": r["contradicted"],
                      "claims": r["claims"], "reader_model": r["model_version"], "causes_read": causes.get(s, {}),
                      "disagree": why})
    dis = sorted(x["sub"] for x in table if x["disagree"])
    rnd = random.Random(int(open(os.path.join(OUT, "seed.txt")).read().split()[0], 16))
    pool = list(dis)
    rnd.shuffle(pool)
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1d):")[1].strip(),
                      "median_fidelity": med,
                      "manifest_all_rooms": dict(collections.Counter("%s / %s" % (x.get("local_status"), x.get("local_grade")) for x in E.values())),
                      "shared_status_all_branches": dict(collections.Counter(b.get("shared_status") for b in B.values())),
                      "first_vs_recheck": dict(collections.Counter("%s -> %s" % (x["first_return"], x["recheck"]) for x in table)),
                      "disagreeing": dis, "seeded_sample": pool[:5], "table": table}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
