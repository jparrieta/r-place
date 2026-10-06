# `handoff/` (RETURN-D.md, TASK-template.md, HANDLER.md)

The templates stage D1 turns into the labelers' folder.

## What it holds

`RETURN-D.md`: what a labeler returns, `model-D.md` (the room's case rewritten in the model's vocabulary, every claim carrying an element id or `[new: ...]` and a concept citation) and `adaptations.jsonl`, and how both are checked. `TASK-template.md`: one room's task and its reading order (RETURN-D.md, MODEL.md, LADDER.md, then case.md, themes.jsonl, codes.jsonl, brief.md, forest.md, placements.jsonl). `HANDLER.md`: the adaptation handler's brief: one fresh OpenAI Codex session per room, rooms by size ascending, returns into `DROPS/D/<sub>/`, `ingest.py D --check <sub>` after each room, `DROPS/D/DONE` at the end.

## Who writes it, and when

Written with the instrument. `build.sh` copies them to `DROPS/D1/handoff/`; at D1 `handoff.py` reads them and writes `out/handoff-D/`.

## Why it exists

FLEET §3: "`RETURN-D.md` carries this text verbatim" (the verdict's criterion). HANDLER.md keeps the handler outside the run: "you never read or write anything in it except this folder and the drop folder."

## Where

[aggregator/instrument/handoff/](../../../aggregator/instrument/handoff/).

Checked against: handoff/HANDLER.md, handoff/RETURN-D.md, handoff/TASK-template.md, harness/build.sh, tools/handoff.py, FLEET.md §3.
