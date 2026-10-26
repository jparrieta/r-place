#!/usr/bin/env python3
"""D4a-05: write the room tree's deliverables from d4a05_tree3.json and d4a05_names.json, to stdout.

    --what forms   room-forms-D4.jsonl (forms, sub-forms and the core, one line each)
    --what tree    room-tree-D4.json (the nested tree; below each terminal node the Ward order to the rooms)
    --what tsv     room-tree-D4.tsv (one row per room: form, sub-forms, secondary forms, branches)
    --what tier --node ID --move-no N   one tier_history.jsonl line for the move that declares ID
    --what md --table forms|subforms|rooms|branches   markdown tables for room-tree-D4.md

    python3 out/_analysis/d4a05_write.py --what forms > out/room-forms-D4.jsonl
"""
import argparse, collections, datetime, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AN = os.path.join(ROOT, "out", "_analysis")
T = json.load(open(os.path.join(AN, "d4a05_tree3.json"), encoding="utf-8"))
NAMES = json.load(open(os.path.join(AN, "d4a05_names.json"), encoding="utf-8"))
ap = argparse.ArgumentParser()
ap.add_argument("--what", required=True)
ap.add_argument("--node")
ap.add_argument("--move-no", type=int)
ap.add_argument("--table")
a = ap.parse_args()

NODES = {n["id"]: n for n in T["nodes"]}
FORMS = sorted(T["forms"])
CORE_ID = "K"


def parent_of(nid):
    return nid.rsplit(".", 1)[0] if "." in nid else None


def children(nid):
    return sorted((k for k in NODES if parent_of(k) == nid), key=lambda k: int(k.rsplit(".", 1)[1]))


def why_kept(nid):
    p = parent_of(nid)
    if p is None:
        top = T["top"][str(T["k_chosen"])]
        return ("one of the %d forms of the Ward cut chosen by the logged rule (k from 4 to 8: highest silhouette, "
                "%.4f against a null 95th percentile of %.4f; bootstrap adjusted Rand %.3f; this form's clusterwise "
                "Jaccard %.3f)" % (T["k_chosen"], top["silhouette"], top["null_sil_p95"], top["boot_ari_mean"],
                                   T["sensitivity"]["top_form_jaccard"][nid]))
    pn = NODES[p]
    return ("a half of %s's split: between-group share %.4f against the permutation null's 95th percentile %.4f; "
            "this half's clusterwise bootstrap Jaccard %.3f (both halves 0.6 or more)"
            % (p, pn["r2"], pn["null_r2_p95"], pn["child_jaccard"][nid]))


def sig(n, key, k=3):
    return [{"node": d["node"], "name": d.get("name"), "share": d["share"], "ratio": d["ratio"], "presence": d["presence"]}
            for d in (n.get(key) or [])[:k]]


def node_line(nid):
    n = NODES[nid]
    src = T["forms"][nid] if nid in T["forms"] else n
    return {"id": nid, "parent": parent_of(nid), "level": "form" if nid in T["forms"] else "sub-form",
            "depth": n["depth"], "n": n["n"], "name": NAMES[nid][0], "what_it_changes": NAMES[nid][1],
            "signature_T4": sig(src, "sig_T4"), "signature_T3": sig(src, "sig_T3"),
            "median_changes": src.get("median_changes"),
            "own_split": ({"sizes": n.get("split_sizes"), "r2": n.get("r2"), "null_r2_p95": n.get("null_r2_p95"),
                           "child_jaccard": n.get("child_jaccard"), "kept": n["kept_split"],
                           "why_stop": n.get("why_stop")} if n.get("r2") is not None or n.get("why_stop") else None),
            "why_kept": why_kept(nid), "terminal": not n["kept_split"],
            "members": sorted(n["members"], key=str.lower), "since": "D4a-05"}


if a.what == "forms":
    for f in FORMS:
        stack = [f]
        while stack:
            nid = stack.pop(0)
            print(json.dumps(node_line(nid), ensure_ascii=False))
            stack = children(nid) + stack
    print(json.dumps({"id": CORE_ID, "parent": None, "level": "core", "depth": 0, "n": len(T["core"]),
                      "name": "the core: rooms with no selected change",
                      "what_it_changes": "Nothing: every accepted line of these rooms instantiates an element or records an absence; they hold no restrict, add-step, add-condition, link or contradict line.",
                      "why_kept": "kept together by the instruction (J's amendment, 26 October 2026)", "terminal": True,
                      "members": T["core"], "since": "D4a-05"}, ensure_ascii=False))

if a.what == "tree":
    def build(nid):
        n = NODES[nid]
        rec = {"id": nid, "name": NAMES[nid][0], "n": n["n"]}
        kids = children(nid)
        if kids:
            rec["children"] = [build(k) for k in kids]
        else:
            rec["rooms"] = sorted(n["members"], key=str.lower)
            rec["ward_order_to_rooms"] = n.get("newick")
            rec["below_here"] = ("the Ward joins below this node run on to every room (ward_order_to_rooms); no "
                                 "split below it passed the stated tests (%s)" % (n.get("why_stop") or ""))
        return rec
    out = {"what": "the room tree, D4a-05 (J's amendment of 26 October 2026)", "unit": "room",
           "root": "the frozen global model (46384686...); the root is not a case",
           "k": T["k_chosen"], "children": [build(f) for f in FORMS] +
           [{"id": CORE_ID, "name": "the core: rooms with no selected change", "n": len(T["core"]), "rooms": T["core"]}],
           "method": "out/_analysis/d4a05_room_tree.py; the rule in the diary at D4a-05"}
    print(json.dumps(out, ensure_ascii=False))


