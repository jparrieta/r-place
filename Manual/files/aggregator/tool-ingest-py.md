# `tools/ingest.py`

Validates the labelers' returns and compiles the adaptation ledger.

## What it holds

The rules are `dreturn.py`'s, the same the D2 close-check applies (audit 2026-09-29). Six rules on every line: the schema; the model version matches `handoff-D/VERSION` and element ids exist and are not withdrawn; concept ids exist and are not retracted; `how` is one sentence under forty words; portability (no subreddit name or proper name outside the relation field, else `portable=false`, a particular); the end marker matches. Then each source node is lifted to third-order, fourth-order and dimension. The room model's own rules follow (a grade line, citations of the room's concepts, every adapted element named), and a none line must be the whole return. Output: `out/adaptations.jsonl` (or `adaptations-recheck.jsonl`, ids `R-<sub>-NNN`), `out/ingest-D.md`, `out/verdicts-D.jsonl` from the verdict fleet's returns, the room copies in `out/rooms/<sub>/`, the D2 counts in `RUN.json`, and every rejected room in `DROPS/D/UNRETURNED.tsv`. The harness runs it when the D2 check leg opens (and `--recheck` when D3b opens). `--relift` re-lifts the ledger to the model as it stands, at D3c.

## Who writes it, and when

Shipped in the analyst's `tools/`. The handler runs `--check <sub>` after each room; the analyst runs `ingest.py D` in D2's check leg.

## Why it exists

Rule 12: an adaptation "counts only if it names a node id that ingest resolves, is stated as a condition another room could meet". FLEET §3 lists the same checks.

## Where

[tools/ingest.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/ingest.py).

Checked against: tools/ingest.py, CONTRACT-aggregator.md rule 12, FLEET.md §3, handoff/HANDLER.md.
