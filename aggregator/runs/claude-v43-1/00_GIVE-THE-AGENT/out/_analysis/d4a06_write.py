#!/usr/bin/env python3
"""D4a-06: the deliverables of the top cut, from d4a06_forms.json and d4a06_names.json (the branches' primary
and secondary assignment from d4a05_tree3.json, which does not depend on the clustering); stdout only.

    --what forms     room-forms-D4a06.jsonl          --what tsv   room-forms-D4a06.tsv
    --what tier --form X --move-no N                 one tier_history.jsonl line
    --what md --table count|forms|read|alt|sets|core|rooms     markdown for room-forms-D4a06.md
    --what fill TEMPLATE                             the template with each {{TABLE:name}} line filled
"""
import argparse, collections, datetime, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AN = os.path.join(ROOT, "out", "_analysis")
T = json.load(open(os.path.join(AN, "d4a06_forms.json"), encoding="utf-8"))
NAMES = json.load(open(os.path.join(AN, "d4a06_names.json"), encoding="utf-8"))
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
    P = placed(f)
    R = [ROOMS[s] for s in P]
    shares = sorted(r["share_own"] for r in R)
    return {"ward_n": C["forms"][f]["ward_n"], "n": len(P), "thin": sum(1 for r in R if not r["defining"]),
            "moved_in": sum(1 for r in R if r["mix_form"] != f),
            "moved_out": sum(1 for s, r in ROOMS.items() if r["mix_form"] == f and r["form"] != f),
            "ties": sum(1 for r in R if r["tied"]), "secondary": sum(1 for r in R if r["secondary"]),
            "near_equal": sum(1 for r in R if r["near_equal_centre"]),
            "no_signature": sum(1 for r in R if r["how"].startswith("no change")),
            "share_median": shares[len(shares) // 2]}


def read_lists(f, n=3):
    P = placed(f)
    best = sorted((s for s in P if ROOMS[s]["defining"]), key=lambda s: (-ROOMS[s]["share_own"], -ROOMS[s]["changes"], s.lower()))[:n]
    out = sorted((s for s, r in ROOMS.items() if r["mix_form"] == f and r["form"] != f), key=lambda s: (-ROOMS[s]["changes"], s.lower()))[:n]
    low = sorted((s for s in P if ROOMS[s]["defining"]), key=lambda s: (ROOMS[s]["share_own"], -ROOMS[s]["changes"], s.lower()))[:n]
    return best, out, low


if a.what == "forms":
    for f in FORMS:
        v = C["forms"][f]
        st = stats(f)
        best, out, low = read_lists(f)
        print(json.dumps({"id": f, "level": "form", "k": int(K), "name": NAMES[f][0], "what_it_changes": NAMES[f][1],
                          "one_kind_or_mixture": NAMES[f][2],
                          "signature_T4": [{k: d[k] for k in ("node", "name", "share", "pop_share", "ratio", "presence")} for d in v["sig_T4"]],
                          "signature_T3": [{k: d[k] for k in ("node", "name", "share", "ratio", "presence")} for d in v["sig_T3"][:3]],
                          "dimensions_top3": [{k: d[k] for k in ("node", "name", "share", "pop_share")} for d in v["dims"][:3]],
                          **st, "best_fits": best, "moved_out_largest": [{"room": s, "to": ROOMS[s]["form"]} for s in out],
                          "lowest_share": low, "members": sorted(placed(f), key=str.lower), "since": "D4a-06",
                          "status": "top cut only; the split below waits for J's talk"}, ensure_ascii=False))
    print(json.dumps({"id": "K", "level": "core", "n": len(T["core"]), "name": "the core: rooms with no selected change",
                      "members": sorted((c["sub"] for c in T["core"]), key=str.lower), "since": "D4a-06"}, ensure_ascii=False))

if a.what == "tsv":
    print("\t".join(["room", "form", "form_name", "placed_by", "tied_forms", "secondary_forms", "whole_mix_form", "moved",
                     "selected_changes", "defines_forms", "share_on_own_signature", "primary_branch", "secondary_branches"]))
    rows = []
    for s, r in ROOMS.items():
        rows.append([s, r["form"], NAMES[r["form"]][0], r["how"], ",".join(r["tied"]), ",".join(r["secondary"]), r["mix_form"],
                     "yes" if r["moved"] else "", str(r["changes"]), "yes" if r["defining"] else "no (below the floor)",
                     "%.3f" % r["share_own"], PB.get(s, ""), ",".join(SB.get(s, []))])
    for c in T["core"]:
        s = c["sub"]
        rows.append([s, "K", "the core: rooms with no selected change", "", "", "", "", "", "0", "", "", PB.get(s, ""), ",".join(SB.get(s, []))])
    for row in sorted(rows, key=lambda x: x[0].lower()):
        print("\t".join(row))

if a.what == "tier":
    f = a.form
    print(json.dumps({"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "stage": "D4",
                      "leg": "D4a-06", "tier": "room-form", "id": "D4a06-" + f, "move": "merging", "event": "room form named",
                      "move_no": a.move_no, "name": NAMES[f][0],
                      "why": ("one of the %s forms of the Ward cut on the %d defining rooms (floor %d), the count carried by "
                              "matched-subsample stability (margin %.4f over the shuffled null); placed by J's rule, the form "
                              "whose signature holds most of a room's selected changes" % (K, T["n_defining"], T["floor"], T["stability"][K]["margin"])),
                      "ground": "the rooms' selected changes; no canvas field, verdict or branch",
                      "parent": None, "members_n": stats(f)["n"]}, ensure_ascii=False))


def md(table):
    out = []
    if table == "count":
        out.append("| k | Ward merge height: the cut begins | ends | lifetime (the gap) | stability: matched subsamples | shuffled null mean | null 95th percentile | margin |")
        out.append("|---|---|---|---|---|---|---|---|")
        for k in sorted(T["gap"], key=int):
            g, s = T["gap"][k], T["stability"][k]
            out.append("| %s | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f |" % (k, g["begins"], g["ends"], g["lifetime"],
                                                                              s["real_mean"], s["null_mean"], s["null_p95"], s["margin"]))
    if table == "forms":
        out.append("| form | the pattern of change | defining rooms (Ward) | placed rooms | of them thin | moved in | moved out | ties | with a secondary form | signature: fourth-order theme (share of members' changes; times the population; members holding it) | one kind or a mixture |")
        out.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for f in FORMS:
            st = stats(f)
            sg = "; ".join("%s %s (%.2f; %.1f; %.0f%%)" % (d["node"], d["name"], d["share"], d["ratio"], 100 * d["presence"]) for d in C["forms"][f]["sig_T4"])
            out.append("| %s | %s | %d | %d | %d | %d | %d | %d | %d | %s | %s |" % (f, NAMES[f][0], st["ward_n"], st["n"], st["thin"],
                                                                               st["moved_in"], st["moved_out"], st["ties"], st["secondary"], sg, NAMES[f][2]))
        out.append("| K | the core: no selected change | | %d | | | | | | none | |" % len(T["core"]))
    if table == "read":
        out.append("| form | best fits (defining rooms, largest share on the signature) | misfits the rule moves out (largest rooms), and where they go | members with the smallest share on the signature |")
        out.append("|---|---|---|---|")
        for f in FORMS:
            best, mv, low = read_lists(f)
            out.append("| %s | %s | %s | %s |" % (
                f, ", ".join("r/%s (%d changes, %.2f)" % (s, ROOMS[s]["changes"], ROOMS[s]["share_own"]) for s in best),
                ", ".join("r/%s (%d) to %s" % (s, ROOMS[s]["changes"], ROOMS[s]["form"]) for s in mv),
                ", ".join("r/%s (%.2f)" % (s, ROOMS[s]["share_own"]) for s in low)))
    if table == "alt":
        A5 = T["cuts"]["5"]
        out.append("| form at k = 5 | defining rooms (Ward) | placed rooms | signature: fourth-order themes |")
        out.append("|---|---|---|---|")
        for f in sorted(A5["forms"]):
            sg = "; ".join("%s %s" % (d["node"], d["name"]) for d in A5["forms"][f]["sig_T4"]) or "none"
            out.append("| %s | %d | %d | %s |" % (f, A5["forms"][f]["ward_n"], A5["sizes"].get(f, 0), sg))
    if table == "sets":
        out.append("| set | rooms | %s | core |" % " | ".join(FORMS))
        out.append("|---|---|%s---|" % ("---|" * len(FORMS)))
        for name, key, by in (("raiding (a change on attack calls)", "raiding", C["raiding_by_form"]),
                              ("takeover (F02)", "takeover", C["takeover_by_form"])):
            out.append("| %s | %d | %s | %d |" % (name, len(T[key]), " | ".join(str(by.get(f, 0)) for f in FORMS), by.get("K", 0)))
    if table == "core":
        out.append("| room | coded concepts |")
        out.append("|---|---|")
        for c in T["core"]:
            out.append("| r/%s | %d |" % (c["sub"], c["codes"]))
    if table == "rooms":
        out.append("| room | form | placed by | tied forms | secondary forms | whole-mix form | changes | primary branch | secondary branches |")
        out.append("|---|---|---|---|---|---|---|---|---|")
        rows = []
        for s, r in ROOMS.items():
            how = {"signature": "signature", "signature tie: nearest centre among the tied": "tie, nearest centre",
                   "no change on any signature: by the whole mix": "whole mix (no signature change)"}[r["how"]]
            rows.append((s, r["form"], how, ", ".join(r["tied"]), ", ".join(r["secondary"]), r["mix_form"] + ("" if r["defining"] else " (thin)"),
                         str(r["changes"]), PB.get(s, ""), ", ".join(SB.get(s, []))))
        for c in T["core"]:
            rows.append((c["sub"], "K", "", "", "", "", "0", PB.get(c["sub"], ""), ", ".join(SB.get(c["sub"], []))))
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
        print(f, stats(f))
