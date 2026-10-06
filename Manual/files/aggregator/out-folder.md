# `out/`

The analyst's working folder: the only place it writes, and its memory on disk.

## What it holds

Empty at the start except for the subfolders `build.sh` makes: `_analysis`, `_questions`, `_views`, `_wiki`, `rooms`, `diary`, `model`, `fourth`, `_closes`. STANDING §2 draws the tree with a writer per line (A analyst, S script at close, H harness, F fleet): `_head.md`, `diary/`, `_questions/`, `_views/`, `_wiki/`, `model/`, `prior.md`, `scheme/`, the contract's records (`saturation.jsonl`, `theme_discovery.jsonl`, `multiplacement_log.jsonl`, `dropped.jsonl`, `RUN.json`), `_fleet_raw/`, `handoff-D/`, `forms/`, the append-only ledgers, `adaptations.jsonl`, `adjudications.jsonl`, `rooms/<sub>/`, `_snap/`, `_probe/` and `_transcripts/`. The read logs, `_closes/`, `interview/` and each stage's notes and handback also land here.

## Who writes it, and when

The analyst, through its tools and `mem.py log`; scripts at close; the harness's `close.sh`; fleets and labelers through the drop.

## Why it exists

Contract, "Think on disk": "Your working memory is the file tree in STANDING-INSTRUCTIONS §2." Rule 18: "Your working files are part of the record. Everything in `out/` travels with a fork. Never delete a file you wrote; supersede it with a new name." `pretool_guard.py` blocks deletes.

## Where

[out/](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/).

Checked against: STANDING-INSTRUCTIONS.md §2, CONTRACT-aggregator.md rule 18, harness/build.sh, harness/pretool_guard.py.
