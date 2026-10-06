#!/usr/bin/env python3
"""
read.py — the corpus reading tool.  Instrument v32.

The third tool.  `cite` grounds a quote, `emit` records a judgement, and this
serves the corpus.

Three properties, and they are the whole design:

  1. EVERYTHING IT RETURNS IS A VERBATIM SLICE OF corpus.txt.
     Nothing is re-rendered, re-wrapped, re-counted or re-ordered.  The
     renderer already decided what a triage window is and printed it; this
     tool hands back exactly those bytes.  Contract §10 — "do not recompute
     any of it" — applies to the harness too.

  2. `read` BECOMES DERIVED INSTEAD OF DECLARED.
     Every service is appended to out/_read.jsonl.  What the coder was shown
     is therefore a fact about the run rather than a claim in it: the
     instrument records its behaviour and not only its claim.

  3. IT RESUMES.
     State lives in the log, replayed on start, exactly as emit replays
     out/_journal.jsonl.  A refusal partway through costs one batch, not a
     run.

Reading is most of the coder's context.  Serving it in bounded batches is what
makes the cost per community fixed rather than a function of the largest
corpus.

--------------------------------------------------------------------------
CLI (this is how the coder calls it)

    python3 read.py CORPUS header
    python3 read.py CORPUS windows [n]        # the next n threads to triage
    python3 read.py CORPUS thread THREAD_ID   # one thread, whole
    python3 read.py CORPUS item ITEM_ID       # one item
    python3 read.py CORPUS state              # where you are
    python3 read.py CORPUS audit              # served vs declared

The log is always CORPUS's dir + /out/_read.jsonl. Calling `windows` again before you have
disposed of the current batch serves the NEXT batch, not the same one: the cursor advances on
serving, not on disposing, and what you were served is in your transcript, not in the tool.
(The environment variable READ_LOG_DIR moves the log; it is the scheduler's, not yours.)
--------------------------------------------------------------------------
"""

import argparse
import json
import os
import re
import sys
import time

INSTRUMENT = "v32"
VERSION = "read-v32"

SEP = "=" * 78

_THREAD_HEAD = re.compile(
    r"^thread (?P<n>\d+)/(?P<of>\d+)\s+(?P<tid>\S+)\s+"
    r"(?P<items>\d+) items\s+(?P<chars>\d+) chars\s+(?P<words>\d+) words\s+"
    r"(?P<title>.*)$",
    re.M,
)

# An item block opens with:  <id>  d<N> MM-DD HH:MM  <author>  ...
_ITEM_HEAD = re.compile(
    r"^(?P<iid>[A-Za-z0-9_]{3,12})  (?P<day>d-?\d+)\s+\d\d-\d\d \d\d:\d\d  ",
    re.M,
)

# Inside a TRIAGE WINDOW block, the three chosen replies are named one per line:
#    1   dfnyiav   its own   27 words,     1 items and     27 words beneath it   at +61
_WINDOW_REPLY = re.compile(r"^\s+\d+\s+([A-Za-z0-9_]{3,12})\s+", re.M)

# The header says so when the opening post is longer than the window shows:
#    TRIAGE WINDOW — the title above, the opening post (first 500 of its 615 words), ...
_OP_CAP = re.compile(r"opening post \(first (\d+) of its \d+ words\)")


class ReadError(Exception):
    pass


# ---------------------------------------------------------------- the reader


