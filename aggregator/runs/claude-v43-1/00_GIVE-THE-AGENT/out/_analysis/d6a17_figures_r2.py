#!/usr/bin/env python3
"""D6a-17, the round-2 figures (J, 27 Oct 14:03 and 15:23 Berlin). Two changes from the round-1 figures of
d6a11_form_telling.py, whose model, cells and room facts this script imports unchanged:

  1. Room figures: a cell of the form that the room does not show has a hollow border (a double blue outline); a cell
     the room shows keeps the solid thick blue border. Every cell of the form is drawn, shown or not.
  2. Restricts on arrows are split by the D5 sort of each restrict line (_analysis/<tag>_restrict_sorted.json, one
     reader's sort): "the arrow fails here" (dark red, bold), "the record cannot show it" (violet, dotted), and
     "a condition or an overlap" (red, dashed). A line sorted "both" is drawn as both. In the form figure a restricted
     arrow cell is drawn as two parallel arrows with the counts of the form's restrict lines on it.

Prints graphviz source.

    python3 out/_analysis/d6a17_figures_r2.py --form C --dot form > out/form-telling-D6-r2/form-C.dot
    python3 out/_analysis/d6a17_figures_r2.py --form C --dot room --sub gatech --role "round 2 and good old" > ...
"""
import argparse, collections, importlib, json, os, sys

ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
ap.add_argument("--dot", choices=["form", "room"], required=True)
ap.add_argument("--sub")
ap.add_argument("--role", default="")
a = ap.parse_args()
AN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AN)
sys.argv = ["d6a11_form_telling.py", "--form", a.form, "--rooms", a.sub or "none"]
M = importlib.import_module("d6a11_form_telling")
F = a.form
srt = json.load(open(os.path.join(AN, "%s_restrict_sorted.json" % M.TAG[F]), encoding="utf-8"))
SORT = {x["id"]: x["code"] for x in srt["sorted"]}
BYARROW = srt["by_arrow"]
BLUE = "#2c7bb6"
KIND = {"F": ("the arrow fails here", "#b2182b", "bold", 2.5),
        "R": ("the record cannot show it", "#5e3c99", "dotted", 2.5),
        "N": ("a condition or an overlap", "#d7191c", "dashed", 2),
        "?": ("restrict, not sorted", "#d7191c", "dashed", 2)}
esc = M.esc


def attrs(d):
    return ", ".join('%s=%s' % (k, v if isinstance(v, (int, float)) or v.startswith('"') else '"%s"' % v)
                     for k, v in d.items())


