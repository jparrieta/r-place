#!/usr/bin/env python3
"""
cut_window.py — re-cut a coder corpus to the v29 window (unchanged since v26).

VERSION 26.  The during-coder's window is the event and one day of reaction:

    OPEN  2017-03-31 16:00 UTC   the canvas opens
    FRZ   2017-04-03 17:00 UTC   placement disabled, 73h later
    END   2017-04-04 17:00 UTC   +24h.  97 hours in total.

WHY THIS WINDOW.  The old cut ran to FRZ + 7 days on the reasoning that a community's own
retrospective account of the event is the one thing you cannot see anywhere else.  That
reasoning was tested rather than argued: across three independent Opus codings and one
early full coding of one community, 748 of 748 codes fall inside END, the last one at +39h, and
the v13 coder read seventy threads beyond END *in full* and coded none of them.  It looked
and there was nothing there.

There is no pre-period.  r/place was an unannounced April Fools feature, so no community
could discuss the canvas before it existed; the ordinary-week baseline that Rule 6 needs is
the brief's job, and a single pre-day would in any case be whatever that community happened
to be doing — for one community, the day before a fixture its members care about.

WHAT IS KEPT.  A thread with at least one item inside the window is kept ENTIRE, including
items on either side of the boundary, which are marked `_context`.  Threads must stay whole
so that every parent resolves and cite() can reach anything quotable — the same reason
pre-window ancestors were always carried.  The tail is cheap: on one measured corpus it is 394
items against 16,161 dropped.

WHAT IS DROPPED.  A thread with no item inside the window is dropped entirely.  On
one measured corpus that is 362 of 731 threads — overwhelmingly match threads and transfer news
from the six days after the canvas froze.

    python3 cut_window_v32.py IN.jsonl OUT.jsonl
"""

import collections
import json
import sys

VERSION = "cut-v32"
WINDOW_REVISION = "w2-2026-07-29"

OPEN = 1490976000
FRZ = 1491238800
END = FRZ + 24 * 3600
LABEL = ["2017-03-31 16:00", "2017-04-04 17:00"]


def thread_of(r):
    if r.get("kind") == "post":
        return r["id"]
    li = r.get("link_id") or ""
    return li[3:] if li.startswith("t3_") else (li or "?")


def body(r):
    return r.get("selftext") if r.get("kind") == "post" else r.get("body")


def cut(inp, outp):
    items = []
    with open(inp, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if "id" in r:
                items.append(r)

    th = collections.defaultdict(list)
    for r in items:
        th[thread_of(r)].append(r)

    kept, dropped, ctx_before, ctx_after = [], 0, 0, 0
    for tid, rs in th.items():
        if not any(OPEN <= r["created_utc"] <= END for r in rs):
            dropped += 1
            continue
        for r in rs:
            if r["created_utc"] < OPEN:
                r["_context"] = True
                ctx_before += 1
            elif r["created_utc"] > END:
                r["_context"] = True
                ctx_after += 1
            else:
                r.pop("_context", None)
        kept.extend(rs)

    kept.sort(key=lambda r: (r["created_utc"], r["id"]))

    # thread index, ordered by human text share — bots and out-of-window items do not vote,
    # exactly as the renderer counts them.
    bysize = collections.defaultdict(lambda: [0, 0])
    for r in kept:
        if r.get("_context"):
            continue
        e = bysize[thread_of(r)]
        e[0] += 1
        e[1] += len(body(r) or "")
    total = sum(v[1] for v in bysize.values()) or 1
    order = sorted(bysize.items(), key=lambda kv: -kv[1][1])
    index, cum = [], 0
    for rank, (tid, (n, c)) in enumerate(order, 1):
        cum += c
        index.append({"thread_id": tid, "index_rank": rank, "items": n,
                      "chars": c, "cum_text_share": round(cum / total, 4)})

    header = {
        "_thread_index": index,
        "_n_threads": len(bysize),
        "_n_items": sum(1 for r in kept if not r.get("_context")),
        "_n_context_items": ctx_before + ctx_after,
        "_n_context_before": ctx_before,
        "_n_context_after": ctx_after,
        "_window_utc": LABEL,
        "_window_revision": WINDOW_REVISION,
        "_cut": VERSION,
    }
    with open(outp, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(header, ensure_ascii=False) + "\n")
        for r in kept:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    return {"threads_in": len(th), "threads_kept": len(bysize), "threads_dropped": dropped,
            "items_in": len(items), "items_kept": len(kept),
            "items_in_window": header["_n_items"],
            "context_before": ctx_before, "context_after": ctx_after}


if __name__ == "__main__":
    print(json.dumps(cut(sys.argv[1], sys.argv[2]), indent=1))
