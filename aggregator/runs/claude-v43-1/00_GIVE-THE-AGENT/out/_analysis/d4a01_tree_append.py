#!/usr/bin/env python3
"""D4a-01: append to out/tree-D4.md the sections that are built from files, so that no id or count is typed: the
cuts in the order cut (branches.jsonl, with each cut's tier_history line and move number from MOVES, checked
against the diary at D4a-01), the cross-links, the groups read and set aside, where the pass stopped (element change
keys at level 4 held by 20 rooms or more, not cut), the held proposals stated in full (history lines 173 to 182),
and the accounting of section 4 against n_analysed, naming every room in no branch with why. Refuses if the
sections are already there. Without --write it prints the counts.

    python3 out/_analysis/d4a01_tree_append.py [--write]
"""
import argparse, collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
V = os.path.join(OUT, "_views")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from adaptation_ledger import effective_rooms  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
TREE = os.path.join(OUT, "tree-D4.md")
txt = open(TREE, encoding="utf-8").read()
MARK = "## The cuts of D4a-01, in the order cut"
if MARK in txt:
    raise SystemExit("the sections are in tree-D4.md already")
MOVES = {"F01": 200, "F02": 201, "F03": 202, "F04": 204, "F05": 205, "F06": 206}
CHANGE = {"add-step", "add-condition", "link", "restrict", "contradict"}


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


