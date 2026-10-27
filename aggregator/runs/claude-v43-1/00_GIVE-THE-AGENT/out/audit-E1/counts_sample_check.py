#!/usr/bin/env python3
"""E1 section 1, the counts rule (E1b-02): the seeded sample of counts_phrases.json, recomputed where a governing file
can be counted. Prints JSON, one row per sampled phrase (1 to 36, in the sample's order).

    python3 out/audit-E1/counts_sample_check.py > out/audit-E1/counts_sample_check.json

The rule, declared before the run (E1b-02): each row names the governing file and how the count is taken from it now.
A ledger whose lines carry a stage is filtered to the stage the handback closed. A count whose only record is a
reading by hand or a prose note is marked "not recomputed", with the file and line where it is stated; it is read in
the audit section, not counted as agreeing.
"""
import collections, csv, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip()]


def n_lines(p):
    return sum(1 for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip())


def main():
    R = {}
    store = lambda f: [json.loads(l) for l in open(os.path.join(ROOT, "package", "store", f), encoding="utf-8") if l.strip()]
    defects = jl("defects.jsonl")
    R[1] = ("A1: 79 of 100 concepts", "not recomputed", "coordinating-rule-A1.md line 85 states the judgment by hand on 100 drawn concepts; no sheet of the 100 judgments is named")
    R[2] = ("A1: defects.jsonl 7 lines", sum(1 for d in defects if d.get("stage") == "A1"), "defects.jsonl lines of stage A1 now; handback-A1.md line 72 says 8 later in A1")
    R[3] = ("B1: 107 episode lines", "not recomputed", "notes-B1.md line 3108 (B2): wrong; 106 (line, kind) pairs over 81 lines, by _analysis/b2_episode_kinds.py")
    R[4] = ("B1: pass2-B1.jsonl 108 rooms", len({r.get("sub") for r in jl("pass2-B1.jsonl")}), "distinct sub in pass2-B1.jsonl")
    R[5] = ("B2: exemplar_candidates.jsonl 68 lines", n_lines("exemplar_candidates.jsonl"), "lines")
    R[6] = ("B2: scheme_edits.jsonl 306 lines", n_lines("scheme_edits.jsonl"), "lines now")
    b3 = jl("batches-B3.jsonl")
    R[7] = ("B3: 1,212 readers", len(b3), "batches-B3.jsonl lines, one reader each")
    R[8] = ("B3: 8 multi lines", sum(1 for d in defects if d.get("stage") == "B3" and (d.get("kind") or "").startswith("reader's record slip: multi line")),
            "defects.jsonl B3 lines of kind 'reader's record slip: multi line ...' (the first run read a 'what' key B3's lines lack)")
    line = open(os.path.join(OUT, "adjudication_report.md"), encoding="utf-8").read().split("\n")[255]
    items = line.split("Items:", 1)[1] if "Items:" in line else ""
    R[9] = ("B4: T3-005|T3-021 90 items", len(re.findall(r"\b\w+ t\d+\b", items)), "items listed in adjudication_report.md line 256")
    rr = jl("readings-R-B4.jsonl")
    R[10] = ("B4: stratum R 185 unresolved items", len({(r.get("sub"), r.get("theme") or r.get("item") or r.get("item_id")) for r in rr if r.get("stratum") == "R"}),
             "distinct items of stratum R in readings-R-B4.jsonl")
    fourth = jl("fourth/fourth.jsonl")
    scheme = jl("scheme_final.jsonl")
    members = set()
    for t in fourth:
        for k in ("members", "third", "third_order"):
            if isinstance(t.get(k), list):
                members |= set(t[k])
    R[11] = ("C1: 195 of 197 third-order themes", "%d of %d" % (len(members & {s.get("id") for s in scheme}), len(scheme)), "fourth.jsonl members against scheme_final.jsonl, now")
    dec = next((t for t in fourth if t.get("name") == "Decided order"), {})
    dm = set(next((dec[k] for k in ("members", "third", "third_order") if isinstance(dec.get(k), list)), []))
    af = jl("assignments_final.jsonl")
    on = [a for a in af if (set(a["third_order"]) if isinstance(a.get("third_order"), list) else {a.get("third_order")}) & dm]
    R[12] = ("C1: Decided order 48 lines in 46 rooms", "%d lines in %d rooms" % (len(on), len({a.get("sub") for a in on})), "assignments_final.jsonl lines on its members %s, now" % sorted(dm))
    R[13] = ("C2: 500 shuffles", "not recomputed", "a parameter of the order test; see the C2 scripts")
    R[14] = ("C2: 28 fourth-order themes", len(fourth), "fourth/fourth.jsonl lines now")
    F = jl("findings.jsonl")
    upto = {"B1", "B2", "C1", "C2", "C3"}
    R[15] = ("C3: findings.jsonl 25 lines and 17 findings", "%d lines and %d findings" % (sum(1 for f in F if f.get("stage") in upto), len({f["id"] for f in F if f.get("stage") in upto})), "lines of stages to C3")
    R[16] = ("C3: 28 fourth-order themes", len(fourth), "fourth/fourth.jsonl lines now")
    R[17] = ("C4: 78 rooms", "not recomputed", "the count of rooms older than the canvas, in the field comparison")
    R[18] = ("C4: 6 items", "not recomputed", "the table of field-C4.md")
    R[19] = ("C5-p14: 115,388 concepts", len(store("codes.jsonl")), "package/store/codes.jsonl lines")
    H = jl("model/history.jsonl")
    R[20] = ("C5-p14: history 31 lines (12 arrow)", "not recomputed", "the model history at pass 14; see the reading")
    R[21] = ("C5: 500 shuffles", "not recomputed", "a parameter of the order test")
    R[22] = ("C5: 7,844 second-order themes", len(store("themes.jsonl")), "package/store/themes.jsonl lines")
    R[23] = ("D1: 28 fourth-order themes", len(fourth), "fourth/fourth.jsonl lines now")
    pr = open(os.path.join(OUT, "prior.md"), encoding="utf-8").read()
    m = re.search(r"floor[^.]{0,80}?(\d+) first-order concepts|(\d+) first-order concepts[^.]{0,40}floor", pr)
    R[24] = ("D1: concept floor 10 first-order concepts", (m.group(1) or m.group(2)) if m else "not found", "prior.md section 8")
    V = jl("verdicts-D.jsonl")
    first = [v for v in V if not v.get("stage")]
    R[25] = ("D2: 705 rooms returned", len({v["sub"] for v in first}), "verdicts-D.jsonl first-return lines, distinct rooms")
    A = jl("adaptations.jsonl")
    np_ = [a for a in A if a.get("portable") is False]
    R[26] = ("D2: non-portable 763 lines in 356 rooms", "%d lines in %d rooms" % (len(np_), len({a["sub"] for a in np_})), "adaptations.jsonl portable false")
    AR = jl("adaptations-recheck.jsonl")
    R[27] = ("D3: 705 rooms went back", len({a["sub"] for a in AR}), "adaptations-recheck.jsonl distinct rooms")
    R[28] = ("D3: fixed in 48 rooms", "not recomputed", "notes-D3.md line 6965 and the table after it")
    R[29] = ("D4: 626 rooms (705 less 79)", 705 - 79, "notes-D4.md line 115 gives the 79 low-information rows")
    R[30] = ("D4: 229 in no branch", None, "counts_rule.json D4_four_counts")
    cr = json.load(open(os.path.join(OUT, "audit-E1", "counts_rule.json"), encoding="utf-8"))
    R[30] = ("D4: 229 in no branch", cr["D4_four_counts"]["rest"], "checks/stage_D4 four_counts (counts_rule.json)")
    R[31] = ("D5-room-forms: room-forms-D5.jsonl 6 lines", n_lines("room-forms-D5.jsonl"), "lines")
    B = jl("branches.jsonl")
    R[32] = ("D5-room-forms: 35 branch accounts", len(B), "branches.jsonl lines")
    in_branch = set()
    for b in B:
        for k in ("members", "rooms", "subs"):
            if isinstance(b.get(k), list):
                in_branch |= set(b[k])
    import glob  # the first run read the analyst's D3 rulings in verdicts-D.jsonl, not the re-check readers
    rv = collections.defaultdict(list)
    for p in glob.glob(os.path.join(OUT, "rooms", "*", "verdict-D-recheck.jsonl")):
        for l in open(p, encoding="utf-8"):
            if l.strip():
                v = json.loads(l)  # keyed by the room's folder: the readers' own `sub` field is spelt variously
                rv[os.path.basename(os.path.dirname(p))].append(v.get("verdict"))
    ct = [s for s, vs in rv.items() if vs and all(x == "cannot-tell" for x in vs)]
    R[33] = ("D5: 19 cannot-tell at the re-check, 16 in no branch", "%d cannot-tell, %d in no branch" % (len(set(ct)), len(set(ct) - in_branch)),
             "rooms/<sub>/verdict-D-recheck.jsonl, rooms where every reader says cannot-tell, against branches.jsonl members")
    R[34] = ("D5: 476 rooms in a branch", len(in_branch), "branches.jsonl members, distinct")
    rows = list(csv.DictReader(open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8"), delimiter="\t"))
    R[35] = ("D6: form B 113 defining rooms", sum(1 for r in rows if r.get("form") == "B" and r.get("role") == "defining"), "room-forms-tree-rooms.tsv")
    R[36] = ("D6: the drawing's 20 arrows", "not recomputed", "figure-D6.md draws the C5 drawing; see the reading")
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-02):")[1].strip(),
                      "rows": [{"n": k, "claim": v[0], "now": v[1], "how": v[2]} for k, v in sorted(R.items())]},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
