# `package/store/neighbours.jsonl`

Every pair of rooms that touch on the canvas or name each other.

## What it holds

One line per ordered pair, both directions written: `sub`, `other`, `shared_artworks` (ids the atlas links to both), `border_px` (pixels of one room's artworks touching the other's), `overlap_px` (pixels covered by an artwork of each), and `mention` (null, or `label`, `n`, `reciprocal`, `direction`: names, named-by or both). A room whose outline the atlas lacks can take its region from `INPUT/canvas/derived_regions.json` (the koi, 541 pixels). `mem.py neighbours` ranks the ties: named both ways, named one way (a claim), shared artwork, overlap, border; the last three are the canvas, the outcome, and stage A2 does not cluster on them.

## Who writes it, and when

`build_neighbours.py`, handler side at build, when `INPUT/canvas/atlas_2017.json` exists. Without it `build.sh` warns that the file "holds no canvas neighbours; mem.py neighbours will say so".

## Why it exists

It serves `mem.py neighbours`, which any stage may read. Its limits: the atlas outline is one annotator's, drawn after the event; a border is not a negotiation; rooms with no artwork in the atlas have no canvas neighbours, "which says nothing about where they built."

## Where

[package/store/neighbours.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/neighbours.jsonl).

Checked against: tools/build_neighbours.py, harness/build.sh, tools/mem.py, STANDING-INSTRUCTIONS.md §1.
