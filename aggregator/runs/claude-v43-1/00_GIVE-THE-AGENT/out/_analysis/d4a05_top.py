#!/usr/bin/env python3
"""D4a-05: the top cut's deliverables (J, 18:36 Berlin: stop at the top cut), from d4a05_tree3.json and
d4a05_names.json; stdout only.

    --what forms     out/room-forms-D4a05.jsonl: the 8 forms and the core, one line each
    --what tsv       out/room-forms-D4a05.tsv: one row per room
    --what nesting   how the Ward cut at k = 4 to 7 joins the 8 forms (recomputed from the ledger)
    --what counter   per form: members nearer another form's centroid, and members with none of their
                     changes on the form's signature nodes, named
    --what md --table forms|rooms|branches|k   markdown tables for room-forms-D4a05.md

    python3 out/_analysis/d4a05_top.py --what forms > out/room-forms-D4a05.jsonl
"""
import argparse, collections, json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
T = json.load(open(os.path.join(AN, "d4a05_tree3.json"), encoding="utf-8"))
NAMES = json.load(open(os.path.join(AN, "d4a05_names.json"), encoding="utf-8"))
ap = argparse.ArgumentParser()
ap.add_argument("--what", required=True)
ap.add_argument("--table")
a = ap.parse_args()
FORMS = sorted(T["forms"])
CORE = "K"


def jac(f):
    return T["sensitivity"]["top_form_jaccard"][f]


def counter(f):
    mem = T["forms"][f]["members"]
    near = sorted((s for s in mem if T["rooms"][s]["nearer_other"]), key=str.lower)
    zero = sorted((s for s in mem if T["rooms"][s]["sig_share_own"] == 0), key=str.lower)
    return near, zero


if a.what == "forms":
    top = T["top"][str(T["k_chosen"])]
    for f in FORMS:
        v = T["forms"][f]
        R = [T["rooms"][s] for s in v["members"]]
        near, zero = counter(f)
        print(json.dumps({
            "id": f, "level": "form", "n": v["n"], "name": NAMES[f][0], "what_it_changes": NAMES[f][1],
            "signature_T4": [{k: d[k] for k in ("node", "name", "share", "pop_share", "ratio", "presence")} for d in v["sig_T4"]],
            "signature_T3": [{k: d[k] for k in ("node", "name", "share", "ratio", "presence")} for d in v["sig_T3"][:3]],
            "dimensions_top3": [{k: d[k] for k in ("node", "name", "share", "pop_share")} for d in v["dims"][:3]],
            "median_changes": v["median_changes"], "mean_dimension_entropy": v["mean_dim_entropy"],
            "fit_two_forms_equally": sum(r["fits_two"] for r in R), "nearer_another_form": len(near),
            "with_no_change_on_the_signature": len(zero), "with_a_secondary_form": sum(1 for r in R if r["secondary"]),
            "clusterwise_jaccard": jac(f),
            "cut": {"k": T["k_chosen"], "silhouette": top["silhouette"], "null_sil_p95": top["null_sil_p95"],
                    "bootstrap_ari": top["boot_ari_mean"]},
            "members": sorted(v["members"], key=str.lower), "since": "D4a-05",
            "status": "top cut only; the split below waits for J's talk"}, ensure_ascii=False))
    print(json.dumps({"id": CORE, "level": "core", "n": len(T["core"]), "name": "the core: rooms with no selected change",
                      "what_it_changes": "Nothing: every accepted line instantiates an element or records an absence; no restrict, add-step, add-condition, link or contradict line.",
                      "members": T["core"], "since": "D4a-05"}, ensure_ascii=False))

if a.what == "tsv":
    print("\t".join(["room", "form", "form_name", "selected_changes", "secondary_forms", "fits_two_equally_with",
                     "nearer_to_form", "share_of_changes_on_own_signature", "primary_branch", "secondary_branches"]))
    rows = []
    for s, r in T["rooms"].items():
        rows.append([s, r["form"], NAMES[r["form"]][0], str(r["changes"]), ",".join(r["secondary"]),
                     r["nearest_other"] if r["fits_two"] else "", r["nearest_other"] if r["nearer_other"] else "",
                     "%.3f" % r["sig_share_own"], T["primary_branch"].get(s, ""), ",".join(T["secondary_branch"].get(s, []))])
    for s in T["core"]:
        rows.append([s, CORE, "the core: rooms with no selected change", "0", "", "", "", "",
                     T["primary_branch"].get(s, ""), ",".join(T["secondary_branch"].get(s, []))])
    for row in sorted(rows, key=lambda x: x[0].lower()):
        print("\t".join(row))

