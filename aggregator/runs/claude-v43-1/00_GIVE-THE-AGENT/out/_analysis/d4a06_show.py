#!/usr/bin/env python3
"""D4a-06: views of d4a06_forms.json. --what count|forms|sets|moves --k K

    python3 out/_analysis/d4a06_show.py --what count
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T = json.load(open(os.path.join(ROOT, "out", "_analysis", "d4a06_forms.json"), encoding="utf-8"))
ap = argparse.ArgumentParser()
ap.add_argument("--what", required=True)
ap.add_argument("--k")
a = ap.parse_args()
k = a.k or str(T["k_stab"])
if a.what == "count":
    for key in ("floor", "n_defining", "n_thin", "n_core", "cols", "k_gap", "k_stab", "agree"):
        print(key, T[key])
    for kk in sorted(T["gap"], key=int):
        print("k", kk, "gap", T["gap"][kk], "stability", T["stability"][kk])
if a.what == "forms":
    C = T["cuts"][k]
    print("k", k, "ward sizes", C["ward_sizes"], "placed sizes", C["sizes"], "ratio", C["ratio"], "moved", C["moved"],
          "(defining", C["moved_defining"], "thin", C["moved_thin"], ") ties", C["ties"], "no signature", C["no_signature"],
          "ARI vs D4a05", C["ari_vs_D4a05"])
    print("codes", C["codes_check"])
    for f, v in sorted(C["forms"].items()):
        R = [r for r in C["rooms"].values() if r["form"] == f]
        print("==", f, "ward", v["ward_n"], "placed", len(R), "thin placed", sum(1 for r in R if not r["defining"]),
              "share_own median", sorted(r["share_own"] for r in R)[len(R) // 2], "ties", sum(1 for r in R if r["tied"]),
              "with secondary", sum(1 for r in R if r["secondary"]), "near-equal centre", sum(1 for r in R if r["near_equal_centre"]))
        print("  T4:", [(d["node"], d["name"], d["share"], d["ratio"], d["presence"]) for d in v["sig_T4"]])
        print("  T3:", [(d["node"], d["name"], d["share"], d["ratio"], d["presence"]) for d in v["sig_T3"]])
        print("  dims:", [(d["node"], d["name"], d["share"], d["pop_share"]) for d in v["dims"]])
if a.what == "moves":
    C = T["cuts"][k]
    m = collections.Counter((r["mix_form"], r["form"]) for r in C["rooms"].values() if r["moved"])
    print("moves mix->signature:", sorted(m.items(), key=lambda x: -x[1]))
    print("how:", collections.Counter(r["how"] for r in C["rooms"].values()))
if a.what == "sets":
    C = T["cuts"][k]
    print("raiding", len(T["raiding"]), C["raiding_by_form"])
    print("takeover", len(T["takeover"]), C["takeover_by_form"])
    print("core (codes; population median %s):" % T["pop_codes_median"], [(x["sub"], x["codes"]) for x in T["core"]])
