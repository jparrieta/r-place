# `tools/cite.py`

The only way a quote enters an output. Every call is logged.

## What it holds

Verbs: `--room <sub> --code <id>` (one concept's words, verbatim); `--theme <tNN> --n K`; `--tier 3rd|4th|dim --id ...` (quotes under a tier, across rooms); `--resolve "<words>"` (which concept holds these words); `--grep <re>`; `--context K` (the quote with its parent and K items either side). Each quote carries its citation `[sub/code_id]` with item, thread, hour, author and second-order theme. With `--n K`, K are drawn at random under `--seed` (default 0), never the first K by id.

## Who writes it, and when

Shipped in the analyst's `tools/`; the analyst runs it at every stage. It writes one line per call to `out/_cite_reads-NN.jsonl`.

## Why it exists

Rule 3: "Quote what you cite, from the bottom tier, through `cite.py`." A quote is the participant's words, never the coder's label, the theme's label or a note; `--resolve` answers `REJECT` when only a label or note holds the words. The B1 close-check and the E1 audit resolve every exemplar with it. Rule 1: the log is an output.

## Where

[tools/cite.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/cite.py).

Checked against: tools/cite.py, CONTRACT-aggregator.md rules 1 and 3, stages/STAGE-E1-formalizing-audit.md.
