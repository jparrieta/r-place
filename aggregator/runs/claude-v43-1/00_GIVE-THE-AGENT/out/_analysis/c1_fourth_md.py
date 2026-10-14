#!/usr/bin/env python3
"""C1 section 8: write out/fourth/fourth.md from out/fourth/fourth.jsonl, the specs' unpicked list, scheme_v2.jsonl
and assignments_final.jsonl. Every fourth-order theme with its declaration, source, gloss, what would disconfirm it,
its prose and its members by name; the third-order themes no fourth-order theme picks up at the foot. Refuses to
overwrite; supersede with a new name.

    python3 out/_analysis/c1_fourth_md.py [--out fourth/fourth.md]
"""
import argparse, collections, json, os, sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jl(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


ap = argparse.ArgumentParser()
ap.add_argument("--out", default=os.path.join("fourth", "fourth.md"))
a = ap.parse_args()
dest = os.path.join(OUT, a.out)
if os.path.exists(dest):
    sys.exit("%s exists; supersede it with a new name" % a.out)

t4 = jl(os.path.join("fourth", "fourth.jsonl"))
scheme = dict((t["id"], t) for t in jl("scheme_v2.jsonl"))
specs = json.load(open(os.path.join(OUT, "_analysis", "c1_t4_specs.json"), encoding="utf-8"))
rows = jl("assignments_final.jsonl")
lines_of, rooms_of = collections.Counter(), collections.defaultdict(set)
reach_lines, reach_rooms = collections.Counter(), collections.defaultdict(set)
owner = dict((m, r["id"]) for r in t4 for m in r["members"])
for r in rows:
    th = r.get("third_order") or []
    for t in th:
        lines_of[t] += 1
        rooms_of[t].add(r["sub"])
    for f in set(owner[t] for t in th if t in owner):
        reach_lines[f] += 1
        reach_rooms[f].add(r["sub"])
unpicked = sorted(set(scheme) - set(owner))

L = ["# Fourth-order themes, stage C1 (cut at C1a-10)", "",
     "These are the fourth-order themes of stage C1, section 8: named groups of third-order themes, each a construct "
     "from the moment it was cut. They partition the third-order tier of `scheme_v2.jsonl`: each third-order theme "
     "sits in one fourth-order theme, and a second-order theme reaches two only through its own placements (rule 0). "
     "The lines are in `fourth/fourth.jsonl`; each cut is a line in `tier_history.jsonl` (tier fourth, event created, "
     "move merging or relating), a move line in the diary and a snap. The specs, and the reasons for each bundle, are "
     "in `out/_analysis/c1_t4_specs.json`.", "",
     "The stories are provisional. They are the structure stage C2 starts from, and C2 may change any of them. No "
     "number was set: the material carries %d constructs over %d of the %d third-order themes, and the diary says why. "
     "Every borrowed or adapted source is recalled, since only the method shelf is held at C1; stage C3 checks each "
     "against a text and verifies or withdraws it. The form-pass findings in `form_pass-C1.md` are a tier of their "
     "own; they are not members of any fourth-order theme." % (len(t4), len(owner), len(scheme)), "",
     "The next table lists each fourth-order theme with its declaration, its move, the number of third-order themes "
     "it holds, and the placement lines and rooms whose second-order themes reach it through any of their placed "
     "themes. The reach is description, not a share: a line placed on two fourth-order themes is counted under each.",
     "", "| id | name | declared | move | third-order themes | lines reached | rooms reached |",
     "|---|---|---|---|---|---|---|"]
for r in t4:
    L.append("| %s | %s | %s | %s | %d | %d | %d |" % (r["id"], r["name"], r["declared"], r["move"], len(r["members"]),
                                                       reach_lines[r["id"]], len(reach_rooms[r["id"]])))
L.append("")
for r in t4:
    L.append("## %s. %s" % (r["id"], r["name"]))
    L.append("")
    L.append("- **Gloss.** \"%s\" [%s]" % (r["gloss"], r["gloss_from"]))
    dec = r["declared"]
    if dec == "coined":
        L.append("- **Declared.** Coined, this corpus's. A reader may mistake it for: %s" % r.get("mistaken_for", ""))
    else:
        L.append("- **Declared.** %s, recalled (stage C3 verifies or withdraws). Source: %s." % (dec.capitalize(), r["source"]))
        if dec == "adapted":
            L.append("- **What changed, and why.** %s" % r.get("adaptation", ""))
    L.append("- **Would be disconfirmed by.** %s" % r["disconfirm"])
    L.append("- **Move.** %s (Grodal, Anteby and Holm)." % r["move"].capitalize())
    L.append("")
    L.append(r["prose"])
    L.append("")
    L.append("Members (placement lines, rooms):")
    L.append("")
    for m in r["members"]:
        s = scheme.get(m) or {}
        L.append("- %s %s%s (%d, %d)" % (m, s.get("name", ""), ", rare" if s.get("tier") == "rare" else "",
                                        lines_of[m], len(rooms_of[m])))
    L.append("")
L.append("## Third-order themes no fourth-order theme picks up")
L.append("")
L.append("They are listed, not gathered into a catch-all (section 8).")
L.append("")
for m in unpicked:
    s = scheme.get(m) or {}
    L.append("- %s %s%s (%d, %d). %s" % (m, s.get("name", ""), ", rare" if s.get("tier") == "rare" else "",
                                        lines_of[m], len(rooms_of[m]), specs.get("unpicked", {}).get(m, "")))
L.append("")
os.makedirs(os.path.dirname(dest), exist_ok=True)
open(dest, "w", encoding="utf-8").write("\n".join(L))
print("wrote %s: %d fourth-order themes, %d third-order themes picked, %d unpicked (%s); %d words" % (
    a.out, len(t4), len(owner), len(unpicked), ", ".join(unpicked), len(" ".join(L).split())))
