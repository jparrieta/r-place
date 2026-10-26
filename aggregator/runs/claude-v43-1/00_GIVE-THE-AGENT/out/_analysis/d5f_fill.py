#!/usr/bin/env python3
"""D5, room-form accounts: fill a template's {{PLACEHOLDERS}} from the leg's files (facts, model, lines, split, restrict
sort, tree-D4.md's held proposals, the model's statements). Prints the filled account to stdout.

    python3 out/_analysis/d5f_fill.py --form A --template out/_analysis/d5a36_template.md > out/room-form-A-account.md
"""
import argparse, collections, json, os, re, sys

ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
ap.add_argument("--template", required=True)
a = ap.parse_args()
sys.argv = [sys.argv[0]]
AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402

tag = {"A": "d5a36", "B": "d5a37", "C": "d5a38", "D": "d5a39", "E": "d5a40", "F": "d5a41"}[a.form]


def J(name):
    return json.load(open(os.path.join(AN, "%s_%s.json" % (tag, name)), encoding="utf-8"))


facts, model, split, rs = J("facts"), J("model"), J("split"), J("restrict_sorted")
els = {r["id"]: r for r in E.jl(os.path.join(OUT, "model", "elements.jsonl"))}
arrows = {r["id"]: r for r in E.jl(os.path.join(OUT, "model", "arrows.jsonl"))}
nd = facts["n_def"]
P = {}

inst = sorted([r for r in model["rows"] if r["op"] == "instantiate" and r["form_share"] >= 0.8], key=lambda r: (-r["form"], r["element"]))
P["INSTANTIATED"] = "\n".join('- %s (%d of %d; %d per cent of the 558): "%s"' % (r["element"], r["form"], nd, round(100 * r["pop_share"]),
                                                                                els[r["element"]]["statement"] if r["element"] in els else
                                                                                "%s to %s" % (arrows[r["element"]]["from"], arrows[r["element"]]["to"]))
                              for r in inst)

rows = sorted([r for r in facts["elements"] if r["form_def"] >= 14 and (r["ratio"] or 0) >= 1.2], key=lambda r: -r["ratio"])
P["ELEMENTS"] = "\n".join(["| element or arrow | op | defining members with a line | share | share among the 558 | ratio |",
                           "|---|---|---|---|---|---|"] +
                          ["| %s | %s | %d | %.3f | %.3f | %.2f |" % (r["element"], r["op"], r["form_def"], r["form_share"], r["pop_share"], r["ratio"])
                           for r in rows])
contra = [r for r in facts["elements"] if r["op"] == "contradict"]
P["CONTRADICT"] = ("%d defining members hold a contradict line (%s)" % (sum(r["form_def"] for r in contra),
                   ", ".join("%s %d" % (r["element"], r["form_def"]) for r in contra if r["form_def"])) if any(r["form_def"] for r in contra)
                   else "No defining member holds a contradict line")

by = rs["by_arrow"]
P["RESTRICTS"] = "\n".join(["| arrow | from, to | lines | the arrow fails here | the record cannot show it | both | neither |",
                            "|---|---|---|---|---|---|---|"] +
                           ["| %s | %s, %s | %d | %d | %d | %d | %d |" % (k, arrows[k]["from"], arrows[k]["to"], sum(v.values()), v.get("F", 0), v.get("R", 0),
                                                                    v.get("B", 0), v.get("N", 0)) for k, v in by.items()] +
                           ["| all | | %d | %d | %d | %d | %d |" % (rs["lines"], rs["total"].get("F", 0), rs["total"].get("R", 0),
                                                                   rs["total"].get("B", 0), rs["total"].get("N", 0))])


def rn(xs):
    return ", ".join("r/" + s for s in sorted(xs, key=str.lower))


mem = E.FORMS[a.form]["members"]
P["UNRESOLVED"] = rn(mem)

tree = open(os.path.join(OUT, "tree-D4.md"), encoding="utf-8").read().splitlines()
held = [l for l in tree if l.startswith("- **P05, move 198") or l.startswith("- **A11, move 199")]
assert len(held) == 2
text = "\n".join(held)
p05_rooms = [x.strip() for x in text[text.find("Rooms: ") + 7:text.find(". Lines:")].split(",")]
a11 = held[1]
a11_rooms = [x.strip() for x in a11[a11.find("Rooms (the talk-only rooms of the failure clause):") + 50:a11.find(". Lines (")].split(",")]
inp, ina = sorted(set(mem) & set(p05_rooms), key=str.lower), sorted(set(mem) & set(a11_rooms), key=str.lower)
P["HELD"] = text + "\n\n" + ("%s of form %s's rooms %s among the rooms of the P05 proposal (%s). " % (len(inp), a.form, "is" if len(inp) == 1 else "are", rn(inp)) if inp
                             else "No room of form %s is among the rooms of the P05 proposal. " % a.form) + \
    ("%d %s among the talk-only rooms of the A11 proposal's failure clause: %s." % (len(ina), "is" if len(ina) == 1 else "are", rn(ina)) if ina
     else "None is among the talk-only rooms of the A11 proposal's failure clause.")

P["ARROWS"] = "\n".join("- %s (%s to %s): %d datings, expected %.3f; not-testable-here" % (x["arrow"], x["from"], x["to"], x["subs"], x["expected"])
                        if x["expected"] < 1 else "- %s (%s to %s): %d datings, expected %.3f; testable" % (x["arrow"], x["from"], x["to"], x["subs"], x["expected"])
                        for x in sorted(facts["arrows"], key=lambda x: int(x["arrow"][1:])))
