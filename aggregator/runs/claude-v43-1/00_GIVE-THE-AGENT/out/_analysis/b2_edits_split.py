#!/usr/bin/env python3
"""B2b-r1, after QB2-003: rewrite the round-1 edits one line per change.

Reads the first, bundled record (out/_analysis/scheme_edits_b2b-r1_bundled.jsonl: one line per theme and
field, mirrors and new questions mixed) and writes out/scheme_edits.jsonl with:
  - each explicit sentence change (must_show, must_not_show, decide_when_both) as its own line, ordinary kind,
    caused_by the round-1 items;
  - each discriminator question added because readers split (b2_edits_r1.ADD), ordinary kind, the items;
  - each new question written for a must_not_show with no discriminator (b2_edits_r1.NEWPAIR), kind
    scheme-ambiguous, caused_by gates:A|B, owing rechecks and a tier_history line;
  - each mirror (a question copied word for word into the other gate), kind gate-check, caused_by gates:A|B,
    no recheck, no tier_history line.
Appends one tier_history line per non-gate-check edit, naming its edit number; the 36 lines written for the
bundled record stay in tier_history.jsonl and are superseded by these (notes-B2.md says so).
Dry run by default; --write writes.
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(OUT, "_analysis"))
import b2_edits_r1 as E  # noqa: E402


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    write = "--write" in sys.argv
    old = jl(os.path.join(OUT, "_analysis", "scheme_edits_b2b-r1_bundled.jsonl"))
    add = {(t, vs) for t, vs, _ in E.ADD}
    newpair = {}
    for a, b, q in E.NEWPAIR:
        newpair[(a, b)] = (a, b)
        newpair[(b, a)] = (a, b)
    expl = {(t, f): (w, op) for t, f, op, _, _, w in E.EXPLICIT}
    lines = []
    for o in old:
        t, f = o["theme"], o["field"]
        if f != "discriminators":
            w, _ = expl[(t, f)]
            lines.append(dict(theme=t, field=f, caused_by=o["caused_by"], kind=E.KIND.get(t, "scheme-ambiguous"),
                              was=o["was"], now=o["now"], why=w))
            continue
        before = {d["vs"] for d in o["was"]}
        for d in o["now"]:
            if d["vs"] in before:
                continue
            vs = d["vs"]
            nowlist = [x for x in o["now"] if x["vs"] in before or x["vs"] == vs]
            if (t, vs) in add:
                lines.append(dict(theme=t, field="discriminators", caused_by=sorted(set(E.ITEMS.get(t) or E.ITEMS[vs])),
                                  kind=E.KIND.get(t, "scheme-ambiguous"), was=o["was"], now=nowlist, added={"vs": vs, "question": d["question"]},
                                  why="a discriminator against %s added because round 1's readers split on the pair" % vs))
            elif (t, vs) in newpair:
                a, b = newpair[(t, vs)]
                lines.append(dict(theme=t, field="discriminators", caused_by=["gates:%s|%s" % (a, b)], kind="scheme-ambiguous",
                                  was=o["was"], now=nowlist, added={"vs": vs, "question": d["question"]},
                                  why="%s's must_not_show sends material to %s with no discriminator between them (mem.py gates); a new question written for both gates" % (a, b)))
            else:
                lines.append(dict(theme=t, field="discriminators", caused_by=["gates:%s|%s" % (vs, t)], kind="gate-check",
                                  was=o["was"], now=nowlist, added={"vs": vs, "question": d["question"]},
                                  why="one-way discriminator: %s's question against %s copied word for word into %s's gate (mem.py gates)" % (vs, t, t)))
    kinds = {}
    for x in lines:
        kinds[x["kind"]] = kinds.get(x["kind"], 0) + 1
    print("lines %d: %s" % (len(lines), kinds))
    if not write:
        return
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(os.path.join(OUT, "scheme_edits.jsonl"), "w", encoding="utf-8") as fh, \
            open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as th:
        for i, x in enumerate(lines, 1):
            rec = {"n": i, "edit": "edit:%d" % i, "round": 1, "leg": "B2b-r1", "t": now}
            rec.update(x)
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if x["kind"] == "gate-check":
                continue
            th.write(json.dumps({"t": now, "stage": "B2", "leg": "B2b-r1", "tier": "third", "id": x["theme"],
                                 "move": "asking questions", "event": "rescoped",
                                 "was": {"field": x["field"], "text": x["was"] if x["field"] != "discriminators" else [d["vs"] for d in x["was"]]},
                                 "now": [{"id": x["theme"], "field": x["field"],
                                          "text": x["now"] if x["field"] != "discriminators" else x["added"]}],
                                 "prompted_by": "B2 round 1: %s" % ", ".join(x["caused_by"]),
                                 "why": x["why"] + "; the theme's members are unchanged (no narrowing)",
                                 "edit": "edit:%d" % i, "supersedes_bundled_line": True}, ensure_ascii=False) + "\n")
    print("wrote out/scheme_edits.jsonl and appended the tier_history lines")


if __name__ == "__main__":
    main()
