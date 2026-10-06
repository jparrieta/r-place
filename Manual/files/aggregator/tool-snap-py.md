# `tools/snap.py`

The record of what existed when: a hash of every file in `out/` under a name.

## What it holds

`snap.py NN <label>` writes `out/_snap/NN-<label>.sha256`: a header line, then one line per file under `out/` (except `_snap/`) with its sha256, size in bytes, the time of the snap and its path. A second snap with the same stage and label is refused. `snap.py --verify <file>` prints, per file, unchanged, changed or gone, and exits 1 if anything changed.

## Who writes it, and when

Shipped in the analyst's `tools/`. The analyst takes a snap for each move (`move-<move>-<n>`) and when an order matters; `close.sh` takes one at every close with its trusted copy.

## Why it exists

"A snap is written once under its name ... because a snap that can be rewritten proves nothing." STANDING §2: move snaps let a reviewer "find the state before and after". Its docstring still names some orderings by older stage numbers.

## Where

[tools/snap.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/snap.py).

Checked against: tools/snap.py, harness/close.sh, STANDING-INSTRUCTIONS.md §2, CLAUDE.md.
