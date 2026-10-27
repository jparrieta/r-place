#!/usr/bin/env python3
"""D6b: figure-D6.md, the stage C5 figure (figure-C5.md, drawing 1) with the six room forms drawn inside it. Every box and
arrow of the C5 drawing is kept, with its id and the proposition that carries each arrow; the five elements outside that
drawing which a form changes are added as boxes (P19, P23, P27, P32) or a note (C01). Each box and arrow carries the forms
that specify or restrict it, read from fractal-forms-D6.jsonl; a box no form changes is drawn plain. The proposals of
proposals-D6.jsonl are not drawn (stage D6, section 4). Prints the whole file; write it with >.

    python3 out/_analysis/d6b_figure.py > out/figure-D6.md
"""
import collections, json, os, re

AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
forms = [json.loads(l) for l in open(os.path.join(OUT, "fractal-forms-D6.jsonl"), encoding="utf-8")]
blines = [json.loads(l) for l in open(os.path.join(OUT, "fractal-D6.jsonl"), encoding="utf-8")]
names = open(os.path.join(OUT, "room-forms-names.md"), encoding="utf-8").read()
FNAME = {m.group(1): m.group(2).strip() for m in re.finditer(r"\| ([A-F]) \| ([^|]+) \|", names)}
assert len(FNAME) == 6
rel = collections.defaultdict(lambda: {"specifies": [], "restricts": []})
for r in forms:
    if r["relation"] in ("specifies", "restricts"):
        rel[r["element"]][r["relation"]].append(r["form"])
c5 = open(os.path.join(OUT, "figure-C5.md"), encoding="utf-8").read()
draw1 = c5.split("## Drawing 1")[1].split("```mermaid")[1].split("```")[0]
BOX = {m.group(1): m.group(2) for m in re.finditer(r'^\s+([A-Z]\d\d)\["\1: ([^"]+)"\]', draw1, re.M)}
EDGES = re.findall(r'^\s+([A-Z]\d\d) -->\|"(A\d\d) (N\d\d)"\| ([A-Z]\d\d)', draw1, re.M)
assert len(BOX) == 21 and len(EDGES) == 20, (len(BOX), len(EDGES))
EXTRA = {"P19": "a guest's work on a host's mark, under the host's rule",
         "P23": "the chat: planning moved off the thread",
         "P27": "choosing the spot before any loss",
         "P32": "members stepping away under strain"}
for e in EXTRA:
    assert e in rel, e


def marks(u):
    s, r = sorted(rel[u]["specifies"]), sorted(rel[u]["restricts"])
    out = []
    if s:
        out.append("specified by " + " ".join(s))
    if r:
        out.append("restricted by " + " ".join(r))
    return out


def node(u, label):
    m = marks(u)
    text = "%s: %s" % (u, label) + "".join("<br/>" + x for x in m)
    return '    %s["%s"]:::%s' % (u, text, "changed" if m else "plain")


cols = {"conditions": ["K01", "K02"], "follows": ["P11", "P12", "P13"]}
mid = [u for u in BOX if u not in cols["conditions"] + cols["follows"]]
L = []
L.append("# The figure: the model with its forms inside it")
L.append("")
L.append("Drawn at D6b from `fractal-forms-D6.jsonl` by `_analysis/d6b_figure.py`. It is the stage C5 figure (`figure-C5.md`, "
         "drawing 1: 21 boxes, 20 arrows, each arrow with the proposition that carries it) with the six room forms drawn "
         "into its boxes and arrows, at the level where they differ: the element or arrow. Each box and arrow names the "
         "forms that specify it (add detail that holds in their rooms) or restrict it (the form's restrict lines lean: "
         "the unit holds there only under a condition, or, for many arrows, the rooms' lines say it fails there or that "
         "the record cannot show it). A box with no form named is held by every form as the model states it. Four "
         "elements outside the C5 drawing are added because a form changes them (P19, P23, P27, P32); the claim C01 "
         "stands beside the figure, as at C5. No form replaces any element, but the coding vocabulary made replacing "
         "nearly unreachable (`retelling-D6.md`, the frame). Most of the changes drawn lean only at the rule's own "
         "thresholds: 20 of the 72 survive ratio 1.5 and floor 15 per cent (`form-cells-sensitivity-D6.tsv`). The "
         "unvalidated proposals (`proposals-D6.jsonl`) are not drawn. Redrawn at D6a-09 with this paragraph and the "
         "legend's line on B corrected; the drawing and the tables are unchanged.")
L.append("")
L.append("## The forms")
L.append("")
for f in "ABCDEF":
    n = sum(1 for r in forms if r["form"] == f and r["relation"] != "untouched")
    L.append("- **%s, %s**: changes %d of the 66 units (elements and arrows) read." % (f, FNAME[f], n))
