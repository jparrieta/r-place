#!/usr/bin/env python3
"""C4a, stage C4 section 2 (a change the field forces follows stage C3 section 6): amend the `prose` of two
fourth-order construct blocks where the field's check shows a sentence that the field and my own rooms contradict.
fourth/fourth.jsonl is edited in place (its `prose` field only); each superseded line goes to tier_history.jsonl as
`was`, with the move, the field items and one clause of reason. Membership, names and the third-order tier do not
change. Refuses to run if either theme already has a C4a tier_history line, or if an old sentence is not found.

    python3 out/_analysis/c4_construct_amend.py
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
FP = os.path.join(OUT, "fourth", "fourth.jsonl")
TH = os.path.join(OUT, "tier_history.jsonl")
# theme: [(old sentence, new sentence)], field items, rooms' items, reason
EDIT = {
    "T4-008": (
        [("an object that settles in advance what each pixel should be, and so replaces argument with reference.",
          "an object that settles in advance what each pixel should be, and so gives an argument something to point "
          "to."),
         ("The standard is the room's strongest coordination at scale, and also the point where scripts can take over "
          "the placing.",
          "A template does not make placers follow it. Members still stray, follow another version, or undo planned "
          "work they take for vandalism, and the template itself can be wrong. The template is also the point where "
          "scripts can take over the placing.")],
        ["r/place 62mg1j c60185", "r/place 6384jy c3580447", "r/place 6384jy c3580448"],
        ["2007scape:c0230", "AvoArmy:c0228", "criticalrole:c0049"],
        "the field shows a design offered as easy to follow that, by its contributor's later account, members failed "
        "to follow until they organised a venue and revised the design; my rooms show strays, a wrong template and "
        "planned work undone; no test ranked the template against other coordination, so 'strongest at scale' and "
        "'replaces argument' claimed more than the evidence holds"),
    "T4-002": (
        [("Every room was a standing community before the canvas opened, with its own subject and rules, and the "
          "canvas arrived as a flood of posts about something else.",
          "Most rooms were standing communities before the canvas opened, with their own subject and rules, and the "
          "canvas arrived as a flood of posts about something else. Some were not: 78 of 705 rooms have no posts in "
          "the week before the canvas, and members opened side subs for the canvas.")],
        ["r/place 62p7xw c570391"],
        [],
        "the field shows a member reporting that they started a new sub for the canvas; my own model already counts "
        "78 of 705 rooms with no posts in the week before the canvas, so the universal sentence contradicted my model "
        "as well as the field"),
}
hist = [json.loads(l) for l in open(TH, encoding="utf-8") if l.strip()]
if any(h.get("leg") == LEG and h.get("id") in EDIT for h in hist):
    sys.exit("a %s tier_history line exists for %s; not written again" % (LEG, ", ".join(EDIT)))
rows = [json.loads(l) for l in open(FP, encoding="utf-8") if l.strip()]
new_hist = []
for r in rows:
    if r["id"] not in EDIT:
        continue
    pairs, field, rooms, why = EDIT[r["id"]]
    was = dict(r)
    prose = r["prose"]
    for old, new in pairs:
        if prose.count(old) != 1:
            sys.exit("%s: old sentence not found exactly once: %s" % (r["id"], old[:60]))
        prose = prose.replace(old, new)
    r["prose"] = prose
    new_hist.append({"t": T, "stage": "C4", "leg": LEG, "tier": "fourth", "id": r["id"],
                     "move": "relating or contrasting", "event": "construct_amended", "was": was,
                     "now": [{"id": r["id"], "prose": r["prose"]}], "why": why, "field_support": field,
                     "rooms": rooms, "prompted_by": "field/check.md (stage C4)"})
if len(new_hist) != len(EDIT):
    sys.exit("not every theme was found")
with open(FP, "w", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
with open(TH, "a", encoding="utf-8") as f:
    f.write("".join(json.dumps(h, ensure_ascii=False) + "\n" for h in new_hist))
print("amended: %s; tier_history lines appended: %d" % (", ".join(h["id"] for h in new_hist), len(new_hist)))
