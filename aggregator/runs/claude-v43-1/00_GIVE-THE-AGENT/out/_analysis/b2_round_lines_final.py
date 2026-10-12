#!/usr/bin/env python3
"""B2d: write the gold round's line (flagged "gold": true) and the two stability rounds' lines to
out/pilot_rounds.jsonl, from out/_analysis/b2_final_score.json. Refuses a second line for any of the three.
Gold items are not exported to exemplar_candidates.jsonl: stage B3 seeds the gold set unannounced, and an exemplar
drawn from it would show a reader a gold item. Dry run unless --write."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def main():
    s = json.load(open(os.path.join(OUT, "_analysis", "b2_final_score.json"), encoding="utf-8"))
    p = os.path.join(OUT, "pilot_rounds.jsonl")
    have = [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]
    if any(str(r.get("round")) in ("gold", "stab-1", "stab-2") for r in have):
        sys.exit("pilot_rounds.jsonl already holds a gold or stability line")
    kept = {}
    for rnd in ("gold", "stab-1", "stab-2"):
        man = json.load(open(os.path.join(OUT, "_packets-B2", "round-%s" % rnd, "MANIFEST.json"), encoding="utf-8"))
        kept[rnd] = sorted(man)
    lines = []
    for rnd in ("gold", "stab-1", "stab-2"):
        f = s["rounds"][rnd]
        line = {"round": rnd, "n_items": 40, "agents": 3, "exemplars": False,
                "fidelity_vs_author": round(f["fidelity"], 3), "agreement_pairwise": round(f["pairwise"], 3),
                "alpha": round(f["alpha"], 3), "items_with_disagreement": f["items_with_disagreement"], "seed": 20261014,
                "readers": ["%s/r%d" % (pk, k) for pk in kept[rnd] for k in (1, 2, 3)],
                "served": "deepseek/deepseek-v4.1-flash", "reader_settings": "called directly, medium reasoning effort, max_tokens 128000",
                "scheme": "scheme_final.jsonl (frozen)", "items": "gold_items.jsonl",
                "primary_match_vs_author": round(f["primary"], 3), "primary_pairwise": round(f["primary_pairwise"], 3),
                "fidelity_vs_rechecked": round(f["fidelity_rechecked"], 3), "multi_lines": f["multi"],
                "also_present_lines": f["also_present_lines"], "leg": "B2d"}
        if rnd == "gold":
            line["gold"] = True
        else:
            line["brief"] = "out/brief-%s.md" % rnd
            line["stability"] = {"cross_round_jaccard_stab1_stab2": round(s["stability"]["stab-1|stab-2"]["jaccard"], 3),
                                 "cross_round_primary": round(s["stability"]["stab-1|stab-2"]["primary"], 3),
                                 "alpha_six_readers": round(s["stability"]["alpha_six"], 3)}
        lines.append(line)
    for l in lines:
        print(l["round"], l["fidelity_vs_author"], l["agreement_pairwise"], l["alpha"], len(l["items_with_disagreement"]))
    if "--write" not in sys.argv:
        return
    with open(p, "a", encoding="utf-8") as fh:
        for l in lines:
            fh.write(json.dumps(l, ensure_ascii=False) + "\n")
    print("pilot_rounds.jsonl now %d lines" % (len(have) + len(lines)))


if __name__ == "__main__":
    main()