class Reader:
    def __init__(self, corpus_path, outdir=None):
        self.corpus_path = os.path.abspath(corpus_path)
        if not os.path.exists(self.corpus_path):
            raise ReadError("no corpus at %s" % self.corpus_path)
        self.outdir = os.path.abspath(
            outdir or os.path.join(os.path.dirname(self.corpus_path), "out")
        )
        os.makedirs(self.outdir, exist_ok=True)
        self.logpath = os.path.join(self.outdir, "_read.jsonl")
        self.idxpath = os.path.join(self.outdir, "_read_index.json")

        self._text = None
        self._index = None
        self._served = {}   # thread_id -> "triaged" | "batch_whole" | "full"
        self._cursor = 0    # next thread ordinal (0-based) not yet served
        self._seq = 0
        self._replay()

    def _allow_raw_read(self):
        """In branch B the case lead may first read raw items in step 5.

        Fleet slices have no local gate file, and branch A is unrestricted. The stage is
        append-only evidence, so this guard turns the E3 ordering rule into an executable one.
        """
        gate_path = os.path.join(self.outdir, "_gate.json")
        branch_b = False
        if os.path.exists(gate_path):
            try:
                branch_b = json.load(open(gate_path, encoding="utf-8")).get("branch") == "B"
            except (OSError, ValueError):
                pass
        else:
            run_dir = os.path.dirname(self.outdir)
            try:
                man = json.load(open(os.path.join(run_dir, "_manifest.json"), encoding="utf-8"))
                corpus = json.load(open(os.path.join(run_dir, "corpus_manifest.json"), encoding="utf-8"))
                branch_b = man.get("role") == "case lead" and corpus.get("items_in_window", 0) > 500
            except (OSError, ValueError):
                pass
        if not branch_b:
            return
        journal = os.path.join(self.outdir, "_journal.jsonl")
        stages = set()
        if os.path.exists(journal):
            with open(journal, encoding="utf-8") as fh:
                for line in fh:
                    try: row = json.loads(line)
                    except ValueError: continue
                    if row.get("kind") == "stage":
                        stages.add(row.get("stage"))
        if "step5_counter" not in stages:
            raise ReadError("branch-B case lead raw reads are locked until step 4 is complete "
                            "and emit.stage('step5_counter') has been recorded")

    # -- corpus text, loaded lazily so `state` and `audit` stay cheap --------

    @property
    def text(self):
        if self._text is None:
            with open(self.corpus_path, encoding="utf-8") as fh:
                self._text = fh.read()
        return self._text

    # -- the index ----------------------------------------------------------

    @property
    def index(self):
        """
        {
          "corpus_chars": int, "header": [a, b],
          "threads": [ {tid, n, items, chars, words, title,
                        head:[a,b], body:[a,b], has_window: bool} ],
          "items": { item_id: [a, b] },
        }
        Character offsets into corpus.txt.  Cached; rebuilt if the corpus
        changed size.
        """
        if self._index is not None:
            return self._index
        if os.path.exists(self.idxpath):
            try:
                with open(self.idxpath, encoding="utf-8") as fh:
                    cached = json.load(fh)
                if cached.get("corpus_chars") == len(self.text) and \
                   cached.get("version") == VERSION:
                    self._index = cached
                    return self._index
            except Exception:
                pass
        self._index = self._build_index()
        with open(self.idxpath, "w", encoding="utf-8") as fh:
            json.dump(self._index, fh)
        return self._index

    def _build_index(self):
        text = self.text
        cuts = [m.start() for m in re.finditer(re.escape(SEP), text)]
        if not cuts:
            raise ReadError("corpus has no thread separators — wrong file?")
        idx = {
            "version": VERSION,
            "corpus_chars": len(text),
            "corpus_path": self.corpus_path,
            "header": [0, cuts[0]],
            "threads": [],
            "items": {},
        }
        # after the header the file alternates: SEP head SEP body SEP head ...
        for k in range(0, len(cuts) - 1, 2):
            head_a = cuts[k] + len(SEP)
            head_b = cuts[k + 1]
            body_a = cuts[k + 1] + len(SEP)
            body_b = cuts[k + 2] if k + 2 < len(cuts) else len(text)
            head = text[head_a:head_b]
            m = _THREAD_HEAD.search(head)
            if not m:
                raise ReadError("unparseable thread header at char %d" % head_a)
            idx["threads"].append({
                "tid": m.group("tid"),
                "n": int(m.group("n")),
                "items": int(m.group("items")),
                "chars": int(m.group("chars")),
                "words": int(m.group("words")),
                "title": m.group("title").strip(),
                "head": [head_a, head_b],
                "body": [body_a, body_b],
                "has_window": "TRIAGE WINDOW" in head,
            })
            for im in _ITEM_HEAD.finditer(text, body_a, body_b):
                start = im.start()
                nxt = _ITEM_HEAD.search(text, im.end(), body_b)
                idx["items"][im.group("iid")] = [start, nxt.start() if nxt else body_b]
        return idx

    def _threads(self):
        return self.index["threads"]

    def _by_id(self, tid):
        for t in self._threads():
            if t["tid"] == tid:
                return t
        raise ReadError("no thread %r in this corpus" % tid)

    # -- the log ------------------------------------------------------------

    def _replay(self):
        if not os.path.exists(self.logpath):
            return
        with open(self.logpath, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                self._seq = max(self._seq, rec.get("seq", 0))
                if rec["kind"] == "windows":
                    self._cursor = max(self._cursor, rec["cursor_after"])
                    for tid, how in rec["served"]:
                        if self._served.get(tid) != "full":
                            self._served[tid] = how
                elif rec["kind"] == "thread":
                    self._served[rec["thread_id"]] = "full"

    def _log(self, kind, **payload):
        self._seq += 1
        rec = {"seq": self._seq,
               "t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "kind": kind, "tool": VERSION}
        rec.update(payload)
        with open(self.logpath, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return rec

    # -- what the coder calls ----------------------------------------------

    def header(self):
        self._allow_raw_read()
        """The block of `#` lines. Everything in it is exact; do not recompute it."""
        a, b = self.index["header"]
        out = self.text[a:b]
        self._log("header", chars=len(out))
        return out

    def _window_text(self, t):
        """
        The triage window's CONTENT for a thread the renderer indexed.

        The renderer's `TRIAGE WINDOW` block does not contain the window — it
        NAMES it: the three chosen reply ids, their sizes, and the line each
        begins at.  The text those ids point to lives in the thread body, and a
        coder reading the file top to bottom reads down into it and stops.

        The first version of this method served the block alone.  Three coders
        caught it independently on the same run and said the same thing: for any
        thread with more than three top-level replies they got the title and an
        index of ids, so 197 of 369 threads were triaged on the title.  That is
        precisely the failure this tool exists to prevent, introduced by the tool.

        So: header block, then the opening post — truncated to the word cap the
        header itself declares — then the three named replies, in corpus order.
        """
        ha, hb = t["head"]
        ba, bb = t["body"]
        head = self.text[ha:hb]
        want = _WINDOW_REPLY.findall(head)

        first = _ITEM_HEAD.search(self.text, ba, bb)
        parts = []
        if first:
            nxt = _ITEM_HEAD.search(self.text, first.end(), bb)
            post = self.text[first.start():(nxt.start() if nxt else bb)]
            cap = _OP_CAP.search(head)
            if cap:
                n_words = int(cap.group(1))
                toks = list(re.finditer(r"\S+", post))
                if len(toks) > n_words:
                    # cut at the character after the nth word, so what is served stays a
                    # verbatim prefix of the body rather than a rejoin of split tokens
                    post = post[:toks[n_words - 1].end()] + (
                        "\n\n   [... the opening post continues past the %d-word triage "
                        "window. call thread() to read it whole ...]\n\n" % n_words)
            parts.append(post)
        shown = [first.group("iid")] if first else []
        for iid in want:
            span = self.index["items"].get(iid)
            if span and ba <= span[0] < bb:
                parts.append(self.text[span[0]:span[1]])
                shown.append(iid)
        # the items the window actually showed, so emit can refuse a code on a reply the
        # coder never saw (a thread served as a window is coded only from these)
        self._last_window_items = shown
        return SEP + head + SEP + "\n" + "".join(parts)

    def windows(self, n=25, max_chars=20000):
        self._allow_raw_read()
        """
        The next `n` threads in corpus order, as triage material.

        A thread the renderer indexed is served as its window: the header block,
        the opening post to the declared word cap, and the three most-discussed
        top-level replies — the window §5 describes, as text.  A thread short
        enough that the renderer printed no window is served whole, because §5
        says so: "Where a thread is shorter than its window, there is nothing to
        decide: you have read it."

        Stops early at `max_chars` so a batch is never unbounded.  Advances the
        cursor only over what it actually returned.
        """
        threads = self._threads()
        if self._cursor >= len(threads):
            return "(no threads left — every thread in this corpus has been served)"
        start = self._cursor
        chunks, served, total = [], [], 0
        window_items = {}
        for t in threads[start:start + max(1, int(n))]:
            if t["has_window"]:
                piece = self._window_text(t)
                how = "triaged"
                window_items[t["tid"]] = list(self._last_window_items)
            else:
                ha, hb = t["head"]
                ba, bb = t["body"]
                piece = SEP + self.text[ha:hb] + SEP + self.text[ba:bb]
                # served whole, but inside a triage batch: the coder was triaging and may
                # honestly call this either "triaged" or "full". Both are true of it.
                how = "batch_whole"
            if chunks and total + len(piece) > max_chars:
                break
            chunks.append(piece)
            served.append([t["tid"], how])
            total += len(piece)
        self._cursor = start + len(chunks)
        for tid, how in served:
            if self._served.get(tid) != "full":
                self._served[tid] = how
        window_items = {k: v for k, v in window_items.items()
                        if any(k == tid for tid, _ in served)}
        self._log("windows", cursor_before=start, cursor_after=self._cursor,
                  n_requested=int(n), n_served=len(chunks),
                  served=served, chars=total, window_items=window_items)
        tail = ("\n\n--- %d of %d threads served. %d remain. "
                "call windows() again for the next batch. ---"
                % (self._cursor, len(threads), len(threads) - self._cursor))
        return "".join(chunks) + tail

    def thread(self, thread_id):
        self._allow_raw_read()
        """One thread, whole, verbatim. Call this on anything that touches the event."""
        t = self._by_id(thread_id)
        ha, hb = t["head"]
        ba, bb = t["body"]
        out = SEP + self.text[ha:hb] + SEP + self.text[ba:bb]
        self._served[thread_id] = "full"
        self._log("thread", thread_id=thread_id, items=t["items"], chars=len(out))
        return out

    def item(self, item_id):
        self._allow_raw_read()
        """One item, verbatim — for reading what find() returned, in §8."""
        span = self.index["items"].get(item_id)
        if span is None:
            raise ReadError("no item %r in this corpus" % item_id)
        out = self.text[span[0]:span[1]]
        self._log("item", item_id=item_id, chars=len(out))
        return out

    def served(self, thread_id):
        """"unread" | "triaged" | "batch_whole" | "full" — observed, not declared."""
        return self._served.get(thread_id, "unread")

    def state(self):
        threads = self._threads()
        full = sum(1 for v in self._served.values() if v in ("full", "batch_whole"))
        return {
            "tool": VERSION,
            "corpus": self.corpus_path,
            "threads_in_corpus": len(threads),
            "threads_served": len(self._served),
            "threads_served_whole": full,
            "threads_served_window_only": len(self._served) - full,
            "cursor": self._cursor,
            "threads_remaining": len(threads) - self._cursor,
            "next_thread": threads[self._cursor]["tid"] if self._cursor < len(threads) else None,
            "chars_served": self._chars_served(),
            "corpus_chars": self.index["corpus_chars"],
        }

    def _chars_served(self):
        if not os.path.exists(self.logpath):
            return 0
        tot = 0
        with open(self.logpath, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    tot += json.loads(line).get("chars", 0)
        return tot

    def audit(self):
        """
        Served against declared.  emit.thread(read=...) is a self-report; this
        is the record of what the harness actually handed over.  Any row here
        is a run that cannot support its own reading claim.
        """
        declared_path = os.path.join(self.outdir, "threads.jsonl")
        # v32: a fleet coder never calls emit.close(), so out/threads.jsonl does not exist in
        # its directory until the case lead consolidates. Read the journal's own thread
        # records instead, so the audit checks something before consolidation too.
        journal_path = os.path.join(self.outdir, "_journal.jsonl")
        source = None
        decls = []
        if os.path.exists(declared_path):
            source = "threads.jsonl"
            with open(declared_path, encoding="utf-8") as fh:
                decls = [json.loads(l) for l in fh if l.strip()]
        elif os.path.exists(journal_path):
            source = "_journal.jsonl"
            seen = {}
            with open(journal_path, encoding="utf-8") as fh:
                for l in fh:
                    l = l.strip()
                    if not l:
                        continue
                    j = json.loads(l)
                    if j.get("kind") == "thread" and isinstance(j.get("rec"), dict):
                        seen[j["rec"].get("thread_id")] = j["rec"]
            decls = list(seen.values())
        rows = []
        if decls:
            for d in decls:
                if True:
                    tid = d.get("thread_id")
                    decl = d.get("read")
                    got = self.served(tid)
                    # what the harness can actually see, ranked. A claim is a defect only
                    # when it asserts MORE reading than was served; understating is honest
                    # and is reported without failing.
                    rank = {"unread": 0, "triaged": 1, "batch_whole": 2, "full": 3}
                    # a thread served whole inside a triage batch satisfies BOTH readings,
                    # and the rank order alone would flag "full" on every short thread —
                    # exactly what the rule text below says is fine. Exempt it first.
                    if got == "batch_whole" and decl in ("triaged", "full"):
                        continue
                    if rank.get(decl, 0) > rank.get(got, 0):
                        rows.append({"thread_id": tid, "declared": decl, "served": got,
                                     "verdict": d.get("verdict"), "kind": "overstated"})
                    elif decl != got and not (got == "batch_whole" and decl in ("triaged", "full")):
                        rows.append({"thread_id": tid, "declared": decl, "served": got,
                                     "verdict": d.get("verdict"), "kind": "understated"})
        return {
            "checked": bool(decls),
            "source": source,
            "declared": len(decls),
            "mismatches": rows,
            "n_mismatches": len(rows),
            "rule": "a declaration may not claim more reading than read.py served. "
                    "'full' on a thread served window-only is the failure this check exists "
                    "for. A thread served whole inside a triage batch may honestly be "
                    "called either triaged or full, and neither is flagged.",
        }


# ---------------------------------------------------------------------- CLI


def main(argv=None):
    p = argparse.ArgumentParser(prog="read.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("corpus")
    p.add_argument("cmd", choices=["header", "windows", "thread", "item", "state", "audit"])
    p.add_argument("arg", nargs="?", default=None)
    p.add_argument("--max-chars", type=int, default=20000)
    a = p.parse_args(argv)

    try:
        r = Reader(a.corpus, os.environ.get("READ_LOG_DIR") or None)
        if a.cmd == "header":
            sys.stdout.write(r.header())
        elif a.cmd == "windows":
            sys.stdout.write(r.windows(int(a.arg) if a.arg else 25, a.max_chars))
        elif a.cmd == "thread":
            if not a.arg:
                raise ReadError("thread needs a thread_id")
            sys.stdout.write(r.thread(a.arg))
        elif a.cmd == "item":
            if not a.arg:
                raise ReadError("item needs an item_id")
            sys.stdout.write(r.item(a.arg))
        elif a.cmd == "state":
            sys.stdout.write(json.dumps(r.state(), indent=2, ensure_ascii=False))
        elif a.cmd == "audit":
            sys.stdout.write(json.dumps(r.audit(), indent=2, ensure_ascii=False))
        sys.stdout.write("\n")
    except ReadError as e:
        sys.stderr.write("ReadError: %s\n" % e)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
