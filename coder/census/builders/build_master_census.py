#!/usr/bin/env python3
"""build_master_census.py — one row per subreddit, and the only place the true count lives.

    python3 build_master_census.py <outdir>

**Why.** The project has been saying "740" for weeks. 740 is what was *downloaded*, not what is a
case. This sheet keeps every subreddit we have, what we know about it, and one column —
`handable` — whose sum is the number we may actually hand the aggregator. When that number moves,
it moves here first and the documents follow.

**The screen is not a verdict.** `screen_class` is a lexical marker count over the 97-hour window.
It agrees with the coders in the direction that matters — of 250 coded, **no community a coder
called `none` has the event named in its text** — but it produces false negatives on non-English
rooms, because the markers are English. r/aeskwadraat, r/azores and r/britaly are all coded `full`
by a reader and score zero here. So a low screen score sets `needs_validation`, never a drop.
"""
import csv, json, os, sys

def load_jsonl(p, key="sub"):
    return {json.loads(l)[key]: json.loads(l) for l in open(p, encoding="utf-8") if l.strip()}

def classify(r):
    h = r["hits"]; soft = h["canvas"] + h["pixel"] + h["coords"] + h["craft"]
    if h["strong"] > 0: return "names_the_event"
    if r["items_in_window"] == 0: return "silent_in_window"
    if soft >= 3: return "talks_without_naming"
    if soft > 0: return "trace_only"
    return "no_event_talk"

