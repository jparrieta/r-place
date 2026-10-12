#!/usr/bin/env python3
"""B2b-r3-p3, the freeze leg: the edits to the T3-002 / T3-033 / T3-038 cluster (J, QB2-012: made here, tested only
by the gold round in B2c), applied to the drafts (out/_analysis/b1e_draft_G*.jsonl), then reassembled.

Round 3's readers divided on signal t01 (T3-033, T3-038, T3-002), n64 t02 (T3-002 with T3-070, T3-002, T3-038)
and 2007scape t04 (T3-070, T3-038, T3-038). Each item holds two or three of the cluster's acts; the readers who
left T3-038 took the opening post (a call, an offer) as "the lead". The three pairs were decided by three
different measures ("the lead", "the larger part", "the side with more concepts"), and none covered an item
holding all three. The edits give the cluster one measure, the concepts of each act counted, and say that the
opening post does not lead because it comes first; and add the missing T3-038/T3-070 question.

  SET       decide_when_both set whole (T3-033, T3-038) or a sentence appended (T3-002)
  REWORD    the pair's question set word for word the same in both gates
  NEWPAIR   a pair with no question in either gate: one question, both gates
Writes, with --write: the drafts; out/scheme_edits.jsonl (one line per theme and field: caused_by, kind, was,
now, why); tier_history.jsonl lines (rescoped, move asking questions); then b1e_assemble.py --write.
"""
import collections, datetime, glob, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
ITEMS = ["signal/t01", "n64/t02", "2007scape/t04"]

COUNT = ("When a theme holds two or more of these acts (an idea of what to make offered to the room, T3-033; "
         "hands called to place, T3-002; the work placed and its progress reported, T3-038), count the concepts "
         "of each: the act with the most concepts of its own is primary, and another is added under rule 0 only "
         "with concepts of its own. The opening post does not lead because it comes first. On a tie, T3-038 when "
         "the work was placed; else T3-002 when the mark was already chosen, T3-033 when it was not.")
SET = [  # (theme, field, op, old, new, why)
    ("T3-002", "decide_when_both", "append", None, " " + COUNT,
     "the cluster had no shared measure for an item holding a call, an offer and the build; one measure, the "
     "concepts of each act counted, is added"),
    ("T3-033", "decide_when_both", "set", None, COUNT,
     "'the lead' was read as the opening post: on signal t01 one reader placed T3-033 on a single opening question "
     "beside two concepts of placing and reporting; the measure is now the concepts of each act counted"),
    ("T3-038", "decide_when_both", "set", None,
     "Building with repairs: the larger part primary and the other under rule 0. " + COUNT,
     "'the larger part' for calls and building differed from the measures of T3-002 and T3-033; the calls are now "
     "under the cluster's one measure, and repairs keep theirs"),
]
Q_002_033 = ("Count the concepts of each: is the larger share an idea of what to make offered to the room (T3-033), "
             "or hands called to a mark already chosen (T3-002)? The opening post does not lead because it comes first.")
Q_002_038 = ("Count the concepts of each: is the larger share the work placed and its progress reported (T3-038), or "
             "hands called for it (T3-002)? An opening call does not lead because it comes first.")
Q_033_038 = ("Count the concepts of each: is the larger share an idea of what to make offered to the room (T3-033), or "
             "the mark placed and its progress reported (T3-038)? A proposal does not lead because it comes first.")
