# `package/<room>/themes.jsonl`

The coder's second-order themes for one room.

## What it holds

One line per theme: `theme_id` (t01 and on), `second_order` (the gerund-led label), `theme_note` (what the passages share and what varies), `regrouped_from`, `n_codes` (the coder's count).

## Who writes it, and when

The coder. `build_store.py` copies it and joins it into the store's `themes.jsonl`, where `n_codes` is recounted after retraction and the coder's figure kept as `n_codes_coder`. The build stops if two themes share an id or a code names a theme this file lacks.

## Why it exists

Contract §2: second-order themes are the "within-case consolidation of a room's concepts", the coders' tier, and "Never call the coders' second-order themes third-order themes." They are what the analyst places at B1 and the fleet places at B3. Contract §5: a theme "can be a bag; read its `theme_note` before you place it."

## Where

Example: [package/armenia/themes.jsonl](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/armenia/themes.jsonl).

Checked against: tools/build_store.py, CONTRACT-aggregator.md §2 and §5, package/armenia/themes.jsonl.
