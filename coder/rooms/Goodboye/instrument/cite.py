#!/usr/bin/env python3
"""cite.py — the coder's citation tool. Feasibility prototype for contract v3.

THE PROBLEM THIS SOLVES
-----------------------
The contract asks the coder for `(item_id, start, end)` plus the exact text between
them, and the harness verifies it afterwards. Two things make that unworkable as
written:

  1. An LLM cannot count characters. It would have to guess offsets, and guessed
     offsets fail.
  2. If the coder types the quote from memory, a single typo — a straightened
     apostrophe, a collapsed double space, a dropped emoji — makes an honest citation
     indistinguishable from a fabricated one.

So the coder must never produce offsets, and must never type the quote into the
output either.

THE INVERSION
-------------
The coder passes a quote it believes is in the item. The tool finds it and returns
BOTH the offsets and the exact substring cut from the body. The coder writes the
tool's return value into `codes.jsonl` verbatim. Therefore:

  * offsets are computed, never guessed
  * `text` is a slice of the body by construction, so it cannot disagree with it
  * a typo is an error the coder sees *while working*, with the nearest real text
    offered back, instead of an audit failure weeks later

Verification does not go away — the harness still re-checks every line independently,
because a tool the coder is trusted to have used is not evidence. What changes is
that a coder acting in good faith can no longer fail the check by accident. That is
the whole point: the check should catch fabrication, not clumsiness.

UNITS, STATED ONCE
------------------
Offsets are **Unicode code points into the decoded body string** — `json.loads` first,
then index. Not bytes, not UTF-16 units, not the escaped JSONL text. `len()` and
slicing in Python 3 use exactly this unit, so `body[start:end]` is the definition and
the implementation at the same time.
"""
import difflib
import json
import os
import re
import sys
import time
import unicodedata

INSTRUMENT = "v32"
VERSION = "cite-v32"


