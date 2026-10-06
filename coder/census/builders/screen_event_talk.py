#!/usr/bin/env python3
"""screen_event_talk.py — does this community actually talk about r/place during the window?

    python3 screen_event_talk.py <corpora_dir> <census.csv> <outdir>

`venue_activity.csv` says how many items a community posted. It does not say whether any of them
are **about the event**, and that is the difference between a community that went quiet and a
community that was never here. For the 250 coded we have a coder's verdict. For the other 490 we
have had nothing at all, and the census has been reported as "740" as though all of them were
cases.

This screens every community in the census on the same terms: marker families counted **inside the
window only**, so a mention of the word "place" in the week before is not event talk.

Five families, counted separately rather than pooled, because they carry different weight:

    strong    r/place, /r/place, rplace          — names the event; near-decisive
    canvas    canvas
    pixel     pixel, pixels
    coords    x=123 y=456, (123,456), 123,456    — a location on the canvas
    craft     template, overlay, script, bot     — the tooling of placing

A `strong` hit is what the earlier 42-community audit used. The other four exist so that a
community discussing the event without ever naming it is visible rather than screened out, and so
that a decision to keep or drop rests on numbers a reader can see.

**Nothing here is a verdict.** It produces counts and a proposed class; the coded 250 already have
a coder's verdict and this is checked against it rather than overriding it.
"""
import csv, json, os, re, sys, time

OPEN = 1490976000
WIN_END = OPEN + 97*3600

FAM = {
    "strong": re.compile(rb'(?:/?r/place\b|\brplace\b|\br /place\b)', re.I),
    "canvas": re.compile(rb'\bcanvas\b', re.I),
    "pixel":  re.compile(rb'\bpixels?\b', re.I),
    "coords": re.compile(rb'(?:\bx\s*=\s*\d{1,4}\b|\(\s*\d{1,4}\s*,\s*\d{1,4}\s*\))', re.I),
    "craft":  re.compile(rb'\b(?:template|overlay|placescript|botting)\b', re.I),
}
RE_T = re.compile(rb'"created_utc":\s*(\d+)')

def seg_files(root, sub):
    """`raw24/<sub>.jsonl` — the complete download. `corpora/` is a cut and is missing everything
    after the freeze for 599 of 740 communities, which truncated the first run of this screen."""
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
    hits = {k: 0 for k in FAM}
    items = 0
    example = None
    for p in seg_files(corpora, sub):
        with open(p, "rb") as fh:
            for line in fh:
                m = RE_T.search(line)
                if not m:
                    continue
                t = int(m.group(1))
                if not (OPEN <= t <= WIN_END):
                    continue
                items += 1
                for k, rx in FAM.items():
                    n = len(rx.findall(line))
                    if n:
                        hits[k] += n
                        if k == "strong" and example is None:
                            i = rx.search(line).start()
                            example = line[max(0, i-70):i+70].decode("utf-8", "replace")
    return {"sub": sub, "items_in_window": items, "hits": hits, "example": example}

def main(corpora, census, outdir):
    subs = [r["sub"] for r in csv.DictReader(open(census, encoding="utf-8"))]
    prog = os.path.join(outdir, "_screen_progress.jsonl")
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
            if i % 50 == 0:
                el = time.time()-t0
                print("  %d/%d  %.0fs, ~%.0fs left" % (i, len(todo), el, el/i*(len(todo)-i)), flush=True)
    print("screen complete", flush=True)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
