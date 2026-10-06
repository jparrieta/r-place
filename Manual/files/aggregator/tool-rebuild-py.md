# `tools/rebuild.py`

A room's model rebuilt from the global model plus its accepted adaptations.

## What it holds

It prints the skeleton: every element of the global model at the frozen version, in dimension order, with the room's accepted or modified lines applied (instantiated with source theme and how, absent, conditioned, extended by a step, linked, restricted, contradicted), and the proposed elements the room contributed. `--json` gives the same as data.

## Who writes it, and when

Shipped in the analyst's `tools/`. `packets.py E1` calls it for each sampled room.

## Why it exists

METHOD: E1 "rebuilds sampled rooms from the global model plus their adaptations"; the contract's §2 says the typing exists so "a room's model can be rebuilt from the global model plus its adaptations." It never reads `model-D.md`, so the E1 reader compares the rebuild with the coder's blind `case.md`.

## Where

[tools/rebuild.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/rebuild.py).

Checked against: tools/rebuild.py, tools/packets.py, METHOD.md, CONTRACT-aggregator.md §2.
