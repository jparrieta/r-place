#!/usr/bin/env python3
"""E1 section 1, the moves: tier_history.jsonl and model/history.jsonl by stage and by move, the move snaps in _snap/
and the diary's move lines against them, and the recuts after C5.

    python3 out/audit-E1/moves.py > out/audit-E1/moves.json

Declared before the run (E1a).
  - Ledger lines by stage and by `move` (as written), both ledgers.
  - Grodal, Anteby and Holm's eight moves: asking questions, focusing on puzzles, dropping, merging, splitting,
    relating, contrasting, developing (or dropping) working hypotheses. A `move` string is mapped to the first of
    these whose key word it holds; one that holds none is listed as unnamed.
  - The diary's move lines (kind `move`, read whole by script from out/diary/) by stage, and the move numbers they
    give ("move N"). The move snaps (_snap/<stage>-move-<name>-<n>.sha256) by stage, with n.
  - From C2 on (the stage file: "since at C2 to D4, and for D6's proposals, a claim with no provenance is a
    defect"): every numbered diary move with no snap of that number at its stage, and every numbered snap with no
    diary move line of that number ("move N", any case). Before C2 the snaps are numbered per move name, so they are
    counted only; at C2 to C5 the diary's move lines carry no number, so lines and snaps are compared by count.
    (A first run read "move N" in lower case only; kept as moves.superseded-1.json.)
  - Recuts after C5: tier_history lines at D1 to D6 by tier and event; model/history lines at D1 to D6 by event, with
    whether each names a D3 cause (adaptations, rechecked or corrects_lines) and whether it is a held proposal.
"""
import collections, glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
# Matched in this order, so that "developing or dropping working hypotheses" is the eighth move, not dropping, and the
# run's joint label "relating or contrasting" stays joint (a first run matched dropping first; moves.superseded-2.json).
EIGHT = [("developing working hypotheses", r"hypothes"), ("relating or contrasting", r"relating or contrasting"),
         ("asking questions", r"asking"), ("focusing on puzzles", r"puzzl"), ("dropping", r"dropp"),
         ("merging", r"merg"), ("splitting", r"split"), ("relating", r"relat"), ("contrasting", r"contrast")]
ORDER = ["A1", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "C5", "D1", "D2", "D3", "D4", "D5", "D6", "E1"]


def jl(p):
    out = []
    for l in open(p, encoding="utf-8"):
        if l.strip():
            try:
                out.append(json.loads(l))
            except ValueError:
                pass
    return out


def eight(m):
    m = (m or "").lower()
    for name, pat in EIGHT:
        if re.search(pat, m):
            return name
    return "unnamed: " + (m or "(none)")


def main():
    th = jl(os.path.join(OUT, "tier_history.jsonl"))
    mh = jl(os.path.join(OUT, "model", "history.jsonl"))
    res = {}
    for name, rows in (("tier_history", th), ("model_history", mh)):
        by = collections.defaultdict(collections.Counter)
        for r in rows:
            by[r.get("stage")][eight(r.get("move"))] += 1
        res[name] = {"lines": len(rows), "by_stage": {s: dict(by[s]) for s in ORDER if s in by},
                     "move_strings": dict(collections.Counter(r.get("move") for r in rows).most_common())}
    diary = [r for p in glob.glob(os.path.join(OUT, "diary", "*.jsonl")) for r in jl(p)]
    dm = [r for r in diary if r.get("kind") == "move"]
    dnum = collections.defaultdict(set)
    for r in dm:
        for n in re.findall(r"\bmoves? (\d+)\b", r.get("text") or "", re.I)[:1]:
            dnum[r.get("stage")].add(int(n))
    snaps = collections.defaultdict(list)
    for p in glob.glob(os.path.join(OUT, "_snap", "*-move-*.sha256")):
        m = re.match(r"^([A-E]\d)-move-(.+)-(\d+)\.sha256$", os.path.basename(p))
        if m:
            snaps[m.group(1)].append((m.group(2), int(m.group(3))))
    res["diary_move_lines"] = {s: sum(1 for r in dm if r.get("stage") == s) for s in ORDER if any(r.get("stage") == s for r in dm)}
    res["diary_move_lines_numbered"] = {s: len(v) for s, v in dnum.items()}
    res["move_snaps"] = {s: len(snaps[s]) for s in ORDER if s in snaps}
    res["move_snap_names"] = {s: dict(collections.Counter(eight(n) for n, _ in snaps[s])) for s in ORDER if s in snaps}
    gaps = {}
    for s in ORDER[ORDER.index("C2"):]:
        sn = {n for _m, n in snaps.get(s, [])}
        dn = dnum.get(s, set())
        if sn or dn:
            gaps[s] = {"diary_move_lines": sum(1 for r in dm if r.get("stage") == s), "move_snaps": len(snaps.get(s, [])),
                       "diary_numbers": len(dn), "snap_numbers": len(sn),
                       "diary_without_snap": sorted(dn - sn), "snap_without_diary": sorted(sn - dn),
                       "range": [min(sn | dn), max(sn | dn)]}
    res["from_C2_numbered"] = gaps
    late = [r for r in th if r.get("stage") in ("D1", "D2", "D3", "D4", "D5", "D6")]
    res["tier_history_after_C5"] = {s: dict(collections.Counter("%s / %s" % (r.get("tier"), r.get("event")) for r in late
                                                                  if r.get("stage") == s)) for s in ORDER if any(r.get("stage") == s for r in late)}
    mlate = [r for r in mh if r.get("stage") in ("D1", "D2", "D3", "D4", "D5", "D6")]
    res["model_history_after_C5"] = {
        "lines": len(mlate),
        "by_stage_event": dict(collections.Counter("%s / %s" % (r.get("stage"), r.get("event")) for r in mlate)),
        "with_D3_cause": sum(1 for r in mlate if r.get("adaptations") or r.get("rechecked") or r.get("corrects_lines")),
        "held_proposal": sum(1 for r in mlate if r.get("held_proposal")),
        "reverts": sum(1 for r in mlate if r.get("reverts_lines") or r.get("reverted_move")),
        "without_D3_cause": [(r.get("stage"), r.get("leg"), r.get("id"), r.get("event")) for r in mlate
                             if not (r.get("adaptations") or r.get("rechecked") or r.get("corrects_lines"))]}
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    sys.exit(main())
