#!/usr/bin/env python3
"""B4b: draw the blind sample as declared in notes-B4.md ("The blind sample, built at B4b") before the draw.

J's rulings (the PI's message, 14:22Z): 500 items, 250 uniform from the analysed set and 250 from the adjudicated
items, by a recorded seed, the two strata reported apart and never pooled.

  stratum U  250 drawn without replacement from the analysed set (assign_final.jsonl's 7,844 second-order themes),
             sorted by (room, theme id), with random.Random("20261013:U").sample
  stratum A  250 drawn without replacement from the ruled items of disagreements.jsonl that U did not take, same
             order, with random.Random("20261013:A").sample
  order      the 500 shuffled together with random.Random("20261013:order"), the strata mixed

Writes out/sample-B4.jsonl (one line per item in serving order: sub, theme_id, stratum, order, and for the check leg
the item's class, whether it was ruled, whether the ruling is unresolved, whether it is a gold or pilot item) and
out/_analysis/b4b_sample.json (the seed, the frames' sizes and sha256, the counts). The sample file names the
strata and never reaches the packets folder. No redraw: the script refuses to overwrite an existing sample.

    python3 out/_analysis/b4b_sample.py [--write]
"""
import argparse, collections, hashlib, json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
SEED = 20261013
N_U, N_A = 250, 250
BIG = ("leagueoflegends", "t02")          # the one item over the 50 KB ceiling alone (b4b_item_sizes.py)


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def sha(p):
    return hashlib.sha256(open(os.path.join(OUT, p), "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    af = jl("assign_final.jsonl")
    dg = jl("disagreements.jsonl")
    frame_u = sorted({(x["sub"], x["theme_id"]) for x in af})
    if len(frame_u) != len(af) or len(frame_u) != 7844:
        sys.exit("the analysed set is not 7,844 distinct items: %d lines, %d distinct" % (len(af), len(frame_u)))
    ruled = {(x["sub"], x["theme_id"]): x for x in dg}
    if len(ruled) != len(dg) or len(ruled) != 3288:
        sys.exit("the ruled items are not 3,288 distinct items: %d lines, %d distinct" % (len(dg), len(ruled)))
    if set(ruled) - set(frame_u):
        sys.exit("ruled items outside the analysed set: %s" % sorted(set(ruled) - set(frame_u))[:5])
    cls = {(x["sub"], x["theme_id"]): x.get("class") for x in af}
    gold = {(x["sub"], x["theme_id"]) for x in jl("gold_items.jsonl")}
    pilot = {(x["sub"], x["theme_id"]) for x in jl("author_items.jsonl")}

    u = random.Random("%d:U" % SEED).sample(frame_u, N_U)
    took = set(u)
    frame_a = sorted(k for k in ruled if k not in took)
    aa = random.Random("%d:A" % SEED).sample(frame_a, N_A)
    both = [(k, "U") for k in u] + [(k, "A") for k in aa]
    random.Random("%d:order" % SEED).shuffle(both)
    rows = []
    for i, (k, st) in enumerate(both, 1):
        r = ruled.get(k)
        rows.append({"sub": k[0], "theme_id": k[1], "item": "%s/%s" % k, "stratum": st, "order": i, "class": cls[k],
                     "ruled": r is not None, "unresolved": bool(r and r.get("unresolved")),
                     "gold": k in gold, "pilot": k in pilot})
    if len({(r["sub"], r["theme_id"]) for r in rows}) != N_U + N_A:
        sys.exit("the strata overlap")
    c = collections.Counter
    for st in ("U", "A"):
        rs = [r for r in rows if r["stratum"] == st]
        print("stratum %s: %d items; ruled %d; unresolved %d; by class %s; gold %d; pilot %d; rooms %d" % (
            st, len(rs), sum(r["ruled"] for r in rs), sum(r["unresolved"] for r in rs),
            dict(sorted(c(r["class"] for r in rs).items())), sum(r["gold"] for r in rs), sum(r["pilot"] for r in rs),
            len({r["sub"] for r in rs})))
    print("frames: analysed set %d; ruled items %d; ruled items U did not take %d" % (len(frame_u), len(ruled), len(frame_a)))
    print("leagueoflegends/t02 drawn: %s" % next((r["stratum"] for r in rows if (r["sub"], r["theme_id"]) == BIG), "no"))
    print("first five in serving order: %s" % ", ".join(r["item"] for r in rows[:5]))
    if not a.write:
        return
    p = os.path.join(OUT, "sample-B4.jsonl")
    if os.path.exists(p):
        sys.exit("out/sample-B4.jsonl exists; no redraw")
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    meta = {"seed": SEED, "streams": {"U": "%d:U" % SEED, "A": "%d:A" % SEED, "order": "%d:order" % SEED},
            "n": {"U": N_U, "A": N_A}, "frames": {"analysed": len(frame_u), "ruled": len(ruled), "ruled_not_in_U": len(frame_a)},
            "frame_order": "sorted by (room, theme id)",
            "assign_final_sha256": sha("assign_final.jsonl"), "disagreements_sha256": sha("disagreements.jsonl"),
            "sample_sha256": sha("sample-B4.jsonl"), "script": "out/_analysis/b4b_sample.py"}
    json.dump(meta, open(os.path.join(OUT, "_analysis", "b4b_sample.json"), "w", encoding="utf-8"), indent=1)
    print("wrote out/sample-B4.jsonl (%d lines) and out/_analysis/b4b_sample.json" % len(rows))


if __name__ == "__main__":
    main()