class Corpus:
    def __init__(self, path, querylog=None):
        self.corpus_path = os.path.abspath(path)
        self.items = {}
        self.meta = {}
        self.skipped_nonrecords = 0
        self.querylog = querylog or (os.path.splitext(path)[0] + ".queries.jsonl")
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)          # decode ONCE, here
                if "id" not in r:
                    # Harness metadata, not a record — the thread index is line 1 of the
                    # corpus. Skip anything without an `id` rather than matching on the
                    # key's name, so a later harness can add a line without breaking the
                    # tool the way the index once did.
                    self.skipped_nonrecords += 1
                    continue
                body = r.get("body")
                if body is None:
                    body = ((r.get("title") or "") +
                            ("\n\n" + r["selftext"] if r.get("selftext") else ""))
                self.items[r["id"]] = body
                self.meta[r["id"]] = {"thread": (r.get("link_id") or
                                                 ("t3_" + r["id"]))[3:],
                                      "kind": r.get("kind"),
                                      "created_utc": r.get("created_utc")}

    # ---- search, which is logged because the log is the evidence -----------
    def find(self, pattern, flags=re.I, context=60, limit=200):
        """Search item bodies. Every call is appended to the query log.

        The contract requires the coder to search *against* its own reading and to
        record what it tried. A query log the coder writes by hand is a claim; this
        one is a by-product of actually searching, which is the difference between
        evidence and assertion. It is also why the coder is told to search only
        through this function: an unlogged search is invisible, and an invisible
        search is how a reading list gets assembled out of expectations.

        Returns a list of {item_id, thread, start, end, snippet}.
        """
        gate_path = os.path.join(os.path.dirname(self.querylog), "out", "_gate.json")
        if not os.path.exists(gate_path):
            gate_path = os.path.join(os.path.dirname(os.path.abspath(self.querylog)), "_gate.json")
        branch_b = False
        if os.path.exists(gate_path):
            branch_b = json.load(open(gate_path, encoding="utf-8")).get("branch") == "B"
        else:
            run_dir = os.path.dirname(self.corpus_path)
            try:
                man = json.load(open(os.path.join(run_dir, "_manifest.json"), encoding="utf-8"))
                corpus = json.load(open(os.path.join(run_dir, "corpus_manifest.json"), encoding="utf-8"))
                branch_b = man.get("role") == "case lead" and corpus.get("items_in_window", 0) > 500
                if branch_b:
                    gate_path = os.path.join(run_dir, "out", "_gate.json")
            except (OSError, ValueError):
                pass
        if branch_b:
            outdir = os.path.dirname(gate_path)
            journal = os.path.join(outdir, "_journal.jsonl")
            stages = set()
            if os.path.exists(journal):
                with open(journal, encoding="utf-8") as fh:
                    for line in fh:
                        try: row = json.loads(line)
                        except ValueError: continue
                        if row.get("kind") == "stage": stages.add(row.get("stage"))
            if "step5_counter" not in stages:
                raise RuntimeError("branch-B case lead search is locked until step 4 is "
                                   "complete and emit.stage('step5_counter') is recorded")
        rx = re.compile(pattern, flags)
        hits = FindResult()
        hits.limit = limit
        scanned = 0
        for iid, body in self.items.items():
            scanned += 1
            m = rx.search(body)
            if not m:
                continue
            a = max(0, m.start() - context)
            b = min(len(body), m.end() + context)
            # `text` is the match itself and `thread_id` is spelled the way every other
            # tool in this instrument spells it. Three coders reported paying an extra
            # read.item() round trip per hit because a hit said which item matched and
            # not what matched; one of them chased eighteen false positives ("ally" inside
            # really, actually, anally, automatically) it could have dismissed on sight.
            hits.append({"item_id": iid,
                         "thread_id": self.meta[iid]["thread"],
                         "thread": self.meta[iid]["thread"],   # kept: older runs read this
                         "start": m.start(), "end": m.end(),
                         "text": body[m.start():m.end()],
                         "snippet": body[a:b]})
            if len(hits) >= limit:
                break
        hits.scanned = scanned
        hits.not_scanned = len(self.items) - scanned
        hits.truncated = hits.not_scanned > 0
        rec = {"t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "kind": "find", "tool": VERSION,
               "pattern": pattern, "n_items_matched": len(hits), "limit": limit,
               "items_scanned": scanned, "items_not_scanned": hits.not_scanned,
               "truncated": hits.truncated}
        with open(self.querylog, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return hits

    # ---- the only other function the coder calls ---------------------------
    def cite(self, item_id, quote, accept_near=False):
        """Return {'item_id','start','end','text'} or raise CiteError.

        `text` is cut from the body. Whatever the coder passed in is discarded.
        """
        if item_id not in self.items:
            raise CiteError(self._why_not_an_item(item_id))
        body = self.items[item_id]

        i = body.find(quote)
        if i >= 0:
            if body.count(quote) > 1:
                # ambiguous: same string twice in one body. Say so rather than
                # silently taking the first, which would put the offsets on a
                # different sentence than the coder meant.
                raise CiteError(
                    "%r occurs %d times in %s — extend the quote to make it unique"
                    % (quote[:40], body.count(quote), item_id))
            return self._span(item_id, body, i, i + len(quote), "exact")

        # not found: is it a normalisation difference or a real mistype?
        n_body, back = _norm_with_map(body)
        n_quote, _ = _norm_with_map(quote)
        j = n_body.find(n_quote)
        if j >= 0 and n_quote:
            if n_body.count(n_quote) > 1:
                raise CiteError(
                    "%r occurs %d times in %s once quotes and dashes are normalised — extend "
                    "the quote to make it unique" % (quote[:40], n_body.count(n_quote), item_id))
            start, end = back[j], back[j + len(n_quote) - 1] + 1
            return self._span(item_id, body, start, end, "normalised")

        near = _nearest(body, quote)
        if near and accept_near:
            return self._span(item_id, body, near[0], near[1], "nearest")
        raise CiteError(
            "not found in %s.\n  you passed : %r\n  nearest    : %r\n"
            "  ratio %.2f — fix the quote, or pass accept_near=True to take the "
            "nearest span" % (item_id, quote[:80],
                              body[near[0]:near[1]][:80] if near else None,
                              near[2] if near else 0.0))

    def _why_not_an_item(self, item_id):
        """Say what the caller passed instead of an item id, not just that it failed.

        Two writers have now passed something that is not an item id — one a thread id,
        one a username — and been told only "no item X in this corpus", which names the
        symptom and withholds the one thing that would fix it. A citation is against a
        single item's body, so a thread id can never resolve; saying which item of that
        thread to try is cheap and turns a dead end into a next call.
        """
        base = "no item %r in this corpus" % item_id
        if not isinstance(item_id, str):
            return base + ". cite() takes an item id as a string."

        members = [i for i, m in self.meta.items() if m.get("thread") == item_id]
        if members:
            members.sort(key=lambda i: self.meta[i].get("created_utc") or 0)
            return (base + ".\n  %r is a THREAD id, and a citation is against one item's "
                    "body.\n  its %d items begin %s — cite the item the words are in."
                    % (item_id, len(members), ", ".join(repr(i) for i in members[:3])))

        if re.fullmatch(r"[a-z0-9]{5,8}", item_id):
            # id-shaped and simply absent. Do not guess at what else it might be.
            return base + "."

        who = item_id.startswith(("u/", "/u/")) or bool(re.fullmatch(r"[A-Za-z0-9_-]{3,20}", item_id))
        return (base + ".\n  that is not an item id%s. cite() takes the id of the post or "
                "comment the words are in\n  — the id printed beside each item in the "
                "corpus, or the item_id a find() hit returns."
                % (" — it looks like a username" if who else ""))

    def _span(self, item_id, body, start, end, how):
        out = {"item_id": item_id, "start": start, "end": end,
               "text": body[start:end]}
        assert body[start:end] == out["text"]
        if how != "exact":
            out["cite_note"] = how
        return out

    def verify(self, rec):
        body = self.items.get(rec["item_id"])
        if body is None:
            return False, "unknown item"
        if not (0 <= rec["start"] <= rec["end"] <= len(body)):
            return False, "offsets out of range"
        got = body[rec["start"]:rec["end"]]
        return (got == rec["text"]), ("ok" if got == rec["text"]
                                      else "text != body[%d:%d]" % (rec["start"], rec["end"]))


class FindResult(list):
    """The hits, and whether the scan was complete. `truncated` is the point: a silently
    short result is how a reading ends up being a reading of a search pattern. Same shape as
    the aggregator's cite_case.FindResult."""
    truncated = False
    limit = None
    scanned = 0
    not_scanned = 0

    def __repr__(self):
        tail = ("  [TRUNCATED at limit=%s; %d items not scanned]"
                % (self.limit, self.not_scanned)) if self.truncated else ""
        return "<FindResult %d hits%s>" % (len(self), tail)


class CiteError(Exception):
    pass


_SMART = {"‘": "'", "’": "'", "“": '"', "”": '"',
          "–": "-", "—": "-", " ": " "}


def _fold_char(ch):
    """The normalised fallback's per-character fold.

    Exact matching always runs first, so a quote with correct diacritics or symbols
    resolves untouched. This fold fires only when exact match failed: it maps smart
    punctuation to plain, and DROPS any other non-ASCII character on both sides of the
    comparison — a quote full of decorative symbols could not be cited at all, and a batch
    was lost to superscript carets. Dropping symmetrically keeps
    Lithuanian and Arabic quotes safe: their exact path matches before this runs.
    """
    if ch in _SMART:
        return _SMART[ch]
    if ord(ch) < 128:
        return ch
    return ""


def _norm_with_map(s):
    """Fold the differences a careful human still gets wrong — smart quotes, NBSP,
    runs of whitespace, NFC — while keeping a map back to original indices."""
    out, idx = [], []
    prev_ws = False
    for k, ch in enumerate(s):
        ch = _fold_char(ch)
        ch = unicodedata.normalize("NFC", ch)
        if ch.isspace():
            if prev_ws:
                continue
            ch, prev_ws = " ", True
        else:
            prev_ws = False
        for c in ch:
            out.append(c)
            idx.append(k)
    return "".join(out), idx


def _nearest(body, quote, floor=0.75):
    """Best-matching window of body the same length as quote."""
    n = len(quote)
    if n == 0 or n > len(body):
        return None
    best = None
    step = max(1, n // 8)
    sm = difflib.SequenceMatcher(b=quote, autojunk=False)
    for i in range(0, len(body) - n + 1, step):
        sm.set_seq1(body[i:i + n])
        r = sm.quick_ratio()
        if best and r <= best[2]:
            continue
        r = sm.ratio()
        if not best or r > best[2]:
            best = (i, i + n, r)
    if best and best[2] >= floor:
        return best
    return None


USAGE = """cite.py RECORD.jsonl <item_id> '<the words you believe are there>'
cite.py RECORD.jsonl --find '<regex>' [limit]

A refusal prints `CiteError: ...` with the nearest span it could find and exits 2; that is the
tool saying your quote is wrong, not the tool breaking. Fix the quote or pick another passage.
(The Python call `cite(item_id, quote, accept_near=True)` takes the nearest span instead; the
shell form has no such flag, and a code that rests on words you did not type is a code you
must reread before you emit it.)

`find` is the second half of this module and §8 requires it — searching for evidence against
your own reading is not optional. It runs from the shell, so you do not have to import the
module to run the disconfirmation search."""


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help"):
        sys.stderr.write(USAGE + "\n")
        raise SystemExit(2)
    C = Corpus(sys.argv[1])
    try:
        if sys.argv[2] in ("--find", "-f", "find"):
            if len(sys.argv) < 4:
                sys.stderr.write(USAGE + "\n")
                raise SystemExit(2)
            limit = int(sys.argv[4]) if len(sys.argv) > 4 else 200
            print(json.dumps(C.find(sys.argv[3], limit=limit), ensure_ascii=False, indent=1))
        else:
            if len(sys.argv) < 4:
                sys.stderr.write("cite.py: a quote is required.\n" + USAGE + "\n")
                raise SystemExit(2)
            if len(sys.argv) > 4:
                sys.stderr.write("cite.py: the shell form takes one quote and no flags; "
                                 "extra arguments ignored: %r\n" % sys.argv[4:])
            print(json.dumps(C.cite(sys.argv[2], sys.argv[3]), ensure_ascii=False, indent=1))
    except CiteError as e:
        sys.stderr.write("CiteError: %s\n" % e)
        raise SystemExit(2)
