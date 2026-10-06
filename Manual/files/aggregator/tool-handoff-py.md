# `tools/handoff.py`

Stage D1's builder of the labelers' folder and the verdict packets.

## What it holds

From the frozen model, the scheme, the assignments, `prior.md` §8, the store, the coder documents, the forests and the `handoff/` templates, it writes `out/handoff-D/` (`VERSION`, `VOCABULARY.json`, `MODEL.md`, `LADDER.md`, `RETURN-D.md`, `HANDLER.md`, `tasks/<sub>/` and `tasks/index.tsv`), `out/verdict-D/<sub>.md` with `RETURN-D2v.md` and `RETURN-D2v.schema.json`, and `handoff-D.sha256`. The expectations and the field's entries are sealed apart and never served: `out/sealed/EXPECTATIONS.jsonl` and `out/sealed/FIELD.jsonl`, the latter written once, at D1. `--recheck` builds `handoff-D/recheck/` for D3.

## Who writes it, and when

Shipped in the analyst's `tools/`; the analyst runs it at D1 after writing `MODEL-D1.md` and `EXPECTATIONS-D1.jsonl`.

## Why it exists

It "writes no judgement": the model's prose and the expectations are the analyst's. METHOD: the return is Eisenhardt's only if something is predicted before it is seen, hence the expectations. A room whose task cannot be built is listed in `UNBUILT.tsv`, "not invented".

## Where

[tools/handoff.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/handoff.py).

Checked against: tools/handoff.py, METHOD.md, FLEET.md §3, handoff/HANDLER.md.
