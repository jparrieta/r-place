#!/usr/bin/env python3
"""Scripted stand-in for a brief writer, used only by selftest_brief.py.

It serves text exclusively through read_brief.py. A small fixture is exhausted with
thread() pages, including any partial-item continuations; a larger fixture is sampled until
every active day is touched. The output is deliberately sparse and clearly simulated.

    python3 simbrief.py <room>/brief
"""

import json
import os
import re
import subprocess
import sys


ITEM_HEAD = re.compile(r"^(?P<item_id>[A-Za-z0-9_]{3,20}) \| [^\n]*$", re.M)
PARTIAL = re.compile(
    r"\[PARTIAL item (?P<item_id>[A-Za-z0-9_]{3,20}) chars \d+:(?P<next>\d+)/\d+; ")
MORE_THREAD = re.compile(
    r"\[More thread items: thread (?P<thread_id>\S+) --offset (?P<next>\d+)\]")
SECTIONS = ["Vernacular", "Who talks", "Recurring formats", "Register",
            "Jokes with a history", "Moderation and its visible traces",
            "The week's shape", "What I could not tell", "Data problems"]


def rendered_items(text):
    """Return (item id, exact served body fragment) pairs from a reader response."""
    found = []
    for match in ITEM_HEAD.finditer(text):
        item_id = match.group("item_id")
        body_start = match.end() + (1 if text[match.end():match.end() + 1] == "\n" else 0)
        end_match = re.search(r"\n\[(?:END|PARTIAL) item %s(?: chars [^\]]+)?\]\n" %
                              re.escape(item_id), text[body_start:])
        if end_match:
            found.append((item_id, text[body_start:body_start + end_match.start()]))
    return found


def quote_candidates(text):
    for item_id, body in rendered_items(text):
        for line in body.splitlines():
            candidate = line.strip()
            if (len(candidate) >= 24 and candidate not in ("[deleted]", "[removed]")
                    and "`" not in candidate and not candidate.startswith("[")):
                yield item_id, candidate[:180]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        raise SystemExit(__doc__)

    bdir = os.path.abspath(argv[0])
    out = os.path.join(bdir, "out")
    os.makedirs(out, exist_ok=True)
    corpus = os.path.join(bdir, "brief_corpus.txt")
    record = os.path.join(bdir, "brief_corpus.jsonl")
    reader = os.path.join(bdir, "read_brief.py")
    cite = os.path.join(bdir, "cite.py")

    def rd(*args):
        result = subprocess.run(["python3", reader, corpus] + list(args),
                                capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError("read_brief %s failed (%d): %s" %
                               (" ".join(args), result.returncode, result.stderr.strip()))
        return result.stdout

    def get_state():
        return json.loads(rd("state"))

    rd("header")
    rd("titles", "50")

    # The synthetic harness may inspect the reader's index to enumerate a small fixture;
    # all body text still has to be returned by logged CLI reads before it can be quoted.
    sys.path.insert(0, bdir)
    from read_brief import BriefReader
    index = BriefReader(corpus)
    total_chars = sum(len(index._bodies[item_id]) for item_id in index.items)
    small = len(index.items) <= 64 and total_chars <= 180000
    served = []

    def finish_partial(text):
        for marker in list(PARTIAL.finditer(text)):
            item_id = marker.group("item_id")
            offset = int(marker.group("next"))
            while True:
                page = rd("item", item_id, "--offset", str(offset))
                served.append(page)
                next_marker = PARTIAL.search(page)
                if not next_marker:
                    break
                new_offset = int(next_marker.group("next"))
                if new_offset <= offset:
                    raise RuntimeError("item continuation did not advance for " + item_id)
                offset = new_offset

    if small:
        for thread_id in index.thread_ids:
            offset = 0
            while True:
                page = rd("thread", thread_id, "--offset", str(offset), "--limit", "50")
                served.append(page)
                finish_partial(page)
                more = MORE_THREAD.search(page)
                if not more:
                    break
                new_offset = int(more.group("next"))
                if new_offset <= offset:
                    raise RuntimeError("thread pagination did not advance for " + thread_id)
                offset = new_offset
    else:
        for _ in range(20):
            state = get_state()
            if not state.get("days_unseen"):
                break
            page = rd("sample", "7")
            served.append(page)
            finish_partial(page)

    state = get_state()
    active_days = state.get("days_with_items") or []
    if state.get("days_touched", 0) < len(active_days):
        raise RuntimeError("scripted reader did not cover every active day")
    if small and state.get("items_complete", 0) < state.get("items_in_corpus", 0):
        raise RuntimeError("scripted reader did not exhaust the small corpus")

    quote = None
    for item_id, candidate in quote_candidates("\n".join(served)):
        # Direct item service makes the quote's final logged span explicit even when it was
        # first encountered on a thread page.
        item_page = rd("item", item_id)
        for served_id, served_candidate in quote_candidates(item_page):
            result = subprocess.run(["python3", cite, record, served_id, served_candidate],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                quote = json.loads(result.stdout)
                break
        if quote:
            break
    if quote is None:
        raise RuntimeError("no citable quote was served by read_brief")

    rd("evidence")
    state = get_state()
    active_days = state.get("days_with_items") or []

    md = ("# Brief: scripted simulation\n\n"
          "**Simulated output — self-test only.**\n\n"
          "## Evidence base\n\n"
          "Reader receipt (state): %d of %d items complete across %d of %d active days.\n\n" %
          (state.get("items_complete", 0), state.get("items_in_corpus", 0),
           state.get("days_touched", 0), len(active_days)))
    for section in SECTIONS:
        md += "## %s\n\n" % section
        if section == "Vernacular":
            md += "> %s (`%s`)\n\n" % (quote["text"], quote["item_id"])
            md += "Simulated citation-validation text.\n\n"
        else:
            md += "Simulated nonempty test text; no substantive finding is asserted.\n\n"

    with open(os.path.join(out, "brief.md"), "w", encoding="utf-8") as fh:
        fh.write(md)
    with open(os.path.join(out, "_transcript.jsonl"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"role": "scripted", "kind": "simulation",
                             "text": "simbrief wrote the synthetic brief"}) + "\n")
    print("simbrief: simulated, 1 served quote, %d words, %d/%d active days" %
          (len(md.split()), state.get("days_touched", 0), len(active_days)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
