#!/usr/bin/env python3
"""Render a coder corpus as text, with every deterministic number precomputed.

VERSION 26.  Changed from v13: the window closes at FRZ + 24h instead of FRZ + 7d, and
items on BOTH sides of it are marked [CONTEXT] rather than only the ones before.  Threads
stay whole across the closing boundary for the same reason they always stayed whole across
the opening one — so every parent resolves and cite() can reach everything quotable.  On
one measured corpus that costs 394 items of tail against 16,161 dropped.

The window is now the event and one day of reaction: 97 hours.  Three Opus codings and one
early full coding of one community put 748 of 748 codes inside it, the last at +39h, and the
v13 coder read 70 threads beyond it in full and coded none of them.

WHY THIS EXISTS
---------------
Reading five pilot coders' transcripts showed them spending ~38% of their turns writing
python. Not analysing — *parsing*. Every agent independently wrote a JSONL loader, a
timestamp converter, an author counter, a day histogram, and a cumulative-share walk. Two
of them wrote a `dump.py` that renders threads as readable text, then read the text back.

They were building this file at runtime, once per community, in context, and paying to
re-read the scaffolding on every subsequent turn. So: ship it.

The design rule behind every choice here is one line long:

    If a step's output is a number, the agent is never the thing that computes it.

WHAT IS AND IS NOT LOST
-----------------------
Nothing a coder uses. Dropped: `subreddit` (constant in the file), `link_id` (redundant
once items are blocked by thread), `kind` (derivable from position), `num_comments`
(already known to be a lie), `permalink` (see below). Kept but compressed: timestamps
become "d3 12:28" (day since OPEN + UTC time), the always-false flags become a short
letter code that appears only when set.

`corpus.jsonl` stays on disk beside `corpus.txt`, unchanged and authoritative. cite()
resolves against it. Offsets are Unicode code points into the decoded body, and the body
is byte-identical in both files, so the citation contract is untouched.

THE PERMALINK
-------------
arctic-shift synthesises a comment permalink that does not resolve:

    /r/Dorset/comments/t3_634hhb/dfrj2ze        <- the t3_ prefix is in the path,
                                                   the title slug is missing

Probed directly against the API to confirm it is upstream and not something this project
constructed. It is 11.5% of corpus bytes and it is wrong, so it is not stored per record.
It is derived on demand, correctly, from the post's own permalink — which the API does
return in valid form — and written only into the citation receipts that need it.
"""
INSTRUMENT = "v30"   # contract, read, cite, emit and renderer all carry this

import collections
import datetime
import json
import os
import re
import sys

BOTS = re.compile(r"(bot|AutoModerator)$", re.I)


def body(r):
    if r.get("body") is not None:
        return r["body"]
    return (r.get("title") or "") + ("\n\n" + r["selftext"] if r.get("selftext") else "")


def permalink(rec, post, sub):
    """The correct one. Posts carry a real permalink; comments hang off it.

    Falls back to the /comment/ form when the post is outside the window, which resolves
    on reddit.com even without the title slug.
    """
    if rec.get("kind") == "post":
        p = rec.get("permalink") or ""
        return p if p and "/t3_" not in p else "/r/%s/comments/%s/" % (sub, rec["id"])
    if post:
        base = post.get("permalink") or ""
        if base and "/t3_" not in base:
            return base.rstrip("/") + "/" + rec["id"] + "/"
    lid = (rec.get("link_id") or "t3_?")[3:]
    return "/r/%s/comments/%s/comment/%s/" % (sub, lid, rec["id"])


def bar(n, scale):
    return "#" * int(round(n * scale)) if n else ""


# The triage window: title, the first BODY_CAP words of the opening post, and the TOP_N
# most-discussed top-level replies. Measured on one corpus — 731 threads,
# 519,369 words — this reads 16% of the corpus, 2.5x what the first two coders read, and
# a fifth of what reading every short thread in full would cost. The body cap is what
# makes it cheap on exactly the threads that matter least: a match thread's opening post
# is itself two thousand words of template.
BODY_CAP = 500
TOP_N = 3


