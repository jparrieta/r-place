#!/usr/bin/env python3
"""D3c: append two model/history.jsonl lines that change no element (history.jsonl is append-only and outside the
model hash). (1) A history correction to line 145 (move 176's bound on A21): its re-examination counted all 36
accepted A21 corrections (families F1 and F2), and its adaptations list named 22 ids; the line names the corrections
it left out, beside line 145's ids, with corrects_lines [145]. (2) P05: section 2's re-examination with every room
back and the scope decision under QD3-011's option (b), citing the nine rooms' re-check corrections. Checks first:
line 145 is A21's bound line; the A21 corrections are 36 and every one is an accepted correction by its last ruling;
the nine P05 lines are accepted corrections on P05; F-024 exists; and the model hash before and after is the same.
Without --write it prints the lines and writes nothing.

    python3 out/_analysis/d3c_history_lines.py [--write]
"""
import argparse, datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


P05_LINES = ["R-completeanarchy-c187508d7ae3-022", "R-polska-dadda7358f9a-049", "R-satania-84df196116f3-022",
             "R-halo-b988854ba168-036", "R-bangtan-7efe23da0d0c-070", "R-thesilphroad-a3f86618e239-018",
             "R-armok-8852b2ab85f8-022", "R-maryland-d1b6e2d1d5f3-017", "R-oneshot-e840e127e9b2-013"]
hist = jl(os.path.join(OUT, "model", "history.jsonl"))
h145 = hist[144]
if h145.get("id") != "A21" or h145.get("field") != "bound" or h145.get("leg") != "D3a-27":
    raise SystemExit("history line 145 is not move 176's bound line on A21")
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
old = jl(os.path.join(OUT, "adaptations.jsonl"))
new = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations-recheck.jsonl"))}
corr = sorted(l["id"] for l in old if l.get("element") == "A21" and last.get(l["id"], {}).get("decision") in
              ("accept", "modify") and last[l["id"]].get("kind") == "correction")
if len(corr) != 36:
    raise SystemExit("A21's accepted first-return corrections are %d, not the 36 line 145 counts" % len(corr))
cited = list(h145.get("adaptations") or [])
missing = [i for i in corr if i not in cited]
errs = []
for i in P05_LINES:
    l, r = new.get(i), last.get(i, {})
    if not l or l.get("element") != "P05" or (r.get("decision"), r.get("kind")) != ("accept", "correction"):
        errs.append("%s is not an accepted P05 correction" % i)
if not any(f.get("id") == "F-024" for f in jl(os.path.join(OUT, "findings.jsonl"))):
    errs.append("F-024 is not in findings.jsonl")
if errs:
    print("\n".join(errs))
    raise SystemExit("refused: nothing written")
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
line1 = {"t": t, "stage": "D3", "leg": "D3c", "id": "A21",
         "event": "history correction for line 145 (move 176's bound): the corrections its re-examination counted, "
                  "named in full",
         "move": "developing working hypotheses",
         "why": ("Line 145 records section 2's re-examination of A21's corrections met twice: the 26 restrict "
                 "corrections of family F1 and the 10 of family F2, 36 in all. Its adaptations list named 22 ids, 11 "
                 "of them corrections and the rest rejected instantiate lines, so 25 of the 36 corrections went "
                 "uncited, and the D3c close-check found two groups met twice with no history line (T4-006: "
                 "katawashoujo-051, newzealand-057; T4-014: adventuretime-051, dallasstars-029, masseffect-056). "
                 "Every one of the 36 is a correction the bound answers, and the re-check carries no correction on "
                 "A21 in 34 of their rooms (the other two, adventuretime and weezer, repeat their first-return "
                 "lines). Line 145 stays as written; this line names the 25 beside its 22 ids. A21 is unchanged by "
                 "this line."),
         "field": "adaptations", "was": cited, "now": cited + missing, "corrects_lines": [145]}
line2 = {"t": t, "stage": "D3", "leg": "D3c", "id": "P05",
         "event": ("corrections met twice re-examined with every room back (section 2), and the scope decided "
                   "without a change to the frozen model (QD3-011, option b): a cluster branch with a bound, "
                   "carried in F-024; the relating revision drafted at D3b held for D4"),
         "move": "developing working hypotheses",
         "why": ("Nine re-check corrections fail the clause move 173 added ('until its keepers are told of it, and "
                 "it is lost or given up where the telling does not reach them'). In six rooms (completeanarchy, "
                 "polska, satania, halo, bangtan, thesilphroad) the keepers read a planned change from its shape "
                 "and stop repairing it, with no telling; polska and satania meet at T4-006, and halo and bangtan "
                 "at T3-170 and T4-019. In three (armok, maryland, oneshot) informed members hold the change against "
                 "keepers who do not know, at three nodes. The re-examination holds the alignment for the six. J "
                 "chose option (b) (23 October, 10:36 Berlin): hold the move and freeze 46384686, the version the "
                 "rooms were re-checked on (section 5). The scope decision is the one rule 12 and section 4 allow "
                 "beside a global revision: the frozen clause is the trunk, bounded to rooms where the keepers can "
                 "learn of a planned change only by being told and no informed member holds it; the six rooms are "
                 "a cluster branch, 'the shape read', carried to D4 and D5, where branches are built and judged; the "
                 "three are a second limit, below the trigger. F-024 states the bounded claim with its refuted_by. "
                 "The revision drafted at D3b is held for D4: the change is repaired away as damage until its "
                 "keepers learn of it, by being told or by seeing enough of its shape to read it; informed members "
                 "can hold it against keepers who do not know; it is lost or given up where neither the telling "
                 "nor the shape reaches the keepers. P05's statement is unchanged by this line."),
         "adaptations": P05_LINES,
         "rooms": ["completeanarchy", "polska", "satania", "halo", "bangtan", "thesilphroad", "armok", "maryland",
                   "oneshot"],
         "evidence": ["F-024", "out/_analysis/d3b2_P05_corrections_rooms.txt"]}
print(json.dumps(line1, ensure_ascii=False)[:600] + " ...")
print("line 1 names %d corrections beside line 145's %d ids: %s" % (len(missing), len(cited), ", ".join(missing)))
print(json.dumps(line2, ensure_ascii=False)[:600] + " ...")
h0 = vlib.model_hash(OUT)
if not a.write:
    print("dry run: nothing written; model hash %s" % h0)
    raise SystemExit(0)
with open(os.path.join(OUT, "model", "history.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(line1, ensure_ascii=False) + "\n")
    f.write(json.dumps(line2, ensure_ascii=False) + "\n")
h1 = vlib.model_hash(OUT)
print("appended 2 lines; history.jsonl now %d lines; model hash before %s, after %s, %s" % (
    len(jl(os.path.join(OUT, "model", "history.jsonl"))), h0[:12], h1[:12], "unchanged" if h0 == h1 else "CHANGED"))
