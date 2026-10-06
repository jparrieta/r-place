#!/usr/bin/env python3
"""Read-only, pre-consolidation checks for one v30 fleet-coder batch.

This file is copied into a dispatched batch as ``_scheduler_preflight.py`` and
run there by the coder.  Fleet coders may not call ``emit.close()`` and thus do
not have the exported JSONL files that the normal end-of-run gate consumes.
All checks below therefore replay the append-only journal directly.
"""

import json
from pathlib import Path
import re
import sys


SECTIONS = (
    "## Chronology",
    "## Relations",
    "## Posts against comments",
    "## Counter-reading",
    "## Saturation",
    "## Selection",
    "## Absence",
)
EDGE_TAG = re.compile(r"\[(closed|inherited|unresolved)\]")
READ_RANK = {"unread": 0, "triaged": 1, "batch_whole": 2, "full": 3}


def json_lines(path):
    rows = []
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError("%s:%d is not JSON: %s" % (path, number, exc))
            if not isinstance(row, dict):
                raise ValueError("%s:%d is not a JSON object" % (path, number))
            rows.append(row)
    return rows


def thread_of(item):
    if item.get("kind") == "post":
        return item.get("id")
    link = item.get("link_id") or ""
    return link[3:] if link.startswith("t3_") else None


def citable_text(item):
    # This is cite.py Corpus.__init__'s rule, copied here so importing cite.py
    # cannot create a query log or otherwise touch the coder's directory.
    body = item.get("body")
    if body is not None:
        return body
    title = item.get("title") or ""
    selftext = item.get("selftext")
    return title + (("\n\n" + selftext) if selftext else "")


def exact_citation(quote, records, expected_thread):
    if not isinstance(quote, dict):
        return False, "excluded_quote is not the dictionary returned by cite.py"
    required = {"item_id", "start", "end", "text"}
    if not required.issubset(quote):
        return False, "excluded_quote lacks %s" % sorted(required - set(quote))
    item = records.get(quote.get("item_id"))
    if item is None:
        return False, "excluded_quote names an item absent from coder_corpus.jsonl"
    if thread_of(item) != expected_thread:
        return False, "excluded_quote item belongs to thread %s" % thread_of(item)
    try:
        start, end = int(quote.get("start")), int(quote.get("end"))
    except (TypeError, ValueError):
        return False, "excluded_quote offsets are not integers"
    body = citable_text(item)
    text = quote.get("text")
    if not isinstance(text, str) or not text.strip():
        return False, "excluded_quote text is empty"
    if not (0 <= start < end <= len(body)) or body[start:end] != text:
        return False, "excluded_quote is not exact corpus text at its offsets"
    return True, ""


def served_reads(rows):
    served = {}
    for row in rows:
        if row.get("kind") == "windows":
            for pair in row.get("served") or []:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise ValueError("malformed served pair in out/_read.jsonl")
                tid, how = pair
                if served.get(tid) != "full":
                    served[tid] = how
        elif row.get("kind") == "thread":
            served[row.get("thread_id")] = "full"
    return served


