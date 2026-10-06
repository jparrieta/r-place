#!/usr/bin/env python3
"""emit.py — the coder's output tool. Companion to cite.py; cite.py is not modified.

CALLS (a Python API; construct once, AGENT.md has the setup block)
    emit = Emit(OUTDIR, corpus_path=RECORD)
    emit.stage(name)                                   # before each step; see CONTRACT §9
    emit.code(cited, first_order, thread_id, exchange_id=None, note="")   -> code_id
    emit.pointer(cited, raw, kind, thread_id, normalised=None, relation="mentioned-only",
                 moved="no", what_still_returns=None, what_you_cannot_see=None,
                 code_ids=None, note="")                                  -> pointer_id
    emit.thread(thread_id, read, verdict, reason, excluded_quote=None)    -> reading tally
    emit.threads_bulk(rows)                            # rows: dicts with the same keys
    emit.theme(label, theme_note, code_ids, regrouped_from=None)          -> theme_id
    emit.theme_add(theme_id, code_ids)
    emit.retract(code_id, reason)
    emit.reading()                                     # the tally, on demand
    emit.close(verdict=None)                           # case lead only; verdict none|trace|full
`cited` is always what cite() returned, unchanged. Every call is journalled and checked as it
arrives; a refusal names its reason.

WHAT IT IS FOR
--------------
The coder writes `case.md` and `notes.md`. Everything else — the codes, the themes, the
thread dispositions, the pointers — is built here from calls made while working, so the
coder never opens an output file, never formats a line and never computes a count.

The design rule from the renderer applies unchanged: *if a step's output is a number,
the agent is never the thing that computes it.* This extends it one step. **If a step's
output is a file, the agent is never the thing that formats it.**

WHAT THIS BUYS BESIDES TOKENS, WHICH IS THE REAL POINT
------------------------------------------------------
`discovered_at` used to be self-reported: the coder wrote its files at the end and
labelled its own codes "step3" or "step5" from memory. A zero could then mean the
counter-reading found nothing, or that it found something and mislabelled it, and
nothing in the record could tell the two apart.

Here the agent declares a stage once, by calling stage(), and **the harness stamps every
subsequent code with the stage that was current when it was minted.** The coder cannot
label a code; it can only mint one, and when it does is observed. So:

  * `discovered_at` becomes a measurement instead of a claim

  * "how far into your reading did the last new code appear" — the first of §8's two
    saturation statements — is computed from the journal, not remembered
  * the counter-reading can be audited on every run, forever, with no special test

APPEND-ONLY IS WRITE-ONCE
-------------------------
Rule 10 exists so that nothing is revised: the coder works in its own notes and commits
at the end. A journal preserves that guarantee more strictly than writing at the end
does, because an appended record cannot be edited at all — not even by an agent that
changes its mind while writing. The output files are materialised once, by close(),
from the journal. The coder never opens them.

THE JOURNAL IS THE EVIDENCE
---------------------------
Every call appends one line to `_journal.jsonl` with a sequence number, a timestamp and
the stage that was current. That file is a by-product of working, not a report about
working, which is the same reason find() logs its own queries. If the journal and the
final outputs ever disagree, the journal is right.
"""
import json
import os
import time

# step5_counter is bounded deliberately. It covers the disconfirmation search and
# nothing else. Writing the account is step6_account, and clerical minting during the
# write-up therefore cannot masquerade as late discovery — which is exactly what the
# first v8 run did: 42 codes stamped step5, none of them from the counter-reading.
INSTRUMENT = "v32"        # contract, read, cite, emit and renderer all carry this
VERSION = "emit-v32"

STAGES = ["step1_brief", "step2_read", "step3_codes", "step4_themes",
          "step5_counter", "step6_account", "step7_write"]


class EmitError(Exception):
    pass


def _resolve_record(path):
    """
    Return the JSONL record file, whatever the coder handed us.

    AGENT.md calls `corpus.txt` "your corpus" and calls `coder_corpus.jsonl` the file you
    never open. So the natural guess is `Emit(outdir, corpus_path=corpus.txt)` — and until
    now that guess raised `JSONDecodeError` on the rendered header's first `#` line. Three
    coders hit it. Documentation was added telling
    them the right path; that is worth having, but a constructor that only accepts the file
    the coder is told not to open, and crashes on the one it is told to read, is a trap
    regardless of what the documentation says.

    Both are now accepted. Neither is required — the header index is what lets reading be
    reported as a fraction rather than a bare count, and a run without it is degraded, not
    broken.
    """
    if not path:
        return None
    if path.endswith(".jsonl") and os.path.exists(path):
        return path
    here = os.path.dirname(os.path.abspath(path))
    for cand in (os.path.join(here, "coder_corpus.jsonl"),
                 os.path.splitext(path)[0] + ".jsonl"):
        if os.path.exists(cand):
            return cand
    return path if os.path.exists(path) else None