if a.dot == "form":
    STY = {"robust": ('"rounded,filled,bold"', "#e66101", 3), "marginal": ('"rounded,filled,dashed"', "#fdb863", 2),
           "size-dependent": ('"rounded,filled,dotted"', "#d8daeb", 2)}
    ESTY = {"robust": "bold", "marginal": "dashed", "size-dependent": "dotted"}
    units = M.drawn_units([c["unit"] for c in M.cells])

    def node(u):
        c = M.cell_by_unit.get(u)
        if not c or c["is_arrow"]:
            return '    %s [label="%s: %s"];' % (u, u, esc(M.label_of(u)))
        st, fill, pw = STY[c["size_mark"]]
        t3, t4 = c["top_t3"][0], c["top_t4"][0]
        lab = "%s: %s\\n%s by %s (%s rooms)\\n%s %s; %s %s; %s\\n%s" % (
            u, esc(M.label_of(u)), c["relation"], ", ".join(c["deciding_ops"]), c["holders"], t3[0], esc(t3[1] or ""),
            t4[0], esc(t4[1] or ""), t4[2], c["size_mark"].upper())
        return '    %s [label="%s", style=%s, fillcolor="%s", penwidth=%d, color="#555555"];' % (u, lab, st, fill, pw)

    L = M.dot_header("Form %s, %s: its changes against the global model (round 2, D6a-17)" % (F, M.FNAME[F]))
    L += M.clusters(units, node)
    for frm, arr, prop, to in M.EDGES:
        c = M.cell_by_unit.get(arr)
        if c and c["relation"] == "restricts":
            ba = BYARROW.get(arr, {})
            n = sum(ba.values())
            fl, rc = ba.get("F", 0) + ba.get("B", 0), ba.get("R", 0) + ba.get("B", 0)
            sty = ESTY[c["size_mark"]]
            L.append('  %s -> %s [label="%s %s, restricts (%s rooms), %s\\nthe arrow fails here: %d of %d lines", '
                     'color="#b2182b", fontcolor="#b2182b", penwidth=3, style=%s];'
                     % (frm, to, arr, prop, c["holders"], c["size_mark"].upper(), fl, n, sty))
            L.append('  %s -> %s [label="the record cannot show it: %d of %d\\n(both %d; a condition or overlap %d)", '
                     'color="#5e3c99", fontcolor="#5e3c99", penwidth=3, style=%s];'
                     % (frm, to, rc, n, ba.get("B", 0), ba.get("N", 0), sty))
        elif c:
            col = {"robust": "#e66101", "marginal": "#f1a340", "size-dependent": "#8073ac"}[c["size_mark"]]
            L.append('  %s -> %s [label="%s %s\\n%s (%s)\\n%s", color="%s", fontcolor="%s", penwidth=3, style=%s];' % (
                frm, to, arr, prop, c["relation"], c["holders"], c["size_mark"].upper(), col, col, ESTY[c["size_mark"]]))
        else:
            L.append('  %s -> %s [label="%s %s"];' % (frm, to, arr, prop))
    for u, c in M.cell_by_unit.items():
        if c["is_arrow"] and not any(arr == u for _f, arr, _p, _t in M.EDGES):
            x = M.arrows[u]
            L.append('  %s -> %s [label="%s\\n%s", color="#e66101", style=dashed];' % (x["from"], x["to"], u,
                                                                                      c["relation"]))
    sig = "\\l".join("%s: changed by %.0f%% of the form's defining rooms, %.2f times the population" % (
        "%s %s (%s)" % (t, esc(n or ""), d) if t else "the link %s" % esc(n or ""), 100 * f_, r)
        for t, n, d, f_, _p, r in M.signature)
    L.append('  subgraph cluster_legend { label="Legend (round 2)"; style=rounded; color="#cccccc";')
    L.append('    lg1 [label="ROBUST: keeps its relation at ratio 1.5 and floor 15 per cent", style="rounded,filled,bold", '
             'fillcolor="#e66101", penwidth=3];')
    L.append('    lg2 [label="MARGINAL: leans only at the rule\'s thresholds", style="rounded,filled,dashed", '
             'fillcolor="#fdb863", penwidth=2];')
    L.append('    lg3 [label="SIZE-DEPENDENT: does not keep its lean with record size held fixed", '
             'style="rounded,filled,dotted", fillcolor="#d8daeb", penwidth=2];')
    L.append('    lg4 [label="unchanged by the form: held as the model states it"];')
    L.append('    lg5 [shape=note, fillcolor="#ffffff", label="The form\'s fourth-order change signature:\\l%s\\l"];' % sig)
    L.append('    lgx1 [label="a restricted arrow of the form", shape=plaintext, fillcolor="#ffffff"];')
    L.append('    lgx2 [label="(one reader\'s sort of the form\'s restrict lines, D5)", shape=plaintext, '
             'fillcolor="#ffffff"];')
    L.append('    lgx1 -> lgx2 [label="lines that say the arrow fails here", color="#b2182b", fontcolor="#b2182b", '
             'penwidth=3];')
    L.append('    lgx1 -> lgx2 [label="lines that say the record cannot show it", color="#5e3c99", '
             'fontcolor="#5e3c99", penwidth=3, style=dotted];')
    L.append("    lg1 -> lg2 -> lg3 -> lg4 -> lg5 -> lgx1 [style=invis];")
    L.append("  }")
    L.append("}")
    print("\n".join(L))
