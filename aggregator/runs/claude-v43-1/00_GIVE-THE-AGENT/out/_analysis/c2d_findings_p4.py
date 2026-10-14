#!/usr/bin/env python3
"""C2d-01, pass 4: re-examine the findings the recuts and tests touch (rule 14: a revision is a new line carrying the
id it supersedes). Numbers are read from model/arrows.jsonl as pass 4 rewrote it and from the evidence files.

  F-008  its coalition clause rested on the coalition element with hosting and cited naruto c0168, whose room joined
         a coalition before any upkeep: restated on the narrowed element, evidence criticalrole.
  F-011  membership carried in, narrowed to the nation beyond the mark: below the null mean; the reverse shows and is
         not tested.
  F-010  the host's line by actor while the canvas runs: both rulings and objections follow the calls.
F-012 stands as written: its coalition test was already run on coalitions without hosting.

    python3 out/_analysis/c2d_findings_p4.py [--write]
"""
import datetime, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
FP = os.path.join(OUT, "findings.jsonl")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
rows = [json.loads(l) for l in open(FP, encoding="utf-8") if l.strip()]
cur = dict((r["id"], r) for r in rows)
A = dict((r["id"], r) for r in (json.loads(l) for l in open(os.path.join(OUT, "model", "arrows.jsonl"), encoding="utf-8")))
k04 = None
for l in open(os.path.join(OUT, "_analysis", "c2_arrow_evidence-p4a.txt"), encoding="utf-8"):
    if l.startswith("== K04 -> P09"):
        k04 = {}
    m = re.search(r"both (\d+); holds in (\d+) \(([\d.]+)\); null mean ([\d.]+), p95 ([\d.]+)", l)
    if k04 == {} and m:
        k04 = dict(zip(("both", "holds", "share", "mean", "p95"), (int(m.group(1)), int(m.group(2)), float(m.group(3)),
                                                                   float(m.group(4)), float(m.group(5)))))
c13, c19 = A["A13"]["counts"], A["A19"]["counts"]
h = A["A20"]["before_h73"]
new = []
f = dict(cur["F-008"])
f.update({"stage": "C2", "leg": LEG, "supersedes": "F-008@%s" % cur["F-008"]["leg"], "status": "standing", "t": T,
          "statement": ("Short of hands, rooms turn to other rooms: in %d of %d rooms carrying both, the first upkeep comes "
                        "before the first help given, asked for or traded with another room (%.3f against a null mean of "
                        "%.3f), and in %d of %d before the first coalition, counted on coalitions without hosting (%.3f "
                        "against %.3f, p95 %.3f)." % (c13["holds"], c13["both"], c13["share"], c13["null_mean"], c19["holds"],
                                                      c19["both"], c19["share"], c19["null_mean"], c19["null_p95"])),
          "evidence": ["out/_analysis/c2_arrow_evidence-p2a.txt", "out/_analysis/c2_arrow_evidence-p4a.txt",
                       "naruto:c0145", "criticalrole:c0058"],
          "bound": ("Late rooms often enter the canvas through other rooms, with help or a coalition first (the coalition "
                    "order holds in %d of %d late rooms). naruto, cited before, joined a coalition before any upkeep, so "
                    "it no longer stands as the coalition instance." % (c19 and A["A19"]["early_late"]["late"],
                                                                         A["A19"]["early_late"]["late_n"])),
          "refuted_by": ["coalitions formed before any upkeep in most rooms carrying both"],
          "why": ("pass 4: the hosting themes left the coalition element (the recut); the coalition clause is recounted "
                  "on coalitions alone, and the naruto evidence fails the instance audit's check (i)")})
new.append(f)
f = dict(cur["F-011"])
f.update({"stage": "C2", "leg": LEG, "supersedes": "F-011@%s" % cur["F-011"]["leg"], "status": "standing", "t": T,
          "statement": ("Membership carried in does not come before the attack: on the nation claimed beyond the mark, "
                        "colour faiths and frames (the candidate narrowed at pass 4), the first such concept comes before "
                        "the first attack in %d of %d rooms carrying both (%.3f), below the null mean of %.3f (p95 %.3f). "
                        "The reverse, attack first and membership told after, shows in the count; it was not declared and "
                        "is not tested." % (k04["holds"], k04["both"], k04["share"], k04["mean"], k04["p95"])),
          "evidence": ["out/_analysis/c2_arrow_evidence-p3a.txt", "out/_analysis/c2_arrow_evidence-p4a.txt"],
          "refuted_by": ["membership concepts coming first in rooms carrying both above the null's 95th percentile"],
          "why": ("pass 4: the flag and emblem themes left Flagging the nation (the second recut); the test was re-run on "
                  "the narrowed candidate as declared")})
new.append(f)
f = dict(cur["F-010"])
f.update({"stage": "C2", "leg": LEG, "supersedes": "F-010@%s" % cur["F-010"]["leg"], "status": "bounded", "t": T,
          "statement": (cur["F-010"]["statement"] + " While the canvas runs (before hour 73), the calls come before the host "
                        "sub's rulings in %d of %d rooms (%.3f, p95 %.3f) and before members' objections in %d of %d "
                        "(%.3f, p95 %.3f)." % (h["rulings"]["holds"], h["rulings"]["both"], h["rulings"]["share"],
                                               h["rulings"]["null_p95"], h["objections"]["holds"], h["objections"]["both"],
                                               h["objections"]["share"], h["objections"]["null_p95"])),
          "evidence": cur["F-010"]["evidence"] + ["out/_analysis/c2_arrow_evidence-p4b.txt"],
          "why": "pass 4 declaration 5: the host's line tested by actor before hour 73; both beat the null"})
new.append(f)
print("\n".join(json.dumps(x, ensure_ascii=False)[:700] for x in new))
if "--write" in sys.argv:
    with open(FP, "a", encoding="utf-8") as fh:
        for x in new:
            fh.write(json.dumps(x, ensure_ascii=False) + "\n")
    print("appended %d; findings.jsonl now %d lines" % (len(new), len(rows) + len(new)))
