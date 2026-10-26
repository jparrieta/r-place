#!/usr/bin/env python3
"""D4a-07: the deliverables of the top cut, from d4a07_forms.json and d4a07_names.json (branches' primary and
secondary assignment from d4a05_tree3.json, independent of the clustering); stdout only.

    --what forms | tsv | tier --form X --move-no N | md --table NAME | fill TEMPLATE | stats
"""
import argparse, collections, datetime, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AN = os.path.join(ROOT, "out", "_analysis")
T = json.load(open(os.path.join(AN, "d4a07_forms.json"), encoding="utf-8"))
NAMES = json.load(open(os.path.join(AN, "d4a07_names.json"), encoding="utf-8"))
T5 = json.load(open(os.path.join(AN, "d4a05_tree3.json"), encoding="utf-8"))
PB, SB = T5["primary_branch"], T5["secondary_branch"]
ap = argparse.ArgumentParser()
ap.add_argument("--what", required=True)
ap.add_argument("--form")
ap.add_argument("--move-no", type=int)
ap.add_argument("--table")
ap.add_argument("template", nargs="?")
a = ap.parse_args()
K = str(T["k_stab"])
C = T["cuts"][K]
FORMS = sorted(C["forms"])
ROOMS = C["rooms"]


def placed(f):
    return [s for s, r in ROOMS.items() if r["form"] == f]


