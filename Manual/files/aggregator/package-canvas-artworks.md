# `package/canvas/artworks.jsonl`

Every atlas artwork, with its pixels, placers and placements by hour.

## What it holds

One line per artwork. The fields `mem.py` reads: `artwork_id`, `name`, `pixels_covered`, `placements`, `placements_smallest_polygon`, `distinct_placers`, `first_hour`, `last_hour`, `subreddits`, `subreddits_in_frame`, `placements_by_hour_0_96`. Other fields: not stated in the sources.

## Who writes it, and when

The handler supplies it in `RUN/INPUT/canvas/`; `build.sh` copies it to `package/canvas/`. `build_neighbours.py` reads it to link artworks to rooms.

## Why it exists

STANDING §1: "every atlas artwork with its index and its placement over time, read beside each room's account; a use is declared (rule 7)." A1 reads each room's placement here for the `made` line of its note, written last. `mem.py canvas` draws each linked artwork's placements as a bar aligned like `when`, with the freeze at hour 73.

## Where

[package/canvas/artworks.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/canvas/artworks.jsonl).

Checked against: STANDING-INSTRUCTIONS.md §1, tools/mem.py, tools/build_neighbours.py, harness/build.sh, stages/STAGE-A1-reading-room-notes.md.
