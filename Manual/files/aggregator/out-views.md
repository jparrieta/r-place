# `out/_views/`

Generated tables over the analyst's files, rebuilt at every close.

## What it holds

`data-structure.tsv` and `.md` (quote, first-order concept, second-order theme, third-order theme, fourth-order theme, aggregate dimension, one row per concept); `rooms-x-third.tsv`; `rooms-x-elements.tsv`; `relations.tsv`; `transitions.tsv`; `moves.tsv`; and after D3 `rooms-x-adaptations.<level>.<kind>.tsv`, `distance.tsv`, `distance.<kind>.tsv`, `tree-likeness.json`. Each carries the sha256 of its sources.

## Who writes it, and when

`gen_views.py`, run by `done.sh` at every close; `distance.py` for the adaptation files. Never edited. Read with `mem.py view [name] [--grep] [--room]`.

## Why it exists

Rule 15: where a display and its file disagree, "the file is right." STANDING §2 lists comparisons "each served by a verb or a generated view, never by reading rooms in order". `links.py` resolves the ids the views name.

## Where

[out/_views/](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/_views/).

Checked against: tools/gen_views.py, tools/distance.py, tools/done.sh, CONTRACT-aggregator.md rule 15, STANDING-INSTRUCTIONS.md §2.
