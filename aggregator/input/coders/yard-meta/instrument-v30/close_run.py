#!/usr/bin/env python3
"""
close_run.py — the end-of-run gate.  Instrument v30.

A run is not finished when the coder stops talking. It is finished when its record is
complete enough that somebody a year from now can say what happened without inferring it.

This exists because that was not true. An earlier session reported "transcripts
saved for all runs"; what had been saved was emit's journal. No transcript of any coder
run exists anywhere in the vault, so the call-level analysis that followed had to be
reconstructed from token accounting — and a reconstruction is not a measurement. The fix
is not a reminder. It is a check that fails.

    python3 close_run.py RUNDIR [--record CORPUS.jsonl] [--role lead|fleet]

v29: `--role fleet` closes a fleet coder's directory, which by contract holds no themes (C4
reports that instead of failing). A case lead's directory in branch B holds the pooled
dispositions, so C6 reads the fleet's read logs from staging/read_batch_*.jsonl beside the
lead's own.

Every check is FAIL or PASS, and it exits non-zero on any FAIL.

  C1  the six outputs exist
  C2  a transcript exists and is not empty          <- the one that was silently skipped
  C3  every code's text is byte-identical to the record          (anti-fabrication)
  C4  every code sits under exactly one theme, every theme has codes
  C5  every out_of_scope thread of >=10 items carries a cited exclusion line
  C6  declared read= matches what read.py served
  C7  the instrument manifest is present and its files still hash to what it recorded
  C8  every pointer's text and every excluded_quote is byte-identical to the record
  C9  every live code and pointer sits on an item read.py served (whole thread, window
      item, or `item` read)                                     (the triaged-thread rule)
  C10 nothing was recorded in the journal after the last emit.close()

C5 is the check the refusals note asked for by name: the completing Sonnet run excluded
eight threads of ten or more items with no cited line, and A1-A7 did not cover it.

C6 is vacuous on a run made before read.py existed, and says so rather than passing.
"""

import hashlib
import json
import os
import sys

INSTRUMENT = "v30"
VERSION = "close-v30"

OUTPUTS = ["codes.jsonl", "themes.jsonl", "threads.jsonl", "pointers.jsonl",
           "case.md", "notes.md"]
TRANSCRIPTS = ["_transcript.jsonl", "_transcript.json", "_transcript.md"]


