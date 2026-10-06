# `package/DATA-manifest-canvas.md`

The manifest of the canvas files, with the caveat the tools print.

## What it holds

A description of the canvas inputs. The one passage the tools read is its bold line "A per-community rate is fine; a canvas-wide total is not." `mem.py` adds that regions overlap and a contested pixel counts for every room that claims it. The rest of its content: not stated in the sources.

## Who writes it, and when

The handler supplies it in `RUN/INPUT/canvas/`; `build.sh` copies it into `package/`.

## Why it exists

Rule 7 asks that "what the canvas measures is stated wherever a canvas figure appears". `mem.py canvas` prints the caveat under every room's canvas block, then "rule 7: you may use this; declare where it shaped a reading."

## Where

[package/DATA-manifest-canvas.md](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/DATA-manifest-canvas.md).

Checked against: tools/mem.py, harness/build.sh, STANDING-INSTRUCTIONS.md §1, CONTRACT-aggregator.md rule 7.
