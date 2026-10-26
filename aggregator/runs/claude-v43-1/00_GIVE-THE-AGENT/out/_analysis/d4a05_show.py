#!/usr/bin/env python3
"""D4a-05: print views of d4a05_tree.json. --what top|forms|nodes|codes|branches|rooms FORM

    python3 out/_analysis/d4a05_show.py --what top
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser()
ap.add_argument("--what", required=True)
ap.add_argument("--form")
ap.add_argument("--file", default="d4a05_tree2.json")
a = ap.parse_args()
T = json.load(open(os.path.join(ROOT, "out", "_analysis", a.file), encoding="utf-8"))
if a.what == "top":
    for k in ("n_lines", "n_placed", "unplaced_ids", "n_changed", "cols", "rooms_without_T3_after_drop",
              "lines_without_node", "rooms_with_empty_level", "k_best_silhouette", "k_chosen", "pop_dim_entropy", "sensitivity"):
        print(k, T[k])
    print("core", len(T["core"]), T["core"])
    for k, v in T["top"].items():
        print("k", k, v)
if a.what == "forms":
    for f, v in T["forms"].items():
        R = [T["rooms"][s] for s in v["members"]]
        print("==", f, "n", v["n"], "median changes", v["median_changes"], "dim entropy", v["mean_dim_entropy"],
              "fits_two", sum(r["fits_two"] for r in R), "nearer_other", sum(r["nearer_other"] for r in R),
              "with secondary", sum(1 for r in R if r["secondary"]), "sig_share_own median",
              sorted(r["sig_share_own"] for r in R)[len(R) // 2])
        print("  dims:", [(d["node"], d["name"], d["share"], d["pop_share"]) for d in v["dims"][:4]])
        print("  T4 sig:", [(d["node"], d["name"], d["share"], d["pop_share"], d["ratio"], d["presence"]) for d in v["sig_T4"]])
        print("  T3 sig:", [(d["node"], d["name"], d["share"], d["ratio"], d["presence"]) for d in v["sig_T3"]])
if a.what == "nodes":
    for n in T["nodes"]:
        if a.form and not n["id"].startswith(a.form):
            continue
        print(n["id"], "n", n["n"], "kept" if n["kept_split"] else "leaf", n.get("split_sizes"), "r2", n.get("r2"),
              "p95", n.get("null_r2_p95"), n.get("why_stop", ""))
        if n.get("sig_T4") is not None:
            print("    T4:", [(d["node"], d["name"], d["share"], d["ratio"], d["presence"]) for d in n["sig_T4"]])
            print("    T3:", [(d["node"], d["name"], d["share"], d["ratio"], d["presence"]) for d in n["sig_T3"]])
if a.what == "nodesum":
    N = T["nodes"]
    kept = [n for n in N if n["kept_split"]]
    leaves = [n for n in N if not n["kept_split"]]
    print("nodes", len(N), "kept splits", len(kept), "leaves", len(leaves))
    print("leaf sizes", sorted(n["n"] for n in leaves))
    print("depth of leaves", collections.Counter(n["depth"] for n in leaves))
    print("why stop", collections.Counter(n.get("why_stop") for n in leaves))
    for f in sorted({n["id"].split(".")[0] for n in N}):
        fk = [n for n in kept if n["id"].split(".")[0] == f]
        fl = [n for n in leaves if n["id"].split(".")[0] == f]
        print(f, "kept", len(fk), "leaves", len(fl), "max depth", max(n["depth"] for n in fl),
              "r2/p95 at first split", [(n["r2"], n["null_r2_p95"]) for n in N if n["id"] == f])
    print("margin r2 - p95 of kept, by depth:")
    for d in sorted({n["depth"] for n in kept}):
        ms = [round(n["r2"] - n["null_r2_p95"], 3) for n in kept if n["depth"] == d]
        print("  depth", d, "n", len(ms), "min", min(ms), "median", sorted(ms)[len(ms) // 2])
if a.what == "codes":
    c = T["codes_check"]
    for k, v in c.items():
        if k != "profiles":
            print(k, v)
    for f, v in c["profiles"].items():
        print(f, "median codes", v["median_codes"], "over", [(x["name"], x["ratio"]) for x in v["over"]],
              "under", [(x["name"], x["ratio"]) for x in v["under"]])
if a.what == "branches":
    for b, v in T["branch_place"].items():
        print(b, v)
if a.what == "rooms":
    for s, r in sorted(T["rooms"].items(), key=lambda kv: kv[0].lower()):
        if a.form and r["form"] != a.form:
            continue
        print(s, r["form"], T["leaf_of"].get(s), r["changes"], r["top_dims"], "sec", r["secondary"], "own sig",
              r["sig_share_own"], "nearer" if r["nearer_other"] else "", r["nearest_other"] if r["fits_two"] else "",
              T["primary_branch"].get(s), T["secondary_branch"].get(s))
