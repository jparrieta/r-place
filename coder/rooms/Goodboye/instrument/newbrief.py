#!/usr/bin/env python3
"""
newbrief.py — scaffold a brief-writer run.  Instrument v32.

    python3 newbrief.py BRIEFDIR SUB RAW24.jsonl MODEL

Cuts the seven days before the canvas opened out of a raw24 file, renders them WITHOUT triage
windows, copies in the tools, substitutes the contract, and writes a manifest.

Two things this fixes, both found by reading what the pipeline was actually doing rather than
what it was supposed to:

**Brief corpora were rendered with the coder's triage windows in them.** The window answers
"does this thread touch the event", which is meaningless in the seven days before the event
existed, and the brief writer's contract never mentioned triage — so the writer was handed an
instruction it had no way to adjudicate, telling it to stop reading threads in a week that
could not possibly touch the canvas. Rendered with `windows=False` now.

**The brief writer had no reading tool**, so it opened the corpus with a general file tool,
read as much as it liked, and left no record. It was the only agent in the pipeline whose
behaviour was entirely unobserved. It now gets `read_brief.py`, which serves the corpus,
samples for breadth across the week, and logs every service.
"""

import collections
import hashlib
import json
import os
import shutil
import sys

INSTRUMENT = "v32"
BRIEF_REVISION = "v32-brief-r1"
HERE = os.path.dirname(os.path.abspath(__file__))

OPEN = 1490976000                 # 2017-03-31 16:00 UTC, the canvas opens
PRE = OPEN - 7 * 86400            # 2017-03-24 16:00 UTC
LABEL = ["2017-03-24 16:00", "2017-03-31 16:00"]

EMPTY_BRIEF = """# Brief: r/%s, 2017-03-24 16:00 → 2017-03-31 16:00 UTC

**Harness-generated empty brief.**

The supplied pre-week archive contains no posts or comments in this window, so there are no
items from which to describe vernacular, participants, recurring formats, register, jokes,
moderation, or the week's shape.

This statement is limited to the supplied archive. It does not establish that the historical
collection is complete, and it makes no claim about what happened after the window.
"""


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def thread_of(r):
    if r.get("kind") == "post":
        return r["id"]
    li = r.get("link_id") or ""
    return li[3:] if li.startswith("t3_") else (li or "?")


