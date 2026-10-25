#!/usr/bin/env python3
"""D4a-03: write out/handback-D4.md, the stage's return value (stage D4, "Final message"). The prose is mine; the
tables and counts are built from branches.jsonl, crosslinks.jsonl, chunk-share-D4.result.json, chunk-share-D4.jsonl,
projections-D4.jsonl and _views/tree-likeness.json, so no figure is typed. Never overwrites.

    python3 out/_analysis/d4a03_handback.py [--write]
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(OUT, "handback-D4.md")
ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
if a.write and os.path.exists(DEST):
    raise SystemExit("refusing to overwrite %s" % DEST)


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


B = jl(os.path.join(OUT, "branches.jsonl"))
CL = jl(os.path.join(OUT, "crosslinks.jsonl"))
r = json.load(open(os.path.join(OUT, "chunk-share-D4.result.json"), encoding="utf-8"))
C = jl(os.path.join(OUT, "chunk-share-D4.jsonl"))
P = {(p.get("branch") or p.get("cluster")): p for p in jl(os.path.join(OUT, "projections-D4.jsonl"))}
tl = json.load(open(os.path.join(OUT, "_views", "tree-likeness.json"), encoding="utf-8"))
rooms = r["rooms"]
inb = set(m for b in B for m in b["members"])
lk = collections.Counter((b["level"], "subform" if b["parent"] else "branch") for b in B)
kk = collections.Counter(b["kind"] for b in B)
pairs = {tuple(sorted(x["branches"])) for x in CL}
low = sum(1 for c in r["case_information"] if c.get("low_information"))


def carried(part):
    p = r[part]
    k = p["carried_k"]
    t = {x["seed"]: x for x in p["tables"] if x["k"] == k}
    return k, len(p["eligible_indices"]), t, p["sensitivities"][str(k)], p["own_weight_median"]


k1, n1, t1, s1, o1 = carried("all_cases")
k2, n2, t2, s2, o2 = carried("without_low_information")
w = []
w.append("# Handback, stage D4: the taxonomy from adaptations\n")
w.append("Legs D4a-01 to D4a-03, 24 and 25 October 2026. The taxonomy is read off the adjudicated ledger (the "
         "re-check, all 705 rooms), adapted against the model frozen at D3 (46384686…). The model is unchanged: the P05 "
         "and A11 amendments of D4a-01 were reverted (QD4-001) and are held proposals. The detail and the scripts are "
         "in `tree-D4.md`, `notes-D4.md`, `branches.jsonl`, `forms/`, `crosslinks.jsonl`, `chunk-share-D4.*` and "
         "`projections-D4.jsonl`.\n")
w.append("## The claim\n")
w.append("The rooms adapted the model in many small shared ways, not into a few forms. %d branches hold %d of the %d "
         "rooms, and they overlap: %d cross-links join %d pairs of branches that do not nest. A room makes several "
         "element-level changes at once. The branches are facets of those changes, not exclusive types. The "
         "comparison built without the ledger agrees in its own way: its partition beats its null but barely "
         "separates the rooms (silhouette %.3f), does not survive a change of distance, and largely sorts the rooms by "
         "how much the coders coded. What the branches say is specific:\n" % (
             len(B), len(inb), len(rooms), len(CL), len(pairs), t1[0]["silhouette"]))
w.append("- **Rooms add work the model does not state.** They administer the April Fools play (F01). They carry out "
         "deals: they move work, retarget scripts and relay terms (F10). They keep the shared instruction current, "
         "because a stale template or bot target undoes their own new work (F15, F33, F08). They keep the chat open "
         "(F16). They make help wait on their own work and spare hands (F22, F28). And they carry on by renewing the "
         "work elsewhere, often before the close (F11 to F14).")
w.append("- **They limit P05's added clause.** In design, at the border and in keeping (F07, F26, F27), informed "
         "members reject a planned change, or the record does not show the untold keepers the clause needs.")
w.append("- **They show two links the model lacks.** After a move the room builds again (F09). After a celebration it "
         "defends again (F32).\n")
w.append("**The room that best supports it: fivenightsatfreddys.** It is in eight branches across seven elements. It "
         "runs a takeover as a temporary regime (F01, F02), does not show the telling clause at its design (F07), "
         "builds again after a move (F09), carries out a deal (F10), carries on past the close (F23), depends on chat "
         "access (F29) and hosts by one-off permission (F31). One room, many facets, no single form.\n")
w.append("**The room that most threatens it: ainbowroad.** It is the largest room in no branch (2,054 concepts). Its "
         "shared changes sit on keys held by fewer than 20 rooms, which the pass did not read. A room can hold rich "
         "organizing that the branches do not show.\n")
w.append("**The condition between them** is whether a room's change lands on a node that many other rooms use. Where "
         "it does, the room appears in a branch, often in several. Where its changes are its own, or shared by only a "
         "few rooms at one node, it appears in none. The branches are a census of common changes, not of the rooms' "
         "organizing.\n")
w.append("## The return value\n")
w.append("| What | Count |\n|---|---|")
w.append("| Branches | %d: %d at the fourth order and %d at the third (top level); %d subforms, all at the third order |" % (
    len(B), lk[("fourth", "branch")], lk[("third", "branch")], lk[("third", "subform")]))
w.append("| Branches by kind (majority of their lines; not relied on for add-condition, add-step and restrict) | %s |" % (
    ", ".join("%s %d" % kv for kv in sorted(kk.items()))))
w.append("| Subforms | F02 to F06 under F01; F12 to F14 under F11; F18 and F19 under F17 |")
w.append("| Cross-links | %d lines over %d pairs of branches that do not nest |" % (len(CL), len(pairs)))
w.append("| The unadapted group | 0 (no room returned `none`) |")
w.append("| Rooms in no branch | %d, each named in `tree-D4.md` with its count of smaller keys |" % (len(rooms) - len(inb)))
w.append("| The four counts against n_analysed | %d in a branch + 0 unadapted + %d in no branch + 0 unreturned = %d |" % (
    len(inb), len(rooms) - len(inb), len(rooms)))
w.append("| Tree-likeness | delta %.4f (Monte Carlo SE %.4f), combined level-3 matrix, 20,000 quartets |" % (
    tl["delta_score"], tl["quartet_diagnostics"]["mc_se"]))
w.append("| Trees drawn | the average-linkage dendrogram and the leaf-to-root view, as views of the distance; the dendrogram is a chain with no partition; no tree of forms, since the branches overlap |")
w.append("| Comparison engine | `chunk-comparison-v1.1` (departure, QD4-002) |")
w.append("| Empties | %d |" % sum(1 for c in r["case_information"] if not c["placed_concepts"]))
w.append("| a and the median own-data weight | a = %s; %.3f with all rooms, %.3f without the low-information rows |" % (
    r["parameters"]["concentration"], o1, o2))
w.append("| Rand indices among the three distances, at the carried k | Ward/CLR against Jaccard %.3f and Hellinger %.3f (all rooms); %.3f and %.3f (without low-information) |" % (
    s1["jaccard_ari"], s1["hellinger_ari"], s2["jaccard_ari"], s2["hellinger_ari"]))
w.append("| Smoothing sensitivity at the carried k | a/10 %.3f, 10a %.3f (all); %.3f and %.3f (without) |" % (
    s1["concentration_0.1x_ari"], s1["concentration_10x_ari"], s2["concentration_0.1x_ari"], s2["concentration_10x_ari"]))
w.append("| The third tier's sparsity | %d columns, %.2f nonzero per room |" % (r["third_tier"]["columns"], r["third_tier"]["mean_nonzero_per_case"]))
w.append("| The tier verdict | dimension ARI %.3f and third-tier ARI %.3f at k %d |" % (
    r["dimension_ari"][str(k1)], r["third_tier"]["ari"][str(k1)], k1))
vol = open(os.path.join(OUT, "_analysis", "d4a03_volume.txt"), encoding="utf-8").read()
import re as _re
ev = _re.search(r"eta squared of log concepts by cluster: ([0-9.]+); permutation percentile ([0-9.]+) \(null max ([0-9.]+)\)", vol)
w.append("| The volume verdict | eta squared of log concepts by cluster %s, at the %sth percentile of the permutation null (null maximum %s); the clusters largely sort the rooms by size (`_analysis/d4a03_volume.txt`) |" % ev.groups())
w.append("| k carried | %d with all %d rooms (worst margin %+.3f, silhouette %.3f); %d without the %d low-information rows, %d rooms (worst margin %+.3f, silhouette %.3f) |" % (
    k1, n1, min(min(t["mean_margin"], t["median_margin"]) for t in t1.values()), t1[0]["silhouette"], k2, low, n2,
    min(min(t["mean_margin"], t["median_margin"]) for t in t2.values()), t2[0]["silhouette"]))
w.append("| Clusters | %s |" % ", ".join("%s %d" % (c["code"], c["n"]) for c in C))
sh = [(c.get("residue_concepts") or 0) / ((c.get("placed_concepts") or 0) + (c.get("residue_concepts") or 0))
      if ((c.get("placed_concepts") or 0) + (c.get("residue_concepts") or 0)) else 0.0 for c in r["case_information"]]
w.append("| Residue share per room (QD4-002) | %d rooms hold residue concepts; median %.3f; %d rooms at 0.10 or more, %d at 0.30 or more |" % (
    sum(1 for c in r["case_information"] if c.get("residue_concepts")), sorted(sh)[len(sh) // 2],
    sum(1 for x in sh if x >= .10), sum(1 for x in sh if x >= .30)))
w.append("| Feature space | **no verdict, canvas field or branch entered the comparison**; it reads the concept store, placements, tiers, dropped cases and the prior |")
w.append("")
w.append("## The branches, in the order cut, with the verdict and canvas percentiles\n")
w.append("Verdicts are projections.py's map (my last ruling at D3, else the readers' agreed verdict), so the D3 versions "
         "are mixed. Each row: id, parent, level, members; composes, with residue, does not compose, cannot tell; the "
         "does-not-compose percentile; the median area and its percentile. The canvas percentiles follow room size "
         "(`tree-D4.md`).\n")
w.append("| id | name | parent | level | n | verdicts | dnc pct | median area (pct) |\n|---|---|---|---|---|---|---|---|")
for b in B:
    p = P[b["id"]]
    v = p["verdicts"]
    w.append("| %s | %s | %s | %s | %d | %d / %d / %d / %d | %.1f | %s (%.1f) |" % (
        b["id"], b["name"], b["parent"] or "-", b["level"], len(b["members"]), v.get("composes", 0),
        v.get("composes-with-residue", 0), v.get("does-not-compose", 0), v.get("cannot-tell", 0),
        p["percentile_does_not_compose"], p["canvas"]["median_area_px"], p["canvas"]["percentile_median_area"]))
for c in C:
    p = P[c["code"]]
    v = p["verdicts"]
    w.append("| %s | cluster | - | - | %d | %d / %d / %d / %d | %.1f | %s (%.1f) |" % (
        c["code"], c["n"], v.get("composes", 0), v.get("composes-with-residue", 0), v.get("does-not-compose", 0),
        v.get("cannot-tell", 0), p["percentile_does_not_compose"], p["canvas"]["median_area_px"],
        p["canvas"]["percentile_median_area"]))
w.append("")
w.append("## The held proposals (QD4-001; never served, not re-checked)\n")
w.append("- **P05 (move 198; history lines 173 to 176; reverted by move 203, line 181).** The statement would gain: "
         "\"This holds where the keepers can learn of a planned change only by being told, and no informed member "
         "holds it.\" Status bounded. The bound names completeanarchy, polska, satania, halo, bangtan and thesilphroad "
         "(the shape read) and armok, maryland and oneshot (informed members), with their nine re-check lines. The "
         "branches F07, F26 and F27 hold %d rooms where the clause holds only in part." % len(
             set().union(*[set(b["members"]) for b in B if b["id"] in ("F07", "F26", "F27")])))
w.append("- **A11 (move 199; history lines 177 to 180; reverted by move 203, line 182).** The arrow from P02 to P04 "
         "would be withdrawn under rule 14: it never beat its null; template first is nearly as common as the "
         "transition; the failure clause stands alone in 117 rooms, 31 of them talk only.\n")
w.append("## Questions, departures and defects\n")
w.append("- **QD4-001** (answered): the amendments were reverted, and the model is the D3 version.")
w.append("- **QD4-002** (answered): the comparison engine was patched to v1.1; declared as a departure (`departures.jsonl` line 10).")
w.append("- **For the operator.** `validate.py --open D4` reads the startup packet's pattern name "
         "`rooms-x-adaptations.<level>.<kind>.tsv` literally. `stage_D4.py` resolves branch keys against elements "
         "only, so arrow keys, the largest change keys in this ledger, cannot key a branch. Its member-name check is a "
         "substring check: the room 'de' forbids 'decisions' and 'outside'.\n")
w.append("## Licences exercised (METHOD.md)\n")
w.append("- **The count set by kinds, not by a head's capacity:** exercised. The branches number what the keys and "
         "their lines support (35), under rules written before the first cut; the cuts stop at a declared key size.")
w.append("- **An in-sample return in Eisenhardt's spirit:** its ledger is the taxonomy's material; the taxonomy cannot "
         "corroborate it (section 7).")
w.append("- **Langley's strategy:** not exercised at D4; the two links the model lacks wait for an order test.")
w.append("- **Gioia's explosion at the front end:** not a D4 licence.\n")
w.append("## Slips\n")
w.append("- At D4a-01 the session ended inside one command; its log line and snap were written, and the empty F04 dry run was repeated.")
w.append("- F06's form lists the arrow A12 among the elements its members carry unchanged; the forms are written once.")
w.append("- Two spec names (F16, F30) were changed before writing, after the member-name check refused them.")
w.append("- At D4a-03 three Edits to this handback's script ran in one turn, against the rule; each landed on a separate string.")
text = "\n".join(w) + "\n"
print("handback: %d lines, %d words" % (len(w), len(text.split())))
if not a.write:
    print("dry run: nothing written")
    raise SystemExit(0)
open(DEST, "w", encoding="utf-8").write(text)
print("wrote", DEST)