def leaf_path(s):
    nid = T["leaf_of"][s]
    parts = nid.split(".")
    return [".".join(parts[:i]) for i in range(2, len(parts) + 1)]


if a.what == "tsv":
    cols = ["room", "form", "form_name", "sub_forms", "deepest_sub_form_name", "selected_changes",
            "secondary_forms", "fits_two_equally_with", "nearer_to_form", "primary_branch", "secondary_branches"]
    print("\t".join(cols))
    rows = []
    for s, r in T["rooms"].items():
        path = leaf_path(s)
        rows.append([s, r["form"], NAMES[r["form"]][0], " > ".join(path), NAMES[path[-1]][0] if path else "",
                     str(r["changes"]), ",".join(r["secondary"]), r["nearest_other"] if r["fits_two"] else "",
                     r["nearest_other"] if r["nearer_other"] else "", T["primary_branch"].get(s, ""),
                     ",".join(T["secondary_branch"].get(s, []))])
    for s in T["core"]:
        rows.append([s, CORE_ID, "the core: rooms with no selected change", "", "", "0", "", "", "",
                     T["primary_branch"].get(s, ""), ",".join(T["secondary_branch"].get(s, []))])
    for row in sorted(rows, key=lambda x: x[0].lower()):
        print("\t".join(row))

if a.what == "tier":
    nid = a.node
    n = NODES[nid]
    print(json.dumps({"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "stage": "D4", "leg": "D4a-05", "tier": "room-form" if nid in T["forms"] else "room-sub-form",
                      "id": nid, "move": "merging" if nid in T["forms"] else "splitting",
                      "event": "room form named" if nid in T["forms"] else "room sub-form declared",
                      "move_no": a.move_no, "name": NAMES[nid][0], "why": why_kept(nid),
                      "ground": "the rooms' selected changes (shares at the third-order, fourth-order and dimension levels); no canvas field, verdict or branch",
                      "parent": parent_of(nid), "members_n": n["n"]}, ensure_ascii=False))

if a.what == "md":
    if a.table == "forms":
        print("| form | rooms | the pattern of change | signature (fourth-order node: share of members' changes, times the population, share of members holding it) | median changes | fit two forms equally | nearer another form | with a secondary form | clusterwise Jaccard |")
        print("|---|---|---|---|---|---|---|---|---|")
        for f in FORMS:
            v = T["forms"][f]
            R = [T["rooms"][s] for s in v["members"]]
            sg = "; ".join("%s %s: %.2f, %.1fx, %.0f%%" % (d["node"], d["name"], d["share"], d["ratio"], 100 * d["presence"]) for d in v["sig_T4"])
            print("| %s | %d | %s | %s | %g | %d | %d | %d | %.3f |" % (
                f, v["n"], NAMES[f][0], sg, v["median_changes"], sum(r["fits_two"] for r in R),
                sum(r["nearer_other"] for r in R), sum(1 for r in R if r["secondary"]),
                T["sensitivity"]["top_form_jaccard"][f]))
        print("| %s | %d | the core: no selected change | none | 0 | | | | |" % (CORE_ID, len(T["core"])))
    if a.table == "subforms":
        print("| sub-form | rooms | the pattern of change | signature (fourth-order node: share, times the population) | parent's split: share against the null's 95th percentile | this half's Jaccard | terminal |")
        print("|---|---|---|---|---|---|---|")
        for f in FORMS:
            stack = children(f)
            while stack:
                nid = stack.pop(0)
                n = NODES[nid]
                pn = NODES[parent_of(nid)]
                sg = "; ".join("%s %s: %.2f, %.1fx" % (d["node"], d["name"], d["share"], d["ratio"]) for d in (n.get("sig_T4") or [])[:2])
                print("| %s | %d | %s | %s | %.4f against %.4f | %.3f | %s |" % (
                    nid, n["n"], NAMES[nid][0], sg, pn["r2"], pn["null_r2_p95"], pn["child_jaccard"][nid],
                    "yes" if not n["kept_split"] else "no"))
                stack = children(nid) + stack
    if a.table == "rooms":
        print("| room | form | sub-forms | changes | secondary forms | fits two equally with | primary branch | secondary branches |")
        print("|---|---|---|---|---|---|---|---|")
        rows = []
        for s, r in T["rooms"].items():
            rows.append((s, r["form"], " > ".join(leaf_path(s)), str(r["changes"]), ", ".join(r["secondary"]),
                         r["nearest_other"] if r["fits_two"] else "", T["primary_branch"].get(s, ""),
                         ", ".join(T["secondary_branch"].get(s, []))))
        for s in T["core"]:
            rows.append((s, CORE_ID, "", "0", "", "", T["primary_branch"].get(s, ""), ", ".join(T["secondary_branch"].get(s, []))))
        for row in sorted(rows, key=lambda x: x[0].lower()):
            print("| %s |" % " | ".join(row))
    if a.table == "branches":
        print("| branch | members | home form | home share | members by form | members whose primary branch it is |")
        print("|---|---|---|---|---|---|")
        for b, v in sorted(T["branch_place"].items(), key=lambda kv: int(kv[0][1:])):
            print("| %s | %d | %s | %.3f | %s | %d |" % (b, v["n"], v["home_form"], v["home_share"],
                                                         ", ".join("%s %d" % kv for kv in v["by_form"].items()),
                                                         v["primary_members"]))
