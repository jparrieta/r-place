#!/usr/bin/env python3
"""B4c, read-only: print out/_analysis/b4c_figures.json's per-family tables, per stratum, with both arms side by side
(fresh against settled by the settled line's first theme; the readers' agreement with each other by B3's rule;
B3's corpus agreement per family beside), as markdown rows. Prints only.

    python3 out/_analysis/b4c_family_print.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AN = os.path.join(ROOT, "out", "_analysis")
A1, A2 = "deepseek-v4.1-flash", "openai-gpt-6-astra"


def f(v):
    return "-" if v is None else "%.3f" % v


def main():
    d = json.load(open(os.path.join(AN, "b4c_figures.json"), encoding="utf-8"))
    fam = {r["family"]: r for r in (json.loads(x) for x in open(os.path.join(ROOT, "out", "families.jsonl"), encoding="utf-8") if x.strip())}
    for s in ("U", "A"):
        t1 = d["arms"][A1]["families"][s]["table"]
        t2 = d["arms"][A2]["families"][s]["table"]
        print("\nstratum %s" % s)
        print("| family | items | arm 1 fresh-settled | arm 2 fresh-settled | arm 1 readers | arm 2 readers | B3 corpus |")
        print("|---|---|---|---|---|---|---|")
        for g in sorted(set(t1) | set(t2)):
            a, b = t1.get(g, {}), t2.get(g, {})
            n = a.get("items_settled") or b.get("items_settled") or 0
            name = (fam.get(g) or {}).get("name", "")
            print("| %s %s | %d | %s | %s | %s | %s | %s |" % (g, name, n, f(a.get("fresh_vs_settled")), f(b.get("fresh_vs_settled")),
                                                           f(a.get("readers_jaccard")), f(b.get("readers_jaccard")),
                                                           f(a.get("b3_corpus_jaccard") or b.get("b3_corpus_jaccard"))))
        print("worst arm 1: %s; arm 2: %s" % (d["arms"][A1]["families"][s]["worst"], d["arms"][A2]["families"][s]["worst"]))


if __name__ == "__main__":
    main()
