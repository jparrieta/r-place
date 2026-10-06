# `tools/distance.py`

The stage D4 distance between rooms, from the adaptation ledger.

## What it holds

It reads accepted and modified lines whose lift exists (particulars, pending and rejected lines excluded) and writes `_views/rooms-x-adaptations.<level>.<kind>.tsv`, `_views/distance.tsv`, `_views/distance.<kind>.tsv` and `_views/tree-likeness.json`. The distance is d = (1 - S) / 2 with S from -1 to 1: 0 identical, 0.5 unrelated, 1 opposite. A room with no lines is 0.5 from every adapted room. Tree-likeness is the delta score over sampled quartets.

## Who writes it, and when

Shipped in the analyst's `tools/`; `gen_views.py` calls it after D3.

## Why it exists

It implements SCHEMA-adaptations §7, "the ladder walk times the operation agreement". Its weights and grades come from `prior.md` §7, written at D1 before any adaptation is seen, else the defaults.

## Where

[tools/distance.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/distance.py).

Checked against: tools/distance.py, tools/gen_views.py, PRIOR-template.md.
