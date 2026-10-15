#!/usr/bin/env python3
"""C5c-02, rule 14, after Stigmergy's recut (C5-move-merging-93, C5-move-splitting-94):
  - F-016 superseded: information provision's four themes now carry 534 of 705 rooms (c5c2_room_unions.json), and
    Stigmergy holds building and reporting the mark alone;
  - F-018 written: the three codings and what they decided (c5c2_stigmergy_three.json);
  - mapping-C3.jsonl's T4-007 line amended in place, its old reason kept as `was_why`.
Refuses if a line of this leg for F-016 or F-018 exists.

    python3 out/_analysis/c5c2_findings.py
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
fp = os.path.join(OUT, "findings.jsonl")
rows = [json.loads(l) for l in open(fp, encoding="utf-8") if l.strip()]
if any(r["id"] in ("F-016", "F-018") and r.get("leg") == LEG for r in rows):
    sys.exit("a %s line for F-016 or F-018 exists" % LEG)
if any(r["id"] == "F-018" for r in rows):
    sys.exit("F-018 is taken")
un = json.load(open(os.path.join(OUT, "_analysis", "c5c2_room_unions.json"), encoding="utf-8"))
th = json.load(open(os.path.join(OUT, "_analysis", "c5c2_stigmergy_three.json"), encoding="utf-8"))
last = [r for r in rows if r["id"] == "F-016"][-1]
old = "Information provision: 4 themes (Sensemaking, Stigmergy, Backstage decision-making, Attribution), %d of 705 rooms." % un["old"]["information"]
if old not in last["statement"]:
    sys.exit("the passage to change is not in F-016's statement")
f16 = dict(last)
f16.update({"stage": "C5", "leg": LEG, "t": T, "supersedes": "F-016",
            "statement": last["statement"].replace(old, (
                "Information provision: 4 themes (Sensemaking, Stigmergy, Backstage decision-making, Attribution), "
                "%d of 705 rooms; since C5c-02 Stigmergy holds building and reporting the mark alone." % un["new"]["information"])),
            "why": "rule 14: Stigmergy's recut at C5c-02 moved extending the room's work and adding a personal piece to "
                   "Collective representation (F-018); the four information themes now carry %d rooms, not %d "
                   "(c5c2_room_unions.py); Collective representation stays in the remainder, among the themes that make "
                   "the goal" % (un["new"]["information"], un["old"]["information"])})
v = {k: th[k]["verdicts"] for k in ("T3-038", "T3-041", "T3-060")}
pairs = th["_pairs"]
f18 = {"stage": "C5", "leg": LEG, "id": "F-018", "tier": "fourth", "warrant": "inferred", "status": "standing", "t": T,
       "statement": ("Stigmergy's cut joined two kinds of record. Three readers coded the 72 records drawn at C5a-01 from "
                     "its three member themes, each record taking the code two of them gave. Building and reporting the "
                     "mark (T3-038) reports the work's state in %d of its %d records that bear on the work. Extending "
                     "the room's work (T3-041) proposes or asks what to add in %d to %d of %d, and adding a personal "
                     "piece (T3-060) in %d of %d. By the rule written before the read, the second two moved to "
                     "Collective representation at C5c-02, and Stigmergy holds building and reporting alone.") % (
           v["T3-038"]["M"][1] - v["T3-038"]["M"][0], v["T3-038"]["M"][1], v["T3-041"]["M"][0], v["T3-041"]["P"][0],
           v["T3-041"]["M"][1], v["T3-060"]["M"][0], v["T3-060"]["M"][1]),
       "evidence": ["out/_analysis/c5_stigmergy_sample.json", "out/_analysis/c5_stigmergy_codes.json",
                    "out/readers-C5/", "out/sources-from-J/RETURN-field-C5.jsonl",
                    "out/_analysis/c5c2_stigmergy_three.py", "out/_analysis/c5c2_stigmergy_three.json"],
       "bound": ("Three coders and 24 records per theme. Agreement is moderate: mine and the fleet reader's %d of 72 "
                 "(kappa %.2f), mine and the field analyst's %d (%.2f), the fleet reader's and the field analyst's %d "
                 "(%.2f). T3-060 meets the rule at exactly half, and the field analyst's codes alone would leave it "
                 "(%d of %d). The record holds the talk, not the placing.") % (
           pairs["mine-fleet"]["agree"], pairs["mine-fleet"]["kappa"], pairs["mine-field"]["agree"],
           pairs["mine-field"]["kappa"], pairs["fleet-field"]["agree"], pairs["fleet-field"]["kappa"],
           th["T3-060"]["field_alone"][0], th["T3-060"]["field_alone"][1]),
       "refuted_by": ["a larger coded draw in which proposals fall below half of the bearing records of extending the "
                      "work and of adding a personal piece"],
       "literature": ["Grasse 1959", "Heylighen 2016"],
       "why": ("J's ruling 3 of 15 October: recut Stigmergy only if the cut joins what Grassé and Heylighen keep "
               "apart; the fleet readers at C5c-01 and the field analyst at C5c-02 coded blind, and the rule, its "
               "destinations and the three-coder combination were logged before each tally")}
with open(fp, "a", encoding="utf-8") as f:
    f.write(json.dumps(f16, ensure_ascii=False) + "\n" + json.dumps(f18, ensure_ascii=False) + "\n")
mp = os.path.join(OUT, "mapping-C3.jsonl")
mrows = [json.loads(l) for l in open(mp, encoding="utf-8") if l.strip()]
hit = [r for r in mrows if r.get("fourth") == "T4-007"]
if len(hit) != 1:
    sys.exit("expected one T4-007 mapping line")
r = hit[0]
r["was_why"] = r["why"]
r["why"] = ("Members report the state of the mark to the thread: what is placed, done or missing, and where; the work "
            "and the reports on it are its own representation (Puranam, Alexy and Reitzig 2014, p. 172).")
r["amended"] = ("C5c-02: Stigmergy keeps building and reporting the mark alone (F-018); the mapping now rests on members' "
                "reports of the work's state")
open(mp, "w", encoding="utf-8").write("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in mrows))
print("F-016 superseded, F-018 written, mapping T4-007 amended")
print(f18["statement"])
print(f18["bound"])
