#!/usr/bin/env python3
"""Stage C4: write out/model-C4.md, a whole file superseding model-C3.md (rule 18). It is model-C3.md with the stage C4
changes written in: a section saying what stage C4 changed; the closure sentence bounded; two disagreements printed
beside F-006 and A04; the limit of dating by the hour of a post; and the tentative entries from the field, read from
model/elements.jsonl and model/arrows.jsonl. Every replaced passage must be found exactly once. Refuses to overwrite an
existing model-C4.md unless --replace is given.

    python3 out/_analysis/c4_model_md.py [--replace]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
SRC = os.path.join(OUT, "model-C3.md")
DEST = os.path.join(OUT, "model-C4.md")
if os.path.exists(DEST) and "--replace" not in sys.argv:
    sys.exit("out/model-C4.md exists; pass --replace to regenerate it whole")
txt = open(SRC, encoding="utf-8").read()
E = [r for r in (json.loads(l) for l in open(os.path.join(OUT, "model", "elements.jsonl"), encoding="utf-8"))
     if r.get("origin") == "from-field"]
A = [r for r in (json.loads(l) for l in open(os.path.join(OUT, "model", "arrows.jsonl"), encoding="utf-8"))
     if r.get("origin") == "from-field"]
if sorted(r["id"] for r in E + A) != ["A21", "P21", "P22"]:
    sys.exit("the from-field entries are not P21, P22 and A21")

C4 = """## What stage C4 changed

This file supersedes `model-C3.md` whole (rule 18). Stage C4 read the model against the field. The field is the model of the event that a separate analyst built from r/place (`field/model.md`), with that analyst's check of my model (`field/check.md`). What each comparison found is in `field-C4.md`. Stage C4 changed:
- **Three tentative entries from the field.** P21: members dispute who may commit the room to an agreement with other rooms. A21: an arrow from deals and truces to that dispute. P22: after placement ends, members contest which version of the canvas and of the event is kept. Each is `origin: from-field` and `status: tentative`, with the field's threads and items. None is counted. None is in the standing count. Stage D asks every room about each. They are listed in their own section, before the theorised arrows.
- **One sentence bounded.** The model said that a room's organizing for this canvas is over at hour 73. Placement on the canvas ends at hour 73. Organizing around its records and copies goes on (`field-C4.md`, list 3, item 1).
- **Two disagreements printed beside the model.** Beside F-006 and C01, the field shows authority sought between groups, which is not decided order placed. Beside A04, the field shows one early buffer negotiated in r/place.
- **One limit written in.** An order count dates each concept by the hour of its post, and a retrospective report does not date the act it reports.
- **Two construct declarations amended** (`structure-C4.md`). Standardization of output no longer says that a template replaces argument or is the strongest coordination at scale. Boundary work no longer says that every room existed before the canvas.

No standing element or arrow was added, bounded, demoted or withdrawn. No strength or count changed. No tier was recut. No finding changed. The story is not rewritten here; that is stage C5's.

The text below is stage C3's, with these changes written into it.

"""


def entry(r):
    if r["id"].startswith("A"):
        head = "- **%s, %s to %s (tentative, from the field).** Connection: %s. Mechanism: %s Fails if: %s" % (
            r["id"], r["from"], r["to"], r["connection"], r["mechanism"], r["mechanism_fails_if"])
        side = r.get("room_side") or []
    else:
        head = "- **%s, %s (tentative, from the field).** %s Range: %s. Sits under %s." % (
            r["id"], r["kind"], r["statement"], r["range"], ", ".join(r["tier"]))
        side = (r.get("evidence") or {}).get("codes") or []
    return "%s Level: %s. The field's mark: %s. Field support: %s. Room side found so far: %s." % (
        head, r["level"], r["field_mark"], "; ".join(r["field_support"]), ", ".join(side) or "none")


TENT = ("## Tentative entries from the field (stage C4)\n\nThese entries came from the field, not from my rooms. "
        "Each is a hypothesis. Stage D sends it to every room, marked tentative and with no word of where it came "
        "from, and each room says from its own record whether it shows its side, contradicts it, or says nothing. "
        "None is counted, and none enters the counts above.\n\n" + "\n".join(entry(r) for r in E + A) + "\n\n")

REPL = [
    ("# The model, stage C3: pass 5 read against the literature\n", "# The model, stage C4: read against the field\n"),
    ("## What stage C3 changed\n", C4 + "## What stage C3 changed\n"),
    ("Its organizing for this canvas is over.",
     "Its organizing of placement on this canvas is over. Organizing around the canvas's records and copies goes on "
     "after it (P12, P13; the tentative P22; `field-C4.md`, list 3, item 1).\n- **Dating by the hour of the post "
     "(C4).** Each order count dates a concept by the hour of its post. A retrospective report posted late does not "
     "date the act it reports. Because the counts compare first concepts, such a report moves an element's first hour "
     "only when it is the room's only concept of that element (`field-C4.md`, list 3, item 6)."),
    ("After it, a room can only celebrate, record, carry on, and keep up its rivalries in talk.",
     "After it, a room can celebrate, record, carry on, keep up its rivalries in talk, and work on copies of the "
     "canvas (the tentative P22)."),
    ("(F-006, bounded at C3a, prompted by O'Mahony and Ferraro 2007).",
     "(F-006, bounded at C3a, prompted by O'Mahony and Ferraro 2007). The field shows members asking who may commit a "
     "group, between large factions and after the close. That is authority sought, not decided order placed, and "
     "F-006 stands (`field-C4.md`, list 3, item 4; the tentative P21)."),
    ("switzerland's own order holds: first upkeep h5.38, first treaty talk h18.62.",
     "switzerland's own order holds: first upkeep h5.38, first treaty talk h18.62. **The field (C4):** one buffer was "
     "negotiated in r/place at hours 5.00 to 7.08 (`62mg1j`). One episode does not test this count, and the bound for "
     "neighbours present from a room's first post already covers it (`field-C4.md`, list 3, item 5)."),
    ("## Theorised arrows, and the model with and without them\n",
     TENT + "## Theorised arrows, and the model with and without them\n"),
]
for old, new in REPL:
    n = txt.count(old)
    if n != 1:
        sys.exit("passage found %d times, not once: %r" % (n, old[:80]))
    txt = txt.replace(old, new)
with open(DEST, "w", encoding="utf-8") as f:
    f.write(txt)
print("model-C4.md written: %d words (model-C3.md %d)" % (len(txt.split()), len(open(SRC, encoding="utf-8").read().split())))
