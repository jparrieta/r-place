# `tools/packets.py`

What a fleet reader is served, assembled by script.

## What it holds

Verbs: `scheme` (the shared pages: `index.md` with rule 0 and every family, one page per family with each theme's tests); `B2 --round K`; `B3` (one file per batch with the sibling block per room; a batch over the ceiling is split into parts served to one reader); `B4` (the blind sample, no ruling or hint); `E1` (per sampled room: the rebuilt skeleton, `case.md` and the second-order themes); `files` (the analyst's own files for C2's reviewer and C5's readers). Each build writes `MANIFEST.json`.

## Who writes it, and when

Shipped in the analyst's `tools/`; the analyst runs it in a fleet stage's build leg, before `done.sh NN --cut packets-out`.

## Why it exists

Every reader gets the same page, and nothing on it is the canvas, a room note or another reader's output (rule 7). Every file is asserted under FLEET's 50 KB ceiling and ends with the end line. It logs and analyses nothing.

## Where

[tools/packets.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/packets.py).

Checked against: tools/packets.py, FLEET.md §1, CONTRACT-aggregator.md rule 7.
