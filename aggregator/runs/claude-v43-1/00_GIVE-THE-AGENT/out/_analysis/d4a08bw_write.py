#!/usr/bin/env python3
"""D4a-08, the variant with changes at two thirds (d4a08w23c_forms.json, k = 8): the forms ledger, the room table,
tier lines and markdown tables for room-forms-D4a08b.*; stdout only.

    --what forms | tsv | tier --form X --move-no N | md --table NAME | fill TEMPLATE
"""
import argparse, datetime, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
T = json.load(open(os.path.join(AN, "d4a08w23c_forms.json"), encoding="utf-8"))
C = T["cuts"]["8"]
T5 = json.load(open(os.path.join(AN, "d4a05_tree3.json"), encoding="utf-8"))
PB, SB = T5["primary_branch"], T5["secondary_branch"]
CORE = [json.loads(l) for l in open(os.path.join(OUT, "room-forms-D4a08.jsonl"), encoding="utf-8") if json.loads(l)["id"] == "K"][0]["members"]
P7, P8 = {}, {}
for f, d in (("room-forms-D4a07.jsonl", P7), ("room-forms-D4a08.jsonl", P8)):
    for l in open(os.path.join(OUT, f), encoding="utf-8"):
        r = json.loads(l)
        if r.get("level") == "form":
            for s in r["members"]:
                d[s] = r["id"]
NAMES = {
    "A": ("the design and its marking", "sure", "Collective representation in 98 per cent of the defining members' changes; recurs in every cut (D4a-05 E, D4a-06 G, D4a-07 C, D4a-08 E)."),
    "B": ("keeping, with traded help and carrying on", "sure of keeping; not of its other parts", "Repair work in 74 per cent; reciprocity and transition in about two fifths. Keeping recurs in every cut; the help and carrying on joined it here."),
    "C": ("the work behind the thread: the chat and the scripts", "not sure", "Backstage decision-making in 49 per cent, workarounds in 37: two practices, a chat and machine hands. Scripts were a clean form on the changes alone (D4a-07 D, 93 per cent); here they join the chat. I would split C at the level below."),
    "D": ("the sub's April Fools play", "sure it is a pole; it is the frame beside the canvas work", "Keying in 71 per cent; the frame holds 49 per cent of their codes against 12 in the average room. The play is the sub's own business beside the canvas; I would set it apart from the forms of canvas organizing, as the account sets the frame apart."),
    "E": ("the terms between neighbours", "sure", "Negotiated order in 90 per cent, repair work in 66; recurs in every cut (D4a-05 A, D4a-06 A, D4a-07 G, D4a-08 C); changes and codes agree."),
    "F": ("the plan made and announced: templates, the work marked done, calls", "not sure", "Standardization of output in 72 per cent, completion ritual in 74, mobilization in 51. A new pole: it did not stand in the earlier cuts."),
    "G": ("the spot: lost, chosen or yielded, and building again", "sure", "Territoriality in 94 per cent; recurs in the change cuts (D4a-05 C, D4a-06 E, D4a-07 F), dissolved when codes weighed equally, and returns here. The narrow form F09 (moving, then building again) lives here."),
    "H": ("raiding as the work", "sure it is a pattern; not that it holds every raiding room", "Attack calls among the changes of 96 per cent of the defining members, workarounds in 64. It holds 9 of the 21 rooms with a quarter or more of their changes on attack calls; the other 12 sit where the rest of their mix lies. The raiding core holds together beyond chance in every space tested (D4a-07 p 0.001; D4a-08 p 0.009). At seven forms H merges into C."),
}
ap = argparse.ArgumentParser()
ap.add_argument("--what", required=True)
ap.add_argument("--form")
ap.add_argument("--move-no", type=int)
ap.add_argument("--table")
ap.add_argument("template", nargs="?")
a = ap.parse_args()
FORMS = sorted(C["forms"])


def members(f):
    return sorted((s for s, x in C["rooms"].items() if x == f), key=str.lower)


if a.what == "forms":
    for f in FORMS:
        v = C["forms"][f]
        print(json.dumps({"id": f, "level": "form", "k": 8, "weights": {"changes": T["w_changes"], "codes": round(1 - T["w_changes"], 4)},
                          "name": NAMES[f][0], "how_sure": NAMES[f][1], "why": NAMES[f][2], "ward_n": v["ward_n"], "n": v["placed"],
                          "change_signature_T4": v["sig"], "codes_over": v["codes_over"], "median_codes": v["median_codes"],
                          "median_changes": v["median_changes"], "members": members(f), "since": "D4a-08",
                          "status": "the cut I would stand behind; put to J; the leg is open"}, ensure_ascii=False))
    print(json.dumps({"id": "K", "level": "core", "n": len(CORE), "name": "the core: rooms with no selected change", "members": CORE}, ensure_ascii=False))

if a.what == "tsv":
    print("\t".join(["room", "form", "form_name", "D4a08_form_k5", "D4a07_form", "primary_branch", "secondary_branches"]))
    rows = [[s, f, NAMES[f][0], P8.get(s, ""), P7.get(s, ""), PB.get(s, ""), ",".join(SB.get(s, []))] for s, f in C["rooms"].items()]
    rows += [[s, "K", "the core: rooms with no selected change", "K", "K", PB.get(s, ""), ",".join(SB.get(s, []))] for s in CORE]
    for row in sorted(rows, key=lambda x: x[0].lower()):
        print("\t".join(row))

