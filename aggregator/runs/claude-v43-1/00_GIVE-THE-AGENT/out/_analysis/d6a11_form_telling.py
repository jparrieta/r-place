#!/usr/bin/env python3
"""D6a-11 to D6a-16, the form tellings (J, 27 Oct 06:41 to 06:58 Berlin): facts and figure sources for one form and its
three rooms. Reads only; prints to stdout (write with >).

  --facts                      JSON: the form's changed cells with their marks (form-cells-sensitivity-D6.tsv), the
                               third- and fourth-order placements and dimension of their deciding lines, the form's
                               fourth-order change signature, and for each room its ops on every unit
                               (_views/rooms-x-elements.tsv), its selected changes (op:element at T3, T4, dimension),
                               the form's cells it shows and where it departs.
  --dot form                   graphviz source: the stage C5 drawing with the form's changed cells drawn by mark.
  --dot room --sub <room>      graphviz source: the stage C5 drawing with the room's instantiation laid on it.

    python3 out/_analysis/d6a11_form_telling.py --form A --rooms FloydVsVoid,prequelmemes,theexpanse --facts
"""
import argparse, collections, csv, json, os, re

ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
ap.add_argument("--rooms", required=True)
ap.add_argument("--facts", action="store_true")
ap.add_argument("--dot", choices=["form", "room"])
ap.add_argument("--sub")
a = ap.parse_args()
AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
TAG = {"A": "d5a36", "B": "d5a37", "C": "d5a38", "D": "d5a39", "E": "d5a40", "F": "d5a41"}
F = a.form
ROOMS = a.rooms.split(",")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


