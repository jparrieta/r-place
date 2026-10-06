# `package/store/_README-neighbours.md`

The neighbours file's own dictionary entry, with its counts.

## What it holds

A section on `neighbours.jsonl`: ordered room pairs that touch, each written both ways; how many share an artwork, border on the atlas outline, overlap, are named in the coders' record, or are both on the canvas and named; rooms with at least one neighbour; artworks with an outline and a room of the frame; atlas entries not joined by name. Then the limit: "a border is where two outlines meet, not a negotiation. A mention is a pointer a coder recorded."

## Who writes it, and when

`build_neighbours.py`, handler side, when `build.sh` finds `INPUT/canvas/atlas_2017.json`; `build_store.py --readme-only` then folds it into `README-store.md`.

## Why it exists

`build_neighbours.py` states the limits in its docstring: the atlas outline is one annotator's, drawn after the event, and pixels are counted on the outline, not recounted from the placement log.

## Where

[package/store/_README-neighbours.md](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/_README-neighbours.md).

Checked against: tools/build_neighbours.py, tools/build_store.py, harness/build.sh.
