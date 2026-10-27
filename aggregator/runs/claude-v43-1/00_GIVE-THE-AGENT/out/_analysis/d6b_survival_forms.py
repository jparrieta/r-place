#!/usr/bin/env python3
"""D6b: the survival reading by room form, from the record, for the telling (stage D6, section 2), and the rooms the
model could not compose. Per form (all members and defining members; D's two splits beside it): the median
organizing_end_hour, the end bands (before 64, 64 to 73, 73 on), the mean aftermath share and the rooms with coordinating
turns after hour 73, the work_remained field (kept, lost, silent: silence counted), and, for the members in a branch, the
D5b re-reading of the field (stood, gone, during, other, unclear, silent). The canvas is not read (rule 7). Also: each
form's rooms in no branch, and the rooms whose verdict (projections.py's map) is does-not-compose or cannot-tell, with
their form, coded concepts and branches. Prints JSON.

    python3 out/_analysis/d6b_survival_forms.py > out/_analysis/d6b_survival_forms.json
"""
import collections, csv, json, os, statistics, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import projections  # noqa: E402

oe = {json.loads(l)["sub"]: json.loads(l) for l in open(os.path.join(OUT, "organizing_end-A1.jsonl"), encoding="utf-8")
      if l.strip()}
reading = {}
for i in range(1, 6):
    reading.update(json.load(open(os.path.join(AN, "d5b_wr_read%d.json" % i), encoding="utf-8")))
reading.update({"detroitlions": ["unclear"], "placetardis": ["unclear"], "liverpoolfc": ["unclear"]})  # d5b overrides
B = [json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8")]
branches_of = collections.defaultdict(list)
for b in B:
    for s in b["members"]:
        branches_of[s].append(b["id"])
rows = list(csv.DictReader(open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8"), delimiter="\t"))
verdict = projections.final_verdicts(OUT)
KINDS = ["stood", "gone", "during", "other", "unclear", "silent"]


def block(members):
    m = sorted(members, key=str.lower)
    ends = [oe[s]["organizing_end_hour"] for s in m if isinstance(oe[s].get("organizing_end_hour"), (int, float))]
    aft = [oe[s]["aftermath_share"] for s in m if isinstance(oe[s].get("aftermath_share"), (int, float))]
    field = collections.Counter(oe[s]["work_remained"] for s in m)
    read = collections.Counter(reading[s][0] for s in m if s in reading)
    return {"n": len(m),
            "median_end": round(statistics.median(ends), 2) if ends else None,
            "end_before_64": sum(1 for e in ends if e < 64), "end_64_73": sum(1 for e in ends if 64 <= e < 73),
            "end_73_on": sum(1 for e in ends if e >= 73),
            "aftermath_mean": round(statistics.mean(aft), 4) if aft else None,
            "rooms_with_aftermath_coord": sum(1 for s in m if oe[s].get("aftermath_coordinating_codes")),
            "field": {k: field.get(k, 0) for k in ("kept", "lost", "silent")},
            "field_kept_share": round(field.get("kept", 0) / len(m), 3) if m else None,
            "in_a_branch": sum(1 for s in m if s in reading),
            "reading": {k: read.get(k, 0) for k in KINDS}}


res = {"forms": {}, "splits": {}, "population": block(set(oe))}
for f in "ABCDEF":
    allm = [r["room"] for r in rows if r["form"] == f]
    dfn = [r["room"] for r in rows if r["form"] == f and r["role"] == "defining"]
    res["forms"][f] = {"all": block(allm), "defining": block(dfn),
                       "in_no_branch": sum(1 for s in allm if not branches_of.get(s))}
for sp in ("D.1", "D.2"):
    dfn = [r["room"] for r in rows if r["form"] == "D" and r["role"] == "defining" and r["k9"].startswith(sp)]
    res["splits"][sp] = block(dfn)
form_of = {r["room"]: r["form"] for r in rows}
size_of = {r["room"]: int(r["coded_concepts"]) for r in rows}
res["uncomposed"] = [{"sub": s, "verdict": verdict.get(s), "form": form_of.get(s), "coded_concepts": size_of.get(s),
                      "role": next((r["role"] for r in rows if r["room"] == s), None),
                      "branches": branches_of.get(s, []), "work_remained": oe[s]["work_remained"],
                      "organizing_end_hour": oe[s].get("organizing_end_hour")}
                     for s in sorted(verdict, key=str.lower) if verdict.get(s) in ("does-not-compose", "cannot-tell")]
res["verdicts_all"] = dict(collections.Counter(verdict.get(s) for s in oe))
res["median_concepts_all"] = statistics.median(size_of.values())
print(json.dumps(res, ensure_ascii=False))