def build(briefdir, sub, raw, model):
    if not model or not str(model).strip():
        raise SystemExit("newbrief.py needs the model the brief writer will run on. "
                         "It is a condition of the brief and v32 will not scaffold "
                         "one without it.")
    os.makedirs(briefdir, exist_ok=True)
    out = os.path.join(briefdir, "out")
    os.makedirs(out, exist_ok=True)

    items = []
    source_items = 0
    out_of_window_items = 0
    with open(raw, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                d = json.loads(line)
            except ValueError as exc:
                raise SystemExit("malformed JSON in %s at line %d: %s" %
                                 (raw, lineno, exc))
            if not isinstance(d, dict):
                raise SystemExit("non-object JSON record in %s at line %d" % (raw, lineno))
            if "id" not in d:
                continue
            source_items += 1
            created = d.get("created_utc")
            if not isinstance(created, (int, float)) or isinstance(created, bool):
                raise SystemExit("record %r in %s at line %d has invalid created_utc" %
                                 (d.get("id"), raw, lineno))
            if PRE <= created < OPEN:
                d.pop("_context", None)
                items.append(d)
            else:
                out_of_window_items += 1

    if not items:
        # Preserve a local record even when the filtered source is empty. The metadata line
        # distinguishes a verified zero-item record from a failed or truncated copy.
        rec = os.path.join(briefdir, "brief_corpus.jsonl")
        source_sha = sha(raw)
        with open(rec, "w", encoding="utf-8") as fh:
            fh.write(json.dumps({"_n_threads": 0, "_n_items": 0,
                                 "_window_utc": LABEL, "_segment": "pre",
                                 "_source_items": source_items,
                                 "_out_of_window_items": out_of_window_items,
                                 "_source_sha256": source_sha},
                                ensure_ascii=False) + "\n")

        brief_path = os.path.join(out, "brief.md")
        with open(brief_path, "w", encoding="utf-8") as fh:
            fh.write(EMPTY_BRIEF % sub)

        record_sha = sha(rec)
        man = {"instrument": INSTRUMENT, "brief_revision": BRIEF_REVISION,
               "kind": "harness", "sub": sub, "model": str(model).strip(),
               "window_utc": LABEL, "preweek_items": 0, "preweek_threads": 0,
               "source_items": source_items,
               "out_of_window_items": out_of_window_items,
               "brief": "harness-written; supplied pre-week archive contains no items",
               "source_record": {"path": "brief_corpus.jsonl", "sha256": record_sha,
                                 "input_sha256": source_sha},
               "sha256": {"brief_corpus.jsonl": record_sha,
                          "out/brief.md": sha(brief_path)}}
        with open(os.path.join(briefdir, "_manifest.json"), "w", encoding="utf-8") as fh:
            json.dump(man, fh, indent=1)
        return {"sub": sub, "items": 0, "threads": 0, "brief": "harness"}

    items.sort(key=lambda r: r["created_utc"])
    rec = os.path.join(briefdir, "brief_corpus.jsonl")
    th = collections.Counter(thread_of(r) for r in items)
    with open(rec, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"_n_threads": len(th), "_n_items": len(items),
                             "_window_utc": LABEL, "_segment": "pre"},
                            ensure_ascii=False) + "\n")
        for r in items:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    sys.path.insert(0, HERE)
    import render_corpus_v32 as RC
    txt, stats = RC.render(rec, PRE, OPEN, sub, LABEL, OPEN, windows=False)
    lines = txt.split("\n")
    lines[1] = ("# window 2017-03-24 16:00 -> 2017-03-31 16:00  "
                "(the seven ordinary days before the event; d0 is 03-24, not the canvas)")
    corpus = os.path.join(briefdir, "brief_corpus.txt")
    open(corpus, "w", encoding="utf-8").write("\n".join(lines))

    for t in ("read_brief.py", "cite.py"):
        shutil.copy2(os.path.join(HERE, t), os.path.join(briefdir, t))

    subs = {"__SUB__": sub, "__CORPUS__": corpus, "__OUTDIR__": out,
            "__READBRIEF__": os.path.join(briefdir, "read_brief.py"),
            "__CITE__": os.path.join(briefdir, "cite.py"),
            "__INSTRUMENT__": INSTRUMENT}
    src = os.path.join(HERE, "CONTRACT-brief-writer.v32.md")
    s = open(src, encoding="utf-8").read()
    for k, v in subs.items():
        s = s.replace(k, v)
    left = [k for k in subs if k in s]
    if left:
        raise SystemExit("unsubstituted placeholders: %s" % left)
    open(os.path.join(briefdir, "CONTRACT.md"), "w", encoding="utf-8").write(s)

    man = {"instrument": INSTRUMENT, "brief_revision": BRIEF_REVISION,
           "kind": "writer", "sub": sub,
           # **Which model wrote the brief.** Required from v28.
           "model": str(model).strip(),
           "window_utc": LABEL, "preweek_items": stats["items"],
           "preweek_threads": stats["threads"], "preweek_chars": stats["chars"],
           "reference_tokens": 25000, "hard_ceiling_tokens": 75000,
           "sha256": {n: sha(os.path.join(briefdir, n))
                      for n in ("read_brief.py", "cite.py", "CONTRACT.md",
                                "brief_corpus.txt", "brief_corpus.jsonl")}}
    json.dump(man, open(os.path.join(briefdir, "_manifest.json"), "w"), indent=1)
    return {"sub": sub, "items": stats["items"], "threads": stats["threads"],
            "chars": stats["chars"], "brief": "writer"}


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit(__doc__)
    print(json.dumps(build(*sys.argv[1:5]), indent=1))
