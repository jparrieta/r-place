#!/usr/bin/env python3
"""C5d: write out/figure-C5.md, the final figure (stage C5 section 10), from model/elements.jsonl, model/arrows.jsonl,
propositions.jsonl and model/loops.jsonl as they stand after pass 10: the boxes in three columns with the terminus, every
drawn arrow with its proposition, strength, grounding, count and instance, two drawings (with and without the theorised
arrows) as text specification and as Mermaid, and what the figure leaves out. Supersedes c5b_figure.py's draft; every id,
count and instance is read, and the short names are my glosses of each element's statement.

    python3 out/_analysis/c5d_figure.py [--write]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip()]


els = {e["id"]: e for e in jl("model/elements.jsonl")}
arrows = [a for a in jl("model/arrows.jsonl") if a.get("in_model")]
props = jl("propositions.jsonl")
loops = jl("model/loops.jsonl") if os.path.exists(os.path.join(OUT, "model", "loops.jsonl")) else []
fourth = {r["id"]: r for r in jl("fourth/fourth.jsonl")}
tag = {a: p["id"] for p in props for a in p.get("rests_on") or []}
theorised = sorted({a for p in props if p.get("theorised") for a in p.get("rests_on") or []})
COLUMNS = [
    ("conditions", "Conditions (left)", [("K01", "the April Fools play, beside the work"), ("K02", "the room judges it has too few hands")]),
    ("mediators", "Mediators, named for what members do (middle)", [
        ("R01", "the starter"), ("P01", "calls for hands"), ("P02", "settling what the mark will show"),
        ("P03", "building and reporting the mark"), ("P04", "templates and coordinates"), ("P05", "upkeep"),
        ("P07", "sparing a neighbour's work"), ("P08", "border talk and deals"), ("P09", "attack calls"),
        ("P10", "the move"), ("P14", "scripts and spare accounts"), ("P15", "the bare answer"),
        ("P16", "help between rooms"), ("P17", "coalitions"), ("P18", "contest in talk"),
        ("P20", "the host sub's line")]),
    ("follows", "What follows (right)", [("P11", "celebration"), ("P12", "records (after hour 73, curation of the record)"),
                                         ("P13", "what the room keeps")]),
]
name = {}
for _, _, boxes in COLUMNS:
    for i, n in boxes:
        if els.get(i, {}).get("status") != "standing":
            sys.exit("%s is not a standing element" % i)
        name[i] = n
standing = sorted(i for i, e in els.items() if e["status"] == "standing")
drawn = [a for a in arrows if a["id"] in tag]
missing = sorted(({a["from"] for a in drawn} | {a["to"] for a in drawn}) - set(name))
if missing:
    sys.exit("arrows touch elements with no box: %s" % missing)


def count(a):
    c = a.get("counts")
    if not c:
        return "a transition in %d rooms; no order count" % len(a.get("subs") or [])
    beat = "beats its null" if c["share"] > c["null_p95"] else "does not beat its null"
    return "%d of %d rooms (%.3f; null 95th percentile %.3f), %s" % (c["holds"], c["both"], c["share"], c["null_p95"], beat)


def instance(a):
    for t in a.get("support_transition") or []:
        if str(t.get("audit", "")).startswith("pass") and t.get("codes") and t.get("hours") and not t.get("recut_note"):
            return "transition", "%s/%s to %s (h%.2f to h%.2f)" % (t["sub"], t["codes"][0], t["codes"][-1], t["hours"][0], t["hours"][-1])
    for s in a.get("support") or []:
        if s.get("quote"):
            return "quote", "%s/%s: '%s'" % (s["sub"], s["code"], s["quote"])
    return None, None


def mermaid(with_theorised):
    L = ["```mermaid", "flowchart LR"]
    for key, title, boxes in COLUMNS:
        L.append('  subgraph %s["%s"]' % (key, title.split(" (")[0]))
        for i, n in boxes:
            L.append('    %s["%s: %s"]' % (i, i, n))
        L.append("  end")
    L.append('  H73(["hour 73: placement stops for every room"])')
    L.append("  P11 --- H73")
    L.append("  H73 --- P12")
    for a in drawn:
        if not with_theorised and a["id"] in theorised:
            continue
        L.append('  %s -->|"%s %s"| %s' % (a["from"], a["id"], tag[a["id"]], a["to"]))
    L.append("```")
    return L


kinds = {a["id"]: instance(a)[0] for a in drawn}
n_tr = sum(1 for v in kinds.values() if v == "transition")
n_q = sum(1 for v in kinds.values() if v == "quote")
unused4 = [t for t in sorted(fourth) if not any(t in (e.get("tier") or []) for e in els.values() if e["status"] == "standing")]
L = ["# The figure (C5d, final)", "",
     "Target length: about 1,700 words with the drawings. The model as it stands after pass 10, drawn once with the "
     "theorised arrows and once without. `gen_views.py` also draws the model into `_views/figure-model.md` at every close. "
     "Every box and arrow is named by id. Each arrow carries the proposition (N01 to N09, in `propositions.jsonl`) that "
     "carries it. An arrow no proposition carries is not drawn.", "",
     "## The count at the top", "",
     "The figure shows all %d standing elements. Twenty-one are boxes: the 20 elements the arrows join, and K01, which "
     "carries no arrow. The two claims, C01 and C02, sit beside the figure. Section 4 set the count: the cuts left 23 "
     "standing elements, and 21 boxes in three columns can be taken in at one pass. The middle column is the widest, so "
     "the figure is a model of mediators, not a two-column lattice." % len(standing), "",
     "## The boxes, in three columns", ""]
for _, col, boxes in COLUMNS:
    L.append("- **%s:** %s." % (col, "; ".join("%s %s" % (i, n) for i, n in boxes)))
L += ["- **The terminus:** a bar at hour 73 crosses the right column. Placement stopped there for every room. P11 and P12 "
      "sit on both sides of it; P13 and the curation of the record sit near it and after it.",
      "- **Beside the figure, not boxes:** C01, a decided element of order, coded in 46 of 705 rooms (F-006); and C02, a "
      "tie from before the canvas that names the rival, untested for order (F-013). Neither carries an arrow.",
      "- **K01 is a box with no arrow.** The model claims no effect of the April Fools play; F-009's held-size test found "
      "no delay of the work.", "",
      "## The arrows", "",
      "Each line gives the arrow, its proposition, its strength, what it is grounded in, its count and one instance. The "
      "grounding is the coders' cited concepts read for order: the rooms where the first concept of one element comes "
      "before the first of the other, of the rooms carrying both, against a null of 500 shuffles within each room. A "
      "transition is a reply in the same thread, by another author, carrying the second element after the first. Of the "
      "%d arrows drawn, %d are shown by an audited transition and %d by a quote." % (len(drawn), n_tr, n_q), ""]
for a in drawn:
    k, inst = instance(a)
    th = " Theorised." if a["id"] in theorised else ""
    L.append("- **%s** %s to %s, %s; %s; %s; %s. Instance (%s): %s.%s" % (
        a["id"], a["from"], a["to"], tag[a["id"]], a.get("strength"), a.get("kind"), count(a), k, inst, th))
L += ["", "## Drawing 1, with the theorised arrows (%d arrows)" % len(drawn), ""] + mermaid(True)
L += ["", "## Drawing 2, without them (%d arrows)" % (len(drawn) - len(theorised)), "",
      "The same, less %s. P02, P04 and P15 then stand with no arrow." % " and ".join(theorised), ""] + mermaid(False)
L += ["", "## Loops", "",
      "None is drawn. `model/loops.jsonl` records %d dated cycles. No room's record runs a whole cycle, and no counted "
      "arrow runs from the move (P10) back to building (P03)." % len(loops), "",
      "## What the figure leaves out", "",
      "It leaves out the field's tentative arrow from P08 to P21, which no proposition carries. It also leaves out the "
      "tentative elements P21 and P22, and the candidates P06, R02, K03, K04 and P19. Seven fourth-order themes are used "
      "by no element and are not drawn: %s. Two third-order themes no fourth-order theme gathers are not drawn either: "
      "ordinary sub talk (T3-017) and a hacked sub (T3-133). The figure also leaves out the register the coders' "
      "topic-based tier scattered: the room's own world used to do the canvas work (a game, a crusade, a mock state). "
      "The scheme split that register across in-jokes, fandom lore, national history and the work itself. Finally, the "
      "figure does not show the rooms the account names as told only in part." % "; ".join(
          "%s %s" % (t, fourth[t]["name"]) for t in unused4), ""]
text = "\n".join(L)
print("[%d bytes, %d words; drawn %d, by transition %d, by quote %d; theorised %s; unused T4 %s]" % (
    len(text.encode("utf-8")), len(text.split()), len(drawn), n_tr, n_q, theorised, unused4))
if "--write" in sys.argv:
    open(os.path.join(OUT, "figure-C5.md"), "w", encoding="utf-8").write(text)
    print("wrote out/figure-C5.md")
