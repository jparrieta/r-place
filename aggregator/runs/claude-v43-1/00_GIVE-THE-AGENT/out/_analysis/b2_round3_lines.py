#!/usr/bin/env python3
"""B2b-r3: write round 3's line to out/pilot_rounds.jsonl and append round 3's dividing items to
out/exemplar_candidates.jsonl (stage B2 section 4). Figures from out/_analysis/b2_r3_score.json; readers' sets
from the translated copies of the kept replies (out/_analysis/b2_r3_returns/, RESCUE-2026-10-12.json). Refuses a
second round-3 line in either file. Dry run unless --write."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
TR = os.path.join(OUT, "_analysis", "b2_r3_returns")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    s = json.load(open(os.path.join(OUT, "_analysis", "b2_r3_score.json"), encoding="utf-8"))
    auth = {r["item"]: r for r in jl(os.path.join(OUT, "author_items.jsonl"))}
    kept = json.load(open(os.path.join(OUT, "_fleet_raw", "B2", "round-3", "RESCUE-2026-10-12.json"), encoding="utf-8"))["packets"]
    pr = jl(os.path.join(OUT, "pilot_rounds.jsonl"))
    ex = jl(os.path.join(OUT, "exemplar_candidates.jsonl"))
    if any(r.get("round") == 3 for r in pr) or any(r.get("round") == 3 for r in ex):
        sys.exit("round 3 is already written")
    readers = ["%s/%s" % (pk, r) for pk in sorted(kept) for r in kept[pk]["kept"]]
    line = {"round": 3, "n_items": len(auth), "agents": 3, "exemplars": False,
            "fidelity_vs_author": round(s["fidelity"], 3), "agreement_pairwise": round(s["pairwise"], 3),
            "alpha": round(s["alpha"], 3), "items_with_disagreement": s["items_with_disagreement"], "seed": 20261013,
            "readers": readers, "served": "deepseek/deepseek-v4.1-flash",
            "reader_settings": "called directly, medium reasoning effort, max_tokens 128000: round 2's readers (QB2-007)",
            "packets": "five self-contained packets in fleet ids; the first three valid replies per packet in reader order, as kept by the handler's RESCUE-2026-10-12.json",
            "primary_match_vs_author": round(s["primary"], 3), "primary_pairwise": round(s["primary_pairwise"], 3),
            "fidelity_vs_rechecked": round(s["fidelity_rechecked"], 3),
            "round_1_items": {k: round(v, 3) for k, v in s["r1items"].items()},
            "ten_biggest_bags": {k: round(v, 3) for k, v in s["bags10"].items()},
            "multi_lines": s["multi_lines"], "also_present_lines": s["also_present_lines"],
            "also_present_themes": s["also_present_themes"], "also_present_under_floor": s["also_present_under_floor"],
            "leg": "B2b-r3"}
    sets = {}
    for pk in sorted(kept):
        for slot in kept[pk]["kept"]:
            for x in jl(os.path.join(TR, pk, slot + ".jsonl")):
                sets.setdefault("%s/%s" % (x["sub"], x["theme_id"]), {})["%s/%s" % (pk, slot)] = x["third_order"]
    new = []
    for it in s["items_with_disagreement"]:
        a = auth[it]
        rs = sets[it]
        play = sorted(set(a["third_order"]) | {t for v in rs.values() for t in v})
        new.append({"key": it, "sub": a["sub"], "theme_id": a["theme_id"], "round": 3, "author": a["third_order"],
                    "author_confidence": a["confidence"], "readers": rs, "themes_in_play": play,
                    "source": a.get("source", "")})
    print(json.dumps(line)[:700])
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
