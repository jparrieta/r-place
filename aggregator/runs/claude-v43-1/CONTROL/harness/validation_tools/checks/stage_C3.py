"""checks/stage_C3.py: the close-check of stage C3, the model against the literature, v38.

Written from stages/STAGE-C3-model-literature.md (its Outputs block, sections 1 to 7, its
Close section) and from the v37 check it descends from (_v37-source/tools/validate.py, stage08).
It checks the SHAPE of the stage's files: existence, parse, ids that resolve, counts that
reconcile. It cannot check whether a reading of the literature is right.

The stage runs three legs (contradicting work; resembling work with the concept; the four
problems), so this check runs at each. literature-C3.md, notes-C3.md and manifest-C3.txt are
required at every leg (stage C5 reads the manifest first, so it says "no successor" until
there is one). mapping-C3.jsonl is leg 3's output: it is required once literature-C3.md carries
the four-problems section, and its absence before that is reported and not failed.

Ported from v37 under the v38 names: v2_manifest.txt -> manifest-C3.txt, listing every stage C2
file with or without its stage C3 successor (model-C3.md, structure-C3.md, concept-C3.md);
edges.v2.jsonl -> model/arrows.jsonl re-checked with stage C2's arrow checks, and each
mechanism rewritten from the literature marked mechanism_source: from-literature with the stage
C2 sentence kept as mechanism_C2 and a model/history.jsonl line for the stage; a stage-C3
tier_history event carries its move (v37 asked for a chunks_log or dimensions_log line, which
v38 folds into tier_history.jsonl's `was`); the warning on literature.md's section on which of
the four problems the structure reaches, now the mapping and part 4.

Not carried: chunks_log.jsonl and dimensions_log.jsonl (no separate log files in v38); the
`§6` heading test on literature.md (the seven parts replace it); the stage 15 B8 reference (the
crossing is gone).

Fields the stage file does not give, checked loosely: the field naming the work a mechanism was
taken from (looked for under work, source_work, mechanism_work or literature, warned about);
manifest-C3.txt's line format (a line is read as naming a stage C2 file and, when a successor
exists, its name); the seven parts of literature-C3.md (part 4's "richly" and "thinly" are
looked for and warned about).
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need
try:
    from checks import stage_C2 as s7
except ImportError:  # run with tools/checks on the path
    import stage_C2 as s7

PROBLEMS_08 = vlib.PROBLEMS + ("none",)      # one vocabulary with stage D5 (vlib.PROBLEMS)
STAGE07_FILES = ("model.md", "structure.md", "concept.md")
SUCCESSORS = {"model.md": "model-C3.md", "structure.md": "structure-C3.md", "concept.md": "concept-C3.md"}
WORK_KEYS = ("work", "source_work", "mechanism_work", "literature", "mechanism_source_work")


def check_mapping(outdir, t4):
    rows = jsonl(os.path.join(outdir, "mapping-C3.jsonl"))
    if rows is None:
        return None
    seen = {}
    for i, r in enumerate(rows, 1):
        f = r.get("fourth")
        if f not in t4:
            err("mapping-C3.jsonl line %d: fourth %r is not in fourth/fourth.jsonl" % (i, f),
                shape="mapping:fourth", where=str(f))
            continue
        if f in seen:
            err("mapping-C3.jsonl maps %s twice (lines %d and %d); one line per fourth-order theme"
                % (f, seen[f], i), shape="mapping:twice", where=f)
        seen[f] = i
        if r.get("problem") not in PROBLEMS_08:
            err("mapping-C3.jsonl %s: problem %r is not division|allocation|reward|information|none"
                % (f, r.get("problem")), shape="mapping:problem", where=f)
        if not r.get("why"):
            err("mapping-C3.jsonl %s carries no why clause" % f, shape="mapping:why", where=f)
        if r.get("problem") in PROBLEMS_08[:4] and not r.get("cannot_do"):
            err("mapping-C3.jsonl %s is mapped to %s and does not say what this material's version cannot "
                "do that the source's can (cannot_do)" % (f, r.get("problem")), shape="mapping:cannot_do", where=f)
    for f in sorted(t4 - set(seen)):
        err("mapping-C3.jsonl has no line for %s; every fourth-order theme is mapped to one of the four "
            "problems or to none, with a clause" % f, shape="mapping:missing", where=f)
    return rows


def check_manifest(outdir):
    """manifest-C3.txt: one line per stage C2 file saying whether it has a stage C3 successor."""
    man = text(outdir, "manifest-C3.txt")
    if not man.strip():
        err("manifest-C3.txt is empty; one line per stage C2 file (model.md, structure.md, concept.md) "
            "saying whether it has a stage C3 successor, which stage C5 reads first")
        return
    for f in STAGE07_FILES:
        if f not in man:
            err("manifest-C3.txt does not list %s; every stage C2 file has a line, with or without a "
                "successor" % f, shape="manifest:missing", where=f)
            continue
        succ = SUCCESSORS[f]
        if os.path.exists(os.path.join(outdir, succ)) and succ not in man:
            err("%s exists and manifest-C3.txt does not name it as %s's successor; stage C5 reads the "
                "manifest first" % (succ, f), shape="manifest:successor-unlisted", where=succ)
        if succ in man and not os.path.exists(os.path.join(outdir, succ)):
            err("manifest-C3.txt names %s and it is not in the output directory" % succ,
                shape="manifest:successor-absent", where=succ)


def check_successors(outdir):
    """A superseding file is whole (rule 18): one much shorter than the stage C2 file it supersedes
    is read downstream as the whole thing."""
    for f, succ in SUCCESSORS.items():
        sp = os.path.join(outdir, succ)
        if not os.path.exists(sp):
            continue
        n0 = len(text(outdir, f).split())
        n1 = len(text(outdir, succ).split())
        if n0 and n1 < n0 * 0.5:
            warn("%s is %d words against %s's %d; a superseding file is the whole file, not what changed "
                 "(rule 18)" % (succ, n1, f, n0))


def check_literature_arrows(rows, history):
    """Arrows whose mechanism the literature supplied: mechanism_C2 kept beside, the work named, and
    a stage-C3 history line."""
    logged = {str(r.get("id") or r.get("arrow") or r.get("element") or "") for r in history
              if str(r.get("stage")) == "C3" or str(r.get("leg", "")).startswith("C3")}
    n = 0
    for r in rows:
        if str(r.get("mechanism_source") or "").replace("_", "-") != "from-literature":
            continue
        n += 1
        aid = r.get("id")
        if not (r.get("mechanism_C2") or r.get("mechanism_07")):
            err("model/arrows.jsonl %s has mechanism_source from-literature and no mechanism_C2; the stage C2 "
                "sentence is kept beside the rewritten mechanism" % aid, shape="arrows:mechanism_C2", where=aid)
        if not any(r.get(k) for k in WORK_KEYS):
            warn("model/arrows.jsonl %s: the work the mechanism came from is not named on the line (work)"
                 % aid, shape="arrows:work", where=aid)
        if aid not in logged:
            err("model/arrows.jsonl %s was rewritten from the literature and model/history.jsonl carries no "
                "stage-C3 line for it" % aid, shape="arrows:no-C3-history", where=aid)
    return n


def check(root, outdir, ctx):
    stage = "C3"
    need(outdir, "literature-C3.md", "notes-C3.md", "manifest-C3.txt", "model/arrows.jsonl",
         "model/elements.jsonl", "model/history.jsonl", "fourth/fourth.jsonl", "dimensions.jsonl",
         "findings.jsonl")
    rooms = s7.frame_or_analysed(stage, "the rooms arrows name", outdir, ctx)
    t3, _ = vlib.load_scheme(outdir)
    if t3 is None:
        err("no scheme file is in the output directory (scheme_v2.jsonl); third-order ids were NOT resolved")
    findings = s7.check_findings(outdir, stage)
    t4, t4rows = s7.check_fourth(outdir, t3, stage)
    dims, _d = s7.check_dimensions(outdir, t4rows, stage)
    s7.check_tier_history(outdir, stage, t3, t4, dims)
    fps = s7.form_pass_ids(outdir)
    elements, _e = s7.check_elements(outdir, ctx, t3 or set(), t4, dims, findings, fps, stage)
    arrows, arows = s7.check_arrows(outdir, root, ctx, elements, rooms, stage)
    # the elements and arrows are C2's and entered by lines checked at C2, so every id is not
    # required to carry a line again; the lines present must still resolve and carry a move
    history = s7.check_history(outdir, stage, elements, arrows, require_all=False)
    nlit = check_literature_arrows(arows, history)

    lit = text(outdir, "literature-C3.md")
    if lit.strip():
        low = lit.lower()
        if "verified" not in low and "recalled" not in low:
            err("literature-C3.md marks no claim verified or recalled; every claim about the literature is "
                "one or the other (stage C3 section 2)")
        if "log" not in low or "check" not in low:
            warn("literature-C3.md does not say that the read log records what was served and not why, so "
                 "it cannot tell a check from a hunt (stage C3 section 1)")
    else:
        err("literature-C3.md is empty")
    notes = text(outdir, "notes-C3.md").lower()
    if notes:
        if "_cite_reads-C3" not in notes and "log point" not in notes:
            err("notes-C3.md does not record the log point (the line counts of _cite_reads-C3.jsonl and "
                "_mem_reads-C3.jsonl before the shelf was opened)")
        if "prior" not in notes:
            err("notes-C3.md does not restate what prior.md expected; it is read first and restated there")
    check_manifest(outdir)
    check_successors(outdir)

    leg3 = bool(re.search(r"four problems|##\s*5\b|leg 3", lit, re.I))
    mapping = check_mapping(outdir, t4)
    if mapping is None:
        if leg3:
            err("literature-C3.md carries the four-problems section and mapping-C3.jsonl is not written; the "
                "one written operation is one line per fourth-order theme (stage C3 section 5)")
        else:
            print("  mapping-C3.jsonl not yet written (leg 3's output)")
    else:
        low = lit.lower()
        if "richly" not in low or "thinly" not in low:
            warn("literature-C3.md does not say which of the four problems the structure reaches richly, "
                 "thinly and not at all (part 4); stage E1 inherits that paragraph")
        if "goal" not in low:
            warn("literature-C3.md says nothing of the goal (part 5)")
    print("  arrows %d (%d with a mechanism from the literature), fourth-order themes %d, mapping lines %d, "
          "successors: %s" % (len(arrows), nlit, len(t4), len(mapping or []),
                              ", ".join(s for s in SUCCESSORS.values() if os.path.exists(os.path.join(outdir, s))) or "none"))


# ---- the self-test fixture --------------------------------------------------------------------

def base(outdir, root):
    s7.base(outdir, root)
    s7._w(outdir, "literature-C3.md", "# literature\n\nWork X (verified) contradicts A01. The log records what "
          "was served and not why, so it cannot tell a check from a hunt.\n")
    s7._w(outdir, "notes-C3.md", "# notes\n\nThe literature is read after the model. prior.md expected calls. "
          "Log point: _cite_reads-C3.jsonl 0 lines, _mem_reads-C3.jsonl 3 lines.\n")
    s7._w(outdir, "manifest-C3.txt", "model.md: no successor\nstructure.md: no successor\nconcept.md: no successor\n")


def _plant_mapping_problem(outdir, root):
    base(outdir, root)
    s7._w(outdir, "literature-C3.md", "# literature\n\nWork X (verified).\n\n## 5. The four problems\n\nrichly: none; "
          "thinly: information. The goal was made. The log records what was served, not why: a check or a hunt.\n")
    s7._wj(outdir, "mapping-C3.jsonl", [{"fourth": "T4-001", "problem": "coordination", "why": "it allocates",
                                         "cannot_do": "no one can allocate"},
                                        {"fourth": "T4-002", "problem": "none", "why": "counting is not a problem"}])


def _plant_successor_unlisted(outdir, root):
    base(outdir, root)
    s7._w(outdir, "model-C3.md", "# model, after the literature\n\nP01 calls; K01 the border; A01 runs from P01 to K01. "
          "ungrounded relationships: none. looked-for-and-not-found: reward talk.\n")


def _plant_literature_arrow_unlogged(outdir, root):
    base(outdir, root)
    a = dict(s7.ARROW_ROW)
    a["mechanism_source"] = "from-literature"
    a["mechanism"] = "a call is a costly signal that recruits"
    a["work"] = "Spence 1973"
    s7._wj(outdir, "model/arrows.jsonl", [a])

PLANTED = [
    ("mapping problem outside the five", _plant_mapping_problem, "is not division|allocation|reward|information|none"),
    ("successor not in manifest", _plant_successor_unlisted, "manifest-C3.txt does not name it"),
    ("literature arrow without mechanism_C2", _plant_literature_arrow_unlogged, "no mechanism_C2"),
]
