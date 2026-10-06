# `package/pixels.csv`

Placements in each room's region, hour by hour.

## What it holds

Rows per room and hour. The columns the tools read are `sub`, `px_in_region_any`, `px_by_pre_members` and `px_by_window_members`; `mem.py canvas` reports the hours as -16 to 72. Other columns: not stated in the sources.

## Who writes it, and when

The handler supplies it in `RUN/INPUT/canvas/`; `build.sh` copies it into `package/`.

## Why it exists

`mem.py` derives two shares per room from it: `px_window_share` (placed by members who wrote in the window, over all placed in the region) and `px_pre_share` (by pre-event members), shown by `mem.py canvas` and `mem.py facts`. A1 reports "the share of each room's own artwork placed by the people who wrote in it", and the contract's §5 says what that share measures. The manifest's caveat is printed beside it.

## Where

[package/pixels.csv](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/pixels.csv).

Checked against: tools/mem.py, harness/build.sh, stages/STAGE-A1-reading-room-notes.md, tools/checks/stage_A1.py.
