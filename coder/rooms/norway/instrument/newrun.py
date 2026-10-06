#!/usr/bin/env python3
"""
newrun.py — scaffold a coder run directory.  Instrument v32.

    python3 newrun.py RUNDIR SUB CORPUS_JSONL BRIEF_MD MODEL

Copies the instrument in, substitutes the placeholders in CONTRACT.md, AGENT.md and
CONTRACT-case-lead.md, renders corpus.txt, creates out/, writes corpus_manifest.json (the
counts the branch gate is decided on) and _manifest.json (the sha256 of every instrument file
as dispatched, so close_run.py can tell afterwards whether anything moved underneath the run).

The directory it builds is the case lead's. A fleet coder's directory is built from it by
`tools/fleet.py dispatch`, which calls `build_fleet()` below.

It also creates `out/_transcript.jsonl` as an EMPTY file. That is deliberate. The dispatcher
must write the agent's own turns into it before the run closes, and `close_run.py` C2 fails
while it is empty.

**The model is a condition of the reading.** `MODEL` is required and is written into the
manifest; a dispatcher that forgets it gets an error, not a plausible value.
"""

import hashlib
import json
import os
import shutil
import sys

INSTRUMENT = "v32"   # one integer, no decimals. see CHANGELOG-v32.md.
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = ["read.py", "cite.py", "emit.py", "close_run.py"]
TOOLDIR = ["tree_builder.py", "audit_fleet.py", "fleet.py"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# Every file that determines what a coder is asked to do or is able to do. The fingerprint
# below is computed from all of them, so it moves whenever any of them moves.
INSTRUMENT_FILES = ["CONTRACT.v32.md", "CONTRACT-case-lead.v32.md",
                    "CONTRACT-fleet-coder.v32.md", "AGENT.v32.md",
                    "read.py", "cite.py", "emit.py", "close_run.py",
                    "render_corpus_v32.py", "cut_window_v32.py", "render_openings_v32.py",
                    "tools/tree_builder.py", "tools/audit_fleet.py", "tools/fleet.py",
                    # the brief stage is the same instrument (v32, after the tools were aligned)
                    "CONTRACT-brief-writer.v32.md", "read_brief.py", "newbrief.py"]


def fingerprint():
    """A derived version stamp: the sha of every instrument file, so the stamp moves whenever
    any of them moves and nobody has to remember to bump it."""
    h = hashlib.sha256()
    for n in INSTRUMENT_FILES:
        p = os.path.join(HERE, n)
        h.update(n.encode())
        h.update(sha(p).encode() if os.path.exists(p) else b"-")
    return h.hexdigest()[:16]


def _substitute(src, dst, subs):
    s = open(src, encoding="utf-8").read()
    for k, v in subs.items():
        s = s.replace(k, v)
    left = sorted({k for k in subs if k in s} | set(_placeholders(s)))
    if left:
        raise SystemExit("unsubstituted placeholders in %s: %s" % (dst, left))
    open(dst, "w", encoding="utf-8").write(s)


def _placeholders(s):
    import re
    return re.findall(r"__[A-Z_]+__", s)


def _copy_tools(rundir):
    for t in TOOLS:
        shutil.copy2(os.path.join(HERE, t), os.path.join(rundir, t))
    os.makedirs(os.path.join(rundir, "tools"), exist_ok=True)
    for t in TOOLDIR:
        shutil.copy2(os.path.join(HERE, "tools", t), os.path.join(rundir, "tools", t))


def _render(record, sub):
    sys.path.insert(0, HERE)
    import render_corpus_v32 as RC
    return RC.render(record, RC.OPEN, RC.FRZ, sub,
                     ["2017-03-31 16:00", "2017-04-04 17:00"], RC.END)


def _manifest(rundir, sub, model, stats, contract_src, files, extra):
    man = {
        "instrument": INSTRUMENT,
        "instrument_fingerprint": fingerprint(),
        "model": str(model).strip(),
        "sub": sub,
        "window_utc": ["2017-03-31 16:00", "2017-04-04 17:00"],
        "window_hours": 97,
        "threads": stats["threads"],
        "items": stats["items"],
        "items_in_window": stats["items_in_window"],
        "contract_sha256": sha(contract_src),
        "sha256": {n: sha(os.path.join(rundir, n)) for n in files},
        "transcript_required": "out/_transcript.jsonl — the dispatcher writes it; "
                               "close_run.py C2 fails while it is empty",
        "instrument_dir": HERE,
    }
    man.update(extra)
    json.dump(man, open(os.path.join(rundir, "_manifest.json"), "w", encoding="utf-8"),
              indent=1)
    return man


def build(rundir, sub, corpus_jsonl, brief_md, model):
    """The case lead's directory: the whole record, the coder contract, the case lead's
    contract, AGENT.md, the three tools and tools/."""
    if not model or not str(model).strip():
        raise SystemExit("newrun.py needs the model the coder will run on. It is a "
                         "condition of the reading and v32 will not scaffold a run "
                         "without it.")
    rundir = os.path.abspath(rundir)
    os.makedirs(rundir, exist_ok=True)
    out = os.path.join(rundir, "out")
    os.makedirs(out, exist_ok=True)
    _copy_tools(rundir)
    record = os.path.join(rundir, "coder_corpus.jsonl")
    if os.path.abspath(corpus_jsonl) != os.path.abspath(record):
        shutil.copy2(corpus_jsonl, record)
    shutil.copy2(brief_md, os.path.join(rundir, "brief.md"))

    txt, stats = _render(record, sub)
    corpus_txt = os.path.join(rundir, "corpus.txt")
    open(corpus_txt, "w", encoding="utf-8").write(txt)
    # v32: the openings file, for the case lead only (build_fleet does not write one)
    import render_openings_v32 as RO
    ost = RO.write(record, sub, rundir)
    openings_note = ("openings.md  %d threads, %s chars%s" % (
        ost["threads"], "{:,}".format(ost["chars_full"]),
        ("; also openings_titles.md (%s chars) and openings_digest.md (%s chars): the room is large, "
         "CONTRACT-case-lead.md §1a says which to read" % ("{:,}".format(ost["chars_titles"]),
                                                            "{:,}".format(ost["chars_digest"])))
        if len(ost["files"]) > 1 else ""))
    stats["openings"] = ost
    # the counts the branch is decided on, written once, by the harness
    json.dump({"sub": sub, "threads": stats["threads"],
               "threads_with_inwindow_items": stats["threads_with_inwindow_items"],
               "items": stats["items"], "items_in_window": stats["items_in_window"],
               "items_by_people": stats["items_by_people"],
               "chars_by_people": stats["chars_by_people"],
               "note": "items_in_window excludes [CONTEXT] items; items_by_people and "
                       "chars_by_people also exclude accounts flagged automatic. The "
                       "branch gate reads items_in_window."},
              open(os.path.join(rundir, "corpus_manifest.json"), "w", encoding="utf-8"),
              indent=1)

    subs = {
        "__SUB__": sub,
        "__RUN_ID__": os.path.basename(os.path.abspath(rundir)),
        "__RUNDIR__": os.path.abspath(rundir),
        "__CORPUS__": corpus_txt,
        "__RECORD__": record,
        "__OPENINGS__": openings_note,
        "__BRIEF__": os.path.join(rundir, "brief.md"),
        "__OUTDIR__": out,
        "__READ__": os.path.join(rundir, "read.py"),
        "__CITE__": os.path.join(rundir, "cite.py"),
        "__EMIT__": os.path.join(rundir, "emit.py"),
        "__N_THREADS__": str(stats["threads"]),
        "__N_ITEMS__": str(stats["items"]),
        "__N_INWINDOW__": str(stats["items_in_window"]),
        "__INSTRUMENT__": INSTRUMENT,
        "__ROLE__": "case lead",
        "__ROLE_FILE__": "CONTRACT-case-lead.md",
        "__BATCH__": "-",
        "__SLICE__": "the whole record",
    }
    contract_src = os.path.join(HERE, "CONTRACT.v32.md")
    subs["__CONTRACT_SHA__"] = sha(contract_src)[:16]
    for src, dst in ((contract_src, "CONTRACT.md"),
                     (os.path.join(HERE, "AGENT.v32.md"), "AGENT.md"),
                     (os.path.join(HERE, "CONTRACT-case-lead.v32.md"), "CONTRACT-case-lead.md")):
        _substitute(src, os.path.join(rundir, dst), subs)
    open(os.path.join(out, "_transcript.jsonl"), "a").close()

    files = TOOLS + ["tools/" + t for t in TOOLDIR] + [
        "CONTRACT.md", "AGENT.md", "CONTRACT-case-lead.md", "corpus.txt",
        "coder_corpus.jsonl", "brief.md", "corpus_manifest.json"]
    man = _manifest(rundir, sub, model, stats, contract_src, files,
                    {"role": "case lead", "batch": None})
    return man, stats


def build_fleet(leaddir, batch, record_slice, model, code_id_start, pointer_id_start,
                slice_note):
    """A fleet coder's directory under <leaddir>/fleet/batch_NN/: its own slice as the
    record, rendered; the coder contract and the fleet coder's contract; AGENT.md; the
    three tools; brief.md, timeline.md and lexicon.md copied from the lead's out/ as they
    stand at dispatch. Its ids continue from the previous coder's."""
    leaddir = os.path.abspath(leaddir)
    sub = json.load(open(os.path.join(leaddir, "corpus_manifest.json")))["sub"]
    rundir = os.path.join(leaddir, "fleet", "batch_%02d" % batch)
    if os.path.exists(os.path.join(rundir, "out", "_journal.jsonl")):
        raise SystemExit("REFUSING: %s already has a journal; a batch is dispatched once"
                         % rundir)
    os.makedirs(rundir, exist_ok=True)
    out = os.path.join(rundir, "out")
    os.makedirs(out, exist_ok=True)
    _copy_tools(rundir)
    record = os.path.join(rundir, "coder_corpus.jsonl")
    if os.path.abspath(record_slice) != os.path.abspath(record):
        shutil.copy2(record_slice, record)
    for f in ("brief.md",):
        shutil.copy2(os.path.join(leaddir, f), os.path.join(rundir, f))
    for f in ("timeline.md", "lexicon.md"):
        src = os.path.join(leaddir, "out", f)
        if not os.path.exists(src):
            raise SystemExit("the lead's out/%s does not exist; the case lead starts it before "
                             "the first coder is dispatched" % f)
        shutil.copy2(src, os.path.join(rundir, f))

    txt, stats = _render(record, sub)
    corpus_txt = os.path.join(rundir, "corpus.txt")
    open(corpus_txt, "w", encoding="utf-8").write(txt)
    subs = {
        "__SUB__": sub,
        "__RUN_ID__": "%s/fleet/batch_%02d" % (os.path.basename(os.path.abspath(leaddir)), batch),
        "__RUNDIR__": os.path.abspath(rundir),
        "__CORPUS__": corpus_txt,
        "__RECORD__": record,
        "__OPENINGS__": "none: your slice carries the openings of earlier slices' threads that touch it, marked",
        "__BRIEF__": os.path.join(rundir, "brief.md"),
        "__OUTDIR__": out,
        "__READ__": os.path.join(rundir, "read.py"),
        "__CITE__": os.path.join(rundir, "cite.py"),
        "__EMIT__": os.path.join(rundir, "emit.py"),
        "__N_THREADS__": str(stats["threads"]),
        "__N_ITEMS__": str(stats["items"]),
        "__N_INWINDOW__": str(stats["items_in_window"]),
        "__INSTRUMENT__": INSTRUMENT,
        "__ROLE__": "fleet coder, batch %02d" % batch,
        "__ROLE_FILE__": "CONTRACT-fleet-coder.md",
        "__BATCH__": "%02d" % batch,
        "__SLICE__": slice_note,
    }
    contract_src = os.path.join(HERE, "CONTRACT.v32.md")
    subs["__CONTRACT_SHA__"] = sha(contract_src)[:16]
    for src, dst in ((contract_src, "CONTRACT.md"),
                     (os.path.join(HERE, "AGENT.v32.md"), "AGENT.md"),
                     (os.path.join(HERE, "CONTRACT-fleet-coder.v32.md"),
                      "CONTRACT-fleet-coder.md")):
        _substitute(src, os.path.join(rundir, dst), subs)
    open(os.path.join(out, "_transcript.jsonl"), "a").close()
    # timeline.md and lexicon.md are the coder's to extend, so they are not under C7's hash;
    # their state at dispatch is recorded beside it instead.
    files = TOOLS + ["tools/" + t for t in TOOLDIR] + [
        "CONTRACT.md", "AGENT.md", "CONTRACT-fleet-coder.md", "corpus.txt",
        "coder_corpus.jsonl", "brief.md"]
    man = _manifest(rundir, sub, model, stats, contract_src, files,
                    {"role": "fleet coder", "batch": "%02d" % batch,
                     "code_id_start": code_id_start, "pointer_id_start": pointer_id_start,
                     "slice": slice_note,
                     "facts_files_at_dispatch": {f: sha(os.path.join(rundir, f))
                                                 for f in ("timeline.md", "lexicon.md")}})
    return rundir, man, stats


if __name__ == "__main__":
    if len(sys.argv) != 6:
        raise SystemExit(__doc__)
    man, stats = build(*sys.argv[1:])
    print(json.dumps({"manifest": {k: v for k, v in man.items() if k != "sha256"},
                      "render": {k: v for k, v in stats.items()}}, indent=1))