def main(outdir):
    here = os.path.dirname(os.path.abspath(__file__))
    A = os.path.join(here, "..", "atlas")
    SB = os.path.join(here, "..", "..", "..", "Sandboxes", "Gioia v28")
    screen = load_jsonl(os.path.join(here, "_screen_progress.jsonl"))
    venue = {r["sub"]: r for r in csv.DictReader(open(os.path.join(here, "venue_summary.csv"), encoding="utf-8"))}
    census = {r["sub"]: r for r in csv.DictReader(open(os.path.join(A, "census_740_mapping.csv"), encoding="utf-8"))}
    facts = load_jsonl(os.path.join(SB, "case_facts.jsonl"))
    # **Adjudications live in a ledger, not in the sheet.** This file is regenerated, so a
    # validation typed into it is lost on the next run — which is how a check gets done twice
    # and then not at all. `validations.jsonl` is where a human or an agent records having read
    # a flagged community, with the evidence, and it survives regeneration.
    vp = os.path.join(here, "validations.jsonl")
    adjudged = load_jsonl(vp) if os.path.exists(vp) else {}

    have_raw = set()
    for d in ("raw24", "raw24_silent", "raw24_post_freeze_only"):
        p = os.path.join(here, "..", d)
        if os.path.isdir(p):
            have_raw |= {f[:-6] for f in os.listdir(p) if f.endswith(".jsonl")}

    cols = ["sub", "downloaded", "window_presence", "coded", "coder_verdict", "positive", "in_population", "coder_model", "n_codes", "n_themes",
            "atlas_artworks", "atlas_area_px", "atlas_names",
            "items_pre168", "items_win97", "items_during73", "items_after_freeze",
            "last_item_hour_in_window",
            "screen_class", "hit_strong", "hit_canvas", "hit_pixel", "hit_coords", "hit_craft",
            "needs_validation", "validated_by", "validation_note", "handable", "disposition"]
    rows = []
    for sub in sorted(screen, key=str.lower):
        s = screen[sub]; v = venue.get(sub, {}); c = census.get(sub, {}); f = facts.get(sub, {})
        cl = classify(s)
        # **The during window is 73 hours, not 97.** A community with nothing while the canvas was
        # open is out of the working set — but "nothing during, something after the freeze" is a
        # third thing and filing it as silence destroys the only evidence it is.
        d73 = int(v.get("n_items_during73") or 0)
        w97 = int(v.get("n_items_win97") or 0)
        presence = ("present" if d73 > 0 else
                    ("post_freeze_only" if w97 > 0 else "silent_in_window"))
        coded = 1 if sub in facts else 0
        verdict = f.get("verdict", "")
        # a coder's reading always outranks the screen
        if coded:
            needs = 0
            validated = "coder"
            note = "coder verdict %s" % verdict
            handable = 1 if verdict in ("full", "trace") else 0
            disp = "case" if handable else "screened_out"
        else:
            needs = 0 if cl == "names_the_event" else 1
            validated = ""
            note = ""
            handable = 1 if cl == "names_the_event" else 0
            disp = "candidate" if handable else "needs_validation"
            # **A room with no text in the window is not a room awaiting validation.**
            # `needs_validation` exists for one reason: the screen's markers are English, so a
            # low score can be a false negative that a human must read past. A venue with zero
            # items in the 97-hour window has nothing for a human to read, and a venue with zero
            # items in the whole 24-day download has nothing at all — the collection *is* the
            # check, and it was run twice. Leaving these flagged put 21 rooms on a reading queue
            # where the reading is empty by construction, which is how a queue stops being read.
            a = adjudged.get(sub)
            if a:
                # A read outranks the screen, exactly as a coder's verdict does.
                needs = 0
                validated = a.get("validated_by", "")
                note = a.get("note", "")
                handable = 1 if a["class"] == "names_the_event" else 0
                disp = "candidate" if handable else "screened_out"
            if presence == "silent_in_window":
                needs = 0
                n_all = int(v.get("n_items_all") or 0)
                validated = "download"
                note = ("empty download: no records anywhere in the 24-day span"
                        if n_all == 0 else
                        "%d records in the span, none in the 97-hour window" % n_all)
        if presence == "silent_in_window" and not coded:
            disp = "silent_in_window"
        if presence == "post_freeze_only":
            # **Ruled out by the PI: post-freeze forums are not added.** They spoke about the
            # canvas only after it had frozen, which is a different thing from organising to
            # place pixels, and pooling them would put rooms that were not there while the
            # problem was live into the population that is supposed to be facing it. Kept,
            # described, and not handed over.
            #
            # **And therefore negative, whatever the coder found.** Four of these six carry a
            # positive verdict — a coder read their after-freeze text and found real canvas
            # talk. The verdict records what was in the text; it does not decide membership of
            # the population, and this is the one place the two come apart. Until 2026-08-31
            # the exclusion was only half-enforced: `handable` dropped them, but any stage
            # counting `coder_verdict in (full, trace)` silently pulled the four back, which is
            # how the positive count read 287 against 283 cases inside the frame. The count is
            # a column now, not a filter each stage reinvents.
            disp = "post_freeze_only"
            handable = 0
            note = ("negative: no items during the 73 hours the canvas was open; "
                    "%s items after the freeze%s" % (
                        v.get("n_items_after_freeze") or 0,
                        ", and a coder read canvas talk in them (verdict %s)" % verdict
                        if verdict in ("full", "trace") else ""))
            validated = validated or "rule"

        # **`positive` is the count.** One column, defined once: a community is positive for the
        # study if it is a case — coded, read as having canvas conduct, and inside the frame.
        # `coder_verdict` stays exactly as the coder wrote it and is not the same question.
        positive = 1 if disp == "case" else 0
        # **`in_population` states the frame and nothing about how anything was read.** The
        # redacted register the analyst receives drops every provenance column, and without this
        # one the population cannot be reproduced from what remains: zero-items-in-73h accounts
        # for the silent and the post-freeze rooms, but not for those a reading set aside. An
        # analyst checking the contract's arithmetic against the register would find it short and
        # have no way to tell which side was wrong.
        in_population = 1 if handable else 0
        rows.append([sub, 1 if sub in have_raw else 0, presence, coded, verdict, positive, in_population,
                     # **Which model read the case.** Not recorded by any manifest before
                     # instrument v28, so for every run before that it is asserted rather than
                     # read: the 250 on the project's Sonnet convention, the 68 of the v27 draw
                     # of 85 on Opus because the dispatcher passed no model argument and the
                     # agents took the parent session's default. It is a condition of the coding
                     # and it belongs in the sheet, stated at the confidence it actually has.
                     f.get("coder_model", ""),
                     f.get("n_codes", ""), f.get("n_themes", ""),
                     c.get("atlas_artworks", ""), c.get("atlas_area_px", ""), c.get("atlas_names", ""),
                     v.get("n_items_pre168", ""), v.get("n_items_win97", ""),
                     v.get("n_items_during73", ""), v.get("n_items_after_freeze", ""),
                     v.get("last_item_hour_in_window", ""),
                     cl, s["hits"]["strong"], s["hits"]["canvas"], s["hits"]["pixel"],
                     s["hits"]["coords"], s["hits"]["craft"],
                     needs, validated, note, handable, disp])
    out = os.path.join(outdir, "MASTER-census.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(cols); w.writerows(rows)

    import collections
    d = collections.Counter(r[cols.index("disposition")] for r in rows)
    print("rows: %d  ->  %s" % (len(rows), out))
    for k, n in d.most_common(): print("   %-20s %4d" % (k, n))
    print()
    print("   HANDABLE TODAY      %4d" % sum(r[cols.index("handable")] for r in rows))
    print("   needs validation    %4d" % sum(r[cols.index("needs_validation")] for r in rows))
    print("   downloaded          %4d" % sum(r[1] for r in rows))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
