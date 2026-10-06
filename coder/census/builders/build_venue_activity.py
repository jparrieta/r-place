#!/usr/bin/env python3
"""build_venue_activity.py — the venue histogram, coded and uncoded alike.

    python3 build_venue_activity.py <corpora_dir> <census.csv> <outdir>

**Why this exists.** The coded stream cannot carry a survival measure. A community whose coder
stopped reading at hour 40 and a community that stopped organizing at hour 40 produce the same
curve, and nothing in the aggregator's package separates them. This counts **every item in the
venue, coded or not** — no text, no ids, no authors, just how many things were posted per hour.
It is rule 6 applied to the venue: before anyone can say a room went quiet, we need to know how
many items it could have had.

Resumable: one line per community appended to `_progress.jsonl`, and a re-run skips what is done.
Only `created_utc` is parsed, by regex, because full JSON parsing of 5.1 GB is not worth it.
"""
import csv, glob, json, os, re, sys, time

OPEN = 1490976000          # 2017-03-31 16:00 UTC, the canvas opens
FRZ  = 1491238800          # +73h, placement stops
WIN_END = OPEN + 97*3600   # the coders' window
LO, HI = -168, 336         # one week before to two weeks after, in hours

RE_T = re.compile(rb'"created_utc":\s*(\d+)')

def seg_files(root, sub):
    """**Read `raw24`, not `corpora`.**

    `corpora/` is a derived cut and it is incomplete after the freeze: only **141 of 740**
    communities have an `after` file at all, so for the other 599 everything past roughly hour 73
    is simply absent. r/lithuania is 577 items in `raw24` and 260 in `corpora`; r/hsv is 570
    against 211. The pre- and during-window spans agree exactly — a first build against `corpora`
    matched the census `items_during73` on 720 of 720 — which is precisely why the gap went
    unnoticed: the part that was checkable was right.

    `raw24/<sub>.jsonl` is the complete download and is what this reads.
    """
    # Housekeeping moves a community between raw24/, raw24_silent/ and
    # raw24_post_freeze_only/ AFTER this scan has classified it — so a scanner that
    # reads one root gives a different answer depending on when it is run, and a
    # re-run after a move would silently re-classify a real community as empty.
    # The three folders are one download; search all of them. `root` may be either
    # 30_data/ or 30_data/raw24 — both spellings resolve.
    base = os.path.dirname(root) if os.path.basename(root).startswith("raw24") else root
    for d in (root, os.path.join(base, "raw24"), os.path.join(base, "raw24_silent"),
              os.path.join(base, "raw24_post_freeze_only")):
        p = os.path.join(d, "%s.jsonl" % sub)
        if os.path.exists(p):
            return [p]
    return []

def one(corpora, sub):
    hours, n, first, last, last_win = {}, 0, None, None, None
    for p in seg_files(corpora, sub):
        with open(p, "rb") as fh:
            for line in fh:
                m = RE_T.search(line)
                if not m:
                    continue
                t = int(m.group(1))
                n += 1
                if first is None or t < first: first = t
                if last is None or t > last: last = t
                if OPEN <= t <= WIN_END and (last_win is None or t > last_win): last_win = t
                h = int((t - OPEN) // 3600)
                if LO <= h <= HI:
                    hours[h] = hours.get(h, 0) + 1
    return {"sub": sub, "n_items_all": n, "first_item_utc": first, "last_item_utc": last,
            "last_item_utc_in_window": last_win,
            "n_files": len(seg_files(corpora, sub)), "hours": hours}

def main(corpora, census, outdir):
    os.makedirs(outdir, exist_ok=True)
    subs = [r["sub"] for r in csv.DictReader(open(census, encoding="utf-8"))]
    prog = os.path.join(outdir, "_progress.jsonl")
    done = set()
    if os.path.exists(prog):
        for l in open(prog, encoding="utf-8"):
            try: done.add(json.loads(l)["sub"])
            except Exception: pass
    todo = [s for s in subs if s not in done]
    print("census %d | done %d | to do %d" % (len(subs), len(done), len(todo)), flush=True)
    t0 = time.time()
    with open(prog, "a", encoding="utf-8") as out:
        for i, s in enumerate(todo, 1):
            out.write(json.dumps(one(corpora, s), ensure_ascii=False) + "\n"); out.flush()
            if i % 25 == 0:
                el = time.time() - t0
                print("  %d/%d  %.0fs elapsed, ~%.0fs left" % (i, len(todo), el, el/i*(len(todo)-i)), flush=True)
    print("scan complete", flush=True)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
