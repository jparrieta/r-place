#!/usr/bin/env python3
"""C1, the revision rate (section 3). --draw: the sample, 200 keys of assign_final.jsonl, sorted, drawn by
random.Random(20261013).sample; written once to out/_analysis/c1_revision/sample.json. --pack A B: a read packet for
sample items A..B (1-based, inclusive), written to out/_analysis/c1_revision/pack-A-B.md: each item's label and note
and every concept whole (id | label | words), then the candidate themes, unattributed and sorted by id (every theme
the settled line, the current line, either reader, my B1 or also_present named), each with its name and must_show
from scheme_v2. Which theme anyone chose, and in what order, is not shown. Refuses to overwrite.

    python3 out/_analysis/c1_revision_pack.py --draw
    python3 out/_analysis/c1_revision_pack.py --pack 1 25
"""
import argparse, importlib.util, json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DIR = os.path.join(OUT, "_analysis", "c1_revision")
SEED, N = 20261013, 200


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--draw", action="store_true"); ap.add_argument("--pack", nargs=2, type=int)
    a = ap.parse_args()
    os.makedirs(DIR, exist_ok=True)
    sp = os.path.join(DIR, "sample.json")
    if a.draw:
        if os.path.exists(sp):
            sys.exit("sample.json exists")
        keys = sorted("%s:%s" % (r["sub"], r["theme_id"]) for r in jl("assign_final.jsonl"))
        sample = random.Random(SEED).sample(keys, N)
        json.dump({"seed": SEED, "n": N, "drawn_from": "assign_final.jsonl keys, sorted", "items": sample},
                  open(sp, "w", encoding="utf-8"), indent=1)
        print("drew %d of %d keys with seed %d" % (N, len(keys), SEED))
        return
    sample = json.load(open(sp, encoding="utf-8"))["items"]
    lo, hi = a.pack
    spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
    bpf = importlib.util.module_from_spec(spec); spec.loader.exec_module(bpf)
    store = bpf.pk.Store(ROOT, OUT)
    st = {"%s:%s" % (r["sub"], r["theme_id"]): r for r in jl("assign_final.jsonl")}
    fin = {"%s:%s" % (r["sub"], r["theme_id"]): r for r in jl("assignments_final.jsonl")}
    b3 = {"%s:%s" % (r["sub"], r["theme_id"]): r for r in jl("b3_classes.jsonl")}
    sch = {r["id"]: r for r in jl("scheme_v2.jsonl")}
    L = ["# Revision-rate packet, items %d to %d of %d (seed %d)" % (lo, hi, len(sample), SEED), ""]
    for i in range(lo, hi + 1):
        it = sample[i - 1]
        s, t = it.split(":")
        th = store.themes[(s, t)]
        cand = set(st[it].get("third_order") or []) | set(fin[it].get("third_order") or [])
        c = b3.get(it) or {}
        for k in ("r1", "r2", "b1"):
            cand |= set(c.get(k) or [])
        cand |= set((st[it].get("also_present") or {}).keys()) | set((fin[it].get("also_present") or {}).keys())
        cand |= set(fin[it].get("b1_themes_without_reader_support") or [])
        L += ["## %d. %s/%s" % (i, s, t), "", "**%s** | note: %s" % (th.get("second_order"), th.get("theme_note")), ""]
        for cid in th.get("code_ids") or []:
            cd = store.codes.get((s, cid))
            if cd:
                L.append("- %s | %s | %s" % (cid, cd.get("first_order"), " ".join(str(cd.get("text") or "").split())))
        L += ["", "candidates (unattributed): " + "; ".join(
            "%s %s [%s]%s" % (x, sch[x]["name"], sch[x].get("must_show"), " (rare)" if sch[x].get("tier") == "rare" else "")
            for x in sorted(cand) if x in sch), ""]
    p = os.path.join(DIR, "pack-%03d-%03d.md" % (lo, hi))
    if os.path.exists(p):
        sys.exit("%s exists" % p)
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote %s: %d bytes, %d lines" % (os.path.relpath(p, ROOT), os.path.getsize(p), len(L)))


if __name__ == "__main__":
    main()