def stats(f):
    R = [ROOMS[s] for s in placed(f)]
    sh = sorted(r["share_own"] for r in R)
    return {"ward_n": C["forms"][f]["ward_n"], "n": len(R), "thin": sum(1 for r in R if not r["defining"]),
            "literal_n": C["literal_sizes"].get(f, 0), "secondary": sum(1 for r in R if r["secondary"]),
            "near_equal": sum(1 for r in R if r["near_equal_centre"]), "share_median": sh[len(sh) // 2],
            "moved_by_literal": sum(1 for r in R if r["moved_by_literal"])}


def read_lists(f, n=3):
    D = [s for s in placed(f) if ROOMS[s]["defining"]]
    best = sorted(D, key=lambda s: (-ROOMS[s]["share_own"], -ROOMS[s]["changes"], s.lower()))[:n]
    mis = sorted(D, key=lambda s: (ROOMS[s]["share_own"], -ROOMS[s]["changes"], s.lower()))[:n]
    return best, mis


def sigtxt(f, k=6):
    return "; ".join("%s (%.2f; %.1f; %.0f%%)" % (d["name"], d["share"], d["ratio"], 100 * d["presence"]) for d in C["forms"][f]["sig_T4"][:k])


if a.what == "forms":
    for f in FORMS:
        v = C["forms"][f]
        best, mis = read_lists(f)
        print(json.dumps({"id": f, "level": "form", "k": int(K), "name": NAMES[f][0], "what_it_changes": NAMES[f][1],
                          "one_kind_or_mixture": NAMES[f][2], "a_differing_account": NAMES[f][3],
                          "signature_T4": [{k: d[k] for k in ("col", "name", "link", "share", "pop_share", "ratio", "presence")} for d in v["sig_T4"]],
                          "signature_T3": [{k: d[k] for k in ("col", "name", "share", "ratio", "presence")} for d in v["sig_T3"][:4]],
                          "dimensions_top3": [{k: d[k] for k in ("col", "name", "share", "pop_share")} for d in v["dims"][:3]],
                          "op_mix": C["op_mix"][f], **stats(f), "best_fits": best,
                          "misfits": [{"room": s, "near": ROOMS[s]["near_equal_centre"] or ROOMS[s]["secondary"]} for s in mis],
                          "members": sorted(placed(f), key=str.lower), "placement": "by the whole mix", "since": "D4a-07",
                          "status": "top cut only; the split below waits for J's talk"}, ensure_ascii=False))
    print(json.dumps({"id": "K", "level": "core", "n": len(T["core"]), "name": "the core: rooms with no selected change",
                      "members": T["core"], "since": "D4a-07"}, ensure_ascii=False))

if a.what == "tsv":
    print("\t".join(["room", "form", "form_name", "literal_rule_form", "literal_rule_ties", "moved_by_literal_rule",
                     "secondary_forms", "near_equal_centres", "selected_changes", "defines_forms", "share_on_own_signature",
                     "primary_branch", "secondary_branches"]))
    rows = []
    for s, r in ROOMS.items():
        rows.append([s, r["form"], NAMES[r["form"]][0], r["literal_form"], ",".join(r["literal_tied"]),
                     "yes" if r["moved_by_literal"] else "", ",".join(r["secondary"]), ",".join(r["near_equal_centre"]),
                     str(r["changes"]), "yes" if r["defining"] else "no (below the floor)", "%.3f" % r["share_own"],
                     PB.get(s, ""), ",".join(SB.get(s, []))])
    for s in T["core"]:
        rows.append([s, "K", "the core: rooms with no selected change", "", "", "", "", "", "0", "", "", PB.get(s, ""), ",".join(SB.get(s, []))])
    for row in sorted(rows, key=lambda x: x[0].lower()):
        print("\t".join(row))

if a.what == "tier":
    f = a.form
    print(json.dumps({"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "stage": "D4",
                      "leg": "D4a-07", "tier": "room-form", "id": "D4a07-" + f, "move": "merging", "event": "room form named",
                      "move_no": a.move_no, "name": NAMES[f][0],
                      "why": ("one of the %s forms of the Ward cut on the %d defining rooms (floor %d), with arrows and link ops "
                              "lifted as links at every level; the count carried by both the merge-height gap and matched-subsample "
                              "stability (margin %.4f over the shuffled null); placed by the whole mix" % (K, T["n_defining"], T["floor"], T["stability"][K]["margin"])),
                      "ground": "the rooms' selected changes, nodes and links; no canvas field, verdict or branch",
                      "parent": None, "members_n": stats(f)["n"]}, ensure_ascii=False))


def md(table):
    out = []
    if table == "count":
        out.append("| k | Ward merge height: the cut begins | ends | lifetime (the gap) | stability: matched subsamples | shuffled null mean | null 95th percentile | margin |")
        out.append("|---|---|---|---|---|---|---|---|")
        for k in sorted(T["gap"], key=int):
            g, s = T["gap"][k], T["stability"][k]
            out.append("| %s | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f |" % (k, g["begins"], g["ends"], g["lifetime"], s["real_mean"], s["null_mean"], s["null_p95"], s["margin"]))
    if table == "forms":
        out.append("| form | the pattern of change | defining rooms (Ward) | placed by the whole mix | by J's literal rule | signature: fourth-order nodes and links (share of members' changes; times the population; members holding it) | restricts among its changes | one kind or a mixture |")
        out.append("|---|---|---|---|---|---|---|---|")
        for f in FORMS:
            st = stats(f)
            out.append("| %s | %s | %d | %d | %d | %s | %.2f | %s |" % (f, NAMES[f][0], st["ward_n"], st["n"], st["literal_n"], sigtxt(f),
                                                                    C["op_mix"][f]["restrict"], NAMES[f][2]))
        out.append("| K | the core: no selected change | | %d | %d | none | | |" % (len(T["core"]), len(T["core"])))
    if table == "accounts":
        out.append("| form | could an account that differs from the global model be written? |")
        out.append("|---|---|")
        for f in FORMS:
            out.append("| %s, %s | %s |" % (f, NAMES[f][0], NAMES[f][3]))
    if table == "read":
        out.append("| form | best fits (defining rooms, largest share on the signature) | misfits (smallest share), and the forms they lie near |")
        out.append("|---|---|---|")
        for f in FORMS:
            best, mis = read_lists(f)
            out.append("| %s | %s | %s |" % (f, ", ".join("r/%s (%d changes, %.2f)" % (s, ROOMS[s]["changes"], ROOMS[s]["share_own"]) for s in best),
                                           ", ".join("r/%s (%.2f; near %s)" % (s, ROOMS[s]["share_own"], ", ".join(ROOMS[s]["near_equal_centre"] or ROOMS[s]["secondary"]) or "none") for s in mis)))
    if table == "sets":
        rc = T["raiding_core"]
        by = rc["by_form"][K]
        tk = C["takeover_by_form"]
        out.append("| set | rooms | %s | core |" % " | ".join(FORMS))
        out.append("|---|---|%s---|" % ("---|" * len(FORMS)))
        out.append("| raiding core (a quarter or more of the changes on attack calls; defining rooms) | %d | %s | 0 |" % (rc["n"], " | ".join(str(by.get(f, 0)) for f in FORMS)))
        out.append("| takeover (F02) | %d | %s | %d |" % (len(T["takeover"]), " | ".join(str(tk.get(f, 0)) for f in FORMS), tk.get("K", 0)))
    if table == "rooms":
        out.append("| room | form | J's literal rule | secondary forms | near-equal centres | changes | primary branch | secondary branches |")
        out.append("|---|---|---|---|---|---|---|---|")
        rows = []
        for s, r in ROOMS.items():
            lit = r["literal_form"] + (" (tie: %s)" % ", ".join(r["literal_tied"]) if r["literal_tied"] else "")
            rows.append((s, r["form"] + ("" if r["defining"] else " (thin)"), lit, ", ".join(r["secondary"]), ", ".join(r["near_equal_centre"]),
                         str(r["changes"]), PB.get(s, ""), ", ".join(SB.get(s, []))))
        for s in T["core"]:
            rows.append((s, "K", "", "", "", "0", PB.get(s, ""), ", ".join(SB.get(s, []))))
        for row in sorted(rows, key=lambda x: x[0].lower()):
            out.append("| %s |" % " | ".join(row))
    return "\n".join(out)


if a.what == "md":
    print(md(a.table))
if a.what == "fill":
    for line in open(a.template, encoding="utf-8").read().split("\n"):
        m = re.fullmatch(r"\{\{TABLE:([a-z]+)\}\}", line.strip())
        print(md(m.group(1)) if m else line)
if a.what == "stats":
    for f in FORMS:
        print(f, stats(f), read_lists(f))
