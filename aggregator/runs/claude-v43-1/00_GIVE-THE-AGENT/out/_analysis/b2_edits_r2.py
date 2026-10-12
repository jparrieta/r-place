#!/usr/bin/env python3
"""B2b-r2-p2: the round-2 scheme edits, applied to the drafts (out/_analysis/b1e_draft_G*.jsonl), then reassembled.

  EXPLICIT  a sentence field changed (set, append or replace), because readers split or all left my placement
  REWORD    a discriminator question reworded, in both gates of the pair, word for word the same
  NEWPAIR   a pair with no question in either gate, on which round 2's readers split: one question, both gates
Writes, with --write: the drafts; out/scheme_edits.jsonl (one line per theme and field changed: caused_by,
kind, was, now, why); tier_history.jsonl lines (rescoped, move asking questions); then b1e_assemble.py
--write. Dry run by default. Round 2's readers were deepseek/deepseek-v4.1-flash at medium effort (J).
"""
import collections, datetime, glob, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")

FLAG = ("Is the work a flag of the land the room is named for or speaks for, a flag built in r/guatemala being "
        "Guatemala's unless its concepts name another (T3-065), or any other picture (T3-002)?")
FLAG26 = ("Is the room's mark announced as up (T3-026), or is the work a flag of the land the room is named for or "
          "speaks for, announced, called for or built (T3-065)? A flag built in a room named for a land is that "
          "land's flag unless its concepts name another.")
EXPLICIT = [  # (theme, field, op, old, new, why, items)
    ("T3-065", "gloss", "append", None,
     " A flag built in a room named for a land is that land's flag unless its concepts name another.",
     "on guatemala t02, whose concepts say only 'a flag' in r/guatemala, all three round-2 readers placed T3-002, "
     "T3-167 and T3-026 and none T3-065, and two never opened G17; the index gloss did not say that a room named "
     "for a land builds that land's flag", ["guatemala/t02"]),
]
REWORD = [  # (theme a, theme b, new question): both gates
    ("T3-002", "T3-065", FLAG, ["guatemala/t02"]),
    ("T3-026", "T3-065", FLAG26, ["guatemala/t02"]),
]
NEWPAIR = [  # (a, b, question, items)
    ("T3-033", "T3-038",
     "Is an idea of what to make offered to the room (T3-033), or a mark being placed and its progress reported "
     "(T3-038)? A proposal followed by its placing: the side with more concepts is primary.",
     ["n64/t02", "dofus/t01"]),
    ("T3-195", "T3-011",
     "Is an agreement already made invoked, spread or said to be broken (T3-195), or another room's work helped or "
     "defended, the pledge named only as the reason for the help (T3-011)?",
     ["nVade/t04"]),
    ("T3-195", "T3-005",
     "Is an agreement already made invoked, spread or said to be broken (T3-195), or the room's own work defended, "
     "the pledge named only as the reason for the defence (T3-005)?",
     ["nVade/t04"]),
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
    why, cause = collections.defaultdict(list), collections.defaultdict(set)
    for t, field, op, old, new, w, items in EXPLICIT:
        r = drafts[t]
        if op == "replace":
            if old not in r[field]:
                sys.exit("not found in %s %s: %r" % (t, field, old))
            r[field] = r[field].replace(old, new)
        elif op == "append":
            if new.strip() in (r[field] or ""):
                sys.exit("%s %s already holds the appended sentence" % (t, field))
            r[field] = (r[field] or "").rstrip() + new
        else:
            r[field] = new
        why[(t, field)].append(w); cause[(t, field)] |= set(items)
    for a, b, q, items in REWORD:
        for x, y in ((a, b), (b, a)):
            ds = [d for d in drafts[x]["discriminators"] if d["vs"] == y]
            if len(ds) != 1:
                sys.exit("%s has %d questions against %s; a reword needs one" % (x, len(ds), y))
            if ds[0]["question"] == q:
                sys.exit("%s vs %s already reads so" % (x, y))
            ds[0]["question"] = q
            why[(x, "discriminators")].append("the %s/%s question reworded in both gates: the reader must be told whose flag a flag in a room named for a land is (guatemala t02, round 2)" % (a, b))
            cause[(x, "discriminators")] |= set(items)
    for a, b, q, items in NEWPAIR:
        for x, y in ((a, b), (b, a)):
            if y in {d["vs"] for d in drafts[x]["discriminators"]}:
                sys.exit("%s already has a question against %s" % (x, y))
            drafts[x]["discriminators"].append({"vs": y, "question": q})
            why[(x, "discriminators")].append("a new question in both gates of %s/%s, which had none; round 2's readers split on the pair (%s)" % (a, b, ", ".join(items)))
            cause[(x, "discriminators")] |= set(items)
    changed = sorted(why)
    print("theme-fields changed %d over %d themes" % (len(changed), len({t for t, _ in changed})))
    for t, f in changed:
        print("  %s %s: %s" % (t, f, "; ".join(sorted(cause[(t, f)]))))
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
            fh.write(json.dumps({"n": i, "edit": "edit:%d" % i, "round": 2, "leg": "B2b-r2-p2", "t": now, "theme": t,
                                 "field": f, "caused_by": sorted(cause[(t, f)]), "kind": "scheme-ambiguous",
                                 "was": was, "now": nw, "why": "; ".join(why[(t, f)]), "asks": []},
                                ensure_ascii=False) + "\n")
            th.write(json.dumps({"t": now, "stage": "B2", "leg": "B2b-r2-p2", "tier": "third", "id": t,
                                 "move": "asking questions", "event": "rescoped", "was": {"field": f, "text": was},
                                 "now": [{"id": t, "field": f, "text": nw}],
                                 "prompted_by": "B2 round 2: readers' placements on %s" % ", ".join(sorted(cause[(t, f)])),
                                 "why": "; ".join(why[(t, f)]) + "; the theme's members are unchanged (no narrowing)",
                                 "edit": "edit:%d" % i}, ensure_ascii=False) + "\n")
    print("scheme_edits.jsonl lines %d to %d" % (n0 + 1, n0 + len(changed)))
    subprocess.run([sys.executable, os.path.join(AN, "b1e_assemble.py"), "--write"], check=True)


if __name__ == "__main__":
    main()