if a.what == "tier":
    f = a.form
    print(json.dumps({"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "stage": "D4", "leg": "D4a-08",
                      "tier": "room-form", "id": "D4a08b-" + f, "move": "merging", "event": "room form named", "move_no": a.move_no,
                      "name": NAMES[f][0],
                      "why": ("one of the 8 forms of the Ward cut on the 558 defining rooms, the change block at two thirds and the code block "
                              "at one third of the total variance; the cut the analyst stands behind (J, 21:24 Berlin); the count chosen on "
                              "substance (every form with a change signature, no middle; raiding apart), not by the gap"),
                      "ground": "the rooms' selected changes and coded concepts; no canvas field, verdict or branch",
                      "parent": None, "members_n": C["forms"][f]["placed"]}, ensure_ascii=False))


def md(table):
    out = []
    if table == "weights":
        out.append("| cut | weight of the changes | forms | share of the change structure explained | share of the code structure explained | adjusted Rand against D4a-07 | against D4a-08 (five forms) |")
        out.append("|---|---|---|---|---|---|---|")
        for fn, label in (("d4a08w1b", "changes only (D4a-07's cut)"), ("d4a08w23c", "changes two thirds"), ("d4a08w05b", "equal (D4a-08)"), ("d4a08w0b", "codes only")):
            X = json.load(open(os.path.join(AN, fn + "_forms.json"), encoding="utf-8"))
            for k in ("5", "8"):
                if k in X["cuts"]:
                    c = X["cuts"][k]
                    out.append("| %s | %.2f | %s | %.3f | %.3f | %.3f | %.3f |" % (label, X["w_changes"], k, c["between_share"]["changes"],
                                                                         c["between_share"]["codes"], c["ari_D4a07"], c["ari_D4a08"]))
    if table == "count":
        out.append("| k | gap (lifetime of the cut) | real stability | sizes ratio | change structure | code structure |")
        out.append("|---|---|---|---|---|---|")
        for k in sorted(T["cuts"], key=int):
            c = T["cuts"][k]
            out.append("| %s | %.4f | %.4f | %.2f | %.3f | %.3f |" % (k, T["gap"][k], T["stability_real"][k], c["ratio"], c["between_share"]["changes"], c["between_share"]["codes"]))
    if table == "forms":
        out.append("| form | the pattern | how sure | defining rooms | placed | change signature (times the population; members holding it) | codes most above the average room | median coded concepts |")
        out.append("|---|---|---|---|---|---|---|---|")
        for f in FORMS:
            v = C["forms"][f]
            sig = "; ".join("%s (%.1f; %.0f%%)" % (d["name"], d["ratio"], 100 * d["presence"]) for d in v["sig"][:3])
            cod = "; ".join("%s (%.3f against %.3f)" % (d["name"], d["share"], d["mean"]) for d in v["codes_over"])
            out.append("| %s | %s | %s | %d | %d | %s | %s | %g |" % (f, NAMES[f][0], NAMES[f][1], v["ward_n"], v["placed"], sig, cod, v["median_codes"]))
        out.append("| K | the core: no selected change | | | %d | | | |" % len(CORE))
    if table == "why":
        for f in FORMS:
            out.append("- **%s, %s (%s).** %s" % (f, NAMES[f][0], NAMES[f][1], NAMES[f][2]))
    if table == "cross":
        out.append("| D4a-07 form | rooms | %s |" % " | ".join(FORMS))
        out.append("|---|---|%s" % ("---|" * len(FORMS)))
        for f7, row in sorted(C["cross_D4a07"].items()):
            out.append("| %s | %d | %s |" % (f7, sum(row.values()), " | ".join(str(row.get(x, 0)) for x in FORMS)))
    if table == "sets":
        out.append("| set | %s |" % " | ".join(FORMS))
        out.append("|---|%s" % ("---|" * len(FORMS)))
        out.append("| raiding core (21 rooms) | %s |" % " | ".join(str(C["raiding_by_form"].get(x, 0)) for x in FORMS))
        out.append("| takeover (F02, 33 rooms) | %s |" % " | ".join(str(C["takeover_by_form"].get(x, 0)) for x in FORMS))
    if table == "rooms":
        out.append("| room | form | D4a-08 (five forms) | D4a-07 | primary branch |")
        out.append("|---|---|---|---|---|")
        rows = [(s, f, P8.get(s, ""), P7.get(s, ""), PB.get(s, "")) for s, f in C["rooms"].items()]
        rows += [(s, "K", "K", "K", PB.get(s, "")) for s in CORE]
        for row in sorted(rows, key=lambda x: x[0].lower()):
            out.append("| %s |" % " | ".join(row))
    return "\n".join(out)


if a.what == "md":
    print(md(a.table))
if a.what == "fill":
    for line in open(a.template, encoding="utf-8").read().split("\n"):
        m = re.fullmatch(r"\{\{TABLE:([a-z]+)\}\}", line.strip())
        print(md(m.group(1)) if m else line)
