#!/usr/bin/env python3
"""B2d: score the blind re-placement (out/_analysis/b2_blind_replace.jsonl) against my own placements of the same
ten items (author_items.jsonl and the rechecked placements), beside the round-3 readers' fidelity on those ten
items and their agreement with each other: if I disagree with myself more than the readers disagree with me, the
fleet is not the problem (stage B2 section 3). Reads only; prints and writes b2_blind_score.json."""
import importlib.util, itertools, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
spec = importlib.util.spec_from_file_location("b2s", os.path.join(AN, "b2_score.py"))
b2s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b2s)
jac, jl = b2s.jac, b2s.jl


def mean(x):
    return sum(x) / len(x) if x else float("nan")


auth = {r["item"]: r["third_order"] for r in jl(os.path.join(OUT, "author_items.jsonl"))}
rech = {r["item"]: r["third_order"] for r in jl(os.path.join(AN, "b2_rechecked_author.jsonl"))}
blind = {r["item"]: r["third_order"] for r in jl(os.path.join(AN, "b2_blind_replace.jsonl"))}
r3 = {}
for pk in sorted(os.listdir(os.path.join(AN, "b2_r3_returns"))):
    for f in sorted(os.listdir(os.path.join(AN, "b2_r3_returns", pk))):
        for x in jl(os.path.join(AN, "b2_r3_returns", pk, f)):
            r3.setdefault("%s/%s" % (x["sub"], x["theme_id"]), []).append(x["third_order"])
rows, sa, sr, sp, rf, rp = [], [], [], [], [], []
for it, b in blind.items():
    a, r, rs = auth[it], rech[it], r3[it]
    sa.append(jac(b, a)); sr.append(jac(b, r)); sp.append(b[0] == a[0])
    rf.append(mean([jac(s, a) for s in rs])); rp.append(mean([jac(x, y) for x, y in itertools.combinations(rs, 2)]))
    rows.append((it, ",".join(b), ",".join(a), ",".join(r), " | ".join(",".join(s) for s in rs), sa[-1], rf[-1]))
for x in rows:
    print("%-22s blind %-15s mine %-22s rechecked %-15s r3 readers %s | self %.2f readers %.2f" % x)
res = {"self_vs_author": mean(sa), "self_vs_rechecked": mean(sr), "self_primary": mean(sp),
       "readers_fidelity_same_items": mean(rf), "readers_pairwise_same_items": mean(rp)}
print("self against author_items %.3f, against rechecked %.3f, primary match %.2f; round-3 readers on the same ten: "
      "fidelity %.3f, pairwise %.3f" % (res["self_vs_author"], res["self_vs_rechecked"], res["self_primary"],
                                         res["readers_fidelity_same_items"], res["readers_pairwise_same_items"]))
json.dump(res, open(os.path.join(AN, "b2_blind_score.json"), "w"), indent=1)
