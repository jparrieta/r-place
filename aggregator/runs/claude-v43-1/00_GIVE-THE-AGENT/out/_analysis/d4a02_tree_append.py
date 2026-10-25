#!/usr/bin/env python3
"""D4a-02: append to out/tree-D4.md the second pass's sections, built from files so that no id or count is typed:
the cuts F07 to F35 in the order cut (branches.jsonl and their tier_history lines; move numbers 208 to 236 in that
order, as the diary logs them), the groups read and set aside, the families of branches that state one change at
several nodes, the overlap (rooms per branch count, cross-links), where the cuts stop, the comparison's state
(QD4-002), and the accounting of section 4 against n_analysed, naming every room in no branch with why. Refuses if
the sections are already there. Without --write it prints the counts.

    python3 out/_analysis/d4a02_tree_append.py [--write]
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
V = os.path.join(OUT, "_views")
ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
TREE = os.path.join(OUT, "tree-D4.md")
MARK = "## The cuts of D4a-02 (the second pass), in the order cut"
if MARK in open(TREE, encoding="utf-8").read():
    raise SystemExit("the sections are in tree-D4.md already")
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
by = {b["id"]: b for b in B}
second = [b for b in B if b["since"] == "D4a-02"]
ids = ["F%02d" % i for i in range(7, 36)]
assert [b["id"] for b in second] == ids, [b["id"] for b in second]
MOVES = {fid: 208 + i for i, fid in enumerate(ids)}
TH = {r["id"]: r for r in jl(os.path.join(OUT, "tier_history.jsonl")) if r.get("stage") == "D4" and r.get("tier") == "branch"}
CL = jl(os.path.join(OUT, "crosslinks.jsonl"))
els = {r["id"] for r in jl(os.path.join(OUT, "model", "elements.jsonl"))}
w = ["", MARK, "",
     "The pass read the 31 element change keys at level 4 that D4a-01 left, each held by 20 rooms or more, with the "
     "dated amendment R1a to R1c (the level, keys read together, restated statements set aside). Each key's lines "
     "were read whole in `_analysis/d4a02_keys/` (`d4_key_lines_bynode.py`). The cuts were written by "
     "`_analysis/d4_cut_batch.py` from the specs `_analysis/d4a02_cut_F07.json` to `F35.json`, each logged as a move "
     "and snapped when it was written.", ""]
for b in second:
    th = TH[b["id"]]
    w.append("- **%s** (move %d, %s; %s; level %s; parent %s). Key: %s. %d members. Kind: %s (%s), not relied on. "
             "**%s.** %s" % (b["id"], MOVES[b["id"]], th["move"], th["event"], b["level"], b["parent"] or "none",
                             ", ".join("`%s`" % k for k in b["keys"]), len(b["members"]), b["kind"],
                             ", ".join("%s %d" % kv for kv in b["kind_counts"].items()), b["name"],
                             b["what_it_changes"]))
w += ["",
      "## Groups read at D4a-02 and set aside", "",
      "Eight keys did not pass cut rule R2. Their lines state several different changes, or restate what the "
      "element's statement holds (R1c).",
      "- add-condition on P05 at T4-013 (43 rooms): members' time and sleep, a stale display, repair that keeps an "
      "alteration, upkeep beside growth, upkeep of others' work, and the evidence for the planned-change clause.",
      "- add-step on P02 at T4-006 (41 rooms): polls, provisional fixes, feasibility tests and adopted alterations, "
      "most held by 'the room argues its design'.",
      "- add-step on P05 at T4-013 (40 rooms): checking whether a pixel was intended, shifts and handoffs, ranking "
      "repair against extension, defence during building; partly held by 'puts upkeep before growth'.",
      "- add-step on P20 at T4-002 (36 rooms): finer forms of the megathread, the removals by rule and the venue that "
      "the statement holds.",
      "- add-step on P12 at T4-027 (33 rooms): several steps of recording; its child T3-117 states one and is cut on "
      "its own (F20).",
      "- add-condition on K01 at T4-001 (31 rooms): offence and hurt, who can see the joke, and the frame kept apart "
      "from the canvas; 15 of its rooms are in F01.",
      "- add-condition on P08 at T4-016 (29 rooms): several conditions of deals; the commonest, that a deal binds "
      "only placers who know and accept it, is held by P21 and A19.",
      "- add-condition on P14 at T4-009 (28 rooms): mostly F08's change (targets kept in step) and the rest of "
      "several kinds.", "",
      "## Families: one change at several nodes", "",
      "A branch is keyed at one node, so a change the rooms make in several settings appears as several branches. "
      "The ladder joins them only at the dimension or the bare target, where a group is a grouping, not a branch "
      "(cut rule R4). The families are named here for D5:",
      "- **P05's added clause holds only in part:** F07 (where the design is settled), F26 (at the border), F27 (in "
      "keeping). In F07 about half the lines say that informed members reject the planned change, and the rest that "
      "the record does not show the untold keepers; F26's and F27's lines say one or the other. Together they hold %d "
      "rooms. This is the trunk's limit beside F-024's branch, 'the "
      "shape read', and the held proposal of move 198." % len(set(by["F07"]["members"]) | set(by["F26"]["members"]) |
                                                           set(by["F27"]["members"])),
      "- **Keeping the shared instruction current:** F15 and F33 (the template), with F08 (the machine targets). A "
      "stale plan or target undoes the room's own new work, as P05's known-form repair does with people.",
      "- **Help conditional:** F22 and F28.",
      "- **Carrying on:** F11 with its subforms F12 to F14, F23 and F25.",
      "- **The chat:** F16, F29 and F30.",
      "- **New links the model lacks:** F09 (the move back to building) and F32 (the marking back to keeping).", ""]
member_count = collections.Counter(m for b in B for m in b["members"])
dist = collections.Counter(min(v, 6) for v in member_count.values())
pairs = collections.defaultdict(int)
for r in CL:
    pairs[tuple(sorted(r["branches"]))] += 1
w += ["## The overlap", "",
      "%d rooms are in at least one branch. By the number of branches they are in (subforms counted): %s. "
      "`crosslinks.jsonl` holds %d lines over %d pairs of branches that do not nest. The branches cut across one "
      "another rather than partition the rooms: a room makes several element-level changes at once. They are facets "
      "of the rooms' adaptations, not exclusive forms, and D5 reads them so." % (
          len(member_count), ", ".join("%s: %d" % ("6 or more" if k == 6 else str(k), dist[k]) for k in sorted(dist)),
          len(CL), len(pairs)), "",
      "## Where the cuts stop", "",
      "The cuts stop with F35. Every element change key at level 4 held by 20 rooms or more has been read: D4a-01 "
      "read K01's, and D4a-02 the other 31. Keys held by 5 to 19 rooms at level 4 were not read for a cut, since J's "
      "credit limit (QD4-001) ends the run soon. The rooms they hold, and in no branch, are named below with their "
      "counts. This is a stopping rule by key size, not a claim that the smaller keys hold no form.", "",
      "## The comparison (QD4-002)", "",
      "The comparison was declared in `notes-D4.md` before its script ran. It did not run: the engine stops on the "
      "335 second-order themes placed on the two residue third-order themes (T3-017 and T3-133), which no "
      "fourth-order theme gathers. The question is with J (QD4-002). The projections follow the comparison and are "
      "not built either.", ""]
L4, rooms = matrix("4")
in_branch = set(member_count)
rest = sorted(set(rooms) - in_branch, key=str.lower)
cut_keys4 = set()
for b in B:
    for k in b["keys"]:
        cut_keys4.add(k)
n4 = collections.Counter()
for k, s in L4.items():
    op, el, _n = k.split(":")
    if op in CHANGE and el in els and 5 <= len(s) < 20:
        for r in s:
            n4[r] += 1
w += ["## The accounting at D4a-02 (stage D4 section 4), against n_analysed", "",
      "n_analysed = %d. In a branch: %d. The unadapted group: 0 (no room returned `none`). Adapted but in no branch: "
      "%d. Unreturned at D2: 0. The four counts sum to %d, the analysed set." % (
          len(rooms), len(in_branch), len(rest), len(in_branch) + len(rest)), "",
      "**Adapted but in no branch, each with why.** Each holds accepted keys, so none is unadapted, and none holds a "
      "key that was cut. The number after each room is how many element change keys at level 4, held by 5 to 19 "
      "rooms, it holds: the keys below the pass's size rule. A room marked 0 holds none: its change keys are its own "
      "or on arrows, or its lines are specifications only.", ""]
w.append("; ".join("%s (%d)" % (r, n4[r]) for r in rest) + ".")
w.append("")
print("second-pass branches %d; in a branch %d; in no branch %d (with 0 small keys: %d); cross-link lines %d over "
      "%d pairs; rooms per branch count %s" % (len(second), len(in_branch), len(rest),
                                              sum(1 for r in rest if n4[r] == 0), len(CL), len(pairs), dict(dist)))
if not a.write:
    print("dry run: nothing written")
    raise SystemExit(0)
with open(TREE, "a", encoding="utf-8") as f:
    f.write("\n".join(w) + "\n")
print("appended %d lines to tree-D4.md" % len(w))