def subtrees(rs, tid):
    """Top-level replies, ranked by the size of the discussion underneath each."""
    kids = collections.defaultdict(list)
    for r in rs:
        p = (r.get("parent_id") or "")
        kids[p[3:] if p[:3] in ("t1_", "t3_") else None].append(r)
    own = {}
    out = []
    for r in kids.get(tid, []):
        if r.get("_context"):
            continue          # pulled in so the thread is whole; not part of the case
        own[r["id"]] = len((body(r) or "").split())
        stack, n, nw = [r], 0, 0
        while stack:
            x = stack.pop()
            n += 1
            nw += len((body(x) or "").split())
            stack.extend(kids.get(x["id"], []))
        out.append((r["id"], n, nw))
    out.sort(key=lambda k: -k[2])
    return out, own


def render(path, open_utc, frz_utc, sub, window_label, end_utc, windows=True):
    """
    `windows=False` suppresses the TRIAGE WINDOW blocks.

    The window exists to answer one question — does this thread touch the event — and a
    brief corpus is the seven ordinary days *before* the event, where that question has no
    meaning. Rendering one into a brief corpus printed "If it touches the event, read the
    whole thread. If not, stop here." above threads in a week that could not touch it, and
    the brief writer's contract says nothing about triage, so the writer received an
    instruction it had no way to adjudicate. Brief corpora are now rendered without them.
    """
    meta = None
    items = []
    for i, line in enumerate(open(path, encoding="utf-8")):
        r = json.loads(line)
        if "id" not in r:
            meta = r
            continue
        items.append(r)

    th = collections.defaultdict(list)
    for r in items:
        tid = r["id"] if r.get("kind") == "post" else (r.get("link_id") or "t3_?")[3:]
        th[tid].append(r)
    for v in th.values():
        v.sort(key=lambda r: r["created_utc"])
    # Ordering and sizing count what people wrote. A single summoned bot can carry most of a
    # thread's characters — two sneakpeekbot items are two thirds of r/Dorset's only thread —
    # and since the index is what fixes the coder's reading order, machine output would
    # otherwise decide what gets read. Bot items stay in the corpus; they just do not vote.
    def human(r):
        # Bots do not vote on reading order (see below). Neither does an out-of-window
        # ancestor: it is here so the thread is whole and so cite() can reach it, not
        # because this community wrote it during the event. Counting it would let
        # pre-window text decide what gets read during the window.
        return not BOTS.search(r.get("author") or "") and not r.get("_context")

    def hchars(tid):
        return sum(len(body(r) or "") for r in th[tid] if human(r))

    def words(tid):
        return sum(len((body(r) or "").split()) for r in th[tid] if human(r))

    def hitems(tid):
        return sum(1 for r in th[tid] if human(r))

    # Time order. Nothing else.
    #
    # Earlier versions sorted by size — largest first through v9, smallest first in v11,
    # long openings held to the end in v12. Each was trying to stop a coder spending its
    # budget on a huge thread before it knew the case. The triage window already does
    # that: a thread costs its title, BODY_CAP words of its post and TOP_N replies,
    # whichever end of the corpus it sits at. So the sorting was solving a solved problem
    # and charging for it in the only currency that matters — a week that no longer reads
    # as a week. §8 asks which practice follows which, and no size-sorted corpus can
    # answer that.
    def opened_at(tid):
        inwin = [r["created_utc"] for r in th[tid] if not r.get("_context")]
        return min(inwin) if inwin else min(r["created_utc"] for r in th[tid])

    def opening_words(tid):
        p = th[tid][0]
        if p.get("kind") != "post" or p.get("_context"):
            return 0
        return (len((p.get("title") or "").split())
                + len(((p.get("selftext") or p.get("body")) or "").split()))

    order = sorted(th, key=lambda k: (opened_at(k), k))
    byid = {r["id"]: r for r in items}
    posts = {tid: (th[tid][0] if th[tid][0].get("kind") == "post" else None) for tid in th}

    ctx = [r for r in items if r.get("_context")]
    tot_chars = sum(len(body(r) or "") for r in items if not r.get("_context"))

    # --- the numbers the agents kept recomputing -----------------------------
    n_replies = n_resolved = 0
    for r in items:
        p = r.get("parent_id") or ""
        if p.startswith("t1_"):
            n_replies += 1
            if p[3:] in byid:
                n_resolved += 1
    def _gone(r):
        """A comment's removed text sits in `body`; a POST's sits in `selftext`.

        The old test read `body` only, so every deleted post was invisible to the count
        while every deleted comment was caught — the header said 1 where three writers
        counted 3, always short, always by the number of deleted posts. Reported
        independently by the bahrain, baylor and malta brief writers, who were forbidden
        by S10 to recompute it and so could only flag it.
        """
        if r.get("kind") == "post":
            return (r.get("selftext") or "") in ("[deleted]", "[removed]")
        return (r.get("body") or "") in ("[deleted]", "[removed]")

    gone = sum(1 for r in items if _gone(r))
    gone_posts = sum(1 for r in items if r.get("kind") == "post" and _gone(r))
    n_posts = sum(1 for r in items if r.get("kind") == "post")
    bots = collections.Counter(r.get("author") or "" for r in items
                               if BOTS.search(r.get("author") or ""))

    days = collections.Counter()
    for r in items:
        days[(r["created_utc"] - open_utc) // 86400] += 1
    dmax = max(days.values()) if days else 1
    scale = min(1.0, 40.0 / dmax)

    auth = collections.defaultdict(lambda: [0, 10 ** 12, 0])
    for r in items:
        a = auth[r.get("author") or "[deleted]"]
        a[0] += 1
        a[1] = min(a[1], r["created_utc"])
        a[2] = max(a[2], r["created_utc"])

    def dstamp(u):
        # Both the elapsed day and the wall clock. The window runs 16:00 to 16:00, so a
        # day index alone reads as the wrong calendar date and a calendar date alone
        # hides how far into the event the item sits. One of the five pilot coders wrote
        # this exact converter three times.
        d = (u - open_utc) // 86400
        return "d%-2d %s" % (d, datetime.datetime.utcfromtimestamp(u).strftime("%m-%d %H:%M"))

    L = []
    w = L.append
    w("# r/%s — coder corpus" % sub)
    w("# window %s  (%.2f days = %.0f hours: the %.0fh event and %.0fh after it)"
      % (" -> ".join(window_label), (end_utc - open_utc) / 86400.0,
         (end_utc - open_utc) / 3600.0, (frz_utc - open_utc) / 3600.0,
         (end_utc - frz_utc) / 3600.0))
    # `human()` is false for a bot AND for an out-of-window ancestor, because neither
    # votes on reading order. Using it here labelled every [CONTEXT] item "automatic" and
    # divided by the in-window denominator, so r/yukon's header read "9 items ... (337%)
    # come from accounts flagged automatic" eight lines above "accounts flagged automatic:
    # none". Reported by the r/yukon coder. Bots are bots; context is context.
    _inwin = [r for r in items if not r.get("_context")]
    bot_chars = sum(len(body(r) or "") for r in _inwin if BOTS.search(r.get("author") or ""))
    bot_items = sum(1 for r in _inwin if BOTS.search(r.get("author") or ""))
    # The headline used to give one number for two populations. Every other tool in the
    # instrument counts in-window items only, so four coders read the two figures as a
    # contradiction between components of the same run. Both are stated here, and the
    # split is named, so the difference reads as a definition rather than a defect.
    w("# %d items in %d threads (%d in-window + %d [CONTEXT]) | %d chars of text "
      "| %d distinct authors"
      % (len(items), len(order), len(_inwin), len(items) - len(_inwin), tot_chars, len(auth)))
    w("#   Every count below, and every count emit reports, is IN-WINDOW ONLY.")
    if bot_items:
        w("# of which %d items and %d chars (%.0f%%) come from accounts flagged automatic"
          % (bot_items, bot_chars, 100.0 * bot_chars / tot_chars if tot_chars else 0))
    w("#")
    w("# COMPUTED BY THE HARNESS — these are exact. Do not recompute them.")
    w("#   posts %d | comments %d" % (n_posts, len(items) - n_posts))
    w("#   replies whose parent is present in this corpus: %d of %d%s"
      % (n_resolved, n_replies, "" if n_resolved == n_replies else "   <- THREADS ARE NOT WHOLE"))
    w("#   items whose text is [deleted] or [removed]: %d (%d of them posts, whose"
      % (gone, gone_posts))
    w("#     removed text sits in selftext rather than body)")
    w("#   accounts whose NAME ends in 'bot', or is AutoModerator: %s"
      % (", ".join("%s (%d)" % (k, v) for k, v in bots.most_common()) or "none"))
    w("#     That sentence is the whole test. It is a string match on the name and not a")
    w("#     judgement about the account: it misses an automated account named anything")
    w("#     else (autotldr, TotesMessenger) and catches a person whose name happens to")
    w("#     end that way. Read the account's own items before treating it as machinery.")
    w("#   num_comments is not carried. It is a snapshot taken at archive time and it lies.")
    w("#   threads run in TIME ORDER of their first in-window item, oldest first, and")
    w("#   nothing is reordered; a thread opened before the window sits where its first")
    w("#   in-window reply falls.")
    w("#   Every thread carries a triage window — its title, the first %d words of its"
      % BODY_CAP)
    w("#   opening post, and its %d most-discussed replies. Many threads are shorter than"
      % TOP_N)
    w("#   that and are simply read whole. %d of the %d have an opening post longer than"
      % (sum(1 for k in order if opening_words(k) >= BODY_CAP), len(order)))
    w("#   the window shows; they are marked where they fall, not moved.")
    n_slice_ctx = sum(1 for r in ctx if r.get("_slice_context"))
    if n_slice_ctx:
        w("#   %d items marked [CONTEXT] are openings of threads an earlier slice holds,"
          % n_slice_ctx)
        w("#   given so the room's running threads are known to you. Read them; never code")
        w("#   or cite them. Their codes belong to the coder who held that slice.")
        ctx = [r for r in ctx if not r.get("_slice_context")]
    if ctx:
        n_before = sum(1 for r in ctx if r["created_utc"] < open_utc)
        n_after = len(ctx) - n_before
        w("#   %d items marked [CONTEXT] fall outside your window — %d before it opens, %d"
          % (len(ctx), n_before, n_after))
        w("#   after it closes. They are here so that every parent resolves (a pre-window")
        w("#   thread arrives as the ancestors of its in-window replies, not entire), and they")
        w("#   are excluded from every count and every share above. Quote")
        w("#   them if you need to — cite reaches them — but they are not this community")
        w("#   acting inside the window you were given.")
    w("#")
    w("# ACTIVITY BY DAY — d0 begins at the moment the canvas opened")
    for d in range(min(days) if days else 0, (max(days) if days else 0) + 1):
        n = days.get(d, 0)
        dt = datetime.datetime.utcfromtimestamp(open_utc + d * 86400).strftime("%m-%d %Hh")
        w("#   d%-3d %s-> %-41s %s" % (d, dt, bar(n, scale), n or ""))
    w("#")
    # Author and thread lists are capped. Uncapped, a 5,000-thread corpus spends more
    # header on the index than the index is worth — but the tail is never silently
    # dropped, because the tail is where a coder decides it has read enough.
    ranked = sorted(auth.items(), key=lambda kv: -kv[1][0])
    w("# AUTHORS — items, first, last%s"
      % ("" if len(ranked) <= 40 else "  (top 40 of %d)" % len(ranked)))
    for a, (n, f, l) in ranked[:40]:
        w("#   %-24s %4d   %-15s %-15s" % (a[:24], n, dstamp(f), dstamp(l)))
    if len(ranked) > 40:
        rest = ranked[40:]
        w("#   ... and %d further accounts holding %d items between them, none above %d"
          % (len(rest), sum(v[0] for _, v in rest), rest[0][1][0]))
    w("#")
    w("# THREADS — in the order they appear below: by first in-window item, oldest first.")
    w("# id, items, chars, and the running share of the window's text. Counts are of what")
    w("# people wrote; where an automatic account also posted, its totals follow in")
    w("# (brackets).")
    hum_tot = sum(hchars(t) for t in order)
    cum = 0
    tail = []
    for rank, tid in enumerate(order, 1):
        # `hchars`/`hitems` exclude bots AND out-of-window [CONTEXT] ancestors, so the
        # "all" figure below differs from the human one for either reason. Labelling that
        # difference "with bot" told three coders their corpus contained machine output
        # when it contained none — r/Greenlantern, r/yerbamate and r/yuyuyu each reported
        # it, and under Rule 11 mislabelling a person as a bot is a way to lose conduct.
        # Count the two separately and name whichever is actually there.
        _bot = [r for r in th[tid] if BOTS.search(r.get("author") or "")]
        _ctx = [r for r in th[tid] if r.get("_context")]
        hc, ac = hchars(tid), sum(len(body(r) or "") for r in th[tid])
        hi, ai = hitems(tid), len(th[tid])
        cum += hc
        share = cum / hum_tot if hum_tot else 0
        _parts = []
        if _bot:
            _parts.append("%d bot" % len(_bot))
        if _ctx:
            _parts.append("%d context" % len(_ctx))
        both = "" if (hc == ac and hi == ai) else \
            "   (%d items %d chars in all: %s)" % (ai, ac, ", ".join(_parts) or "unattributed")
        if share < 0.97 or rank <= 40:
            w("#   %-4d %-8s %5d %8d   %.3f%s" % (rank, tid, hi, hc, share, both))
        else:
            tail.append("%s(%d)" % (tid, hi))
    if tail:
        w("#   the remaining %d threads hold the last %.1f%% of the text. Ids and item"
          % (len(tail), 100 * (1 - (tot_chars - sum(
              len(body(r) or "") for t in [order[i] for i in range(len(order) - len(tail),
                                                                   len(order))]
              for r in th[t])) / tot_chars if tot_chars else 0)))
        w("#   counts, so nothing is hidden from you:")
        line = "#     "
        for t in tail:
            if len(line) + len(t) > 96:
                w(line)
                line = "#     "
            line += t + " "
        w(line)
    w("#")
    w("# HOW TO READ WHAT FOLLOWS")
    w("#   id  day+time  author  score  [flags]  [^parent]")
    w("#   then the item's text, verbatim, to the next blank-line-separated id.")
    w("#   flags: S stickied, M spoke as a moderator, E edited. Absent means not set.")
    w("#   ^abc123 means this is a reply to item abc123. No ^ means it replies to the post.")
    w("#")
    w("#   To quote, run cite against the record file, not against this one:")
    w("#     python3 %s \\" % os.path.join(os.path.dirname(os.path.abspath(path)), "cite.py"))
    w("#            %s \\" % os.path.abspath(path))
    w("#            '<item id>' '<the words you believe are there>'")
    w("#   That file is the same items unrendered, and it is what your offsets are measured")
    w("#   against. You never need to open it; cite reads it for you.")
    w("")

    for rank, tid in enumerate(order, 1):
        rs = th[tid]
        post = posts.get(tid)
        c = sum(len(body(r) or "") for r in rs)
        # Naming this "(post outside window)" made five writers read it as a statement
        # about the THREAD, when the thread's items are in-window and only its opening
        # post is not. r/elonmusk put the cost precisely: its largest thread, 44 items,
        # is "unmoored from any visible topic" — and a reader who does not know why will
        # reconstruct the missing subject, which is the one thing the contract forbids.
        title = ((post or {}).get("title") or
                 "(this thread's opening post falls outside the window; the items below "
                 "are in-window replies to a post you cannot see)")

        # Render the thread into a local block first, remembering where each item
        # starts. Items stay in time order — a thread has to be readable as the thing
        # that happened — but a coder triaging a long one needs to reach the part of
        # it that carries the discussion, and that part is rarely at the top. So the
        # offsets are collected here and turned into a guide printed above the thread.
        blk, at = [], {}
        for r in rs:
            flags = "".join(ch for ch, k in (("S", "stickied"), ("M", "distinguished"),
                                             ("E", "edited")) if r.get(k))
            par = ""
            p = r.get("parent_id") or ""
            if p.startswith("t1_"):
                par = "  ^" + p[3:]
            extra = ""
            if r.get("_slice_context"):
                extra = "  [CONTEXT — an earlier slice's opening; read, never code, never cite]"
            elif r.get("_context"):
                extra = ("  [CONTEXT — after your window]"
                         if r["created_utc"] >= end_utc
                         else "  [CONTEXT — before your window]")
            if r.get("kind") == "post":
                extra = "  POST" + extra        # a context post keeps its mark (v28 dropped it)
                if r.get("url") and r.get("domain") and "self." not in (r.get("domain") or ""):
                    extra += "  %s %s" % (r["domain"], r["url"])
            blk.append("")
            at[r["id"]] = len(blk)
            blk.append("%s  %s  %s  %+d%s%s%s"
                       % (r["id"], dstamp(r["created_utc"]), r.get("author") or "[deleted]",
                          r.get("score") or 0, "  " + flags if flags else "", par, extra))
            blk.append(body(r) or "")

        tw = words(tid)
        kids, own = subtrees(rs, tid)
        ow = 0 if (post or {}).get("_context") else len(
            (((post or {}).get("selftext") or (post or {}).get("body")) or "").split())
        w("=" * 78)
        w("thread %d/%d  %s  %d items  %d chars  %d words   %s"
          % (rank, len(order), tid, len(rs), c, tw, title))
        if windows and (len(kids) > TOP_N or ow > BODY_CAP):
            w("-" * 78)
            w("TRIAGE WINDOW — the title above, the opening post%s, and these %d replies,"
              % (" (first %d of its %d words)" % (BODY_CAP, ow) if ow > BODY_CAP
                 else "", min(TOP_N, len(kids))))
            w("which are the ones with the most discussion under them. Read that much, then")
            w("decide. If it touches the event, read the whole thread. If not, stop here.")
            for i, (cid, nit, nw) in enumerate(kids[:TOP_N], 1):
                w("   %-2d  %-8s  its own %4d words, %5d items and %6d words beneath it   at +%d"
                  % (i, cid, own.get(cid, 0), nit, nw, at.get(cid, 0)))
            if len(kids) > TOP_N:
                w("   (%d further top-level replies, not part of the window)" % (len(kids) - TOP_N))
        w("=" * 78)
        L.extend(blk)
        w("")
    # v29: the counts a case lead's branch gate is decided on, written by the harness
    # rather than recomputed by anyone. `items_in_window` excludes [CONTEXT] items;
    # `items_by_people` and `chars_by_people` exclude [CONTEXT] items and automatic
    # accounts as well, which is what the THREADS index above already counts.
    return "\n".join(L) + "\n", {
        "items": len(items), "threads": len(order), "chars": tot_chars,
        "replies_resolved": [n_resolved, n_replies], "deleted": gone,
        "items_in_window": len(_inwin),
        "items_by_people": sum(hitems(t) for t in order),
        "chars_by_people": hum_tot,
        "threads_with_inwindow_items": sum(1 for t in order if hitems(t) > 0),
        "slice_context_items": sum(1 for r in items if r.get("_slice_context")),
    }


OPEN = 1490976000          # 2017-03-31 16:00 UTC — the canvas opens
FRZ = 1491238800           # 2017-04-03 17:00 UTC — placement disabled, 73h later
END = FRZ + 24 * 3600      # 2017-04-04 17:00 UTC — +24h of reaction. 97h in total.

if __name__ == "__main__":
    src = sys.argv[1]
    sub = sys.argv[2]
    out = os.path.join(os.path.dirname(src), "corpus.txt")
    txt, stats = render(src, OPEN, FRZ, sub,
                        ["2017-03-31 16:00", "2017-04-04 17:00"], END)
    open(out, "w", encoding="utf-8").write(txt)
    stats["jsonl_bytes"] = os.path.getsize(src)
    stats["txt_bytes"] = os.path.getsize(out)
    stats["cut_pct"] = round(100 - 100 * stats["txt_bytes"] / stats["jsonl_bytes"], 1)
    print(json.dumps(stats, indent=1))
