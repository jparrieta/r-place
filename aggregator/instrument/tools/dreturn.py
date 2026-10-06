#!/usr/bin/env python3
"""dreturn.py, v38: the one rule set for stage D's returns (audit 2026-09-29, H11 and H13).

ingest.py applies it to each labeler's return before a room enters the ledger; checks/stage_D2.py
applies the same functions to what ingest compiled; handoff.py writes the verdict schema from it
and fleet.py validates the verdict readers' lines against that schema. A rule lives here once.

    OPS             each op's required fields in a labeler's line (RETURN-D.md §2, SCHEMA §2)
    KIND            the kind ingest computes from the op
    model_problems  the room model's rules (SCHEMA §5): end marker, grade, citations, ids, and
                    every adapted element named
    lift_of         the four-entry path of a source node through the placements at the model version
    VERDICT_*       the verdict reader's line (RETURN-D2v) and verdict_problems
"""
import re

# a labeler's line: the fields each op requires (`how` is the free text; `absent` takes `why`)
OPS = {
    "instantiate": ("element", "source", "how"),
    "absent": ("element", "why", "observation"),
    "add-condition": ("element", "source", "how"),
    "add-step": ("element", "source", "how"),
    "link": ("from", "to", "kind", "how"),
    "restrict": ("element", "source", "how"),
    "contradict": ("element", "statement", "how"),
    "propose": ("statement", "source", "how"),
    "none": ("how",),
}
OPTIONAL = ("condition", "statement", "source", "relation", "evidence", "why", "how", "element",
            "from", "to", "kind", "model_version", "origin", "labeler_run", "observation")
OBSERVATIONS = ("observed-absent", "not-needed", "unobserved", "not-testable")
LOCAL_STATUSES = ("validated", "unresolved", "insufficient-evidence")


def absence_problems(line, require_observation=True):
    """Silence is an epistemic state, never substantive evidence of absence."""
    if line.get("op") != "absent":
        return []
    observation = line.get("observation")
    if observation not in OBSERVATIONS:
        return ["absent requires observation in " + "|".join(OBSERVATIONS)] if require_observation else []
    if observation in ("observed-absent", "not-needed") and not (line.get("evidence") or {}).get("codes"):
        return ["evidenced absence or lack of need requires evidence.codes"]
    return []


def local_status_of(model):
    match = re.search(r"^local_status:\s*(\S+)", model or "", re.M)
    return match.group(1) if match and match.group(1) in LOCAL_STATUSES else None
KIND = {"instantiate": "specification", "absent": "specification", "add-condition": "elaboration",
        "add-step": "elaboration", "link": "elaboration", "restrict": "correction",
        "contradict": "correction", "propose": "proposal", "none": "none"}
# the ledger line ingest writes: the fields each op requires there (link's from is its source)
LEDGER_NEEDS = {"instantiate": ("element", "source", "how"), "absent": ("element", "how"),
                "add-condition": ("element", "source", "how"), "add-step": ("element", "source", "how"),
                "link": ("element", "source", "how"), "restrict": ("element", "source", "how"),
                "contradict": ("element", "statement", "how"), "propose": ("statement", "source", "how"),
                "none": ("how",)}
SOURCE_OPTIONAL = ("absent", "none", "contradict")
GRADES = ("composes", "composes-with-residue", "does-not-compose")
BRACKET = re.compile(r"\[(absent\s+)?([PKCRA]\d{2})\]")
CITE = re.compile(r"\[(c\d{4,5})\]")
DIM = re.compile(r"^D\d{1,2}$")


def one_sentence(s):
    s = " ".join((s or "").split())
    if not s or len(s.split()) > 40:
        return False
    body = s.rstrip(".!?")
    return not re.search(r"[.!?]\s", body)