def jl(p):
    if not os.path.exists(p):
        return []
    out = []
    with open(p, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def citable(r):
    """
    The strings cite() may have measured offsets against, per Rule 3.

    A comment cites against its body. A post cites against its body where it has one and
    against its TITLE where it does not — an image post, a link post, or a post whose body
    was removed while the title survived. Runs have also stored a post's citable string as
    title + blank line + selftext, which is the same rule with the title kept in view.

    All three are accepted here and the one that resolved is reported, so a convention
    change between instrument versions shows up as drift rather than as a fabrication.
    """
    if r.get("kind") != "post":
        return {"body": r.get("body") or ""}
    t = (r.get("title") or "")
    s = (r.get("selftext") or "")
    v = {"title": t}
    if s:
        v["selftext"] = s
        v["title+selftext"] = t + "\n\n" + s
    return v


def _verdict(out):
    """The verdict emit.close(verdict=...) recorded in _run.json; failing that, the one the
    coder wrote at the top of case.md."""
    rp = os.path.join(out, "_run.json")
    if os.path.exists(rp):
        try:
            v = json.load(open(rp, encoding="utf-8")).get("verdict")
            if v in ("none", "trace", "full"):
                return v
        except (ValueError, OSError):
            pass
    p = os.path.join(out, "case.md")
    if not os.path.exists(p):
        return None
    head = open(p, encoding="utf-8").read()[:4000].lower()
    for v in ("none", "trace", "full"):
        for pat in ("verdict: `%s`" % v, "verdict:** `%s`" % v, "verdict: %s" % v,
                    "verdict** %s" % v, "**%s**" % v):
            if pat in head:
                return v
    return None


def check(rundir, record=None, role="lead"):
    out = os.path.join(rundir, "out")
    if not os.path.isdir(out):
        out = rundir
    R = []

    def add(cid, ok, msg, detail=None):
        R.append({"check": cid, "status": "PASS" if ok else "FAIL",
                  "message": msg, "detail": detail or []})

    # C1 --------------------------------------------------------------------
    missing = [f for f in OUTPUTS if not os.path.exists(os.path.join(out, f))]
    add("C1", not missing, "the six outputs exist", missing)
    if len(missing) == len(OUTPUTS):
        R.append({"check": "--", "status": "STOP",
                  "message": "this run has produced no outputs at all — nothing to close",
                  "detail": ["scaffolded but not yet run, or dispatched and died before "
                             "emit.close(). the remaining checks are not run, because "
                             "passing them vacuously is how a missing run looks like a "
                             "clean one."]})
        return R

    # C2 --------------------------------------------------------------------
    tp = [f for f in TRANSCRIPTS
          if os.path.exists(os.path.join(out, f))
          and os.path.getsize(os.path.join(out, f)) > 0]
    add("C2", bool(tp),
        "a non-empty transcript of the agent's own turns is stored in the run",
        [] if tp else ["none of %s found in %s" % ("/".join(TRANSCRIPTS), out),
                       "emit's _journal.jsonl is a decision log, NOT a transcript"])

    codes = jl(os.path.join(out, "codes.jsonl"))
    themes = jl(os.path.join(out, "themes.jsonl"))
    threads = jl(os.path.join(out, "threads.jsonl"))

    # C3 --------------------------------------------------------------------
    rec = record or os.path.join(rundir, "coder_corpus.jsonl")
    idx, item_thread = {}, {}
    if os.path.exists(rec):
        with open(rec, encoding="utf-8") as fh:
            for line in fh:
                d = json.loads(line)
                if "id" in d:
                    idx[d["id"]] = citable(d)
                    item_thread[d["id"]] = (d["id"] if d.get("kind") == "post"
                                            else (d.get("link_id") or "t3_?")[3:])

    def verify_span(row, label):
        """None when the row's text is a slice of a citable string of its item, else why not.
        An empty text, an offset outside the string, or a wrong thread is a failure: a Python
        slice out of range is '' and '' == '', which is how an invented row once passed."""
        cand = idx.get(row.get("item_id"))
        if cand is None:
            return "%s: item_id %s not in record" % (label, row.get("item_id"))
        try:
            a, b = int(row.get("start")), int(row.get("end"))
        except (TypeError, ValueError):
            return "%s: start/end are not integers" % label
        text = row.get("text")
        if not isinstance(text, str) or not text.strip():
            return "%s (%s): empty text" % (label, row.get("item_id"))
        hit = [k for k, v in cand.items() if 0 <= a < b <= len(v) and v[a:b] == text]
        if not hit:
            return "%s (%s): text is not any citable string at [%d:%d]" % (label, row.get("item_id"), a, b)
        if row.get("thread_id") and item_thread.get(row.get("item_id")) not in (None, row.get("thread_id")):
            return "%s: item %s is in thread %s, row says %s" % (
                label, row.get("item_id"), item_thread.get(row.get("item_id")), row.get("thread_id"))
        return hit[0]

    if os.path.exists(rec) and codes:
        bad, how = [], {}
        for c in codes:
            r = verify_span(c, c.get("code_id"))
            if r in ("body", "title", "selftext", "title+selftext"):
                how[r] = how.get(r, 0) + 1
            else:
                bad.append(r)
        add("C3", not bad,
            "every code's text is byte-identical to the record (%d codes)" % len(codes),
            bad[:20] or ["resolved against: " + ", ".join("%s x%d" % kv for kv in sorted(how.items()))])
    elif os.path.exists(rec) and not codes and _verdict(out) == "none":
        # A `none` verdict means the corpus was not about the event, and §8 says so explicitly:
        # "Code the mentions and stop there" is `trace`; `none` is nothing to code at all. A run
        # with no codes because there was nothing codeable is correct, not unverifiable.
        add("C3", True, "no codes to verify — verdict is `none`, which is the correct output "
                        "for a corpus with nothing about the event in it", [])
    else:
        add("C3", False,
            "cannot verify citations — %s" % ("no codes were recorded" if os.path.exists(rec)
                                              else "the record file is not archived with this run"),
            ["looked for %s" % rec,
             "a run whose coder_corpus.jsonl is missing cannot have its citations checked, ever"]
            if not os.path.exists(rec) else ["a run with no codes cannot be closed"])

    # C4 --------------------------------------------------------------------
    tids = {t.get("theme_id") for t in themes}
    orphan = [c.get("code_id") for c in codes
              if not c.get("theme_id") and not c.get("retracted")]
    unknown = [c.get("code_id") for c in codes
               if c.get("theme_id") and c["theme_id"] not in tids]
    empty = [t.get("theme_id") for t in themes
             if not any(c.get("theme_id") == t.get("theme_id") for c in codes)]
    if role == "fleet":
        add("C4", not themes,
            "a fleet coder mints no theme; %d codes wait for the case lead's step 4" % len(codes),
            ["themes found in a fleet coder's directory: %s" % sorted(tids)] if themes else [])
    else:
        add("C4", not (orphan or unknown or empty),
            "every code under exactly one theme, every theme under at least one code",
            [("orphan codes: %s" % orphan[:10]) if orphan else "",
             ("codes pointing at no such theme: %s" % unknown[:10]) if unknown else "",
             ("empty themes: %s" % empty[:10]) if empty else ""])

    # C5 --------------------------------------------------------------------
    sizes = {}
    if os.path.exists(rec):
        with open(rec, encoding="utf-8") as fh:
            for line in fh:
                d = json.loads(line)
                if "id" not in d:
                    continue
                if d.get("_context"):
                    # An out-of-window ancestor is not this community acting, and the rule
                    # this check enforces is about how much conduct a coder passed over.
                    # Counting context pushed threads over ten on items the coder was never
                    # asked to judge — a run can reach thirty on almost all of them, and
                    # then has to write cited exclusions for threads it could read one
                    # item of. Reported by both.
                    continue
                t = d["id"] if d.get("kind") == "post" else (d.get("link_id") or "t3_?")[3:]
                sizes[t] = sizes.get(t, 0) + 1
    uncited = [t["thread_id"] for t in threads
               if t.get("verdict") == "out_of_scope"
               and t.get("read") != "unread"
               and sizes.get(t.get("thread_id"), 0) >= 10
               and not t.get("excluded_quote")]
    add("C5", not uncited,
        "every read out_of_scope thread of >=10 IN-WINDOW items carries a cited exclusion line",
        ["%d uncited: %s" % (len(uncited), uncited[:12])] if uncited else [])

    # C6 --------------------------------------------------------------------
    rl = os.path.join(out, "_read.jsonl")
    import glob as _glob
    fleet_logs = sorted(_glob.glob(os.path.join(rundir, "staging", "read_batch_*.jsonl")))
    if not os.path.exists(rl) and not fleet_logs:
        add("C6", False, "declared read= cannot be checked — no read.py log",
            ["this run predates the reading tool; the read= field is a self-report",
             "and nothing in this run can confirm or refute it"])
    else:
        served = {}
        for lp in ([rl] if os.path.exists(rl) else []) + fleet_logs:
            for r in jl(lp):
                if r["kind"] == "windows":
                    for tid, how in r["served"]:
                        if served.get(tid) != "full":
                            served[tid] = how
                elif r["kind"] == "thread":
                    served[r["thread_id"]] = "full"
        rank = {"unread": 0, "triaged": 1, "batch_whole": 2, "full": 3}
        over, under = [], []
        for t in threads:
            decl = t.get("read")
            got = served.get(t["thread_id"], "unread")
            if got == "batch_whole" and decl in ("triaged", "full"):
                continue          # both readings are true of it; see read.py audit()
            if rank.get(decl, 0) > rank.get(got, 0):
                over.append("%s declared %s, served %s" % (t["thread_id"], decl, got))
            elif decl != got and not (got == "batch_whole" and decl in ("triaged", "full")):
                under.append("%s declared %s, served %s" % (t["thread_id"], decl, got))
        add("C6", not over,
            "no thread claims more reading than read.py served",
            over[:12] + (["(understated, not a failure: %d)" % len(under)] if under else []))

    # C8 --------------------------------------------------------------------
    pointers = jl(os.path.join(out, "pointers.jsonl"))
    if os.path.exists(rec):
        bad8 = []
        for p_ in pointers:
            r = verify_span(p_, p_.get("pointer_id"))
            if r not in ("body", "title", "selftext", "title+selftext"):
                bad8.append(r)
        for t in threads:
            q = t.get("excluded_quote")
            if not q:
                continue
            if not isinstance(q, dict):
                bad8.append("%s: excluded_quote is typed text, not what cite() returned" % t.get("thread_id"))
                continue
            r = verify_span(q, "excluded_quote of %s" % t.get("thread_id"))
            if r not in ("body", "title", "selftext", "title+selftext"):
                bad8.append(r)
            elif item_thread.get(q.get("item_id")) not in (None, t.get("thread_id")):
                bad8.append("excluded_quote of %s cites item %s, which is in thread %s"
                            % (t.get("thread_id"), q.get("item_id"), item_thread.get(q.get("item_id"))))
        add("C8", not bad8, "every pointer's text and every excluded_quote is byte-identical to "
                            "the record (%d pointers, %d exclusion quotes)"
            % (len(pointers), sum(1 for t in threads if t.get("excluded_quote"))), bad8[:20])
    else:
        add("C8", False, "pointers and exclusion quotes cannot be verified: no record archived", [])

    # C9 --------------------------------------------------------------------
    whole, items = set(), set()
    logs9 = ([rl] if os.path.exists(rl) else []) + fleet_logs
    for lp in logs9:
        for r in jl(lp):
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
    if not logs9:
        add("C9", False, "coded items cannot be checked against what was served: no read.py log", [])
    else:
        unserved = []
        for row, label in ([(c, c.get("code_id")) for c in codes if not c.get("retracted")]
                           + [(p_, p_.get("pointer_id")) for p_ in pointers]):
            iid = row.get("item_id")
            if iid in items or item_thread.get(iid) in whole:
                continue
            unserved.append("%s: item %s of thread %s was not served (window at most)"
                            % (label, iid, item_thread.get(iid)))
        add("C9", not unserved, "every live code and pointer sits on an item read.py served "
                                "(%d threads whole, %d single items)" % (len(whole), len(items)),
            unserved[:20])

    # C10 -------------------------------------------------------------------
    jrows = jl(os.path.join(out, "_journal.jsonl"))
    closes = [r for r in jrows if r.get("kind") == "close"]
    if not jrows:
        add("C10", False, "no journal: nothing to close", [])
    elif not closes:
        add("C10", False, "the journal holds no emit.close() record", [])
    else:
        last = closes[-1].get("seq", 0)
        after = [r for r in jrows if r.get("seq", 0) > last and r.get("kind") != "stage"]
        add("C10", not after, "nothing recorded after the last emit.close() (%d close calls)" % len(closes),
            ["%s at seq %s" % (r.get("kind"), r.get("seq")) for r in after[:10]])

    # C7 --------------------------------------------------------------------
    mp = os.path.join(rundir, "_manifest.json")
    if not os.path.exists(mp):
        add("C7", False, "instrument manifest present", ["no _manifest.json in %s" % rundir])
    else:
        man = json.load(open(mp, encoding="utf-8"))
        drift = []
        for name, want in (man.get("sha256") or {}).items():
            p = os.path.join(rundir, name)
            if not os.path.exists(p):
                drift.append("%s: gone" % name)
            else:
                got = hashlib.sha256(open(p, "rb").read()).hexdigest()
                if got != want:
                    drift.append("%s: changed since dispatch" % name)
        ver = man.get("instrument")
        if ver != INSTRUMENT:
            drift.append("manifest says instrument %r, this checker is %r" % (ver, INSTRUMENT))
        if not man.get("instrument_fingerprint"):
            drift.append("no instrument_fingerprint — dispatched before the derived stamp "
                         "existed, so its version label rests on somebody having remembered")
        add("C7", not drift, "instrument manifest present and unchanged since dispatch", drift)

    def _num(r):
        d = "".join(ch for ch in r["check"] if ch.isdigit())
        return int(d) if d else 99
    R.sort(key=_num)
    return R


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return 0
    rundir = argv[1] if len(argv) > 1 and not argv[1].startswith("--") else "."
    record = None
    if "--record" in argv:
        record = argv[argv.index("--record") + 1]
    role = "lead"
    if "--role" in argv:
        role = argv[argv.index("--role") + 1]
        if role not in ("lead", "fleet"):
            raise SystemExit("--role must be lead or fleet")
    R = check(rundir, record, role)
    fails = [r for r in R if r["status"] in ("FAIL", "STOP")]
    print("close_run %s — %s" % (VERSION, os.path.abspath(rundir)))
    for r in R:
        print("  %-4s %s  %s" % (r["status"], r["check"], r["message"]))
        for d in r["detail"]:
            if d:
                print("           %s" % d)
    print("\n%d of %d checks passed." % (len(R) - len(fails), len(R)))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
