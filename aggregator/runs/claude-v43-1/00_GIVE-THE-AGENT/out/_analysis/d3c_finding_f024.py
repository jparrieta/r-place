#!/usr/bin/env python3
"""D3c: append finding F-024, the scope decision for P05's added clause under QD3-011's option (b), to
findings.jsonl (rule 14: append-only, a new id since no finding touched P05). Before writing it checks that the id
is new, that every cited re-check line exists, sits on P05 and carries an accepted correction as its last ruling,
and that every cited concept exists in its room. Without --write it prints the line and writes nothing.

    python3 out/_analysis/d3c_finding_f024.py [--write]
"""
import argparse, datetime, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()

BRANCH = ["R-completeanarchy-c187508d7ae3-022", "R-polska-dadda7358f9a-049", "R-satania-84df196116f3-022",
          "R-halo-b988854ba168-036", "R-bangtan-7efe23da0d0c-070", "R-thesilphroad-a3f86618e239-018"]
CARRY = ["R-armok-8852b2ab85f8-022", "R-maryland-d1b6e2d1d5f3-017", "R-oneshot-e840e127e9b2-013"]
CODES = ["completeanarchy:c0169", "polska:c0095", "satania:c0086", "satania:c0087", "halo:c0401", "halo:c0402",
         "bangtan:c0092", "thesilphroad:c0700", "armok:c0054", "maryland:c0223", "oneshot:c0040"]


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


finds = jl(os.path.join(OUT, "findings.jsonl"))
if any(f.get("id") == "F-024" for f in finds):
    raise SystemExit("F-024 exists already; nothing written")
rec = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations-recheck.jsonl")) if l["id"] in set(BRANCH + CARRY)}
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    if r["adaptation"] in rec:
        last[r["adaptation"]] = r
errs = []
for i in BRANCH + CARRY:
    l, r = rec.get(i), last.get(i, {})
    if not l:
        errs.append("%s is not a re-check line" % i)
    elif l.get("element") != "P05" or (r.get("decision"), r.get("kind")) != ("accept", "correction"):
        errs.append("%s: element %s, last ruling %s/%s" % (i, l.get("element"), r.get("decision"), r.get("kind")))
want = {c.split(":")[0] for c in CODES}
have = set()
for line in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"):
    r = json.loads(line)
    if r["sub"] in want:
        have.add("%s:%s" % (r["sub"], r["code_id"]))
errs += ["concept %s not found" % c for c in CODES if c not in have]
if errs:
    print("\n".join(errs))
    raise SystemExit("refused: nothing written")

f = {
    "stage": "D3", "leg": "D3c", "id": "F-024", "tier": "element", "warrant": "read", "status": "bounded",
    "t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "statement": ("Keepers repair a change the room has planned or agreed (P02) away as damage until they learn of "
                  "it. P05, frozen at D3c, names one route to that knowledge, the telling, and holds that the change "
                  "is lost or given up where the telling does not reach the keepers. The re-check of all 705 rooms "
                  "shows two more routes by which the change outlasts the missing telling: in six rooms the keepers "
                  "read the change from its shape and stop repairing it ('once it reached a critical mass and people "
                  "saw what it was they just naturally began protecting it instead of destroying it' [halo/c0402]), "
                  "and in three informed members hold it against keepers who do not know."),
    "evidence": BRANCH + CARRY + CODES + ["out/_analysis/d3b2_P05_corrections_rooms.txt",
                                          "out/_analysis/d3b_before_after_out_v2.txt"],
    "bound": ("The told route, P05's frozen clause, holds where the keepers can learn of a planned change only by "
              "being told and no informed member holds it. It does not hold in nine rooms whose re-check correction "
              "the ledger accepts. In completeanarchy, polska, satania, halo, bangtan and thesilphroad the keepers "
              "read the change from its shape before anyone tells them; this is a cluster branch, 'the shape read', "
              "warranted at D3b by two pairs meeting at one node (polska and satania at T4-006, halo and bangtan at "
              "T4-019), and carried to D4 and D5, where branches are built and judged. In armok, maryland and "
              "oneshot informed members hold the change against keepers who do not know; these are paired "
              "corrections at three nodes, below the trigger, named here as a second limit. P05's four cause rooms "
              "(OnePiece, leagueoflegends, monsterhunter, portugal) carry no correction of the clause. 25 absent "
              "lines in 25 rooms leave the clause untested. The element's words are unchanged in the frozen model "
              "(QD3-011, option b); the revision drafted at D3b is held for D4."),
    "refuted_by": ["a room whose keepers knew of a planned change, by being told or by reading its shape, and kept "
                   "repairing it away as damage",
                   "a room where the change could not be read from its shape, no one told the keepers and no "
                   "informed member held it, and the change still stood"],
    "literature": [],
    "why": ("the scope decision for P05's added clause under QD3-011 (J, 23 October, 10:36 Berlin: option b; "
            "freeze 46384686, hold the move): a claim corrected locally cannot remain universal globally without "
            "a scope decision (rule 12); no finding touched P05, so the bounded claim is a new finding (rule 14)"),
}
print(json.dumps(f, ensure_ascii=False, indent=1))
if not a.write:
    print("dry run: nothing written")
    raise SystemExit(0)
with open(os.path.join(OUT, "findings.jsonl"), "a", encoding="utf-8") as fh:
    fh.write(json.dumps(f, ensure_ascii=False) + "\n")
print("appended F-024; findings.jsonl now %d lines" % len(jl(os.path.join(OUT, "findings.jsonl"))))
