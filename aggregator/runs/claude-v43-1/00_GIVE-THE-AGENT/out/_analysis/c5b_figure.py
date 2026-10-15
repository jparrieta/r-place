#!/usr/bin/env python3
"""C5b: write out/figure-C5.md, the figure as text (stage C5 section 10), from model/elements.jsonl,
model/arrows.jsonl and propositions.jsonl, so that every id, count, tag and instance is read and not typed. The short
names are my glosses of each element's statement, as account.md uses them; the script refuses one whose id is not a
standing element. Re-emitted at C5d from the model that survives the readers.

    python3 out/_analysis/c5b_figure.py            print the text and its size
    python3 out/_analysis/c5b_figure.py --write    write out/figure-C5.md
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip()]


els = {e["id"]: e for e in jl("model/elements.jsonl")}
arrows = [a for a in jl("model/arrows.jsonl") if a.get("in_model")]
props = jl("propositions.jsonl")
tag = {a: p["id"] for p in props for a in p.get("rests_on") or []}
theorised = sorted({a for p in props if p.get("theorised") for a in p.get("rests_on") or []})
COLUMNS = [
    ("Conditions (left)", [("K01", "the April Fools play, beside the work"), ("K02", "doubt about hands")]),
    ("Mediators, named for what members do (middle)", [
        ("R01", "the starter"), ("P01", "calls for hands"), ("P02", "settling what to make"),
        ("P03", "building and reporting the mark"), ("P04", "templates"), ("P05", "upkeep"),
        ("P07", "sparing a neighbour's work"), ("P08", "border talk and deals"), ("P09", "attack calls"),
        ("P10", "the move"), ("P14", "scripts and spare accounts"), ("P15", "the bare answer"),
        ("P16", "help between rooms"), ("P17", "coalitions"), ("P18", "contest in talk"),
        ("P20", "the host sub's line")]),
    ("What follows (right)", [("P11", "celebration"), ("P12", "records (after hour 73, curation of the record)"),
                              ("P13", "carrying the work on")]),
]
name = {}
for _, boxes in COLUMNS:
    for i, n in boxes:
        if els.get(i, {}).get("status") != "standing":
            sys.exit("%s is not a standing element" % i)
        name[i] = n
drawn_ids = {a["from"] for a in arrows} | {a["to"] for a in arrows}
missing = sorted(drawn_ids - set(name))
if missing:
    sys.exit("arrows touch elements with no box: %s" % missing)


def count(a):
    c = a.get("counts")
    if not c:
        return "a transition in %d rooms; no order count" % len(a.get("subs") or [])
    beat = "beats its null" if c["share"] > c["null_p95"] else "does not beat its null"
    return "%d of %d rooms, %s" % (c["holds"], c["both"], beat)


def instance(a):
    for t in a.get("support_transition") or []:
        if str(t.get("audit", "")).startswith("pass") and t.get("codes") and t.get("hours"):
            return "%s/%s to %s (h%.2f to h%.2f)" % (t["sub"], t["codes"][0], t["codes"][-1], t["hours"][0], t["hours"][-1])
    for s in a.get("support") or []:
        if s.get("quote"):
            return "%s/%s" % (s["sub"], s["code"])
    return None


L = ["# The figure, as text (C5b draft)", "",
     "Target length: about 900 words. The figure the readers see at C5b. It is drawn again at C5d from the model that "
     "survives the readers. Every box and arrow is named by id. Each arrow carries the proposition (N01 to N09, in "
     "`propositions.jsonl`) that carries it; an arrow no proposition carries is not drawn.", "",
     "## The boxes, in three columns", ""]
for col, boxes in COLUMNS:
    L.append("- **%s:** %s." % (col, "; ".join("%s %s" % (i, n) for i, n in boxes)))
L += ["- **The terminus:** a vertical bar at hour 73 crosses the right column. Placement stopped there for every room. "
      "P11 and P12 sit on both sides of it; P13 and the curation of the record sit after it.",
      "- **Beside the figure, not boxes:** the claims C01 (a decided element of order, in 46 of 705 rooms; F-006) and "
      "C02 (a tie from before the canvas names the rival; untested for order). They carry no arrow.",
      "- **K01 is drawn as a box with no arrow.** The model claims no effect of the April Fools play; F-009 found that "
      "it did not delay the work.", "",
      "## The arrows", "",
      "Each line gives the arrow, its proposition, its strength, its count (rooms where the order holds, of the rooms "
      "carrying both elements, against a null of 500 shuffles within each room) and one instance from its support: "
      "the first transition the audit passed, by room, codes and hours.", ""]
for a in arrows:
    if a["id"] not in tag:
        continue
    th = " Theorised." if a["id"] in theorised else ""
    L.append("- **%s** %s to %s, %s; %s; %s. Instance: %s.%s" % (
        a["id"], a["from"], a["to"], tag[a["id"]], a.get("strength"), count(a), instance(a) or "none", th))
L += ["", "## Two drawings", "",
      "- **Drawing 1, with the theorised arrows:** all %d arrows above." % sum(1 for a in arrows if a["id"] in tag),
      "- **Drawing 2, without them:** the same, less %s. P02, P04 and P15 then stand with no arrow." % " and ".join(theorised),
      "- **Loops:** none is drawn. No room's dated record runs a whole cycle, and no counted arrow runs from the move "
      "(P10) back to building (P03).", "",
      "## What the figure leaves out", "",
      "It leaves out the field's tentative arrow from P08 to P21, which no proposition carries, and the tentative elements "
      "P21 and P22. It leaves out the candidates P06, R02, K03, K04 and P19. It does not draw the third-order themes "
      "the model does not use, or the rooms the account names as beyond its reach. The left column is near empty: "
      "the model is mostly mediators and what follows them.", ""]
text = "\n".join(L)
print(text)
print("[%d bytes, %d words]" % (len(text.encode("utf-8")), len(text.split())))
if "--write" in sys.argv:
    open(os.path.join(OUT, "figure-C5.md"), "w", encoding="utf-8").write(text)
    print("wrote out/figure-C5.md")