def main():
    batch_dir = Path.cwd()
    required = [batch_dir / "_manifest.json", batch_dir / "coder_corpus.jsonl",
                batch_dir / "out" / "_journal.jsonl", batch_dir / "out" / "_read.jsonl"]
    missing = [str(path.relative_to(batch_dir)) for path in required if not path.is_file()]
    if missing:
        print("PREFLIGHT FAILED")
        for name in missing:
            print("- missing " + name)
        return 1

    failures = []
    try:
        manifest = json.loads(required[0].read_text(encoding="utf-8"))
        corpus_rows = json_lines(required[1])
        journal = json_lines(required[2])
        read_log = json_lines(required[3])
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("PREFLIGHT FAILED\n- " + str(exc))
        return 1

    if manifest.get("role") != "fleet coder":
        failures.append("_manifest.json does not identify a fleet coder")
    batch = str(manifest.get("batch", "")).zfill(2)
    meta = next((row for row in corpus_rows if isinstance(row.get("_slice"), dict)), {})
    slice_meta = meta.get("_slice") or {}
    if str(slice_meta.get("batch", "")).zfill(2) != batch:
        failures.append("corpus slice batch does not match the manifest")

    records = {row["id"]: row for row in corpus_rows if row.get("id")}
    # The metadata index contains exactly this batch's threads. Some of their opening
    # posts are themselves out of the 97-hour window and carry _context, so deriving
    # ownership from item flags would incorrectly discard valid slice threads.
    wanted = {row.get("thread_id") for row in meta.get("_thread_index", [])
              if row.get("thread_id")}
    if slice_meta.get("n_threads") is not None and len(wanted) != slice_meta.get("n_threads"):
        failures.append("derived slice has %d threads; metadata says %s" %
                        (len(wanted), slice_meta.get("n_threads")))

    dispositions = {}
    for row in journal:
        if row.get("kind") == "close":
            failures.append("journal contains emit.close(); fleet coders are forbidden to close")
        if row.get("kind") != "thread":
            continue
        rec = row.get("rec")
        if not isinstance(rec, dict) or not rec.get("thread_id"):
            failures.append("journal has a malformed thread disposition")
            continue
        tid = rec["thread_id"]
        if tid in dispositions:
            failures.append("thread %s has more than one disposition" % tid)
        dispositions[tid] = rec

    got = set(dispositions)
    if wanted - got:
        failures.append("%d slice threads lack dispositions: %s" %
                        (len(wanted - got), sorted(wanted - got)[:10]))
    if got - wanted:
        failures.append("%d dispositions are outside the slice: %s" %
                        (len(got - wanted), sorted(got - wanted)[:10]))

    retracted = {row.get("code_id") for row in journal if row.get("kind") == "retract"}
    live_code_threads = {
        row["rec"].get("thread_id") for row in journal
        if row.get("kind") == "code" and isinstance(row.get("rec"), dict)
        and not row["rec"].get("retracted")
        and row["rec"].get("code_id") not in retracted
    }
    empty_coded = sorted(tid for tid, rec in dispositions.items()
                         if rec.get("verdict") == "coded" and tid not in live_code_threads)
    if empty_coded:
        failures.append("coded threads have no LIVE code: %s" % empty_coded[:10])

    sizes = {}
    for item in records.values():
        if item.get("_context"):
            continue
        tid = thread_of(item)
        if tid:
            sizes[tid] = sizes.get(tid, 0) + 1
    for tid, rec in dispositions.items():
        if (rec.get("verdict") == "out_of_scope" and rec.get("read") != "unread"
                and sizes.get(tid, 0) >= 10):
            ok, why = exact_citation(rec.get("excluded_quote"), records, tid)
            if not ok:
                failures.append("thread %s: C5 exclusion citation: %s" % (tid, why))

    try:
        served = served_reads(read_log)
    except ValueError as exc:
        failures.append(str(exc))
        served = {}
    for tid, rec in dispositions.items():
        declared = rec.get("read")
        actual = served.get(tid, "unread")
        if actual == "batch_whole" and declared in ("triaged", "full"):
            continue
        if declared not in READ_RANK:
            failures.append("thread %s has invalid read=%r" % (tid, declared))
        elif READ_RANK[declared] > READ_RANK.get(actual, 0):
            failures.append("thread %s declares read=%s but read.py served %s" %
                            (tid, declared, actual))

    case = batch_dir / "out" / "case.md"
    notes = batch_dir / "out" / "notes.md"
    if not case.is_file() or case.stat().st_size < 500:
        failures.append("out/case.md is missing or under 500 bytes")
    else:
        content = case.read_text(encoding="utf-8")
        for section in SECTIONS:
            if section not in content:
                failures.append("out/case.md lacks " + section)
        if not EDGE_TAG.search(content):
            failures.append("out/case.md has no [closed], [inherited], or [unresolved] tag")
    if not notes.is_file() or notes.stat().st_size < 200:
        failures.append("out/notes.md is missing or under 200 bytes")

    # Export files prove an impermissible close in this pre-consolidation directory.
    exports = ["codes.jsonl", "themes.jsonl", "threads.jsonl", "pointers.jsonl", "_run.json"]
    present_exports = [name for name in exports if (batch_dir / "out" / name).exists()]
    if present_exports:
        failures.append("pre-consolidation exports exist (do not call emit.close): %s" % present_exports)

    if failures:
        print("PREFLIGHT FAILED (%d)" % len(failures))
        for failure in failures:
            print("- " + failure)
        print("Journal dispositions are append-only: do not append a replacement for a bad or duplicate disposition.")
        return 1
    print("PREFLIGHT PASSED: batch %s; %d/%d threads disposed, %d coded threads have LIVE codes; read audit and C5 citations pass; case/notes complete."
          % (batch, len(dispositions), len(wanted),
             sum(1 for rec in dispositions.values() if rec.get("verdict") == "coded")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
