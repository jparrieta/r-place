#!/usr/bin/env python3
"""D4a-07: views of d4a07_forms.json. --what count|forms|raid|sens  [--k K]

    python3 out/_analysis/d4a07_show.py --what count
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T = json.load(open(os.path.join(ROOT, "out", "_analysis", "d4a07_forms.json"), encoding="utf-8"))
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
    print("k", k, "ward", C["ward_sizes"], "placed (whole mix)", C["sizes"], "ratio", C["ratio"])
    print("literal rule", C["literal_sizes"], "ratio", C["literal_ratio"], "moved", C["moved_by_literal"], "ties", C["literal_ties"],
          "ARI vs D4a06", C["ari_vs_D4a06"])
    print("codes", C["codes_check"])
    print("takeover", C["takeover_by_form"])
    for f, v in sorted(C["forms"].items()):
        R = [r for r in C["rooms"].values() if r["form"] == f]
        print("==", f, "ward", v["ward_n"], "placed", len(R), "mixture" if v["mixture"] else "", "NO SIGNATURE" if v["no_signature"] else "",
              "share_own median", sorted(r["share_own"] for r in R)[len(R) // 2], "secondary", sum(1 for r in R if r["secondary"]),
              "near-equal", sum(1 for r in R if r["near_equal_centre"]), "ops", C["op_mix"][f])
        print("  T4:", [(d["name"], d["share"], d["ratio"], d["presence"]) for d in v["sig_T4"][:6]])
        print("  T3:", [(d["name"], d["share"], d["ratio"], d["presence"]) for d in v["sig_T3"][:4]])
        print("  dims:", [(d["name"], d["share"], d["pop_share"]) for d in v["dims"][:3]], "dim links:", [(d["name"], d["ratio"], d["presence"]) for d in v["dim_links"]])
    for f, h in C["mixture_splits"].items():
        print("split of", f, [(x["n"], [(y["name"], y["ratio"], y["presence"]) for y in x["leading"]]) for x in h])
if a.what == "raid":
    print({k2: v for k2, v in T["raiding_core"].items() if k2 != "core"})
    print("core rooms", T["raiding_core"]["core"])
if a.what == "sens":
    print(T["sensitivity"])