P["ARROW_MAX"] = "%.3f" % max(x["expected"] for x in facts["arrows"])
P["ARROW_MIN"] = "%.3f" % min(x["expected"] for x in facts["arrows"])
P["IN_SUBS"] = "; ".join("r/%s (%s)" % (s, ", ".join(sorted((x["arrow"] for x in facts["arrows"] if s in x["members_in_subs"]), key=lambda z: int(z[1:]))))
                         for s in sorted({s for x in facts["arrows"] for s in x["members_in_subs"]}, key=str.lower)) or "none"
P["PROPS"] = "%s; the highest expectation among the arrows they rest on is %.3f" % (
    ", ".join(p["id"] for p in facts["propositions"]), max(p["max_expected"] for p in facts["propositions"]))

bt = sorted(facts["branches"], key=lambda b: (-b["ratio"], b["branch"]))
P["BRANCHES"] = "\n".join(["| branch | parent | name | rooms | in form %s (defining, thin, core) | share of the branch in the form | against the form's share of 705 |" % a.form,
                           "|---|---|---|---|---|---|---|"] +
                          ["| %s | %s | %s | %d | %d (%d, %d, %d) | %.3f | %.2f |" % (b["branch"], b["parent"] or "", b["name"], b["n"], b["in_form"], b["def"], b["thin"], b["core"],
                                                                                    b["share_in_form"], b["ratio"]) for b in bt])
nb = facts["no_branch"]
role = {x["sub"]: "thin" for x in facts["thin"]}
role.update({x["sub"]: "core" for x in facts["core"]})
P["NOBRANCH"] = "%d rooms (%d defining): %s" % (len(nb), facts["no_branch_def"], ", ".join("r/%s%s" % (s, " (%s)" % role[s] if s in role else "")
                                                                                         for s in sorted(nb, key=str.lower)))
P["THIN"] = ", ".join("r/%s (%d %s, %d concepts)" % (x["sub"], x["changes"], "change" if x["changes"] == 1 else "changes", x["codes"])
                      for x in sorted(facts["thin"], key=lambda x: x["sub"].lower()))
P["CORE"] = ", ".join("r/%s (%d %s; verdict %s)" % (x["sub"], x["codes"], "concept" if x["codes"] == 1 else "concepts", x["verdict"] or "unruled")
                      for x in sorted(facts["core"], key=lambda x: x["sub"].lower()))
P["THIN_LINES"] = "; ".join("%s %s %d (%s)" % (t["element"], t["op"], t["lines"], rn(t["rooms"])) for t in model["thin_lines"][:8])
P["NEARER"] = ", ".join("%s %d" % (k, v) for k, v in sorted(model["defining_nearer_other_centre"].items(), key=lambda x: -x[1]))
P["CENTRES"] = ", ".join("%s %.3f" % (k, v) for k, v in sorted(facts["centre_distances"].items(), key=lambda x: x[1]))

srows = []
for w in split["walk"]:
    for part, v in w["parts"].items():
        srows.append("| %s | %d | %s | %d | %d | %s | %s |" % (w["group"], w["splits_at_k"], part, v["defining"], v["all"],
                                                            "; ".join("%s (%.2f times the parent's share; %.3f of the part, %.3f of the other)" % (
                                                                x["name"], x["ratio_to_parent"], x["presence"], x["presence_other"]) for x in v["leans"][:3]) or "none",
                                                            "yes" if w["reads_as_split"] else "no"))
P["SPLIT"] = "\n".join(["| group | splits at k | part | defining rooms | all rooms | change columns the part leans to | reads as a split |",
                        "|---|---|---|---|---|---|---|"] + srows)
# the form's signature columns in each part of its first split
w0 = split["walk"][0] if split["walk"] else None
if w0:
    addr = {}
    tl = open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8").read().splitlines()
    hd = tl[0].split("\t")
    for line in tl[1:]:
        c = dict(zip(hd, line.split("\t")))
        addr[c["room"]] = (c["role"], c["address"].split("/")[0])
    cols = E.CCOLS["T4"]
    Pm = E.MCD["T4"] > 0
    out = []
    for part in w0["parts"]:
        idx = [E.IDX[s] for s, (rl, ad) in addr.items() if rl == "defining" and (ad == part or ad.startswith(part + "."))]
        out.append("%s: %s" % (part, ", ".join("%s %.3f" % (x["name"], float(Pm[idx, cols.index(x["col"])].mean())) for x in facts["signature_T4"])))
    P["SPLIT_SIG"] = "; ".join(out)
over = facts["themes_over"]
P["OVER"] = "\n".join("- **%s:** %.1f per cent of the defining members' coded concepts against %.1f per cent (ratio %.2f), in %d members." % (
    r["name"], 100 * r["form_share"], 100 * r["pop_share"], r["ratio"], r["members"]) for r in sorted(over, key=lambda r: -r["ratio"]))
P["UNDER"] = ", ".join("%s (ratio %.2f)" % (r["name"], r["ratio"]) for r in sorted(facts["themes_under"], key=lambda r: r["ratio"]))
P["VERDICTS"] = "composes %d, composes with residue %d, does not compose %d, cannot tell %d" % tuple(
    facts["verdicts_all"].get(k, 0) for k in ("composes", "composes-with-residue", "does-not-compose", "cannot-tell"))
P["VERDICTS_DEF"] = "composes %d, composes with residue %d, does not compose %d, cannot tell %d" % tuple(
    facts["verdicts_def"].get(k, 0) for k in ("composes", "composes-with-residue", "does-not-compose", "cannot-tell"))

t = open(a.template, encoding="utf-8").read()
missing = sorted(set(re.findall(r"\{\{([A-Z_]+)\}\}", t)) - set(P))
assert not missing, missing
for k, v in P.items():
    t = t.replace("{{%s}}" % k, v)
sys.stdout.write(t)
