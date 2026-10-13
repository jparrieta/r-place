#!/usr/bin/env python3
"""B4c, read-only: two figures beside the declared ones, from reassign.jsonl and reassign-openai-astra.jsonl, per arm.
(1) The uniform stratum without its class 2 items (the settled line there is my B1 grouping, notes-B4.md "Class 2 on a
row of its own"). (2) The uniform stratum with class 2 scored against the themes the settled line places with concepts
(jaccard_placed). Both are mean Jaccard over readings whose settled line is resolved, exact rate beside. Prints only.

    python3 out/_analysis/b4c_extra.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    for name in ("reassign.jsonl", "reassign-openai-astra.jsonl"):
        L = [r for r in jl(os.path.join(OUT, name)) if r["stratum"] == "uniform" and r["outcome"] != "disagrees-unresolved"]
        no2 = [r for r in L if r["class"] != 2]
        j1 = sum(r["jaccard"] for r in no2) / len(no2)
        e1 = sum(r["outcome"] == "agrees" for r in no2) / len(no2)
        pl = [r["jaccard_placed"] if r["class"] == 2 else r["jaccard"] for r in L]
        ex = [(r["jaccard_placed"] == 1) if r["class"] == 2 else (r["outcome"] == "agrees") for r in L]
        print("%s: U without class 2: readings %d, Jaccard %.3f, exact %.3f | U with class 2 against placed themes: readings %d, Jaccard %.3f, exact %.3f"
              % (name, len(no2), j1, e1, len(L), sum(pl) / len(pl), sum(ex) / len(ex)))


if __name__ == "__main__":
    main()