class Emit:
    def __init__(self, outdir, corpus_path=None):
        self.outdir = outdir
        os.makedirs(outdir, exist_ok=True)
        self.journal = os.path.join(outdir, "_journal.jsonl")
        self.corpus_path = _resolve_record(corpus_path)
        self.corpus_path_given = corpus_path
        self.stage_now = None
        self.seq = 0
        self.codes = []
        self.themes = []
        self.threads = []
        self.pointers = []
        self._stage_marks = []
        self._close_records = []
        self._verdict = None
        self._rec = None
        self._rec_threads = {}
        self._corpus_thread_items = None
        # v29, the fleet. A fleet coder's run directory carries `_manifest.json` with
        # `batch` and `code_id_start`: its ids continue where the previous coder's ended,
        # so the pooled codes of one community stay unique without anybody renumbering
        # them. A single-reading run has neither key and starts at c0001 as before.
        self.batch = None
        self.code_start = 1
        self.pointer_start = 1
        self.slice_context = set()
        man_path = os.path.join(os.path.dirname(os.path.abspath(outdir)), "_manifest.json")
        if os.path.exists(man_path):
            try:
                man = json.load(open(man_path, encoding="utf-8"))
                self.batch = man.get("batch")
                self.code_start = int(man.get("code_id_start") or 1)
                self.pointer_start = int(man.get("pointer_id_start") or 1)
            except (ValueError, OSError):
                pass
        # The corpus header already knows every thread's item count, character count
        # and cumulative share. Reading it here is what lets reading be reported as a
        # fraction of something, instead of as a bare count with no denominator.
        self._replay()
        self.index = {}
        self.index_source = None
        if self.corpus_path and os.path.exists(self.corpus_path):
            try:
                with open(self.corpus_path, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            r = json.loads(line)
                        except ValueError:
                            # a rendered corpus, or anything else that is not JSONL. The
                            # index is an optimisation; refuse to die for it.
                            break
                        if "id" in r:
                            break
                        for t in (r.get("_thread_index") or []):
                            self.index[t["thread_id"]] = t
                if self.index:
                    self.index_source = self.corpus_path
            except OSError:
                pass
            # items a fleet coder is given as context from an earlier slice. Quotable in
            # prose, never coded: their codes belong to whoever held that slice.
            try:
                with open(self.corpus_path, encoding="utf-8") as f:
                    for line in f:
                        if '"_slice_context"' not in line:
                            continue
                        try:
                            r = json.loads(line)
                        except ValueError:
                            continue
                        if r.get("_slice_context") and r.get("id"):
                            self.slice_context.add(r["id"])
            except OSError:
                pass

    def _replay(self):
        """Rebuild state from the journal.

        The coder works across many separate processes — every shell call is a fresh
        interpreter — so state cannot live in memory. The journal is the state. This
        reads it back on construction, which makes `Emit(outdir, corpus)` resumable
        and idempotent: the coder constructs one whenever it needs one and carries on
        from wherever it actually got to.
        """
        if not os.path.exists(self.journal):
            return
        for line in open(self.journal, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            self.seq = max(self.seq, r.get("seq", 0))
            k = r.get("kind")
            if k == "stage":
                self.stage_now = r.get("entered")
                self._stage_marks.append({"stage": r.get("entered"),
                                          "from": r.get("left"),
                                          "at_seq": r.get("seq"),
                                          "codes_so_far": len(self.codes),
                                          "corpus_reads_self_reported":
                                              r.get("corpus_reads_self_reported")})
            elif k == "code":
                self.codes.append(r["rec"])
                c = r["rec"]
                self._seen_codes = getattr(self, "_seen_codes", set())
                self._seen_codes.add(self._dup_key(c.get("item_id"), c.get("start"),
                                                   c.get("end"), c.get("first_order")))
            elif k == "theme":
                self.themes.append(r["rec"])
                ids = set(r.get("code_ids") or [])
                for c in self.codes:
                    if c["code_id"] in ids:
                        c["theme_id"] = r["rec"]["theme_id"]
            elif k == "theme_add":
                ids = set(r.get("code_ids") or [])
                for c in self.codes:
                    if c["code_id"] in ids:
                        c["theme_id"] = r["theme_id"]
                for x in self.themes:
                    if x["theme_id"] == r["theme_id"]:
                        x["n_codes"] = sum(1 for c in self.codes
                                           if c["theme_id"] == r["theme_id"])
            elif k == "thread":
                self.threads.append(r["rec"])
            elif k == "pointer":
                self.pointers.append(r["rec"])
                pr = r["rec"]
                self._seen_pointers = getattr(self, "_seen_pointers", set())
                self._seen_pointers.add((str(pr.get("raw") or "").strip().lower(),
                                         pr.get("item_id"), pr.get("start"), pr.get("end")))
            elif k == "retract":
                for c in self.codes:
                    if c["code_id"] == r.get("code_id"):
                        c["retracted"] = True
                        c["retracted_reason"] = r.get("reason")
            elif k == "close":
                # v32: close() journals itself, so the count of closes and the last
                # verdict survive the end of the process that made them.
                self._close_records.append(r)
                if r.get("verdict") is not None:
                    self._verdict = r.get("verdict")

    # ---- the record, read lazily: only a code or a pointer needs it ---------
    def _record(self):
        """item id -> {body, thread, kind, author, created_utc}; thread -> [item ids].

        Loaded on the first code() or pointer() call, never in __init__: a case lead of a
        large room constructs Emit many times for themes alone, and the record of r/place
        is hundreds of megabytes.
        """
        if self._rec is not None:
            return self._rec
        self._rec = {}
        self._rec_threads = {}
        if not (self.corpus_path and os.path.exists(self.corpus_path)):
            return self._rec
        with open(self.corpus_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                if "id" not in r:
                    continue
                body = r.get("body")
                title = r.get("title") or ""
                selftext = r.get("selftext") or ""
                if body is None:
                    body = title + ("\n\n" + selftext if selftext else "")
                tid = (r.get("link_id") or ("t3_" + r["id"]))[3:]
                self._rec[r["id"]] = {"body": body, "title": title, "selftext": selftext,
                                      "thread": tid, "kind": r.get("kind"),
                                      "author": r.get("author"),
                                      "created_utc": r.get("created_utc")}
                self._rec_threads.setdefault(tid, []).append(r["id"])
        return self._rec

    def _verify_cited(self, cited, thread_id, what):
        """A quote is a slice of the item's body, non-empty, in the thread named."""
        if not isinstance(cited, dict):
            raise EmitError("`cited` must be the dict cite() returned, not %s"
                            % type(cited).__name__)
        for k in ("item_id", "start", "end", "text"):
            if k not in cited:
                raise EmitError("`cited` must be what cite() returned; missing %r" % k)
        text = cited.get("text")
        if not isinstance(text, str) or not text.strip():
            raise EmitError("%s refused: the quote is empty; cite() never returns an empty "
                            "span" % what)
        rec = self._record()
        if not rec:
            return          # no record archived beside this run: the end-of-run checks say so
        it = rec.get(cited["item_id"])
        if it is None:
            raise EmitError("%s refused: item %s is not in the record" % (what, cited["item_id"]))
        try:
            a, b = int(cited["start"]), int(cited["end"])
        except (TypeError, ValueError):
            raise EmitError("%s refused: start and end must be integers from cite()" % what)
        cands = [it["body"]]
        if it["kind"] == "post":
            cands += [it["title"], it["selftext"]]
        if not any(0 <= a < b <= len(c) and c[a:b] == text for c in cands):
            raise EmitError("%s refused: text is not the record's slice %s[%d:%d]. Pass "
                            "cite()'s return value through unchanged." % (what, cited["item_id"], a, b))
        if thread_id and it["thread"] != thread_id:
            raise EmitError("%s refused: item %s belongs to thread %s, not %s"
                            % (what, cited["item_id"], it["thread"], thread_id))

    def _corpus_item_count(self, thread_id):
        """In-window item count from coder_corpus.jsonl rows, excluding context."""
        if self._corpus_thread_items is None:
            self._corpus_thread_items = {}
            if not (self.corpus_path and os.path.exists(self.corpus_path)):
                return None
            try:
                with open(self.corpus_path, encoding="utf-8") as fh:
                    for line in fh:
                        try:
                            d = json.loads(line)
                        except ValueError:
                            continue
                        if "id" not in d or d.get("_context"):
                            continue
                        tid = d["id"] if d.get("kind") == "post" else (d.get("link_id") or "t3_?")[3:]
                        self._corpus_thread_items[tid] = self._corpus_thread_items.get(tid, 0) + 1
            except OSError:
                pass
        return self._corpus_thread_items.get(thread_id)

    def _thread_item_count(self, thread_id):
        """In-window item count for a thread, from the corpus header or read index."""
        if self.index and thread_id in self.index:
            n = self.index[thread_id].get("items", self.index[thread_id].get("n"))
            try:
                return int(n)
            except (TypeError, ValueError):
                pass
        return self._corpus_item_count(thread_id)

    def _check_excluded_quote(self, thread_id, read, verdict, excluded_quote):
        """C5 at write time: substantial read exclusions carry a cite() quote."""
        if excluded_quote is not None:
            self._verify_cited(excluded_quote, thread_id, "excluded_quote")
        n_items = self._thread_item_count(thread_id)
        if (verdict == "out_of_scope" and read != "unread"
                and n_items is not None and n_items >= 10 and excluded_quote is None):
            raise EmitError(
                "excluded_quote required for thread %s: verdict='out_of_scope', read=%r, "
                "and %d in-window items. Reading the thread in full does not replace the "
                "cited exclusion line. Call cite.py and pass its dict unchanged; use None "
                "only for unread exclusions or out-of-scope threads below ten in-window "
                "items." % (thread_id, read, n_items))

    def _served_items(self):
        """The items read.py has served to this directory: every item of a thread served
        whole (`thread`, or whole inside a windows batch), the items a triage window showed,
        and every `item` read. Read from out/_read.jsonl on each call, since read.py runs in
        its own process."""
        rl = os.path.join(self.outdir, "_read.jsonl")
        whole, items = set(), set()
        if not os.path.exists(rl):
            return None
        with open(rl, encoding="utf-8") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                k = r.get("kind")
                if k == "windows":
                    for tid, how in r.get("served") or []:
                        if how == "batch_whole":
                            whole.add(tid)
                    for tid, ids in (r.get("window_items") or {}).items():
                        items.update(ids)
                elif k == "thread":
                    tids = r.get("threads") or ([r["thread_id"]] if r.get("thread_id") else [])
                    whole.update(tids)
                elif k == "item" and r.get("item_id"):
                    items.add(r["item_id"])
        return whole, items

    def _check_served(self, item_id, what):
        """AGENT §3: a thread only triaged cannot be coded. A code or a pointer sits on an
        item read.py served: in a thread read whole, in a triage window, or by `item`."""
        got = self._served_items()
        if got is None:
            raise EmitError("%s refused: nothing has been served through read.py in this "
                            "directory (no out/_read.jsonl). Read through read.py; a code "
                            "rests on what it served." % what)
        whole, items = got
        if item_id in items:
            return
        rec = self._record()
        it = rec.get(item_id) if rec else None
        if it is not None and it["thread"] in whole:
            return
        if not rec:
            return
        raise EmitError("%s refused: item %s was never served to you. Its thread was read as "
                        "a window at most, and this item was not in the window. Call "
                        "`read.py ... thread %s` and read it whole first."
                        % (what, item_id, it["thread"] if it else "?"))

    # ---- the journal -------------------------------------------------------
    def _append(self, kind, payload):
        self.seq += 1
        rec = {"seq": self.seq,
               "t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "stage": self.stage_now, "kind": kind}
        rec.update(payload)
        with open(self.journal, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return rec

    # ---- stage transitions -------------------------------------------------
    def stage(self, name, corpus_reads=None, note=""):
        """Declare which step you are starting. Call it once per step, before the work.

        `corpus_reads` is optional and is your own count of how many times you have
        gone back to the corpus so far. It is the one self-reported number here; it is
        recorded as a self-report and is checkable against the transcript.
        """
        if name not in STAGES:
            raise EmitError("unknown stage %r — one of %s" % (name, STAGES))
        prev = self.stage_now
        self.stage_now = name
        mark = {"stage": name, "from": prev, "at_seq": self.seq,
                "codes_so_far": len(self.codes),
                "corpus_reads_self_reported": corpus_reads}
        self._stage_marks.append(mark)
        self._append("stage", {"entered": name, "left": prev,
                               "corpus_reads_self_reported": corpus_reads,
                               "note": note})
        return {"stage": name, "codes_so_far": len(self.codes)}

    # ---- what a coder emits ------------------------------------
    def code(self, cited, first_order, thread_id, exchange_id=None, note=""):
        """Record one code on one passage.

        `cited` is the dict cite() returned — pass it through unchanged. text, start
        and end come from it by construction, and v32 checks them against the record
        here: a quote that is not a slice of the item's body, an empty quote, or an
        item outside the thread named is refused at the call.

        `discovered_at` is NOT a parameter. The harness stamps it from the current
        stage. That is the whole point.
        """
        if self.stage_now is None:
            raise EmitError("call stage() before emitting anything")
        self._verify_cited(cited, thread_id, "code")
        if not first_order or not str(first_order).strip():
            raise EmitError("a code needs a first-order label")
        if cited.get("item_id") in self.slice_context:
            raise EmitError("item %s is an opening from an earlier slice, given to you as "
                            "context. It is never coded here: its codes belong to the coder "
                            "who held that slice." % cited.get("item_id"))
        self._check_served(cited["item_id"], "code")
        _k = self._dup_key(cited.get("item_id"), cited.get("start"),
                           cited.get("end"), first_order)
        if _k in getattr(self, "_seen_codes", set()):
            raise ValueError("duplicate code: %r already recorded for %s[%s:%s] — emit is "
                             "append-only, so a duplicate cannot be withdrawn afterwards. "
                             "Running one call twice is the usual cause; if one got through "
                             "anyway, emit.retract() is how you say so."
                             % (first_order[:40], cited.get("item_id"),
                                         cited.get("start"), cited.get("end")))
        self._seen_codes = getattr(self, "_seen_codes", set())
        self._seen_codes.add(_k)
        meta = (self._record() or {}).get(cited["item_id"]) or {}
        n = max(self.code_start + len(self.codes), self._max_id(self.codes, "code_id") + 1)
        cid = "c%04d" % n
        rec = {"passage_id": n, "code_id": cid, "batch": self.batch,
               "first_order": first_order,
               "theme_id": None,
               "thread_id": thread_id, "item_id": cited["item_id"],
               "item_kind": meta.get("kind"), "author": meta.get("author"),
               "created_utc": meta.get("created_utc"),
               "exchange_id": exchange_id,
               # Truthful, not tidy. A code minted while writing the account was not
               # discovered at step 3 and was not turned up by the counter-reading
               # either; calling it either of those is the same class of lie the
               # self-reported field used to permit. It gets its own value.
               "discovered_at": {"step3_codes": "step3",
                                 "step5_counter": "step5"}.get(self.stage_now,
                                                               self.stage_now),
               "minted_in_stage": self.stage_now,
               "start": cited["start"], "end": cited["end"],
               "text": cited["text"], "note": note,
               "minted_after_n_codes": len(self.codes),
               "corpus_position": self._position(thread_id)}
        self.codes.append(rec)
        self._append("code", {"rec": rec})
        return cid


    MOVED = ("yes", "partial", "no")
    RELATIONS = ("allied", "attacked", "attacked-by", "asked-help-from", "gave-help-to",
                 "negotiated", "mourned", "destroyed-carelessly", "mentioned-only")

    def pointer(self, cited, raw, kind, thread_id, normalised=None,
                relation="mentioned-only", moved="no", what_still_returns=None,
                what_you_cannot_see=None, code_ids=None, note=""):
        """One line for anything this record points at, from a thread you kept.

        A subreddit, a Discord, a strawpoll, a doc, a voice channel, another site — one
        list, one line each. A thread naming a Sonic Discord and another subreddit
        produces two lines.

        Only from threads you judged to touch the event. A pointer inside a thread you
        recorded `out_of_scope` is refused: this is a record of what these people pointed
        at while doing the thing, not of every link in the room's week.

        `cited` is what cite() returned, so the words that name it and the item they sit
        in travel with the row. That is what makes it a reference somebody can follow
        rather than a claim they have to take.

        `raw` verbatim — the `r/`, the invite link, the typo. `normalised` separately, or
        None. Do not silently correct: a handle can arrive with a character missing, and a
        coder who fixes it in `raw` destroys the evidence that it happened.
        """
        if self.stage_now is None:
            raise EmitError("call stage() before emitting anything")
        self._verify_cited(cited, thread_id, "pointer")
        self._check_served(cited["item_id"], "pointer")
        if kind not in ("subreddit", "off_platform"):
            raise EmitError("kind is %r, not 'subreddit' or 'off_platform'" % kind)
        if relation not in self.RELATIONS:
            raise EmitError("relation %r is not one of %s" % (relation, list(self.RELATIONS)))
        if moved not in self.MOVED:
            raise EmitError("moved is %r, not one of %s" % (moved, list(self.MOVED)))
        if not raw or not str(raw).strip():
            raise EmitError("`raw` is what the record writes and cannot be empty")
        if not thread_id:
            raise EmitError("`thread_id` is required: a pointer is recorded from a thread you "
                            "kept, and without it the kept-thread rule cannot be checked")
        if True:
            for t in self.threads:
                if t.get("thread_id") == thread_id and t.get("verdict") == "out_of_scope":
                    raise EmitError(
                        "thread %s was recorded out_of_scope; pointers are only recorded "
                        "from threads you kept. If this thread does touch the event, say so "
                        "in notes.md — emit.thread will not take it twice." % thread_id)
        key = (str(raw).strip().lower(), cited.get("item_id"),
               cited.get("start"), cited.get("end"))
        self._seen_pointers = getattr(self, "_seen_pointers", set())
        if key in self._seen_pointers:
            raise ValueError("duplicate pointer: %r already recorded at %s[%s:%s] — one line "
                             "per thing pointed at, using the passage that shows it best"
                             % (raw, cited.get("item_id"), cited.get("start"),
                                cited.get("end")))
        self._seen_pointers.add(key)
        if cited.get("item_id") in self.slice_context:
            raise EmitError("item %s is an opening from an earlier slice, given to you as "
                            "context; a pointer on it belongs to that slice's coder."
                            % cited.get("item_id"))
        pid = "p%04d" % max(self.pointer_start + len(self.pointers),
                            self._max_id(self.pointers, "pointer_id") + 1)
        rec = {"pointer_id": pid, "batch": self.batch, "raw": raw, "normalised": normalised,
               "kind": kind,
               "relation": relation, "moved": moved,
               "what_still_returns": what_still_returns,
               "what_you_cannot_see": what_you_cannot_see,
               "thread_id": thread_id, "item_id": cited["item_id"],
               "start": cited["start"], "end": cited["end"], "text": cited["text"],
               "code_ids": list(code_ids or []),
               "minted_in_stage": self.stage_now, "note": note,
               "corpus_position": self._position(thread_id)}
        self.pointers.append(rec)
        self._append("pointer", {"rec": rec})
        return pid


    def retract(self, code_id, reason):
        """Withdraw a code by **appending** a retraction. Nothing is edited or deleted.

        Rule 10 is right and does not move: you revise nothing. But a coder who emits the
        same sixty codes twice, notices, and has no way to say so leaves the duplicates
        live in every file above — and two later draws ran over one such community without
        opening it. This is the one call that was missing to make rule 10 enforceable
        rather than merely obeyed.

        The journal keeps the code and the retraction, both. `codes.jsonl` carries the row
        with `retracted: true` and the reason beside it, so what happened stays visible;
        nothing above has to guess, and nothing below is rewritten.
        """
        if self.stage_now is None:
            raise EmitError("call stage() before emitting anything")
        if not reason or not str(reason).strip():
            raise EmitError("a retraction without a reason is a deletion; say what happened")
        hit = [c for c in self.codes if c["code_id"] == code_id]
        if not hit:
            raise EmitError("no code %r in this run" % code_id)
        if hit[0].get("retracted"):
            raise EmitError("%s is already retracted" % code_id)
        rec = {"code_id": code_id, "reason": reason, "stage": self.stage_now}
        hit[0]["retracted"] = True
        hit[0]["retracted_reason"] = reason
        self._append("retract", rec)
        return code_id

    def theme_add(self, theme_id, code_ids):
        """Put further codes into a theme that already exists.

        Codes are append-only because that stops retroactive tidying. Theme *membership*
        is a different thing, and making it append-only was a design fault: on the first
        v8 run every code minted after §7 had nowhere to go, so six of twenty themes were
        founded purely to hold them and the output carried 30% more themes than the
        reading did. Placing a code is not revising it — the code, its quote and its
        stamp are all untouched, and the placement is journalled like everything else.
        """
        t = next((x for x in self.themes if x["theme_id"] == theme_id), None)
        if t is None:
            raise EmitError("no theme %r — create it with theme() first" % theme_id)
        known = {c["code_id"] for c in self.codes}
        bad = [c for c in code_ids if c not in known]
        if bad:
            raise EmitError("no such code_id: %s" % ", ".join(bad))
        placed = []
        for c in self.codes:
            if c["code_id"] in code_ids:
                if c["theme_id"] not in (None, theme_id):
                    raise EmitError("%s is already in %s — a code belongs to exactly one "
                                    "theme" % (c["code_id"], c["theme_id"]))
                if c["theme_id"] is None:
                    c["theme_id"] = theme_id
                    placed.append(c["code_id"])
        t["n_codes"] = sum(1 for c in self.codes if c["theme_id"] == theme_id)
        self._append("theme_add", {"theme_id": theme_id, "code_ids": placed})
        return {"theme_id": theme_id, "added": placed, "n_codes": t["n_codes"]}

    def theme(self, second_order, theme_note, code_ids, regrouped_from=None):
        """Record one theme and the codes under it. One line per theme, not per code."""
        if self.stage_now is None:
            raise EmitError("call stage() before emitting anything")
        if not code_ids:
            raise EmitError("a theme with nothing under it is a theme you brought with you; "
                            "give it at least one code_id")
        if not second_order or not str(second_order).strip():
            raise EmitError("a theme needs a label")
        known = {c["code_id"] for c in self.codes}
        bad = [c for c in code_ids if c not in known]
        if bad:
            raise EmitError("no such code_id: %s" % ", ".join(bad))
        tid = "t%02d" % (len(self.themes) + 1)
        for c in self.codes:
            if c["code_id"] in code_ids:
                if c["theme_id"] is not None:
                    raise EmitError("%s is already in %s — a code belongs to exactly "
                                    "one theme" % (c["code_id"], c["theme_id"]))
                c["theme_id"] = tid
        rec = {"theme_id": tid, "second_order": second_order,
               "theme_note": theme_note, "regrouped_from": regrouped_from,
               "n_codes": len(code_ids)}
        self.themes.append(rec)
        self._append("theme", {"rec": rec, "code_ids": list(code_ids)})
        return tid

    def thread(self, thread_id, read, verdict, reason, excluded_quote=None,
               _bulk=False):
        """Record one thread's selection decision, at the moment you finish with it.

        Call this as you go, thread by thread, not in a batch at the end. Recorded as
        you go it is a reading tally that can be watched while a long run is still
        running; recorded at the end it is only ever a report about a run that is
        already over. The return value tells you where you are.
        """
        if self.stage_now is None:
            raise EmitError("call stage() before emitting anything")
        if not thread_id:
            raise EmitError("a thread disposition needs the thread's id; without one there is "
                            "nothing for the read log to reconcile it against")
        if self.index and thread_id not in self.index and thread_id not in self.slice_context:
            raise EmitError("no thread %r in this corpus; a disposition names a thread of "
                            "your slice" % thread_id)
        if thread_id in self.slice_context:
            raise EmitError("thread %s is an earlier slice's, given to you as context; its "
                            "disposition belongs to the coder who held that slice" % thread_id)
        if read not in ("full", "triaged", "unread"):
            raise EmitError("read must be full|triaged|unread")
        if verdict not in ("coded", "out_of_scope"):
            raise EmitError("verdict must be coded|out_of_scope")
        if any(t["thread_id"] == thread_id for t in self.threads):
            raise EmitError("%s already recorded — this file is append-only"
                            % thread_id)
        self._check_excluded_quote(thread_id, read, verdict, excluded_quote)
        rec = {"thread_id": thread_id, "read": read, "verdict": verdict,
               "reason": reason, "excluded_quote": excluded_quote,
               "recorded": "bulk" if _bulk else "singly", "batch": self.batch}
        self.threads.append(rec)
        p = None if _bulk else self.reading()
        self._append("thread", {"rec": rec, "reading": p})
        return p

    def threads_bulk(self, rows):
        """Record many thread decisions at once.

        "Record each thread the moment you finish with it" is right for the threads you
        actually opened and impossible for the seven hundred you disposed of in a single
        titles-and-openings pass. Rather than have the coder pretend a loop is
        thread-by-thread work, this says what it is: one pass, recorded as one pass. The
        journal marks these `bulk`, so the reading tally can tell a thread that was
        weighed on its own from one that went past in a sweep.
        """
        out = []
        for r in rows:
            out.append(self.thread(r["thread_id"], r["read"], r["verdict"],
                                   r.get("reason", ""), r.get("excluded_quote"),
                                   _bulk=True))
        self._append("threads_bulk", {"n": len(rows)})
        return self.reading()

    def reading(self):
        """The reading tally. How far through the corpus are we, by threads, by items,
        and by share of the text — against the denominators in the corpus header.

        This is the one thing about a run that is not recoverable from the outputs
        afterwards and not visible from anywhere else while it is happening.
        """
        seen = {t["thread_id"]: t for t in self.threads}
        opened = {k: v for k, v in seen.items() if v["read"] == "full"}
        def tot(keys, field):
            return sum(self.index[k][field] for k in keys if k in self.index)
        n_total = len(self.index) or None
        all_items = tot(self.index, "items")
        all_chars = tot(self.index, "chars")
        out = {"threads_disposed": len(seen),
               "threads_in_corpus": n_total,
               "threads_undisposed": (n_total - len([k for k in seen if k in self.index])
                                      if n_total else None),
               "read_in_full": len(opened),
               "triaged_and_dropped": sum(1 for v in seen.values()
                                          if v["read"] == "triaged"),
               "unread": sum(1 for v in seen.values() if v["read"] == "unread"),
               "coded": sum(1 for v in seen.values() if v["verdict"] == "coded"),
               "items_in_threads_read": tot(opened, "items"),
               # NAMED, not renamed. The rendered header's headline counts [CONTEXT]
               # items — out-of-window ancestors kept so threads stay whole — and this
               # index does not. Coders reported the two numbers as a contradiction,
               # correctly: nothing said they counted different populations.
               "items_in_window": all_items or None,
               "items_in_corpus_note": ("in-window items only; the corpus header's "
                                        "headline additionally counts [CONTEXT] items")}
        if n_total:
            out["share_of_threads_disposed"] = round(len(seen) / n_total, 3)
        if n_total:
            # A run can read almost every thread whole and still score low here, because
            # one triaged thread can hold most of the text. A text-weighted share alone
            # makes a thorough coder look idle, so the thread-weighted one sits beside it.
            out["share_of_threads_read_in_full"] = round(len(opened) / n_total, 3)
        if all_chars:
            out["share_of_text_read_in_full"] = round(tot(opened, "chars") / all_chars, 3)
        return out

    # ---- materialise -------------------------------------------------------

    def _position(self, thread_id):
        """Where in the reading this thread sits — the drift axis, computed, never asked.

        **Reading order, not the header's index.** §5 fixes the order: the coder passes over
        the corpus once, oldest thread first, and disposes of every thread as it goes. So the
        order of `self.threads` *is* the reading order, and a code minted on the seventh
        thread the coder met and one minted on the two hundred and eightieth are
        distinguishable afterwards without the coder recording anything.

        The corpus header's `_thread_index` is sorted by size, not by time, so it cannot be
        used for the rank — only for the per-thread item counts that turn a rank into a share.
        An earlier version of this method read the index in file order and would have reported
        a size rank while calling it a position.

        Returns None for a thread that was never disposed. The field is an instrument, not a
        requirement, and it must never fail a run.
        """
        if thread_id is None:
            return None
        order = [t.get("thread_id") for t in self.threads]
        if thread_id not in order:
            return None
        i = order.index(thread_id)
        out = {"thread_rank": i + 1, "of_threads_disposed": len(order)}
        if self.index:
            cum = sum((self.index.get(k) or {}).get("items") or 0 for k in order[:i + 1])
            tot = sum((v.get("items") or 0) for v in self.index.values())
            out["cum_items"] = cum
            if tot:
                out["share_of_corpus"] = round(cum / tot, 4)
        return out

    def _dup_key(self, item_id, start, end, first_order):
        return (item_id, start, end, first_order)

    @staticmethod
    def _max_id(rows, key):
        """The largest numeric id among rows, so a pooled journal with gaps still mints
        a fresh id above everything already there."""
        m = 0
        for r in rows:
            v = str(r.get(key) or "")
            digits = "".join(ch for ch in v if ch.isdigit())
            if digits:
                m = max(m, int(digits))
        return m

    def close(self, verdict=None):
        """Write the three machine-readable files, plus the run record.

        **Safe to call more than once, and it says so when you do.** A run triggered
        this inadvertently through a defensive `hasattr` line at the end of section 7, got
        a run summary back, and carried on — nothing was lost, but a method named `close`
        that is silently non-terminal is a trap, and the coder had no way to know whether
        it had just ended its own run. A repeat call now rewrites the same three files
        from current state and stamps `reopened_after_close` in the run record, so the
        fact is visible afterwards instead of being invisible at the time.
        """
        if verdict is not None:
            if verdict not in ("none", "trace", "full"):
                raise ValueError("verdict must be none, trace or full — got %r" % verdict)
            self._verdict = verdict
        # v32: the close is a journal record like everything else, so a second call from
        # a later process is counted, the verdict outlives the process that gave it, and
        # close_run can see anything recorded after the last close.
        self._append("close", {"verdict": verdict, "n_codes": len(self.codes),
                               "n_threads": len(self.threads), "n_themes": len(self.themes),
                               "n_pointers": len(self.pointers)})
        self._close_records.append({"seq": self.seq, "verdict": verdict})
        self._closed = len(self._close_records)
        # ---- derive read= from the read log, which knows what was actually served ------
        # Coders reported that AGENT §3's rule ("triaged for a window, full for a thread()
        # call") gives no answer for a thread served whole inside a windows() batch, which
        # on some corpora is most of them. The read log is
        # the authority on what was served, so close() now reconciles every disposition
        # against it: the coder's own word is kept as `claimed_read`, the derived state
        # becomes `read`, and a claim of MORE reading than was served is an error here
        # rather than a gate failure later.
        rl = os.path.join(self.outdir, "_read.jsonl")
        if os.path.exists(rl):
            served = {}
            with open(rl, encoding="utf-8") as fh:
                for line in fh:
                    try:
                        r = json.loads(line)
                    except ValueError:
                        continue
                    if r.get("kind") == "windows":
                        for tid, how in r.get("served") or []:
                            if served.get(tid) != "full":
                                served[tid] = how
                    elif r.get("kind") == "thread":
                        # read.py logs a single-thread service as `thread_id`, not
                        # `threads`. Reading only the plural key meant no thread()
                        # call was ever counted as served, so a thread first met as a
                        # triage window and then honestly read whole raised here and
                        # the run wrote no outputs at all — which is the workflow
                        # AGENT §3 prescribes. Introduced with this reconciliation at
                        # v25 and found by the first coder to run it. Accept both.
                        tids = r.get("threads")
                        if not tids:
                            one = r.get("thread_id")
                            tids = [one] if one else []
                        for tid in tids:
                            served[tid] = "full"
            RANK = {"unread": 0, "triaged": 1, "batch_whole": 2, "full": 3}
            for t in self.threads:
                got = served.get(t.get("thread_id"))
                if got is None:
                    continue
                claimed = t.get("read")
                if claimed != got:
                    t["claimed_read"] = claimed
                    t["read"] = "full" if got == "batch_whole" else got
                if RANK.get(claimed, 0) > RANK.get("full" if got == "batch_whole" else got, 3):
                    raise ValueError("thread %s claims read=%r but the log served %r"
                                     % (t.get("thread_id"), claimed, got))
        _oos = {t.get("thread_id") for t in self.threads
                if t.get("verdict") == "out_of_scope"}
        stray_ptr = [p["pointer_id"] for p in self.pointers
                     if p.get("thread_id") in _oos]
        if stray_ptr:
            raise ValueError("pointers recorded on out_of_scope threads: %s — a pointer is "
                             "a record of what these people pointed at while doing the "
                             "thing" % stray_ptr[:6])
        orphan = [c["code_id"] for c in self.codes
                  if c["theme_id"] is None and not c.get("retracted")]
        empty = [t["theme_id"] for t in self.themes
                 if not any(c["theme_id"] == t["theme_id"] for c in self.codes)]

        def dump(name, rows):
            p = os.path.join(self.outdir, name)
            with open(p, "w", encoding="utf-8") as f:
                for r in rows:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            return p

        dump("codes.jsonl", self.codes)
        dump("themes.jsonl", self.themes)
        dump("threads.jsonl", self.threads)
        dump("pointers.jsonl", self.pointers)

        run = {"instrument": INSTRUMENT, "emit": VERSION,
               "verdict": self._verdict,
               "verdict_note": ("set by emit.close(verdict=...); a verdict that exists only "
                                "as prose in case.md cannot be read back reliably"),
               "close_calls": self._closed,
               "reopened_after_close": self._closed > 1,
               "last_close_seq": self.seq,
               "stages": self._stage_marks,
               "reading": self.reading(),
               "calls_by_stage": self._calls_by_stage(),
               "n_codes": sum(1 for c in self.codes if not c.get("retracted")),
               "n_codes_emitted": len(self.codes),
               "n_retracted": sum(1 for c in self.codes if c.get("retracted")),
               "n_themes": len(self.themes),
               "n_threads": len(self.threads),
               "n_pointers": len(self.pointers),
               "n_subreddits_named": len({(p.get("normalised") or p["raw"]).lower()
                                          for p in self.pointers
                                          if p["kind"] == "subreddit"}),
               "n_off_platform": len({(p.get("normalised") or p["raw"]).lower()
                                      for p in self.pointers
                                      if p["kind"] == "off_platform"}),
               "isolated": not any(p["kind"] == "subreddit" for p in self.pointers),
               "coordination_left_the_venue": any(p["moved"] in ("yes", "partial")
                                                  for p in self.pointers),
               "discovered_at": {k: sum(1 for c in self.codes
                                        if c["discovered_at"] == k)
                                 for k in sorted({c["discovered_at"]
                                                  for c in self.codes})},
               "saturation_observed": self._saturation(),
               "integrity": {"codes_with_no_theme": orphan,
                             "themes_with_no_code": empty,
                             "ok": not orphan and not empty}}
        # v29: the case lead's gate record (branch, threshold, the two counts, the slices,
        # one line per coder) lives in out/_gate.json, written by tools/fleet.py, and is
        # carried into _run.json here so the run record holds it. It is never rewritten
        # by close(); the gate file stays the authority.
        gate_path = os.path.join(self.outdir, "_gate.json")
        if os.path.exists(gate_path):
            try:
                run["gate"] = json.load(open(gate_path, encoding="utf-8"))
                run["branch"] = run["gate"].get("branch")
            except (ValueError, OSError) as e:
                run["gate"] = {"error": "unreadable _gate.json: %s" % e}
        if self.batch:
            run["batch"] = self.batch
        with open(os.path.join(self.outdir, "_run.json"), "w", encoding="utf-8") as f:
            json.dump(run, f, ensure_ascii=False, indent=1)
        return run

    def _calls_by_stage(self):
        out = {}
        if not os.path.exists(self.journal):
            return out
        for line in open(self.journal, encoding="utf-8"):
            r = json.loads(line)
            s = r.get("stage") or "(none)"
            out.setdefault(s, {}).setdefault(r["kind"], 0)
            out[s][r["kind"]] += 1
        # find() logs itself, in its own file, with its own timestamps. Merge by time
        # rather than instrumenting cite.py, which is load-bearing and stays untouched.
        if self.corpus_path:
            q = os.path.splitext(self.corpus_path)[0] + ".queries.jsonl"
            if os.path.exists(q):
                marks = [(m["stage"], m) for m in self._stage_marks]
                times = self._stage_times()
                for line in open(q, encoding="utf-8"):
                    r = json.loads(line)
                    s = self._stage_at(r.get("t"), times) or "(none)"
                    out.setdefault(s, {}).setdefault("find", 0)
                    out[s]["find"] += 1
        return out

    def _stage_times(self):
        ts = []
        if not os.path.exists(self.journal):
            return ts
        for line in open(self.journal, encoding="utf-8"):
            r = json.loads(line)
            if r["kind"] == "stage":
                ts.append((r["t"], r["entered"]))
        return ts

    @staticmethod
    def _stage_at(t, times):
        cur = None
        for start, name in times:
            if t and t >= start:
                cur = name
        return cur

    def _saturation(self):
        """How far into the minting did the last genuinely new code appear.

        Observed, not remembered: the position of the final code in the journal
        against the total, per stage.
        """
        if not self.codes:
            return None
        last3 = max((i for i, c in enumerate(self.codes, 1)
                     if c["discovered_at"] == "step3"), default=0)
        return {"n_codes": len(self.codes),
                "last_step3_code_at": last3,
                "codes_minted_after_it": len(self.codes) - last3,
                "share_of_minting_before_last_new_step3_code":
                    round(last3 / len(self.codes), 3)}


if __name__ == "__main__":
    print(__doc__)
