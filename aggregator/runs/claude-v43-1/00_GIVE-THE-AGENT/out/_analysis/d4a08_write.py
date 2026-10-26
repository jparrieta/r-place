#!/usr/bin/env python3
"""D4a-08: the deliverables of the carried cut (k = 5) with the k = 8 cut beside it, from d4a08e_forms.json and
d4a08_names.json (branches from d4a05_tree3.json; D4a-07 forms from room-forms-D4a07.jsonl); stdout only.

    --what forms | tsv | tier --form X --move-no N | md --table NAME | fill TEMPLATE
"""
import argparse, datetime, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
T = json.load(open(os.path.join(AN, "d4a08e_forms.json"), encoding="utf-8"))
NAMES = json.load(open(os.path.join(AN, "d4a08_names.json"), encoding="utf-8"))
T5 = json.load(open(os.path.join(AN, "d4a05_tree3.json"), encoding="utf-8"))
PB, SB = T5["primary_branch"], T5["secondary_branch"]
P7 = {}
for l in open(os.path.join(OUT, "room-forms-D4a07.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r.get("level") == "form":
        for s in r["members"]:
            P7[s] = r["id"]
ap = argparse.ArgumentParser()
ap.add_argument("--what", required=True)
ap.add_argument("--form")
ap.add_argument("--move-no", type=int)
ap.add_argument("--table")
ap.add_argument("template", nargs="?")
a = ap.parse_args()
K, K8 = "5", "8"
C, C8 = T["cuts"][K], T["cuts"][K8]
FORMS = sorted(C["forms"])
N5 = NAMES["5"]


def members(cut, f):
    return [s for s, r in cut["rooms"].items() if r["form"] == f]


def sig(cut, f, k=4):
    return "; ".join("%s (%.2f; %.1f; %.0f%%)" % (d["name"], d["share"], d["ratio"], 100 * d["presence"]) for d in cut["forms"][f]["sig_T4"][:k]) or "none"


def codes(cut, f, k=3):
    return "; ".join("%s (%.3f against %.3f)" % (d["name"], d["share"], d["mean_share"]) for d in cut["forms"][f]["code_over"][:k])


if a.what == "forms":
    for f in FORMS:
        v = C["forms"][f]
        R = [C["rooms"][s] for s in members(C, f)]
        print(json.dumps({"id": f, "level": "form", "k": 5, "name": N5[f][0], "what_it_changes_and_does": N5[f][1],
                          "one_kind_or_mixture": N5[f][2], "a_differing_account": N5[f][3],
                          "change_signature_T4": [{x: d[x] for x in ("col", "name", "link", "share", "ratio", "presence")} for d in v["sig_T4"]],
                          "codes_over": v["code_over"], "codes_under": v["code_under"], "code_dimensions_over": v["code_dims"],
                          "ward_n": v["ward_n"], "n": len(R), "thin": sum(1 for r in R if not r["defining"]),
                          "median_codes": C["median_codes"][f], "median_changes": C["median_changes"][f], "op_mix": C["op_mix"][f],
                          "with_secondary": sum(1 for r in R if r["secondary"]), "near_equal": sum(1 for r in R if r["near_equal_centre"]),
                          "ward_split": v.get("ward_split"), "members": sorted(members(C, f), key=str.lower),
                          "placement": "by the whole mix of both blocks", "since": "D4a-08",
                          "status": "top cut, written for J to iterate on; the leg is not closed"}, ensure_ascii=False))
    print(json.dumps({"id": "K", "level": "core", "n": len(T["core"]), "name": "the core: rooms with no selected change",
                      "members": T["core"], "by_codes_alone": C["core_by_codes"], "since": "D4a-08"}, ensure_ascii=False))

if a.what == "tsv":
    print("\t".join(["room", "form_k5", "form_k5_name", "form_k8", "D4a07_form", "secondary_forms_k5", "near_equal_centres_k5",
                     "selected_changes", "coded_concepts", "defines_forms", "primary_branch", "secondary_branches"]))
    rows = []
    for s, r in C["rooms"].items():
        rows.append([s, r["form"], N5[r["form"]][0], C8["rooms"][s]["form"], P7.get(s, ""), ",".join(r["secondary"]),
                     ",".join(r["near_equal_centre"]), str(r["changes"]), str(r["codes"]), "yes" if r["defining"] else "no (below the floor)",
                     PB.get(s, ""), ",".join(SB.get(s, []))])
    for s in T["core"]:
        rows.append([s, "K", "the core: rooms with no selected change", "K", "K", "", "", "0", "", "",
                     PB.get(s, ""), ",".join(SB.get(s, []))])
    for row in sorted(rows, key=lambda x: x[0].lower()):
        print("\t".join(row))

if a.what == "tier":
    f = a.form
    print(json.dumps({"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "stage": "D4",
                      "leg": "D4a-08", "tier": "room-form", "id": "D4a08-" + f, "move": "merging", "event": "room form named",
                      "move_no": a.move_no, "name": N5[f][0],
                      "why": ("one of the 5 forms of the Ward cut on the %d defining rooms (floor %d), on two blocks counting equally: "
                              "the D4a-07 change block and the code block of deviations from the mean share; the count carried by the "
                              "merge-height gap (lifetime %.4f), the shuffled-null stability being unusable for this distance (diary); "
                              "placed by the whole mix" % (T["n_defining"], T["floor"], T["gap"][K]["lifetime"])),
                      "ground": "the rooms' selected changes and coded concepts; no canvas field, verdict or branch",
                      "parent": None, "members_n": len(members(C, f))}, ensure_ascii=False))


def md(table):
    out = []
    if table == "count":
        out.append("| k | Ward merge height: the cut begins | ends | lifetime (the gap) | stability: matched subsamples | shuffled null mean | null 95th percentile | margin | sizes of the real cut | sizes of one shuffled copy's cut |")
        out.append("|---|---|---|---|---|---|---|---|---|---|")
        for k in sorted(T["gap"], key=int):
            g, s = T["gap"][k], T["stability"][k]
            out.append("| %s | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %s | %s |" % (
                k, g["begins"], g["ends"], g["lifetime"], s["real_mean"], s["null_mean"], s["null_p95"], s["margin"],
                ", ".join(map(str, T["real_cut_sizes"][k])), ", ".join(map(str, T["null_cut_sizes"][k]))))
    if table == "forms":
        out.append("| form | what its rooms change and do | defining rooms (Ward) | placed | change signature: fourth-order nodes and links (share; times the population; members holding it) | codes most above the average room (form's share against the mean share) | median coded concepts | one kind or a mixture |")
        out.append("|---|---|---|---|---|---|---|---|")
        for f in FORMS:
            v = C["forms"][f]
            out.append("| %s | %s | %d | %d | %s | %s | %g | %s |" % (f, N5[f][0], v["ward_n"], len(members(C, f)), sig(C, f), codes(C, f),
                                                                    C["median_codes"][f], N5[f][2]))
        out.append("| K | the core: no selected change | | %d | none | | | |" % len(T["core"]))
    if table == "alt":
        out.append("| form at k = 8 | reading | defining rooms (Ward) | placed | change signature | codes most above the average room |")
        out.append("|---|---|---|---|---|---|")
        for f in sorted(C8["forms"]):
            v = C8["forms"][f]
            out.append("| %s | %s | %d | %d | %s | %s |" % (f, NAMES["8"][f], v["ward_n"], len(members(C8, f)), sig(C8, f, 3), codes(C8, f)))
    if table == "accounts":
        out.append("| form | could an account that differs from the global model be written? |")
        out.append("|---|---|")
        for f in FORMS:
            out.append("| %s, %s | %s |" % (f, N5[f][0], N5[f][3]))
    if table == "cross":
        out.append("| D4a-07 form | rooms | in D4a-08's A | B | C | D | E |")
        out.append("|---|---|---|---|---|---|---|")
        for f7, row in sorted(T["D4a07_to_D4a08"].items()):
            out.append("| %s | %d | %s |" % (f7, sum(row.values()), " | ".join(str(row.get(x, 0)) for x in FORMS)))
    if table == "sets":
        rc = T["raiding_core"]["by_form"]
        tk = C["takeover_by_form"]
        out.append("| set | rooms | %s | core |" % " | ".join(FORMS))
        out.append("|---|---|%s---|" % ("---|" * len(FORMS)))
        out.append("| raiding core (a quarter or more of the changes on attack calls) | %d | %s | 0 |" % (T["raiding_core"]["n"], " | ".join(str(rc.get(x, 0)) for x in FORMS)))
        out.append("| takeover (F02) | %d | %s | %d |" % (len(T["takeover"]), " | ".join(str(tk.get(x, 0)) for x in FORMS), tk.get("K", 0)))
    if table == "core":
        out.append("| core room | the form its codes alone are nearest (k = 5) |")
        out.append("|---|---|")
        for s in T["core"]:
            out.append("| r/%s | %s |" % (s, C["core_by_codes"].get(s, "")))
    if table == "rooms":
        out.append("| room | form (k = 5) | form at k = 8 | D4a-07 form | secondary forms | near-equal centres | changes | coded concepts | primary branch |")
        out.append("|---|---|---|---|---|---|---|---|---|")
        rows = []
        for s, r in C["rooms"].items():
            rows.append((s, r["form"] + ("" if r["defining"] else " (thin)"), C8["rooms"][s]["form"], P7.get(s, ""), ", ".join(r["secondary"]),
                         ", ".join(r["near_equal_centre"]), str(r["changes"]), str(r["codes"]), PB.get(s, "")))
        for s in T["core"]:
            rows.append((s, "K", "K", "K", "", "", "0", "", PB.get(s, "")))
        for row in sorted(rows, key=lambda x: x[0].lower()):
            out.append("| %s |" % " | ".join(row))
    return "\n".join(out)


if a.what == "md":
    print(md(a.table))
if a.what == "fill":
    for line in open(a.template, encoding="utf-8").read().split("\n"):
        m = re.fullmatch(r"\{\{TABLE:([a-z]+)\}\}", line.strip())
        print(md(m.group(1)) if m else line)
