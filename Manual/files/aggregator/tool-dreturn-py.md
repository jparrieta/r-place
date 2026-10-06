# `tools/dreturn.py`

The one rule set for stage D's returns.

## What it holds

Each op's required fields in a labeler's line and in the ledger, the kind each op carries, the room model's rules (end marker, grade line, concept citations of the room, ids of the vocabulary, every adapted element named), the path a source theme lifts through the placements, and the verdict reader's line with its schema. `ingest.py` applies it to every return before a room enters the ledger; the D2 close-check applies the same functions to what ingest compiled; `handoff.py` writes `RETURN-D2v.schema.json` from it, which `fleet.py` validates every verdict line against.

## Who writes it, and when

Written 2026-09-29 after the audit found that ingest and the D2 check applied different rules (audit 2026-09-29, H11 and H13). A rule changes here, once.

## Links

[ingest.py](tool-ingest-py.md), [the D2 check](tool-checks.md), [handoff.py](tool-handoff-py.md).
