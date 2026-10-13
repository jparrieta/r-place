#!/usr/bin/env python3
"""C1, section 1: the four sources that say where the scheme is weak, counted per third-order theme as declared in
notes-C1.md ("Pass 2 (C1a-02)", before counting).

  disagreements   the theme is the `theme` of a scheme-ambiguous ruling (the sentence that failed); count of rulings
  reassign        arm 1 (reassign.jsonl): on a disagrees-contested reading, the theme in the settled set and not the
                  fresh set, or in the fresh set and not the settled set; count of readings. Arm 2
                  (reassign-openai-astra.jsonl) counted the same way and reported beside, never pooled
  conflicts       the theme is in a pair a coder conflict "may explain"; count of conflicts
  row 4           the theme is in my set or the readers' set on an item of transmission-B4.md's fourth row; count of items

Prints the themes in three or four sources, and with --write records every theme's counts in
out/_analysis/c1_weak_sources.json.

    python3 out/_analysis/c1_weak_sources.py [--write]
"""
import collections, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def fresh(name):
    c = collections.Counter()
    for r in jl(name):
        if r.get("outcome") != "disagrees-contested":
            continue
        S, F = set(r.get("settled") or []), set(r.get("third_order") or [])
        for t in S ^ F:
            c[t] += 1
    return c


def main():
    S = {r["id"]: r for r in jl("scheme_final.jsonl")}
    dis = collections.Counter(d["theme"] for d in jl("disagreements.jsonl")
                              if d.get("taxonomy") == "scheme-ambiguous" and d.get("theme"))
    re1, re2 = fresh("reassign.jsonl"), fresh("reassign-openai-astra.jsonl")
    cc = collections.Counter()
    for c in jl("coder_conflicts.jsonl"):
        for t in {t for p in c.get("pairs_it_may_explain") or [] for t in p.split("|")}:
            cc[t] += 1
    r4 = collections.Counter()
    sec = open(os.path.join(OUT, "transmission-B4.md"), encoding="utf-8").read().split("## Row 4")[1].split("## Row 1")[0]
    for ln in sec.splitlines():
        if ln.startswith("| G"):
            cells = [x.strip() for x in ln.split("|")]
            for t in set(re.findall(r"T3-\d{3}", " ".join(cells[3:6]))):
                r4[t] += 1
    rows = []
    for t in sorted(S):
        n = sum(1 for c in (dis, re1, cc, r4) if c.get(t))
        rows.append({"theme": t, "name": S[t]["name"], "family": S[t]["family"], "sources": n,
                     "disagreements": dis.get(t, 0), "reassign_arm1": re1.get(t, 0), "reassign_arm2": re2.get(t, 0),
                     "conflicts": cc.get(t, 0), "row4": r4.get(t, 0)})
    by = collections.Counter(r["sources"] for r in rows)
    print("themes by number of sources: %s" % dict(sorted(by.items())))
    print("in three or four sources (theme, name, family: disagreements, reassign arm 1 [arm 2], conflicts, row 4):")
    for r in sorted(rows, key=lambda r: (-r["sources"], -(r["disagreements"] + r["reassign_arm1"]), r["theme"])):
        if r["sources"] >= 3:
            print("  %s %s (%s), %d sources: %d, %d [%d], %d, %d" % (r["theme"], r["name"], r["family"], r["sources"],
                  r["disagreements"], r["reassign_arm1"], r["reassign_arm2"], r["conflicts"], r["row4"]))
    if "--write" in sys.argv:
        json.dump({"declared": "notes-C1.md, Pass 2 (C1a-02)", "rows": rows}, open(os.path.join(OUT, "_analysis", "c1_weak_sources.json"), "w"), indent=1)
        print("wrote out/_analysis/c1_weak_sources.json")


if __name__ == "__main__":
    main()
