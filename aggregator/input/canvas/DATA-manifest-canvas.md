# The canvas — manifest

**In the package from the start** (the contract's §2, §4 and rule 7). Three files: `case_facts_outcome.jsonl`, the six canvas fields per room, joined into
`store/rooms.jsonl` at build and shown by `mem.py room`; and `pixels.csv`, the placement series.
`canvas/artworks.jsonl`, below, is the third. They are the outcome measured on the canvas rather than reported in the room, and they exist so
that the study can say something about doing rather than only about saying. What they may do in
your work is rule 7's: data about what was made, never a warrant; never a feature, never a ground
for a cut or a placement; never served to a fleet or a reader; and what they measure is stated
wherever a canvas figure appears.

---

## `case_facts_outcome.jsonl` — one line per room of the census

    sub, canvas_entries, canvas_area_px, canvas_centre, canvas_ring, canvas_artwork, canvas_source

`canvas_entries` is the number of atlas entries linked to the room; `canvas_area_px` the area of
the atlas polygon(s), in pixels, not a recount from the pixel log; `canvas_centre` the centroid
`[x, y]` on the 1000 × 1000 canvas; `canvas_ring` one of `centre`, `middle`, `edge`, a coarse band of distance from the centre;
`canvas_artwork` the atlas's name for what was drawn; `canvas_source` the provenance sentence,
repeated on every line on purpose. Source: placeAtlas 2017 (github.com/placeAtlas/atlas-2017),
1,473 entries. The atlas records what survived the last hour of a 97-hour event: a room that
organized, placed and was overwritten before the freeze has no artwork and no row, and nothing
repairs that. This is the one measure in the package not made of a community's own words; treat
it as an outcome, never as evidence of intent.

## `pixels.csv` — one row per room per hour

    sub, hour_since_open, px_in_region_any, px_by_pre_members, px_by_window_members

Hours **−16 to +72**. The published placement record begins about sixteen hours before the 97-hour
window opens, which is why the range starts where it does.

**Definitions, because the column names do not carry them.** A placement counts for a community
if it lands inside that community's region, the union of the atlas artworks linked to it.
`pre_members` posted in the venue in the 168 hours before the window; `window_members` posted
inside `[OPEN, FRZ + 7 days]`. Both membership columns are **placements in the community's own
region by its own people**, not placements anywhere on the canvas.

**How the membership columns are possible.** The placement record identifies a placer as
`base64(sha1(username))` and the venue record identifies a poster by handle. The join does not
need to run backwards: hashing a *known* handle with the same recipe reproduces the placer string
exactly. So *did this community's people place these pixels* is answerable and *who placed this
pixel* is not.

**Regions overlap and nothing adjudicates it.** 1,231,586 pixel-community pairs cover 921,826
distinct pixels, an overlap factor of 1.34, so a contested pixel counts for every community that
claims it, and the columns summed across communities (22.6 M) exceed the placement count
(16.6 M). **A per-community rate is fine; a canvas-wide total is not.**

**Two checks it passed.** The parse independently reproduces the published record's own figures,
1,166,924 distinct placers and 16,556,641 in-range placements, with 3,256 out-of-canvas rows
dropped. And `px_by_window_members`, which counts inside the region, never exceeds an independent
count of the same authors' placements anywhere: 740 communities checked, 0 violations.

---

## What it closes, and what it does not

The contract's §4 names the widest limit on the study: everything the analyst can see is text,
and most of the work left no text. `px_by_window_members` against `px_in_region_any` is the share
of a community's own artwork placed by people who wrote in its room, the one measure that bears
on how far the text stands in for the doing; stage 01 reports its distribution and every later
canvas figure carries §4's sentence beside it. The frame is the rooms whose coding finished, not
a random draw of the population, so any association between what a room did and what it kept is
measured on that frame; say which way a selection could bias it wherever a canvas figure appears. The
canvas says nothing about whether the room went on, whether the arrangements held or whether
anyone came back: a null here is not a null on §1's last question.

---

## `canvas/artworks.jsonl` — one line per atlas artwork (1,473)

    artwork_id, name, subreddits, subreddits_in_frame, pixels_covered, centre, placements,
    placements_smallest_polygon, distinct_placers, first_hour, last_hour, placements_by_hour_0_96

Every placement in the pixel record routed to the artwork or artworks whose atlas polygon holds
it. `pixels_covered` counts the canvas pixels inside the polygon (a raster count, so it runs a
little above `canvas_area_px`, which is the polygon's area). `placements_smallest_polygon` counts
only the placements where this artwork is the smallest polygon holding the pixel. Hours are from
the canvas opening; placement stopped at hour 73. `placements_by_hour_0_96` is the artwork's
placement over time, one count per hour. Read it beside a room's account for the `made` line; it
is never a feature, a cut or a ground for a placement (rule 7).


## Derived regions (2026-09-28)

`derived_regions.json` holds one region no atlas entry outlines: r/OrderOfTheKoi's koi, 541 pixels drawn from the pixel record (hours 38 to 60), erased before the freeze. It is that room's canvas region in `case_facts_outcome.jsonl` and `pixels.csv`, and it enters `store/neighbours.jsonl` as its own region (it lies inside the Flag of Italy). It is not an atlas artwork and is not in `artworks.jsonl`.
