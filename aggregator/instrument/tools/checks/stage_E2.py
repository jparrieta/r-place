"""checks/stage_E2.py: the close-check of stage E2, the feedback, v38.

Written from stages/STAGE-E2-formalizing-feedback.md (its Outputs block, sections 1 and 2, its
Close). It checks the SHAPE, never whether the audit of the handling is fair:

  1. handling-E2.md (step E2a): four sections, by a heading word each (inconsistent, harder,
     helped, freedom), and at least one citation of a file or a transcript.
  2. next-instrument-E2.md (step E2b, required once the handback exists): present, and it reads
     the proposal (the word appears).
  3. notes-E2.md exists.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import err, warn, text, need

HANDLING_HEADS = (("inconsisten", "where what the handler, the principal investigator or the instrument said was inconsistent"),
                  ("harder", "what made the work harder"),
                  ("helped", "what helped"),
                  ("freedom", "where freedom was given and where it was taken"))


def check(root, outdir, ctx):
    need(outdir, "notes-E2.md")
    h = text(outdir, "handling-E2.md")
    if not h:
        err("handling-E2.md is absent; step E2a writes it (section 1)")
    else:
        heads = " ".join(l.lower() for l in h.split("\n") if l.startswith("#"))
        for word, what in HANDLING_HEADS:
            if word not in heads:
                err("handling-E2.md has no section on %s (a heading holding '%s'; section 1)" % (what, word))
        if not re.search(r"`[^`]+\.(md|jsonl|json|tsv|log|txt)`|_transcripts/|interviews/|harness-log/", h):
            err("handling-E2.md cites no file or transcript; every point it makes is cited (section 1)")
    n = text(outdir, "next-instrument-E2.md")
    final = os.path.exists(os.path.join(outdir, "handback-E2.md"))
    if not n:
        (err if final else warn)("next-instrument-E2.md is not written%s (step E2b, section 2)"
                                 % ("; the handback exists, so the stage cannot close without it" if final else " yet"))
    elif "proposal" not in n.lower():
        err("next-instrument-E2.md never reads the proposal; it is written against handling/proposal.md (section 2)")


# ---- the planted fixture ----------------------------------------------------------------------

HANDLING = ("# handling-E2\n\n## 1. Where what I was told was inconsistent\nThe stage B1 file and `_head.md` differ.\n\n"
            "## 2. What made the work harder\nx\n\n## 3. What helped\nx\n\n## 4. Freedom given and taken\nx\n")


def _w(outdir, name, txt):
    p = os.path.join(outdir, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(txt)


def base(outdir, root):
    _w(outdir, "notes-E2.md", "# notes-E2\n")
    _w(outdir, "handling-E2.md", HANDLING)
    _w(outdir, "next-instrument-E2.md", "# next-instrument-E2\n\nThe proposal promises a census; this run read it.\n")
    _w(outdir, "handback-E2.md", "# handback-E2\n")


def _plant_no_next(outdir, root):
    base(outdir, root)
    os.remove(os.path.join(outdir, "next-instrument-E2.md"))


def _plant_no_inconsistency(outdir, root):
    base(outdir, root)
    _w(outdir, "handling-E2.md", HANDLING.replace("inconsistent", "odd"))


def _plant_uncited(outdir, root):
    base(outdir, root)
    _w(outdir, "handling-E2.md", HANDLING.replace("`_head.md`", "the head"))


PLANTED = [
    ("the handback without the next instrument", _plant_no_next, "next-instrument-E2.md is not written"),
    ("handling without inconsistencies", _plant_no_inconsistency, "no section on where what the handler"),
    ("handling uncited", _plant_uncited, "cites no file or transcript"),
]
