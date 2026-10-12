#!/usr/bin/env python3
"""B2b-r3-p3, the freeze leg, second set: fixes the pair reading (out/_analysis/b2_pairs_read.txt, 449 pairs)
called for before the pairs could be confirmed.

  T3-072 and T3-157 decide_when_both said "T3-009 primary" for thanks to allies and for reflection inside a
  celebration, while T3-009's (and T3-043's) says the side with more concepts is primary: the two gates of each
  pair contradicted each other. They now say what T3-009 says.
  The T3-038/T3-070 question added at edits 301 and 302 sent "where to see it" and a link to the finished work
  to T3-038, which T3-026's must_show already takes ("others pointed to where it is"). It now keeps T3-038 for
  the work in progress and points a link to the finished work at T3-026.
Applied to the drafts, then b1e_assemble.py; scheme_edits.jsonl and tier_history.jsonl lines as at
b2_edits_freeze.py. Dry run unless --write.
"""
import collections, datetime, glob, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")

SET = [  # (theme, field, old, new, caused_by, why)
    ("T3-072", "decide_when_both",
     "Thanks to allies inside a celebration: T3-009 primary; T3-072 added where the allies have concepts of their own",
     "Thanks to allies inside a celebration: the side with more concepts is primary, T3-009 when the celebrating "
     "holds more; the other added only where its part has concepts of its own",
     ["gates:T3-009|T3-072"],
     "the pair's gates contradicted each other: T3-009 makes T3-072 primary when the allies hold more concepts, "
     "T3-072 said T3-009 primary; T3-072 now says what T3-009 and T3-043 say"),
    ("T3-157", "decide_when_both",
     "Reflection inside a celebration: T3-009 primary; T3-157 added where the reflection has concepts of its own",
     "Reflection inside a celebration: the side with more concepts is primary, T3-009 when the celebrating holds "
     "more; the other added only where its part has concepts of its own",
     ["gates:T3-009|T3-157"],
     "the pair's gates contradicted each other: T3-009 makes T3-157 primary when the reflection holds more "
     "concepts, T3-157 said T3-009 primary; T3-157 now says what T3-009 and T3-043 say"),
]
Q = ("Is the mark being placed and its progress reported, coordinates given as where the work in progress stands "
     "(T3-038), or are directions posted for placers to follow, coordinates, templates, guides or colour plans "
     "(T3-070)? A link that only shows where the finished work is points to it (T3-026), not a direction.")
REWORD = [("T3-038", "T3-070", Q, ["n64/t02", "2007scape/t04", "gates:T3-026|T3-038"])]


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
    why, cause = collections.defaultdict(list), collections.defaultdict(list)
    for t, f, old, new, cb, w in SET:
        if drafts[t][f].count(old) != 1:
            sys.exit("%s %s does not hold the sentence once: %r" % (t, f, drafts[t][f]))
        drafts[t][f] = drafts[t][f].replace(old, new)
        why[(t, f)].append(w); cause[(t, f)] += cb
    for a, b, q, cb in REWORD:
        for x, y in ((a, b), (b, a)):
            ds = [d for d in drafts[x]["discriminators"] if d["vs"] == y]
            if len(ds) != 1 or ds[0]["question"] == q:
                sys.exit("%s vs %s: %d questions, or already so" % (x, y, len(ds)))
            ds[0]["question"] = q
            why[(x, "discriminators")].append(
                "the T3-038/T3-070 question sent a link to the finished work to T3-038, which T3-026's must_show takes; "
                "it now keeps T3-038 for the work in progress and points such a link at T3-026 (found reading the "
                "T3-026/T3-038 pair at the freeze)")
            cause[(x, "discriminators")] += cb
    changed = sorted(why)
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
                                 "field": f, "caused_by": sorted(set(cause[(t, f)])), "kind": "scheme-ambiguous",
                                 "was": was, "now": nw,
                                 "why": w + "; made at the freeze, tested only by the gold round in B2c (J, QB2-012)",
                                 "asks": ["QB2-012"]}, ensure_ascii=False) + "\n")
            th.write(json.dumps({"t": now, "stage": "B2", "leg": "B2b-r3-p3", "tier": "third", "id": t,
                                 "move": "asking questions", "event": "rescoped", "was": {"field": f, "text": was},
                                 "now": [{"id": t, "field": f, "text": nw}],
                                 "prompted_by": "B2 freeze: the gate-pair reading", "why": w + "; the theme's members are "
                                 "unchanged (no narrowing)", "edit": "edit:%d" % i}, ensure_ascii=False) + "\n")
    print("scheme_edits.jsonl lines %d to %d" % (n0 + 1, n0 + len(changed)))
    subprocess.run([sys.executable, os.path.join(AN, "b1e_assemble.py"), "--write"], check=True)


if __name__ == "__main__":
    main()