REWORD = [  # (a, b, question)
    ("T3-002", "T3-033", Q_002_033),
    ("T3-002", "T3-038", Q_002_038),
    ("T3-033", "T3-038", Q_033_038),
]
NEWPAIR = [  # (a, b, question)
    ("T3-038", "T3-070",
     "Is the mark placed and its state reported, coordinates given as where the work stands or where to see it "
     "(T3-038), or are directions posted for placers to follow, coordinates, templates, guides or colour plans "
     "(T3-070)? A link to the finished work is a report, not a direction."),
]


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    write = "--write" in sys.argv
    drafts, files = {}, {}
    for p in sorted(glob.glob(os.path.join(AN, "b1e_draft_G*.jsonl"))):
        rows = jl(p)
        files[p] = rows
        for r in rows:
            drafts[r["id"]] = r
    before = {t: json.loads(json.dumps(r)) for t, r in drafts.items()}
    why = collections.defaultdict(list)
    for t, field, op, old, new, w in SET:
        r = drafts[t]
        if op == "append":
            if new.strip() in (r[field] or ""):
                sys.exit("%s %s already holds the appended sentence" % (t, field))
            r[field] = (r[field] or "").rstrip() + new
        else:
            if r[field] == new:
                sys.exit("%s %s already reads so" % (t, field))
            r[field] = new
        why[(t, field)].append(w)
    for a, b, q in REWORD:
        for x, y in ((a, b), (b, a)):
            ds = [d for d in drafts[x]["discriminators"] if d["vs"] == y]
            if len(ds) != 1:
                sys.exit("%s has %d questions against %s; a reword needs one" % (x, len(ds), y))
            if ds[0]["question"] == q:
                sys.exit("%s vs %s already reads so" % (x, y))
            ds[0]["question"] = q
            why[(x, "discriminators")].append("the %s/%s question set word for word in both gates, with the cluster's "
                                              "one measure (concepts of each act counted)" % (a, b))
    for a, b, q in NEWPAIR:
        for x, y in ((a, b), (b, a)):
            if y in {d["vs"] for d in drafts[x]["discriminators"]}:
                sys.exit("%s already has a question against %s" % (x, y))
            drafts[x]["discriminators"].append({"vs": y, "question": q})
            why[(x, "discriminators")].append("a new question in both gates of %s/%s, which had none; on 2007scape t04 "
                                              "one round-3 reader placed T3-070 where two placed T3-038, and on n64 t02 "
                                              "one added T3-070 for the link to the finished logo" % (a, b))
    changed = sorted(why)
    print("theme-fields changed %d over %d themes" % (len(changed), len({t for t, _ in changed})))
    for t, f in changed:
        print("  %s %s" % (t, f))
    if not write:
        return
    for p, rows in files.items():
        with open(p, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ep = os.path.join(OUT, "scheme_edits.jsonl")
    n0 = len(jl(ep))
    with open(ep, "a", encoding="utf-8") as fh, open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as th:
        for i, (t, f) in enumerate(changed, n0 + 1):
            was, nw = before[t][f], drafts[t][f]
            w = "; ".join(why[(t, f)])
            fh.write(json.dumps({"n": i, "edit": "edit:%d" % i, "round": 3, "leg": "B2b-r3-p3", "t": now, "theme": t,
                                 "field": f, "caused_by": ITEMS, "kind": "scheme-ambiguous", "was": was, "now": nw,
                                 "why": w + "; made at the freeze, tested only by the gold round in B2c (J, QB2-012)",
                                 "asks": ["QB2-012"]}, ensure_ascii=False) + "\n")
            th.write(json.dumps({"t": now, "stage": "B2", "leg": "B2b-r3-p3", "tier": "third", "id": t,
                                 "move": "asking questions", "event": "rescoped", "was": {"field": f, "text": was},
                                 "now": [{"id": t, "field": f, "text": nw}],
                                 "prompted_by": "B2 round 3: readers' placements on %s" % ", ".join(ITEMS),
                                 "why": w + "; the theme's members are unchanged (no narrowing)",
                                 "edit": "edit:%d" % i}, ensure_ascii=False) + "\n")
    print("scheme_edits.jsonl lines %d to %d" % (n0 + 1, n0 + len(changed)))
    subprocess.run([sys.executable, os.path.join(AN, "b1e_assemble.py"), "--write"], check=True)


if __name__ == "__main__":
    main()