units = sorted({r["element"] for r in forms})
L.append("")
L.append("Units read: %d (each with six form lines, %d lines in all); lines that specify %d, restrict %d, replace 0, leave "
         "untouched %d." % (len(units), len(forms), sum(1 for r in forms if r["relation"] == "specifies"),
                           sum(1 for r in forms if r["relation"] == "restricts"),
                           sum(1 for r in forms if r["relation"] == "untouched")))
assert len(units) == 66, len(units)
L.append("")
L.append("## Drawing 1, the model with the forms in its boxes and arrows")
L.append("")
L.append("```mermaid")
L.append("flowchart LR")
L.append("  classDef changed fill:#fff4d6,stroke:#8a6d00")
L.append("  classDef plain fill:#f4f4f4,stroke:#999")
L.append('  subgraph conditions["Conditions"]')
for u in cols["conditions"]:
    L.append(node(u, BOX[u]))
L.append("  end")
L.append('  subgraph mediators["Mediators, named for what the room and its members do"]')
for u in mid:
    L.append(node(u, BOX[u]))
for u, lab in EXTRA.items():
    L.append(node(u, lab))
L.append("  end")
L.append('  subgraph follows["What follows"]')
for u in cols["follows"]:
    L.append(node(u, BOX[u]))
L.append("  end")
L.append('  C01note["C01, beside the figure: a decided element of order<br/>%s"]:::changed' % "<br/>".join(marks("C01")))
L.append('  H73(["hour 73: placement stops for every room"])')
L.append("  P11 --- H73")
L.append("  H73 --- P12")
for frm, arr, prop, to in EDGES:
    m = marks(arr)
    lab = "%s %s" % (arr, prop) + ("; " + "; ".join(m) if m else "")
    L.append('  %s -->|"%s"| %s' % (frm, lab, to))
L.append("```")
L.append("")
L.append("## Legend")
L.append("")
L.append("- **Boxes.** Left, the conditions; middle, what the room and its members do; right, what follows the work. The bar "
         "at hour 73 marks the close. Shaded boxes are changed by at least one form; grey boxes by none.")
L.append("- **specified by X**: in form X, add-step, add-condition or link lines on the unit lean (held by at least the "
         "larger of 5 and a tenth of X's defining rooms, at 1.2 times the 558 defining rooms' share or more). "
         "**restricted by X**: restrict lines lean and outnumber the other leaning ops. The rule was logged at D6a-01 before "
         "it ran (`_analysis/d6_fractal.py`).")
spec_arrows = sorted(arr for _f, arr, _p, _t in EDGES if rel[arr]["specifies"])
L.append("- **Arrows.** Each keeps its C5 label: its id and the proposition (N01 to N09) that carries it, then the forms that "
         "specify or restrict it. Of the 20 arrows, %s specified by a form (%s), and %d are restricted by one or more. "
         "A restriction says the order holds in that form only under a condition, or that the record there cannot show it."
         % ("one is" if len(spec_arrows) == 1 else "%d are" % len(spec_arrows),
            "; ".join("%s, by %s" % (a, " and ".join(sorted(rel[a]["specifies"]))) for a in spec_arrows) or "none",
            sum(1 for _f, arr, _p, _t in EDGES if rel[arr]["restricts"])))
L.append("- **Forms.** A to F are the six room forms of D4a-08c, by their final names (`room-forms-names.md`). B is a residual "
         "grouping, not a form: three facets (the chat, the scripts and the raids) held by different rooms at about "
         "chance overlap. The 35 branches are the level below and are not drawn; the table names the branches "
         "that explain each form's changes (`fractal-D6.jsonl`).")
L.append("")
L.append("## Where each form differs, with the branches that explain it")
L.append("")
L.append("| form | specifies | restricts | branches with a line in this form (`fractal-D6.jsonl`) |")
L.append("|---|---|---|---|")
for f in "ABCDEF":
    sp = sorted(r["element"] for r in forms if r["form"] == f and r["relation"] == "specifies")
    rs = sorted(r["element"] for r in forms if r["form"] == f and r["relation"] == "restricts")
    bs = sorted({b["branch"] for b in blines if b.get("form") == f})
    L.append("| %s, %s | %s | %s | %s |" % (f, FNAME[f], ", ".join(sp) or "none", ", ".join(rs) or "none",
                                         ", ".join(bs) or "none"))
untouched_all = sorted(u for u in units if not rel[u]["specifies"] and not rel[u]["restricts"])
L.append("")
L.append("**Held by every form as the model states it (%d units):** %s." % (len(untouched_all), ", ".join(untouched_all)))
L.append("")
L.append("## What the figure leaves out")
L.append("")
L.append("It leaves out what the C5 figure left out (its last section), the eleven unvalidated proposals, the two held "
         "proposals (QD4-001; stated in full in `retelling-D6.md`), and the rates at which the forms hold an element "
         "without changing it, which the rule does not test (told in the retelling under D05 and D08). It does not draw the "
         "branches, the splits of form D, or the survival reading by form, which the retelling gives in words.")
print("\n".join(L))
