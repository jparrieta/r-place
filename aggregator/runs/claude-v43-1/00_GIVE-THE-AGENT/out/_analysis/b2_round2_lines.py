#!/usr/bin/env python3
"""B2b-r2-p2: write round 2's line to out/pilot_rounds.jsonl and append round 2's dividing items to
out/exemplar_candidates.jsonl (stage B2 section 4). Figures from out/_analysis/b2_r2_score.json; readers'
sets from the returns (a mistyped heading mapped by position, as b2_score_r2.py does). Refuses a second
round-2 line in either file. Dry run unless --write."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RAW = os.path.join(OUT, "_fleet_raw", "B2", "round-2")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    s = json.load(open(os.path.join(OUT, "_analysis", "b2_r2_score.json"), encoding="utf-8"))
    auth = {r["item"]: r for r in jl(os.path.join(OUT, "author_items.jsonl"))}
    order = json.load(open(os.path.join(OUT, "_analysis", "b2_order_r2b.json"), encoding="utf-8"))["packets"]
    pr = jl(os.path.join(OUT, "pilot_rounds.jsonl"))
    ex = jl(os.path.join(OUT, "exemplar_candidates.jsonl"))
    if any(r.get("round") == 2 for r in pr) or any(r.get("round") == 2 for r in ex):
        sys.exit("round 2 is already written")
    line = {"round": 2, "n_items": len(auth), "agents": 3, "exemplars": False,
            "fidelity_vs_author": round(s["fidelity"], 3), "agreement_pairwise": round(s["pairwise"], 3),
            "alpha": round(s["alpha"], 3), "items_with_disagreement": s["items_with_disagreement"], "seed": 20261012,
            "readers": ["%s/%s" % (pk, r) for pk in sorted(order) for r in ("r1", "r2", "r3")],
            "served": "deepseek/deepseek-v4.1-flash",
            "reader_settings": "called directly (not @preset/cheap), medium reasoning effort, max_tokens 128000 (J, 2026-10-12)",
            "packets": "five self-contained packets, three fresh readers each",
            "primary_match_vs_author": round(s["primary"], 3), "primary_pairwise": round(s["primary_pairwise"], 3),
            "fidelity_vs_rechecked": round(s["fidelity_rechecked"], 3),
            "round_1_items": {k: round(v, 3) for k, v in s["r1items"].items()},
            "ten_biggest_bags": {k: round(v, 3) for k, v in s["bags10"].items()},
            "leg": "B2b-r2-p2"}
    sets = {}
    for pk, its in order.items():
        for slot in ("r1", "r2", "r3"):
            for x in jl(os.path.join(RAW, pk, slot + ".jsonl")):
                it = "%s/%s" % (x["sub"], x["theme_id"])
                if it not in its:
                    it = its[x["position"] - 1]
                sets.setdefault(it, {})["%s/%s" % (pk, slot)] = x["third_order"]
    new = []
    for it in s["items_with_disagreement"]:
        a = auth[it]
        rs = sets[it]
        play = sorted(set(a["third_order"]) | {t for v in rs.values() for t in v})
        new.append({"key": it, "sub": a["sub"], "theme_id": a["theme_id"], "round": 2, "author": a["third_order"],
                    "author_confidence": a["confidence"], "readers": rs, "themes_in_play": play,
                    "source": a.get("source", "")})
    print(json.dumps(line)[:600])
    print("exemplar candidates to append: %d" % len(new))
    if "--write" not in sys.argv:
        return
    with open(os.path.join(OUT, "pilot_rounds.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    with open(os.path.join(OUT, "exemplar_candidates.jsonl"), "a", encoding="utf-8") as f:
        for r in new:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("pilot_rounds.jsonl %d lines; exemplar_candidates.jsonl %d lines" % (len(pr) + 1, len(ex) + len(new)))


if __name__ == "__main__":
    main()