else:
    rf = M.room_facts(a.sub)
    ops = M.rx.get(a.sub, {})
    by_unit = collections.defaultdict(list)
    for c in rf["changes"]:
        by_unit[c["unit"]].append(c)
    shows = set(rf["shows_form_cells"])
    extra = list(rf["changed_units"]) + [c["unit"] for c in M.cells]
    extra += [e for u in list(extra) if u in M.arrows for e in (M.arrows[u]["from"], M.arrows[u]["to"])]
    units = M.drawn_units(extra)

    def node(u):
        v = ops.get(u, [])
        ch = by_unit.get(u)
        cell = M.cell_by_unit.get(u)
        d = {}
        if ch:
            parts = ["%s (%s %s)" % (c["op"], c["t3"], esc((c["t3_name"] or "")[:34])) for c in ch[:3]]
            more = " +%d more" % (len(ch) - 3) if len(ch) > 3 else ""
            lab = "%s: %s\\n%s%s" % (u, esc(M.label_of(u)), "\\n".join(parts), more)
            d.update(fillcolor="#fdb863", color="#999999", penwidth=1)
        elif u in rf["ledger_changes_not_selected"]:
            lab = "%s: %s\\nchange in the ledger view, not selected" % (u, esc(M.label_of(u)))
            d.update(fillcolor="#fee8c8", style='"rounded,filled,dashed"')
        elif "instantiate" in v:
            lab = "%s: %s\\ncarried as stated" % (u, esc(M.label_of(u)))
            d.update(fillcolor="#d9f0d3")
        elif "absent" in v:
            lab = "%s: %s\\nabsent" % (u, esc(M.label_of(u)))
            d.update(style='"rounded,dashed"', color="#999999")
        else:
            lab = "%s: %s\\nno line" % (u, esc(M.label_of(u)))
            d.update(fontcolor="#999999", color="#dddddd")
        if cell and u in shows:
            lab += "\\nFORM %s CHANGE, SHOWN" % F
            d.update(color=BLUE, penwidth=3)
        elif cell:
            lab += "\\nform %s cell, not shown here" % F
            d.update(color=BLUE, peripheries=2, penwidth=1.5)
        return '    %s [label="%s", %s];' % (u, lab, attrs(d))

    title = "r/%s (form %s, %s; %s): the global model as instantiated in this room (round 2, D6a-17)" % (
        a.sub, F, M.FNAME[F], a.role or "round 2")
    L = M.dot_header(title)
    L += M.clusters(units, node)
    drawn = set(units)
    # a change whose element is a dimension (QD1-001) has no box in the stage C5 drawing: drawn apart, beside the model
    for u in rf["changed_units"]:
        if u not in drawn and u not in M.arrows:
            ch = by_unit.get(u, [])
            parts = ["%s (%s %s)" % (c["op"], c["t3"], esc((c["t3_name"] or "")[:34])) for c in ch[:3]]
            L.append('  %s [label="%s: the dimension %s, as the element of the change\\n%s", fillcolor="#fdb863", '
                     'color="#999999"];' % (u, u, esc(M.dimname.get(u, u)), "\\n".join(parts)))
    for x in M.arrows.values():
        if x["from"] not in drawn or x["to"] not in drawn:
            continue
        u = x["id"]
        v = ops.get(u, [])
        ch = by_unit.get(u)
        prop = next((p for _f, arr, p, _t in M.EDGES if arr == u), "")
        cell = M.cell_by_unit.get(u)
        tag = ("\\nFORM %s CHANGE, SHOWN" % F if u in shows else
               ("\\n(form %s cell, not shown here)" % F if cell else ""))
        E = []
        if ch:
            kinds = []
            for c in ch:
                if c["op"] != "restrict":
                    continue
                code = SORT.get(c["id"], "?")
                for k in ({"B": ["F", "R"]}.get(code) or [code]):
                    if k not in kinds:
                        kinds.append(k)
            for k in [k for k in ("F", "R", "N", "?") if k in kinds]:
                name, col, sty, pw = KIND[k]
                deciding = cell is not None and "restrict" in cell["deciding_ops"] and u in shows
                E.append('  %s -> %s [label="%s %s\\nrestrict: %s%s", color="%s", fontcolor="%s", penwidth=%s, '
                         'style=%s];' % (x["from"], x["to"], u, prop, name, tag if not E else "", col, col,
                                         3.5 if deciding else pw, sty))
            other = sorted({c["op"] for c in ch if c["op"] != "restrict"})
            if other:
                deciding = cell is not None and any(o in cell["deciding_ops"] for o in other) and u in shows
                E.append('  %s -> %s [label="%s %s\\n%s%s", color="#e66101", fontcolor="#e66101", penwidth=%s, '
                         'style=dashed];' % (x["from"], x["to"], u, prop, ", ".join(other), tag if not E else "",
                                             3.5 if deciding else 2))
        elif u in rf["ledger_changes_not_selected"]:
            E.append('  %s -> %s [label="%s %s\\nledger view: %s, not selected%s", color="#fdae61", '
                     'fontcolor="#d7191c", style=dashed];' % (x["from"], x["to"], u, prop, ", ".join(
                         o for o in v if o not in ("instantiate", "absent")), tag))
        elif "instantiate" in v:
            E.append('  %s -> %s [label="%s %s\\nholds%s", color="#1a9641", fontcolor="#1a9641", penwidth=2];'
                     % (x["from"], x["to"], u, prop, tag))
        elif "absent" in v:
            E.append('  %s -> %s [label="%s absent%s", style=dotted, color="#999999", fontcolor="#999999"];'
                     % (x["from"], x["to"], u, tag))
        else:
            E.append('  %s -> %s [label="%s%s", color="#dddddd", fontcolor="#bbbbbb"];' % (x["from"], x["to"], u, tag))
        L += E
    L.append('  subgraph cluster_legend { label="Legend (round 2)"; style=rounded; color="#cccccc";')
    L.append('    k1 [label="carried as stated (instantiated, no change)", fillcolor="#d9f0d3"];')
    L.append('    k2 [label="changed by the room: op (T3 where the change sits)", fillcolor="#fdb863"];')
    L.append('    k3 [label="one of form %s\'s changes, shown by the room", fillcolor="#fdb863", penwidth=3, color="%s"];'
             % (F, BLUE))
    L.append('    k4 [label="one of form %s\'s changes, not shown by the room (hollow border)", fillcolor="#ffffff", '
             'peripheries=2, penwidth=1.5, color="%s"];' % (F, BLUE))
    L.append('    k5 [label="absent from the record", style="rounded,dashed"];')
    L.append('    k6 [label="no line in the ledger", fontcolor="#999999", color="#dddddd"];')
    L.append('    ka [label="arrows", shape=plaintext, fillcolor="#ffffff"];')
    L.append('    kb [label="(restricts by one reader\'s sort of the line, D5)", shape=plaintext, fillcolor="#ffffff"];')
    L.append('    ka -> kb [label="holds", color="#1a9641", fontcolor="#1a9641", penwidth=2];')
    L.append('    ka -> kb [label="restrict: the arrow fails here", color="#b2182b", fontcolor="#b2182b", penwidth=2.5, '
             'style=bold];')
    L.append('    ka -> kb [label="restrict: the record cannot show it", color="#5e3c99", fontcolor="#5e3c99", '
             'penwidth=2.5, style=dotted];')
    L.append('    ka -> kb [label="restrict: a condition or an overlap", color="#d7191c", fontcolor="#d7191c", '
             'style=dashed];')
    L.append('    ka -> kb [label="other change (add-step, add-condition, link)", color="#e66101", fontcolor="#e66101", '
             'style=dashed];')
    L.append('    ka -> kb [label="absent", color="#999999", fontcolor="#999999", style=dotted];')
    L.append("    k1 -> k2 -> k3 -> k4 -> k5 -> k6 -> ka [style=invis];")
    L.append("  }")
    L.append("}")
    print("\n".join(L))
