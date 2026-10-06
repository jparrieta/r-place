"""checks/stage_C4.py: the close-check of stage C4, the field, v38 (added 2026-09-27).

Written from stages/STAGE-C4-model-the-field.md. It checks the SHAPE of the stage's files:
field-C4.md, once field/ has arrived, carrying the three lists; every entry marked from-field
with a model/history.jsonl line; manifest-C4.txt when the stage wrote a successor. It cannot
check whether a reading of the field is right.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vlib import err, warn, jsonl, text, need
try:
    from checks import stage_C3 as s8
except ImportError:
    import stage_C3 as s8
s7 = s8.s7
SUCCESSORS = {"model": "model-C4.md", "structure": "structure-C4.md", "concept": "concept-C4.md"}


def check_field(outdir):
    """Stage C4: the return to the field. field-C4.md is required once field/ has
    arrived; before that its absence is reported and not failed. A field-C4.md saying the field was
    not held passes. Every entry marked from-field must carry a model/history.jsonl line."""
    held = os.path.isdir(os.path.join(outdir, "field"))
    ft = text(outdir, "field-C4.md")
    low = ft.lower()
    if not held:                 # the field did not arrive: the file says so, and why (section 1)
        if "not held" not in low:
            err("field/ has not arrived and field-C4.md does not say the field was not held and why (stage C4 "
                "section 1)", shape="field:not-held")
        else:
            print("  field-C4.md: the field was not held")
        return 0
    if not ft.strip():
        err("field/ has arrived and field-C4.md is not written; it carries the three lists (stage C4 section 2)",
            shape="field:missing")
        return 0
    for word, part in (("agree", "1, where the two agree"), ("only the field", "2, what only the field sees"),
                       ("disagree", "3, where they disagree")):
        if word not in low:
            warn("field-C4.md does not carry list %s (stage C4 section 2)" % part)
    ids = set()
    for f in ("model/elements.jsonl", "model/arrows.jsonl"):
        for r in jsonl(os.path.join(outdir, f)) or []:
            if r.get("origin") == "from-field" or r.get("status") == "tentative":
                i = r.get("id")
                ids.add(i)
                if r.get("origin") != "from-field" or r.get("status") != "tentative":
                    err("%s %s: a field entry is origin from-field and status tentative, both (stage C4 section 2)"
                        % (f, i), shape="field:tentative", where=str(i))
                if not r.get("field_support"):
                    err("%s %s enters from the field with no field_support (the field's threads or items that "
                        "show it)" % (f, i), shape="field:support", where=str(i))
    for r in jsonl(os.path.join(outdir, "fourth/fourth.jsonl")) or []:
        if "from-field" in str(r.get("origin", "")) + str(r.get("source", "")):
            err("fourth/fourth.jsonl %s is marked from-field; a fourth-order theme never enters from the field, "
                "since no room can answer a grouping (stage C4 section 2)" % r.get("id"), shape="field:fourth",
                where=str(r.get("id")))
    hist = set()
    for r in (jsonl(os.path.join(outdir, "model/history.jsonl")) or []):
        for k in ("id", "element", "arrow", "ids"):
            v = r.get(k) if isinstance(r, dict) else None
            hist.update(str(x) for x in (v if isinstance(v, list) else [v]) if x)
    for i in sorted(x for x in ids if x):
        if i not in hist:   # the id itself, not a substring of another (audit 2026-09-29b)
            err("%s is marked from-field and has no model/history.jsonl line (stage C4 section 2)" % i,
                shape="field:history", where=str(i))
    return len(ids)



def check(root, outdir, ctx):
    need(outdir, "notes-C4.md", "model/arrows.jsonl", "model/history.jsonl", "fourth/fourth.jsonl")
    n = check_field(outdir)
    wrote = [f for f in SUCCESSORS.values() if os.path.exists(os.path.join(outdir, f))]
    if wrote and not os.path.exists(os.path.join(outdir, "manifest-C4.txt")):
        err("stage C4 wrote %s and manifest-C4.txt is missing; stage C5 reads it first" % ", ".join(wrote),
            shape="manifest-C4", where="manifest-C4.txt")
    man = text(outdir, "manifest-C4.txt")
    for f in wrote:
        if f not in man:
            err("%s is written and manifest-C4.txt does not name it" % f, shape="manifest-C4:unlisted", where=f)
    print("  entries from the field: %d; successors: %s" % (n, ", ".join(wrote) or "none"))


# ---- the self-test fixture --------------------------------------------------------------------

def base(outdir, root):
    s8.base(outdir, root)
    s7._w(outdir, "notes-C4.md", "# notes\n\nThe field did not arrive.\n")
    s7._w(outdir, "field-C4.md", "The field was not held: the handler had no field package.\n")


def _plant_field_entry_unlogged(outdir, root):
    base(outdir, root)
    a = dict(s7.ARROW_ROW)
    a["id"] = "A09"
    a.update(origin="from-field", status="tentative", field_support=["r/place thread 62abcd"])
    s7._wj(outdir, "model/arrows.jsonl", [a])
    os.makedirs(os.path.join(outdir, "field"), exist_ok=True)
    s7._w(outdir, "field-C4.md", "Where the two agree: ... What only the field sees: ... Where they disagree: ...\n")


def _plant_field_not_tentative(outdir, root):
    base(outdir, root)
    a = dict(s7.ARROW_ROW)
    a["id"] = "A09"
    a.update(origin="from-field", status="standing", field_support=["r/place thread 62abcd"])
    s7._wj(outdir, "model/arrows.jsonl", [a])
    s7._wj(outdir, "model/history.jsonl", [{"id": "A09", "move": "entered from the field"}])
    os.makedirs(os.path.join(outdir, "field"), exist_ok=True)
    s7._w(outdir, "field-C4.md", "Where the two agree: ... What only the field sees: ... Where they disagree: ...\n")


def _plant_field_unread(outdir, root):
    base(outdir, root)
    os.makedirs(os.path.join(outdir, "field"), exist_ok=True)
    s7._w(outdir, "field-C4.md", "")


def _plant_successor_unlisted(outdir, root):
    base(outdir, root)
    s7._w(outdir, "model-C4.md", "# model after the field\n")
    s7._w(outdir, "manifest-C4.txt", "model.md: no successor\n")


PLANTED = [
    ("field entry without a history line", _plant_field_entry_unlogged, "is marked from-field and has no model/history.jsonl line"),
    ("a field entry not tentative", _plant_field_not_tentative, "origin from-field and status tentative, both"),
    ("the field arrived and not read", _plant_field_unread, "field-C4.md is not written"),
    ("C4 successor not in manifest", _plant_successor_unlisted, "manifest-C4.txt does not name it"),
]
