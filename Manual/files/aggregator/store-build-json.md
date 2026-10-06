# `package/store/_build.json`

The build record: what went into the store and what came out.

## What it holds

`input` and `rooms_tsv`; counts (`communities`, `codes`, `codes_retracted_dropped`, `themes`, `threads`, `items`, `items_coded`, `items_bridge`, `items_removed`, `items_dropped`, `pointers`, `codes_unjoined` with `codes_unjoined_by_sub`); `themes_n_codes_mismatch` per room; `briefs`; `open_utc`, `freeze_utc`, `end_utc`; `frame` (date, rooms, sha256); after the join, `canvas` (`joined_from`, `rooms_joined`, `rooms_without_outcome_line`, `fields`).

## Who writes it, and when

`build_store.py` at stage 00; `--join-canvas` adds the canvas block.

## Why it exists

`write_readme` fills `README-store.md`'s counts from it. A theme whose coder count differs from the codes naming it "is reported, not fatal". A1 recomputes the build figures, and "What you compute wins; carry both to stage E1."

## Where

[package/store/_build.json](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/_build.json).

Checked against: tools/build_store.py, stages/STAGE-A1-reading-room-notes.md.
