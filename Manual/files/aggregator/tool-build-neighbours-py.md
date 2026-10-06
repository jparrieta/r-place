# `tools/build_neighbours.py` (build script)

Stage 00: who neighbours whom, on the canvas and in the coders' record.

## What it holds

It reads the atlas polygons (`atlas_2017.json`, every `path` of every entry), `package/canvas/artworks.jsonl`, `rooms.jsonl` and `relations.jsonl`, and writes `package/store/neighbours.jsonl` (shared artworks, border pixels by 4-neighbour contact, overlap pixels, and the mention) and `_README-neighbours.md` with the counts. It works on a 1,000 by 1,000 grid.

## Who writes it, and when

Handler side. `build.sh` runs it when `INPUT/canvas/atlas_2017.json` exists, then refreshes `README-store.md`; the analyst's `tools/` does not ship it.

## Why it exists

It serves `mem.py neighbours`. Its stated limits: the polygons are "one annotator's outline at one time" drawn after the event; pixels are counted on the outline, not from the placement log; a mention carries `relations.py`'s limit.

## Where

[aggregator/instrument/tools/build_neighbours.py](../../../aggregator/instrument/tools/build_neighbours.py).

Checked against: tools/build_neighbours.py, harness/build.sh.