els = {e["id"]: e for e in jl(os.path.join(OUT, "model", "elements.jsonl"))}
arrows = {x["id"]: x for x in jl(os.path.join(OUT, "model", "arrows.jsonl"))}
t3name = {r["id"]: r["name"] for r in jl(os.path.join(OUT, "scheme_final.jsonl")) if r.get("id", "").startswith("T3")}
t4name = {r["id"]: r["name"] for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
dims = jl(os.path.join(OUT, "dimensions.jsonl"))
t4dim = {t: d["id"] for d in dims for t in d["members"]}
dimname = {d["id"]: d["label"] for d in dims}
names = open(os.path.join(OUT, "room-forms-names.md"), encoding="utf-8").read()
FNAME = {m.group(1): m.group(2).strip() for m in re.finditer(r"\| ([A-F]) \| ([^|]+) \|", names)}
c5 = open(os.path.join(OUT, "figure-C5.md"), encoding="utf-8").read()
draw1 = c5.split("## Drawing 1")[1].split("```mermaid")[1].split("```")[0]
BOX = {m.group(1): m.group(2) for m in re.finditer(r'^\s+([A-Z]\d\d)\["\1: ([^"]+)"\]', draw1, re.M)}
EDGES = re.findall(r'^\s+([A-Z]\d\d) -->\|"(A\d\d) (N\d\d)"\| ([A-Z]\d\d)', draw1, re.M)
assert len(BOX) == 21 and len(EDGES) == 20
SHORT = {"P06": "working out who changed the work", "P19": "a guest's work under a host's rule",
         "P21": "who may commit the room", "P22": "which version is kept", "P23": "the chat",
         "P24": "explaining the canvas", "P25": "newcomers through the work", "P26": "jokes made of the work",
         "P27": "choosing the spot before any loss", "P28": "a room formed around a mark", "P29": "what offends",
         "P30": "the work turned to outsiders", "P31": "whether covering is fair", "P32": "stepping away under strain",
         "P33": "plans kept from rivals", "P34": "turning on the room's own mark", "K03": "a quarrel carried in",
         "K04": "the room as a body it was before", "K05": "members' own time and devices", "K06": "the site's faults",
         "K07": "members of both rooms", "R02": "the envoy", "C01": "decided order", "C02": "a prior tie names the rival"}
COLS = {"conditions": ["K01", "K02"], "follows": ["P11", "P12", "P13"]}

tree = {r["room"]: r for r in csv.DictReader(open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8"),
                                             delimiter="\t")}
dfn = [s for s, r in tree.items() if r["form"] == F and r["role"] == "defining"]
pop = [s for s, r in tree.items() if r["role"] == "defining"]
lines = []
for t in TAG.values():
    lines += [l for l in json.load(open(os.path.join(AN, "%s_lines.json" % t), encoding="utf-8"))["lines"]
              if l.get("role") == "defining"]
forms = [json.loads(l) for l in open(os.path.join(OUT, "fractal-forms-D6.jsonl"), encoding="utf-8")]
sens = {(r["element"], r["form"]): r for r in csv.DictReader(
    open(os.path.join(OUT, "form-cells-sensitivity-D6.tsv"), encoding="utf-8"), delimiter="\t")}
rx = {}
with open(os.path.join(OUT, "_views", "rooms-x-elements.tsv"), encoding="utf-8") as fh:
    hdr = None
    for raw in fh:
        if raw.startswith("#"):
            continue
        c = raw.rstrip("\n").split("\t")
        if hdr is None:
            hdr = c
            continue
        rx[c[0]] = {hdr[i]: [x for x in c[i].split(",") if x] for i in range(1, len(hdr)) if i < len(c)}


def t3t4(l):
    t3 = l.get("t3")
    t4 = l.get("t4") if isinstance(l.get("t4"), str) else (l.get("t4") or [None])[0]
    return t3, t4, t4dim.get(t4)


def label_of(u):
    return BOX.get(u) or SHORT.get(u) or u


# the form's changed cells
cells = []
for w in forms:
    if w["form"] != F or w["relation"] == "untouched":
        continue
    s = sens[(w["element"], F)]
    ops = s["deciding_ops"].split(",")
    dl = [l for l in lines if l["sub"] in set(dfn) and l["element"] == w["element"] and l["op"] in ops]
    c3 = collections.Counter(t3t4(l)[0] for l in dl)
    c4 = collections.Counter(t3t4(l)[1] for l in dl)
    cells.append({"unit": w["element"], "relation": w["relation"], "deciding_ops": ops, "holders": s["holders"],
                  "ratio": s["ratio"], "mark": s["mark"], "size_mark": s["size_mark"], "dimension": w["dimension"],
                  "how": w["how"], "is_arrow": w["element"] in arrows,
                  "arrow": ("%s to %s" % (arrows[w["element"]]["from"], arrows[w["element"]]["to"])
                            if w["element"] in arrows else None),
                  "top_t3": [(t, t3name.get(t), n) for t, n in c3.most_common(3)],
                  "top_t4": [(t, t4name.get(t), t4dim.get(t), n) for t, n in c4.most_common(2)]})

# the form's fourth-order change signature, as the allocation wrote it (room-forms-D4a08c.jsonl, change_signature_T4:
# the fourth-order themes the form's defining members change at 1.5 times the defining population's share or more, held
# by a third of them or more; the allocation's own columns, which a line-level count does not reproduce)
alloc = {r["id"]: r for r in jl(os.path.join(OUT, "room-forms-D4a08c.jsonl"))}
t4id = {v: k for k, v in t4name.items()}
signature = [(t4id.get(s["name"]), s["name"], t4dim.get(t4id.get(s["name"])), s["presence"],
              round(s["presence"] / s["ratio"], 3), s["ratio"]) for s in alloc[F]["change_signature_T4"]]
cell_by_unit = {c["unit"]: c for c in cells}


def room_facts(sub):
    mine = [l for l in lines if l["sub"] == sub]
    changes = []
    for l in mine:
        t3, t4, d = t3t4(l)
        changes.append({"op": l["op"], "unit": l["element"], "t3": t3, "t3_name": t3name.get(t3), "t4": t4,
                        "t4_name": t4name.get(t4), "dimension": d, "how": l["how"], "codes": l["codes"][:3],
                        "arrow": ("%s to %s" % (arrows[l["element"]]["from"], arrows[l["element"]]["to"])
                                  if l["element"] in arrows else None)})
    ops = rx.get(sub, {})
    carried = sorted(u for u, v in ops.items() if v == ["instantiate"])
    changed_units = sorted({c["unit"] for c in changes})
    absent = sorted(u for u, v in ops.items() if "absent" in v)
    shows = [c["unit"] for c in cells if any(x["unit"] == c["unit"] and x["op"] in c["deciding_ops"] for x in changes)]
    lacks = [c["unit"] for c in cells if c["unit"] not in shows]
    off_form = sorted(u for u in changed_units if u not in cell_by_unit)
    ledger_only = sorted(u for u, v in ops.items() if u not in changed_units
                         and any(o not in ("instantiate", "absent", "propose") for o in v))
    # carried as stated: instantiated, with no selected change and no other change line in the ledger view (as drawn)
    carried = sorted(u for u, v in ops.items() if "instantiate" in v and u not in changed_units and u not in ledger_only)
    absent = sorted(u for u, v in ops.items() if "absent" in v and "instantiate" not in v and u not in changed_units
                    and u not in ledger_only)
    return {"sub": sub, "form": tree[sub]["form"], "role": tree[sub]["role"],
            "selected_changes": int(tree[sub]["selected_changes"]), "coded_concepts": int(tree[sub]["coded_concepts"]),
            "carried_as_stated": carried, "changed_units": changed_units, "absent": absent,
            "ledger_changes_not_selected": ledger_only,
            "no_line": sorted(u for u in list(els) + list(arrows) if not ops.get(u)),
            "shows_form_cells": shows, "lacks_form_cells": lacks, "changes_outside_form_cells": off_form,
            "changes": sorted(changes, key=lambda c: (c["dimension"] or "", c["unit"], c["op"]))}


def drawn_units(extra):
    return list(BOX) + [u for u in extra if u not in BOX and u in els]


def dot_header(title):
    return ["digraph G {", '  graph [rankdir=LR, fontname="Helvetica", fontsize=12, labelloc=t, label="%s", nodesep=0.25, '
            'ranksep=0.6];' % title.replace('"', "'"),
            '  node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=10, fillcolor="#ffffff", '
            'color="#999999"];', '  edge [fontname="Helvetica", fontsize=8, color="#bbbbbb"];']


def clusters(units, node):
    out = []
    groups = [("conditions", "Conditions", [u for u in units if u in COLS["conditions"] or u.startswith("K")]),
              ("follows", "What follows", [u for u in units if u in COLS["follows"]]),
              ("mediators", "Mediators: what the room and its members do",
               [u for u in units if u not in COLS["follows"] and not u.startswith("K") and not u.startswith("C")]),
              ("claims", "Claims beside the model", [u for u in units if u.startswith("C")])]
    for key, lab, us in groups:
        if not us:
            continue
        out.append('  subgraph cluster_%s { label="%s"; style=rounded; color="#cccccc";' % (key, lab))
        for u in us:
            out.append(node(u))
        out.append("  }")
    out.append('  H73 [label="hour 73: placement stops", shape=ellipse, fillcolor="#eeeeee"];')
    out.append('  P11 -> H73 [arrowhead=none, style=dotted]; H73 -> P12 [arrowhead=none, style=dotted];')
    return out


def esc(s):
    return s.replace('"', "'")


if a.facts:
    print(json.dumps({"form": F, "form_name": FNAME[F], "defining": len(dfn), "cells": cells, "signature": signature,
                      "rooms": [room_facts(s) for s in ROOMS]}, ensure_ascii=False))
elif a.dot == "form":
    STY = {"robust": ('"rounded,filled,bold"', "#e66101", 3), "marginal": ('"rounded,filled,dashed"', "#fdb863", 2),
           "size-dependent": ('"rounded,filled,dotted"', "#d8daeb", 2)}
    units = drawn_units([c["unit"] for c in cells])

    def node(u):
        c = cell_by_unit.get(u)
        if not c or c["is_arrow"]:
            return '    %s [label="%s: %s"];' % (u, u, esc(label_of(u)))
        st, fill, pw = STY[c["size_mark"]]
        t3 = c["top_t3"][0]
        t4 = c["top_t4"][0]
        lab = "%s: %s\\n%s by %s (%s rooms)\\n%s %s; %s %s; %s\\n%s" % (
            u, esc(label_of(u)), c["relation"], ", ".join(c["deciding_ops"]), c["holders"], t3[0], esc(t3[1] or ""),
            t4[0], esc(t4[1] or ""), t4[2], c["size_mark"].upper())
        return '    %s [label="%s", style=%s, fillcolor="%s", penwidth=%d, color="#555555"];' % (u, lab, st, fill, pw)

    L = dot_header("Form %s, %s: its changes against the global model (D6a-11 to D6a-16)" % (F, FNAME[F]))
    L += clusters(units, node)
    for frm, arr, prop, to in EDGES:
        c = cell_by_unit.get(arr)
        if c:
            col = {"robust": "#e66101", "marginal": "#f1a340", "size-dependent": "#8073ac"}[c["size_mark"]]
            sty = {"robust": "solid", "marginal": "dashed", "size-dependent": "dotted"}[c["size_mark"]]
            L.append('  %s -> %s [label="%s %s\\n%s (%s)\\n%s", color="%s", fontcolor="%s", penwidth=3, style=%s];' % (
                frm, to, arr, prop, c["relation"], c["holders"], c["size_mark"].upper(), col, col, sty))
        else:
            L.append('  %s -> %s [label="%s %s"];' % (frm, to, arr, prop))
    for u, c in cell_by_unit.items():
        if c["is_arrow"] and not any(arr == u for _f, arr, _p, _t in EDGES):
            x = arrows[u]
            L.append('  %s -> %s [label="%s\\n%s", color="#e66101", style=dashed];' % (x["from"], x["to"], u, c["relation"]))
    # D6a-16: a signature column can be a link between two themes (no T4 id, no dimension); name it as a link.
    sig = "\\l".join("%s: changed by %.0f%% of the form's defining rooms, %.2f times the population" % (
        "%s %s (%s)" % (t, esc(n or ""), d) if t else "the link %s" % esc(n or ""), 100 * f_, r)
        for t, n, d, f_, _p, r in signature)
    L.append('  subgraph cluster_legend { label="Legend"; style=rounded; color="#cccccc";')
    L.append('    lg1 [label="ROBUST: keeps its relation at ratio 1.5 and floor 15 per cent", style="rounded,filled,bold", '
             'fillcolor="#e66101", penwidth=3];')
    L.append('    lg2 [label="MARGINAL: leans only at the rule\'s thresholds", style="rounded,filled,dashed", '
             'fillcolor="#fdb863", penwidth=2];')
    L.append('    lg3 [label="SIZE-DEPENDENT: does not keep its lean with record size held fixed", '
             'style="rounded,filled,dotted", fillcolor="#d8daeb", penwidth=2];')
    L.append('    lg4 [label="unchanged by the form: held as the model states it"];')
    L.append('    lg5 [shape=note, fillcolor="#ffffff", label="The form\'s fourth-order change signature:\\l%s\\l"];' % sig)
    L.append("    lg1 -> lg2 -> lg3 -> lg4 -> lg5 [style=invis];")
    L.append("  }")
    L.append("}")
    print("\n".join(L))
elif a.dot == "room":
    rf = room_facts(a.sub)
    ops = rx.get(a.sub, {})
    by_unit = collections.defaultdict(list)
    for c in rf["changes"]:
        by_unit[c["unit"]].append(c)
    # D6a-13: the ends of a changed arrow outside the C5 drawing are drawn too, so that every change is shown.
    units = drawn_units(rf["changed_units"] + [e for u in rf["changed_units"] if u in arrows
                                               for e in (arrows[u]["from"], arrows[u]["to"])])

    def node(u):
        v = ops.get(u, [])
        ch = by_unit.get(u)
        form_cell = u in rf["shows_form_cells"]
        if ch:
            parts = ["%s (%s %s)" % (c["op"], c["t3"], esc((c["t3_name"] or "")[:34])) for c in ch[:3]]
            more = " +%d more" % (len(ch) - 3) if len(ch) > 3 else ""
            lab = "%s: %s\\n%s%s%s" % (u, esc(label_of(u)), "\\n".join(parts), more,
                                       "\\nFORM %s CHANGE" % F if form_cell else "")
            return '    %s [label="%s", fillcolor="#fdb863", penwidth=%d, color="%s"];' % (
                u, lab, 3 if form_cell else 1, "#2c7bb6" if form_cell else "#999999")
        if u in rf["ledger_changes_not_selected"]:
            return ('    %s [label="%s: %s\\nchange in the ledger view, not selected", fillcolor="#fee8c8", '
                    'style="rounded,filled,dashed"];' % (u, u, esc(label_of(u))))
        if v == ["instantiate"] or (v and "instantiate" in v):
            return '    %s [label="%s: %s\\ncarried as stated", fillcolor="#d9f0d3"];' % (u, u, esc(label_of(u)))
        if "absent" in v:
            return '    %s [label="%s: %s\\nabsent", style="rounded,dashed", color="#999999"];' % (u, u, esc(label_of(u)))
        return '    %s [label="%s: %s\\nno line", fontcolor="#999999", color="#dddddd"];' % (u, u, esc(label_of(u)))

    L = dot_header("r/%s (form %s, %s): the global model as instantiated in this room" % (a.sub, F, FNAME[F]))
    L += clusters(units, node)
    drawn = set(units)
    for x in arrows.values():
        if x["from"] not in drawn or x["to"] not in drawn:
            continue
        v = ops.get(x["id"], [])
        ch = by_unit.get(x["id"])
        prop = next((p for _f, arr, p, _t in EDGES if arr == x["id"]), "")
        if ch:
            fc = x["id"] in rf["shows_form_cells"]
            L.append('  %s -> %s [label="%s %s\\n%s%s", color="#d7191c", fontcolor="#d7191c", penwidth=%d, style=dashed];'
                     % (x["from"], x["to"], x["id"], prop, ", ".join(sorted({c["op"] for c in ch})),
                        "\\nFORM %s CHANGE" % F if fc else "", 3 if fc else 2))
        elif x["id"] in rf["ledger_changes_not_selected"]:
            L.append('  %s -> %s [label="%s %s\\nledger view: %s, not selected", color="#fdae61", fontcolor="#d7191c", '
                     'style=dashed];' % (x["from"], x["to"], x["id"], prop,
                                         ", ".join(o for o in v if o not in ("instantiate", "absent"))))
        elif "instantiate" in v:
            L.append('  %s -> %s [label="%s %s\\nholds", color="#1a9641", fontcolor="#1a9641", penwidth=2];'
                     % (x["from"], x["to"], x["id"], prop))
        elif "absent" in v:
            L.append('  %s -> %s [label="%s absent", style=dotted, color="#999999", fontcolor="#999999"];'
                     % (x["from"], x["to"], x["id"]))
        else:
            L.append('  %s -> %s [label="%s", color="#dddddd", fontcolor="#bbbbbb"];' % (x["from"], x["to"], x["id"]))
    L.append('  subgraph cluster_legend { label="Legend"; style=rounded; color="#cccccc";')
    L.append('    k1 [label="carried as stated (instantiated, no change)", fillcolor="#d9f0d3"];')
    L.append('    k2 [label="changed by the room: op (T3 where the change sits)", fillcolor="#fdb863"];')
    L.append('    k3 [label="changed, and one of form %s\'s defining changes", fillcolor="#fdb863", penwidth=3, color="#2c7bb6"];' % F)
    L.append('    k4 [label="absent from the record", style="rounded,dashed"];')
    L.append('    k5 [label="no line in the ledger", fontcolor="#999999", color="#dddddd"];')
    L.append('    k6 [shape=plaintext, fillcolor="#ffffff", label="arrows: green holds; red dashed changed; grey dotted absent"];')
    L.append("    k1 -> k2 -> k3 -> k4 -> k5 -> k6 [style=invis];")
    L.append("  }")
    L.append("}")
    print("\n".join(L))
