# `tools/counts.py`

The denominators, from the canonical files.

## What it holds

It prints `census_rooms`; `dropped` and `analysed_rooms` (null until `out/dropped.jsonl` exists); concepts, themes, threads and items over the census and over the analysed set; `rooms_without_theme`, `rooms_with_one_or_two_themes`; and `assignment_items_expected`, every second-order theme of the analysed set.

## Who writes it, and when

Shipped in the analyst's `tools/`. `validate.py --open` prints its census at every leg; A1 runs it before and after the screen.

## Why it exists

Its docstring: "Run it; never copy its numbers by hand", and "Counts only" (code mass measures the coding, not the room). Rule 5: the three numbers of a counted theme "sum to the analysed set from `counts.py`". Rule 19: a count asserted in a file is computed in the same act from the file that governs.

## Where

[tools/counts.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/counts.py).

Checked against: tools/counts.py, tools/validate.py, CONTRACT-aggregator.md rules 5 and 19, stages/STAGE-A1-reading-room-notes.md.
