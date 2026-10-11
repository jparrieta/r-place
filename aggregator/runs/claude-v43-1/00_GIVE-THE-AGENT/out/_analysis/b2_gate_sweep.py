#!/usr/bin/env python3
"""B2b-r1, after QB2-003: repair the gate defects that no item caused, in the drafts, then reassemble.

  --mirror FILE   every "X has one against Y; Y none against X" line in FILE (a saved `mem.py gates` report):
                  X's question copied word for word into Y's gate; kind gate-check, caused_by gates:X|Y
  --pairs FILE    a JSON list of [A, B, question]: a new question for A's must_not_show naming B, added to both
                  gates; kind scheme-ambiguous, caused_by gates:A|B (owes rechecks and a tier_history line)
Appends to out/scheme_edits.jsonl (numbering on) and, for new questions, to tier_history.jsonl.
Dry run by default; --write writes and runs b1e_assemble.py --write.
"""
import datetime, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    write = "--write" in sys.argv
    files, drafts = {}, {}
    for p in sorted(glob.glob(os.path.join(AN, "b1e_draft_G*.jsonl"))):
        files[p] = jl(p)
        for r in files[p]:
            drafts[r["id"]] = r
    recs = []

    def add(t, vs, q, kind, cb, why):
        r = drafts[t]
        if vs in {d["vs"] for d in r["discriminators"]}:
            return
        was = json.loads(json.dumps(r["discriminators"]))
        r["discriminators"].append({"vs": vs, "question": q})
        recs.append(dict(theme=t, field="discriminators", caused_by=[cb], kind=kind, was=was,
                         now=json.loads(json.dumps(r["discriminators"])), added={"vs": vs, "question": q}, why=why))

    if "--mirror" in sys.argv:
        one = re.compile(r"^\s+(T3-\d+) has one against (T3-\d+); (T3-\d+) none against")
        for line in open(sys.argv[sys.argv.index("--mirror") + 1], encoding="utf-8"):
            m = one.match(line)
            if m:
                x, y = m.group(1), m.group(2)
                q = next(d["question"] for d in drafts[x]["discriminators"] if d["vs"] == y)
                add(y, x, q, "gate-check", "gates:%s|%s" % (x, y),
                    "one-way discriminator: %s's question against %s copied word for word into %s's gate (mem.py gates)" % (x, y, y))
    if "--pairs" in sys.argv:
        for a, b, q in json.load(open(sys.argv[sys.argv.index("--pairs") + 1], encoding="utf-8")):
            w = "%s's must_not_show sends material to %s with no discriminator between them (mem.py gates); a new question written for both gates" % (a, b)
            add(a, b, q, "scheme-ambiguous", "gates:%s|%s" % (a, b), w)
            add(b, a, q, "scheme-ambiguous", "gates:%s|%s" % (a, b), w)
    kinds = {}
    for x in recs:
        kinds[x["kind"]] = kinds.get(x["kind"], 0) + 1
    print("questions added %d: %s; themes touched %d" % (len(recs), kinds, len({x["theme"] for x in recs})))
    if not write:
        return
    for p, rows in files.items():
        with open(p, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    ep = os.path.join(OUT, "scheme_edits.jsonl")
    n0 = len(jl(ep))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(ep, "a", encoding="utf-8") as fh, open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as th:
        for i, x in enumerate(recs, n0 + 1):
            rec = {"n": i, "edit": "edit:%d" % i, "round": 1, "leg": "B2b-r1", "t": now}
            rec.update(x)
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if x["kind"] != "gate-check":
                th.write(json.dumps({"t": now, "stage": "B2", "leg": "B2b-r1", "tier": "third", "id": x["theme"],
                                     "move": "asking questions", "event": "rescoped",
                                     "was": {"field": "discriminators", "text": [d["vs"] for d in x["was"]]},
                                     "now": [{"id": x["theme"], "field": "discriminators", "text": x["added"]}],
                                     "prompted_by": "the gate check (mem.py gates): %s" % x["caused_by"][0],
                                     "why": x["why"] + "; the theme's members are unchanged (no narrowing)",
                                     "edit": "edit:%d" % i}, ensure_ascii=False) + "\n")
    print("scheme_edits.jsonl lines %d to %d" % (n0 + 1, n0 + len(recs)))
    subprocess.run([sys.executable, os.path.join(AN, "b1e_assemble.py"), "--write"], check=True)


if __name__ == "__main__":
    main()
