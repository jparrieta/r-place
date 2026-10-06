# `tools/build_store.py` (build script)

Stage 00: the joined store from the coders' documents.

## What it holds

Three modes. `--input RUN/INPUT/coders --root RUN` reads each room in `ROOMS.tsv` (`brief.md`, `case.md`, `codes.jsonl`, `themes.jsonl`, `threads.jsonl`, `pointers.jsonl`, `window.json`, `forest/`) and writes `package/<sub>/`, `package/forest.jsonl`, `package/tree_index.json`, `package/FRAME.md`, `trees/<sub>.md` and the store files. `--join-canvas F` writes the six canvas fields into `rooms.jsonl`. `--readme-only` rewrites `README-store.md`. Hard stops: a code whose theme its room lacks; two themes sharing an id; a canvas field in the input.

## Who writes it, and when

Handler side. `build.sh` runs it before stage A1; the analyst's `tools/` does not ship it.

## Why it exists

"Deterministic. Nothing here reads a model or an assignment file; the store is built once, before stage A1, and never rebuilt during a run." Rule 7 keeps the canvas out until `--join-canvas`.

## Where

[aggregator/instrument/tools/build_store.py](../../../aggregator/instrument/tools/build_store.py).

Checked against: tools/build_store.py, harness/build.sh, CONTRACT-aggregator.md rule 7.
