# `tools/gen_views.py`

Regenerates `out/_views/` and `out/_wiki/` from the canonical files.

## What it holds

It writes, when the sources exist: `_views/data-structure.tsv` and `.md` (quote to dimension, one row per first-order concept; above 2 MB the `.md` holds only a pointer to `mem.py view`); `rooms-x-third.tsv`; `rooms-x-elements.tsv`; `relations.tsv`; `transitions.tsv`; `moves.tsv`; `_wiki/rooms/<sub>.md` and `_wiki/model/<id>.md`. After D3 it calls `distance.py`. Every file carries the sha256 of its sources in its header.

## Who writes it, and when

Shipped in the analyst's `tools/`; `done.sh` runs it at every close.

## Why it exists

Rule 15: "A display owes its file. Views and wiki pages are generated from files by `gen_views.py` and never edited; where a display and the file it displays disagree, the file is right."

## Where

[tools/gen_views.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/gen_views.py).

Checked against: tools/gen_views.py, tools/done.sh, CONTRACT-aggregator.md rule 15.