def model_problems(model, sub, vocab_ids, room_codes, adapted, require_local=False):
    """The room model's rules (SCHEMA §5), as strings; empty when it passes. vocab_ids: the element and
    arrow ids the room was served; room_codes: the room's concept ids; adapted: the element ids its
    ledger adapts (ops other than none, dimensions aside)."""
    out = []
    if not model.rstrip().endswith("<!-- end -->"):
        out.append("rule 6: model-D.md has no end marker <!-- end -->")
    g = re.search(r"^grade:\s*(\S+)", model, re.M)
    if not g or g.group(1).strip() not in GRADES:
        out.append("rule 1: model-D.md has no grade line (composes | composes-with-residue | does-not-compose)")
    if require_local:
        local = re.search(r"^local_status:\s*(\S+)", model, re.M)
        status = local.group(1) if local else None
        if status not in ('validated', 'unresolved', 'insufficient-evidence'):
            out.append('rule 1: missing or invalid local_status')
        section = re.search(r'^## Local exceptions\s*\n(.+?)(?=^## |<!-- end -->|\Z)', model, re.M | re.S)
        if not section or not section.group(1).strip():
            out.append('rule 1: missing Local exceptions account')
        if status == 'validated' and g and g.group(1).strip() != 'composes':
            out.append('rule 1: validated local status conflicts with unresolved adapted grade')
    ids = {m.group(2) for m in BRACKET.finditer(model)}
    if vocab_ids is not None:
        bad = sorted(i for i in ids if i not in vocab_ids)
        if bad:
            out.append("rule 2: model-D.md cites ids not in VOCABULARY.json: %s" % ", ".join(bad[:6]))
    cites = {m.group(1) for m in CITE.finditer(model)}
    if not cites:
        out.append("rule 3: model-D.md carries no concept citation [cNNNN]")
    elif room_codes is not None:
        bad = sorted(c for c in cites if c not in room_codes)
        if bad:
            out.append("rule 3: model-D.md cites concepts not in r/%s: %s" % (sub, ", ".join(bad[:6])))
    missing = sorted(e for e in adapted if e and not DIM.match(str(e)) and e not in ids)
    if missing:
        out.append("SCHEMA §5: model-D.md never names adapted element(s) %s" % ", ".join(missing[:6]))
    return out


def grade_of(model):
    g = re.search(r"^grade:\s*(\S+)", model or "", re.M)
    return g.group(1).strip() if g and g.group(1).strip() in GRADES else None


def lift_of(sub, source, placed, fourth_of, dim_of, code_theme=None):
    """source: '<sub>:<theme_id>', '<theme_id>' or a concept id. The path [theme, T3, T4, D], null above an
    unplaced level; the first placement stands for a theme placed under more than one (rule 0)."""
    node = source.split(":", 1)[1] if ":" in source else source
    if code_theme and (sub, node) in code_theme:
        node = code_theme[(sub, node)] or node
    t3 = (placed.get((sub, node)) or [None])[0]
    t4 = fourth_of.get(t3) if t3 else None
    d = dim_of.get(t4) if t4 else None
    return ["%s:%s" % (sub, node), t3, t4, d]


# the verdict reader's line (RETURN-D2v)
VERDICTS = ("composes", "composes-with-residue", "does-not-compose", "cannot-tell")
THRESHOLDS = ("coded-share", "off-platform", "both", "missing-decisive-evidence", "conflicting-evidence", "other-evidence-limit")
VERDICT_REQUIRED = ("sub", "reader", "verdict", "themes", "concepts", "residue", "cannot_tell_under",
                    "sentence", "served")


def verdict_schema():
    """RETURN-D2v.schema.json: fleet.py checks the required keys on every line and reissues a line that
    lacks one."""
    return {"title": "RETURN-D2v", "type": "object", "required": list(VERDICT_REQUIRED),
            "properties": {"verdict": {"enum": list(VERDICTS)},
                           "cannot_tell_under": {"enum": list(THRESHOLDS) + [None]}}}


def verdict_problems(r, sub, room_themes=None, room_codes=None):
    """A reader's line against RETURN-D2v, as strings. residue lists theme or concept ids of the room."""
    out = []
    v = r.get("verdict")
    if v not in VERDICTS:
        out.append("verdict %r is not one of the four" % v)
    res = r.get("residue")
    if v == "composes-with-residue" and not res:
        out.append("composes-with-residue with no residue named")
    if v != "composes-with-residue" and res not in (None, [], ""):
        out.append("residue named on a verdict that is not composes-with-residue")
    ctu = r.get("cannot_tell_under")
    if v == "cannot-tell" and ctu not in THRESHOLDS:
        out.append("cannot-tell without a recognized cannot_tell_under evidence-limit reason")
    if v != "cannot-tell" and ctu not in (None, "null", ""):
        out.append("cannot_tell_under on a verdict that is not cannot-tell")
    if not str(r.get("sentence") or "").strip():
        out.append("no sentence")
    th, co = r.get("themes"), r.get("concepts", [])
    if not isinstance(th, list):
        out.append("themes is not a list of the room's second-order theme ids")
        th = []
    if not isinstance(co, list):
        out.append("concepts is not a list of the room's concept ids")
        co = []
    if room_themes is not None:
        bad = [t for t in th if str(t).split(":")[-1] not in room_themes]
        if bad:
            out.append("theme ids %s are not second-order themes of r/%s" % (bad[:4], sub))
    if room_codes is not None:
        bad = [c for c in co if str(c).split(":")[-1] not in room_codes]
        if bad:
            out.append("concept ids %s are not concepts of r/%s" % (bad[:4], sub))
    if room_themes is not None and room_codes is not None:
        bad = [x for x in (res or []) if str(x).split(":")[-1] not in room_themes
               and str(x).split(":")[-1] not in room_codes]
        if bad:
            out.append("residue ids %s are neither themes nor concepts of r/%s" % (bad[:4], sub))
    return out
