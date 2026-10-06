# `package/case_facts_outcome.jsonl`

The canvas outcome per room: the six canvas fields.

## What it holds

One line per room, keyed by `sub`, carrying `canvas_entries`, `canvas_area_px`, `canvas_centre`, `canvas_ring`, `canvas_artwork` and `canvas_source`. Any other field: not stated in the sources.

## Who writes it, and when

The handler supplies it in `RUN/INPUT/canvas/`. `build.sh` copies it into `package/` and runs `build_store.py --join-canvas`, which writes the six fields into `store/rooms.jsonl` and nowhere else; a room with no line gets six nulls. `build.sh` refuses a partial canvas: "the canvas joins whole or not at all".

## Why it exists

Rule 7: "The canvas is what was made: use it, and say where you did." Contract §5: the atlas "is not a score"; it records what survived the last hour. `build_store.py` refuses to build if a coder's input carries a canvas field.

## Where

[package/case_facts_outcome.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/case_facts_outcome.jsonl).

Checked against: harness/build.sh, tools/build_store.py, CONTRACT-aggregator.md rule 7 and §5, tools/checks/stage_A1.py.
