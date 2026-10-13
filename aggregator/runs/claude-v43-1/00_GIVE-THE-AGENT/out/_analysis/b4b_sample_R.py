#!/usr/bin/env python3
"""B4b-p2: draw stratum R as declared in notes-B4.md ("Stratum R, the other 18 unresolved items") before the draw.

J (16:43 Berlin): "draw other 18". The PI's reading: 18 more of the unresolved items that sample-B4.jsonl does not
hold, by a recorded seed, a third stratum reported apart and never pooled with U or A; diagnostic only.

  frame   the unresolved rulings of disagreements.jsonl not in sample-B4.jsonl, sorted by (room, theme id)
  draw    18 without replacement with random.Random("20261013:R").sample
  order   random.Random("20261013:R-order").shuffle of the 18; orders 501..518, after sample-B4.jsonl's 500

Writes the sibling record out/sample-B4-R.jsonl (sample-B4.jsonl's fields, stratum "R") and
out/_analysis/b4b_sample_R.json. sample-B4.jsonl is read and left as it stands. Refuses to overwrite (no redraw).

    python3 out/_analysis/b4b_sample_R.py [--write]
"""
import argparse, collections, hashlib, json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
SEED = 20261013
N_R = 18


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def sha(p):
    return hashlib.sha256(open(os.path.join(OUT, p), "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    s0 = jl("sample-B4.jsonl")
    have = {(r["sub"], r["theme_id"]) for r in s0}
    if len(s0) != 500 or len(have) != 500 or max(r["order"] for r in s0) != 500:
        sys.exit("sample-B4.jsonl is not the 500 items of B4b")
    dg = jl("disagreements.jsonl")
    unres = {(x["sub"], x["theme_id"]): x for x in dg if x.get("unresolved")}
    if len(unres) != 185:
        sys.exit("expected 185 unresolved rulings, found %d" % len(unres))
    already = sorted(k for k in unres if k in have)
    frame = sorted(k for k in unres if k not in have)
    if len(already) != 18 or len(frame) != 167:
        sys.exit("expected 18 unresolved items already drawn and a frame of 167; found %d and %d" % (len(already), len(frame)))
    cls = {(x["sub"], x["theme_id"]): x.get("class") for x in jl("assign_final.jsonl")}
    gold = {(x["sub"], x["theme_id"]) for x in jl("gold_items.jsonl")}
    pilot = {(x["sub"], x["theme_id"]) for x in jl("author_items.jsonl")}
    r = random.Random("%d:R" % SEED).sample(frame, N_R)
    random.Random("%d:R-order" % SEED).shuffle(r)
    rows = [{"sub": k[0], "theme_id": k[1], "item": "%s/%s" % k, "stratum": "R", "order": 500 + i, "class": cls[k],
             "ruled": True, "unresolved": True, "gold": k in gold, "pilot": k in pilot}
            for i, k in enumerate(r, 1)]
    by_st = collections.Counter(r0["stratum"] for r0 in s0 if (r0["sub"], r0["theme_id"]) in unres)
    print("unresolved rulings 185: already drawn %d (%s); frame %d" % (len(already), dict(by_st), len(frame)))
    print("stratum R: %d items over %d rooms; by class %s; by taxonomy %s; gold %d; pilot %d" % (
        len(rows), len({x["sub"] for x in rows}), dict(sorted(collections.Counter(x["class"] for x in rows).items())),
        dict(collections.Counter(unres[(x["sub"], x["theme_id"])].get("taxonomy") for x in rows)),
        sum(x["gold"] for x in rows), sum(x["pilot"] for x in rows)))
    print("serving order: %s" % ", ".join(x["item"] for x in rows))
    if not a.write:
        return
    p = os.path.join(OUT, "sample-B4-R.jsonl")
    if os.path.exists(p):
        sys.exit("out/sample-B4-R.jsonl exists; no redraw")
    with open(p, "w", encoding="utf-8") as f:
        for x in rows:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    meta = {"seed": SEED, "streams": {"R": "%d:R" % SEED, "order": "%d:R-order" % SEED}, "n": N_R,
            "frame": "the 185 unresolved rulings of disagreements.jsonl not in sample-B4.jsonl, sorted by (room, theme id)",
            "frame_size": len(frame), "already_drawn": ["%s/%s" % k for k in already],
            "sample_B4_sha256": sha("sample-B4.jsonl"), "disagreements_sha256": sha("disagreements.jsonl"),
            "assign_final_sha256": sha("assign_final.jsonl"), "sample_R_sha256": sha("sample-B4-R.jsonl"),
            "script": "out/_analysis/b4b_sample_R.py"}
    json.dump(meta, open(os.path.join(OUT, "_analysis", "b4b_sample_R.json"), "w", encoding="utf-8"), indent=1)
    print("wrote out/sample-B4-R.jsonl (%d lines) and out/_analysis/b4b_sample_R.json" % len(rows))


if __name__ == "__main__":
    main()