if a.what == "nesting":
    import numpy as np
    from scipy.cluster.hierarchy import linkage, fcluster
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import adaptation_ledger as al
    CH = {"add-step", "add-condition", "link", "restrict", "contradict"}
    L = [r for r in al.shared_lines(OUT) if r.get("op") in CH and len(r.get("lift") or []) >= 4]
    rooms = sorted({r["sub"] for r in L}, key=str.lower)
    idx = {s: i for i, s in enumerate(rooms)}
    blocks = []
    for i, lv in ((1, "T3"), (2, "T4"), (3, "dim")):
        held = collections.defaultdict(set)
        for r in L:
            if r["lift"][i]:
                held[r["lift"][i]].add(r["sub"])
        keep = sorted(k for k, v in held.items() if not (lv == "T3" and len(v) == 1))
        ci = {k: j for j, k in enumerate(keep)}
        m = np.zeros((len(rooms), len(keep)))
        for r in L:
            if r["lift"][i] in ci:
                m[idx[r["sub"]], ci[r["lift"][i]]] += 1
        tot = m.sum(axis=1, keepdims=True)
        blocks.append(np.sqrt(np.divide(m, tot, out=np.zeros_like(m), where=tot > 0)) / math.sqrt(6))
    Z = linkage(np.hstack(blocks), method="ward")
    lab8 = fcluster(Z, 8, criterion="maxclust")
    same = all(T["rooms"][s]["form"] == T["rooms"][rooms[0]]["form"] or True for s in rooms)
    f_of = {s: T["rooms"][s]["form"] for s in rooms}
    check = len({(lab8[idx[s]], f_of[s]) for s in rooms}) == 8
    print("the recomputed k = 8 cut matches the forms one to one:", check)
    for k in range(4, 8):
        lk = fcluster(Z, k, criterion="maxclust")
        groups = collections.defaultdict(set)
        for s in rooms:
            groups[lk[idx[s]]].add(f_of[s])
        print("k = %d:" % k, sorted(("+".join(sorted(g)), sum(T["forms"][f]["n"] for f in g)) for g in groups.values()))

if a.what == "counter":
    for f in FORMS:
        near, zero = counter(f)
        print(f, "nearer another form", len(near), near[:8], "| none on the signature", len(zero), zero[:8])

if a.what == "md":
    if a.table == "forms":
        print("| form | rooms | the pattern of change | signature: fourth-order node (share of members' changes; times the population; members holding it) | median changes | fit two forms equally | nearer another form | none of its changes on the signature | with a secondary form | clusterwise Jaccard |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        for f in FORMS:
            v = T["forms"][f]
            R = [T["rooms"][s] for s in v["members"]]
            near, zero = counter(f)
            sg = "; ".join("%s %s (%.2f; %.1f; %.0f%%)" % (d["node"], d["name"], d["share"], d["ratio"], 100 * d["presence"]) for d in v["sig_T4"])
            print("| %s | %d | %s | %s | %g | %d | %d | %d | %d | %.3f |" % (
                f, v["n"], NAMES[f][0], sg, v["median_changes"], sum(r["fits_two"] for r in R), len(near), len(zero),
                sum(1 for r in R if r["secondary"]), jac(f)))
        print("| %s | %d | the core: no selected change | none | 0 | | | | | |" % (CORE, len(T["core"])))
    if a.table == "k":
        print("| k | sizes | largest to smallest | silhouette | null 95th percentile | bootstrap adjusted Rand |")
        print("|---|---|---|---|---|---|")
        for k, v in T["top"].items():
            print("| %s | %s | %.2f | %.4f | %.4f | %.3f |" % (k, ", ".join(map(str, v["sizes"])), v["ratio"], v["silhouette"],
                                                             v["null_sil_p95"], v["boot_ari_mean"]))
    if a.table == "rooms":
        print("| room | form | changes | secondary forms | fits two equally with | primary branch | secondary branches |")
        print("|---|---|---|---|---|---|---|")
        rows = []
        for s, r in T["rooms"].items():
            rows.append((s, r["form"], str(r["changes"]), ", ".join(r["secondary"]), r["nearest_other"] if r["fits_two"] else "",
                         T["primary_branch"].get(s, ""), ", ".join(T["secondary_branch"].get(s, []))))
        for s in T["core"]:
            rows.append((s, CORE, "0", "", "", T["primary_branch"].get(s, ""), ", ".join(T["secondary_branch"].get(s, []))))
        for row in sorted(rows, key=lambda x: x[0].lower()):
            print("| %s |" % " | ".join(row))
    if a.table == "branches":
        print("| branch | members | home form | home share | members by form |")
        print("|---|---|---|---|---|")
        for b, v in sorted(T["branch_place"].items(), key=lambda kv: int(kv[0][1:])):
            print("| %s | %d | %s | %.3f | %s |" % (b, v["n"], v["home_form"], v["home_share"],
                                                  ", ".join("%s %d" % kv for kv in v["by_form"].items())))