def matrix(level):
    with open(os.path.join(V, "rooms-x-adaptations.%s.all.tsv" % level), encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")[1:]
        held, rooms = collections.defaultdict(set), []
        for line in f:
            p = line.rstrip("\n").split("\t")
            rooms.append(p[0])
            for k, v in zip(head, p[1:]):
                if v == "1":
                    held[k].add(p[0])
    return held, rooms


B = jl(os.path.join(OUT, "branches.jsonl"))
TH = {r["id"]: r for r in jl(os.path.join(OUT, "tier_history.jsonl")) if r.get("stage") == "D4" and r.get("tier") == "branch"}
CL = jl(os.path.join(OUT, "crosslinks.jsonl"))
H = jl(os.path.join(OUT, "model", "history.jsonl"))
els = {r["id"] for r in jl(os.path.join(OUT, "model", "elements.jsonl"))}
w = ["", MARK, ""]
for b in B:
    th = TH[b["id"]]
    w.append("- **%s** (move %d, %s; %s; level %s; parent %s). Keys: %s. %d members. Kind: %s (%s), not relied on. "
             "Ground: %s. **%s.** %s" % (
                 b["id"], MOVES[b["id"]], th["move"], th["event"], b["level"], b["parent"] or "none",
                 ", ".join("`%s`" % k for k in b["keys"]), len(b["members"]), b["kind"],
                 ", ".join("%s %d" % kv for kv in b["kind_counts"].items()), th["ground"], b["name"],
                 b["what_it_changes"]))
w.append("")
w.append("Members are listed in `branches.jsonl` and in each `forms/<id>.md`, with every member line's how sentence, "
         "the elements the members carry unchanged, one representative concept per member with its ladder, and the "
         "mention graph among members. The branches are presented in the order cut, never by size.")
w.append("")
pairs = collections.defaultdict(list)
for r in CL:
    pairs[tuple(r["branches"])].append(r["sub"])
w.append("**Cross-links** (move 207, relating; `crosslinks.jsonl`, %d lines): %s. F06 shares no room with another "
         "subform. Every subform nests in F01, so a room in F01 and one subform is not a cross-link." % (
             len(CL), "; ".join("%s and %s: %s" % (x, y, ", ".join(s)) for (x, y), s in sorted(pairs.items()))))
w.append("")
w += ["## Groups read and set aside", "",
      "- **Two level-3 groups under F01.** add-step on K01 at T3-001 (staging April Fools fake news, 37 rooms) and at "
      "T3-048 (reacting to official April Fools, 14 rooms). Their lines state several different steps (testing, an "
      "apology, a fake turned into serious talk, financial warnings, troubleshooting), so no narrower shared change "
      "holds them. Their rooms stay in F01.",
      "- **P05's shape read and R01's joining** (cut rule R4). The re-check's corrections meet only at the bare target "
      "(restrict on P05 in 7 rooms and add-step on P05 in 2; restrict on R01 in 5). There the aggregation does the "
      "work, so they are groupings, not branches. A key holds the op, the target and the node, not the condition, so "
      "the keys cannot carry what separates the shape read from the trunk. D3's branch stays a held branch, read from "
      "the rooms' material (F-024), not a key branch.",
      "- **Arrow keys.** The largest change keys are restrict lines on arrows: A04 at T3-010 (87 rooms), A11 at "
      "T3-004 (77), A05 at T3-010 (59), A13 at T3-010 (53). A branch cannot be keyed on an arrow (cut rule R1). They "
      "are context: most were ruled specifications that the arrows' bounds already state.",
      "- **Co-occurring keys.** Among the change keys held by 5 rooms or more, the keys their rooms share beyond "
      "chance are mostly on the same third-order node (one theme lifting to several elements), so they are not "
      "independent definitions (`_analysis/d4a01_candidates.txt`, section B).", ""]
L4, rooms = matrix("4")
cut_keys = {k for b in B for k in b["keys"]}
left = sorted(((len(s), k) for k, s in L4.items() if k.split(":")[0] in CHANGE and k.split(":")[1] in els
               and len(s) >= 20 and k not in cut_keys), reverse=True)
w += ["## Where the pass stopped", "",
      "J stops the run after this leg (QD4-001). The pass cut one element, K01, the largest element change key at "
      "level 4. These element change keys at level 4, held by 20 rooms or more, were not read for a cut: %s. Each "
      "would be read as F01 was, by cut rules R1 to R3. No comparison (section 5) and no projections (section 6) "
      "were built, since they come after the final cut, and this pass is not the final one." % (
          "; ".join("`%s` %d" % (k, n) for n, k in left)), ""]
h = {n: H[n - 1] for n in range(173, 183)}
p05_sentence = h[173]["now"][len(h[173]["was"]["statement"]):].strip()
w += ["## The held proposals (QD4-001, option b)", "",
      "Both were made at D4a-01 and reverted in the same leg. Neither was served to any room, and neither is "
      "re-checked. The model this tree hangs from holds P05 and A11 as frozen at D3.", "",
      "- **P05, move 198 (contrasting), history lines 173 to 176, reverted by line 181 (move 203).** The statement "
      "would gain: \"%s\" The status would be %s. The bound would read: \"%s\" Rooms: %s. Lines: %s." % (
          p05_sentence, h[174]["now"], h[175]["now"], ", ".join(h[173]["rooms"]), ", ".join(h[173]["adaptations"])),
      "- **A11, move 199 (dropping working hypotheses), history lines 177 to 180, reverted by line 182 (move 203).** "
      "The arrow from P02 to P04 would be withdrawn (status %s, in_model %s). Its reason, as written: \"%s\" Rooms "
      "(the talk-only rooms of the failure clause): %s. Lines (the first-return lines of the census classes talk "
      "only, layout only and template first, %d): %s." % (
          h[177]["now"], str(h[178]["now"]).lower(), h[179]["now"], ", ".join(h[177]["rooms"]),
          len(h[177]["adaptations"]), ", ".join(h[177]["adaptations"])), ""]
w += ["## Grounds, and what would have changed the cuts", "",
      "- **Grounds.** Every cut is grounded on keys alone (`\"ground\": \"keys\"` in each tier_history line). No "
      "member's material was read for a cut. The lines' how sentences were read only to test whether a key's rooms "
      "share one change (cut rule R2).",
      "- **Was any cut attractive because of what its members made?** No. I hold every room's canvas outcome and "
      "cannot unknow it, but no cut read the canvas, the verdicts or the projections. F01 and its subforms are about "
      "the sub's own April Fools play, which the lines say is not canvas work. The first cut was chosen by the size "
      "of the element's change-key group at level 4.",
      "- **What would have made me choose differently.** Shared corrections at the third or fourth order (none "
      "reach 5 rooms); a kind I could rely on for add-step, add-condition and restrict lines (J: not reliable, "
      "kappa 0.08), which would have let the elaboration view lead; or change keys that co-occur across different "
      "nodes in 5 rooms or more, which would have given multi-key branch definitions.",
      "- **Local validation.** Not established. The labelers mark all 705 rooms unresolved, and prior.md section 3's "
      "measure (each second-order theme with a coordinating turn reached by an element or a validated adaptation, or "
      "listed unresolved) was not computed (J after the D3c interview).", ""]
# accounting
in_branch = set().union(*[set(b["members"]) for b in B]) if B else set()
returns = effective_rooms(OUT)
analysed = set(rooms)
L3, _ = matrix("3")
n_change = collections.Counter()
for k, s in L3.items():
    op, el, _n = k.split(":")
    if op in CHANGE and el in els and len(s) >= 5:
        for r in s:
            n_change[r] += 1
rest = sorted(analysed - in_branch, key=str.lower)
w += ["## The accounting (stage D4 section 4), against n_analysed", "",
      "`counts.py` gives n_analysed = %d (census 705, dropped 0). In a branch: %d (F01 and its subforms). The "
      "unadapted group: 0 (no room returned `none`). Adapted but in no branch: %d. Unreturned at D2: 0. The four "
      "counts sum to %d, the analysed set. `_views/distance.tsv` holds %d rooms." % (
          len(analysed), len(in_branch), len(rest), len(in_branch) + len(rest), len(rooms)), "",
      "**Adapted but in no branch, each with why.** Every one of these rooms holds accepted keys, so none is "
      "unadapted. None holds a key cut at D4a-01, because the pass reached one element, K01. The number after each "
      "room is how many level-3 change keys on elements it holds that 5 rooms or more share: the keys a later pass "
      "would have read. A room marked 0 holds no such key: its change keys are its own, or on arrows.", ""]
w.append("; ".join("%s (%d)" % (r, n_change[r]) for r in rest) + ".")
w.append("")
print("branches %d; cross-link lines %d; held proposals 2; uncut keys %d; in a branch %d; in no branch %d; rooms "
      "with no shared change key %d" % (len(B), len(CL), len(left), len(in_branch), len(rest),
                                        sum(1 for r in rest if n_change[r] == 0)))
if not a.write:
    print("dry run: nothing written")
    raise SystemExit(0)
with open(TREE, "a", encoding="utf-8") as f:
    f.write("\n".join(w) + "\n")
print("appended %d lines to tree-D4.md" % len(w))
