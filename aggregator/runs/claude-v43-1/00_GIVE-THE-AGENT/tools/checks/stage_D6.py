"""checks/stage_D6.py: the close-check of stage D6, the retelling, v38.

Written from stages/STAGE-D6-forming-the-retelling.md. It checks the SHAPE: that fractal-D6.jsonl names
elements and branches that exist, with a relation from the four and evidence that resolves; that
at the last leg (retelling-D6.md present) every branch appears in the telling and in at least
one fractal line; that the figure and the notes exist; that amendments carry what, id, change and
why. It cannot check whether the telling is right.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need
from checks import stage_D4 as s11
from checks import stage_D5 as s12

RELATIONS = ("specifies", "restricts", "replaces", "untouched")


def check(root, outdir, ctx):
    need(outdir, "notes-D6.md")
    vlib.model_moved(outdir, "D3", "D6")
    vlib.tree_moved(outdir)
    if not vlib.frozen_hash(outdir, "D3"):
        err("D6 requires the validated D3 model closure hash", shape="model:unfrozen")
    el, ar = s11.elements(outdir)
    ids = (el or set()) | (ar or set()) | (s11.fourth_ids(outdir) or set()) | (s11.dimension_ids(outdir) or set())
    branches = {b.get("id") for b in s11.branches(outdir) if b.get("id")}
    rows = jsonl(os.path.join(outdir, "fractal-D6.jsonl")) or []
    seen = set()
    for i, r in enumerate(rows, 1):
        where = "fractal-D6.jsonl line %d" % i
        if r.get("element") not in ids:
            err("%s: element %r resolves to no element, arrow, fourth-order theme or dimension" % (where, r.get("element")),
                shape="fractal: element unresolved", where=where)
        if r.get("branch") not in branches:
            err("%s: branch %r is not in branches.jsonl" % (where, r.get("branch")), shape="fractal: branch unresolved", where=where)
        if r.get("relation") not in RELATIONS:
            err("%s: relation %r is not one of %s" % (where, r.get("relation"), "|".join(RELATIONS)),
                shape="fractal: relation", where=where)
        if not str(r.get("how") or "").strip():
            err("%s: no how sentence" % where, shape="fractal: how", where=where)
        ev = r.get("evidence") or {}
        if not (ev.get("codes") or ev.get("rooms")):
            warn("%s: no evidence (codes or rooms)" % where, shape="fractal: evidence", where=where)
        seen.add(r.get("branch"))
    hist = " ".join(json.dumps(r) for r in (jsonl(os.path.join(outdir, "model", "history.jsonl")) or []))
    diary = " ".join(json.dumps(r) for r in vlib.diary_lines(outdir, "D6"))
    for i, a in enumerate(jsonl(os.path.join(outdir, "amendments-D6.jsonl")) or [], 1):
        if a.get("what") in ("element", "arrow", "branch", "subform", "crosslink"):
            err("D6 cannot apply substantive amendments after the affected-case return; record an unvalidated proposal in proposals-D6.jsonl",
                shape="amendment:unvalidated", where=str(i))
        for k in ("what", "id", "change", "why"):
            if not str(a.get(k) or "").strip():
                err("amendments-D6.jsonl line %d has no %s" % (i, k), shape="amendment: %s" % k, where=str(i))
        aid = str(a.get("id") or "")
        if aid and a.get("what") in ("element", "arrow") and aid not in hist:
            err("amendments-D6.jsonl line %d amends %s and model/history.jsonl has no line for it; an amendment to the "
                "model is a history line, as at D3 (rule 11)" % (i, aid), shape="amendment: history", where=aid)
        if aid and aid not in diary:
            err("amendments-D6.jsonl line %d (%s) has no diary line; each amendment is logged with mem.py log --kind "
                "move when it is made (section 4)" % (i, aid), shape="amendment: diary", where=aid)
    for i, proposal in enumerate(jsonl(os.path.join(outdir, "proposals-D6.jsonl")) or [], 1):
        if proposal.get("status") != "unvalidated" or proposal.get("base_model_version") != vlib.model_hash(outdir):
            err("proposals-D6.jsonl line %d must be unvalidated against the unchanged current model" % i,
                shape="proposal:version-status", where=str(i))
        for key in ("id", "what", "change", "why", "evidence", "affected_rooms"):
            if not proposal.get(key):
                err("proposals-D6.jsonl line %d lacks %s" % (i, key), shape="proposal:required", where=str(i))
    tell = text(outdir, "retelling-D6.md")
    if vlib.current_step(root) == "D6b" and not tell:
        err("retelling-D6.md is not written; D6b is the telling (section 2)", shape="telling: missing")
    if tell:
        need(outdir, "figure-D6.md", "handback-D6.md")
        for b in sorted(branches):
            if b not in seen:
                err("branch %s has no line in fractal-D6.jsonl; the retelling places every form" % b,
                    shape="fractal: branch missing", where=b)
            if not re.search(r"\b%s\b" % re.escape(b), tell):
                err("retelling-D6.md never names branch %s" % b, shape="telling: branch unnamed", where=b)
    else:
        warn("retelling-D6.md is not written yet; the branch coverage is checked at the last leg")
    print("  fractal lines %d, branches placed %d of %d" % (len(rows), len(seen & branches), len(branches)))


def base(outdir, root):
    s12.base(outdir, root)
    _w, _wj = s11._w, s11._wj
    _w(outdir, "_closes/model-D3.sha256", vlib.model_hash(outdir) + "\n")
    _w(outdir, "_closes/tree-D4.sha256", vlib.tree_hash(outdir) + "\n")
    el, _ = s11.elements(outdir)
    e = sorted(el)[0]
    _wj(outdir, "fractal-D6.jsonl", [{"element": e, "branch": "F01", "relation": "specifies",
                                       "how": "In F01 the element runs only under a two-sided attack.",
                                       "evidence": {"rooms": ["denmark"]}, "canvas": False}])
    _w(outdir, "retelling-D6.md", "# Retelling\n\nForm F01 specifies %s.\n" % e)
    _w(outdir, "figure-D6.md", "```mermaid\ngraph TD; D1-->F01\n```\n")
    _wj(outdir, "amendments-D6.jsonl", [])
    _w(outdir, "notes-D6.md", "# notes-D6\n")
    _w(outdir, "handback-D6.md", "# handback-D6\n")


def _plant_bad_relation(outdir, root):
    base(outdir, root)
    rows = jsonl(os.path.join(outdir, "fractal-D6.jsonl"))
    s11._wj(outdir, "fractal-D6.jsonl", [dict(rows[0], relation="improves")])


def _plant_branch_unnamed(outdir, root):
    base(outdir, root)
    s11._w(outdir, "retelling-D6.md", "# Retelling\n\nOne form only.\n")


def _plant_element_unresolved(outdir, root):
    base(outdir, root)
    rows = jsonl(os.path.join(outdir, "fractal-D6.jsonl"))
    s11._wj(outdir, "fractal-D6.jsonl", [dict(rows[0], element="P99")])


def _plant_amendment_untraced(outdir, root):
    base(outdir, root)
    el, _ = s11.elements(outdir)
    s11._wj(outdir, "amendments-D6.jsonl", [{"t": "x", "what": "element", "id": sorted(el)[0], "change": "reworded",
                                             "why": "the telling needed it", "evidence": {}}])


PLANTED = [
    ("an amendment with no history line", _plant_amendment_untraced, "model/history.jsonl has no line for it"),
    ("relation not one of the four", _plant_bad_relation, "is not one of specifies"),
    ("branch never named in the telling", _plant_branch_unnamed, "never names branch F01"),
    ("element unresolved", _plant_element_unresolved, "resolves to no element"),
]
