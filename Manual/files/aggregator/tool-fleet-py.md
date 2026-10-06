# `tools/fleet.py` (the handler's)

The dispatch leg of a fleet stage, run outside the analyst's session.

## What it holds

For every packet it sends the shared pages, the packet and the return specification to R fresh readers on the route in `arm.json`, validates each reply (end marker, one JSON object per line, required keys, item count from `MANIFEST.json`), reissues a failed one to a fresh reader id, and writes under `--raw`: `arm.json` (the model that served), per reader `.jsonl`, `.raw.txt`, `.meta.json` and `.failed.txt`, `log.jsonl`, `EXHAUSTED.tsv`, and `DONE` with counts, spend and tokens. Two routes: `gateway` (OpenRouter, a preset alias, the key from the Keychain or `$OPENROUTER_KEY`) and `cli` (the Claude Code CLI on the subscription). An Anthropic model is refused unless `--allow-anthropic` is passed, which `arm.json` sets for C2 and C5.

## Who writes it, and when

The handler, through `dispatch.sh`. `build.sh` leaves it out of the analyst's `tools/` and puts it in `CONTROL/harness/validation_tools/`.

## Why it exists

FLEET §1: "the dispatch is not yours". It "analyses nothing", so no model reads a return before the analyst's check leg does.

## Where

[CONTROL/harness/validation_tools/fleet.py](../../../aggregator/runs/claude-v43-1/CONTROL/harness/validation_tools/fleet.py); source [aggregator/instrument/tools/fleet.py](../../../aggregator/instrument/tools/fleet.py).

Checked against: tools/fleet.py, harness/dispatch.sh, harness/build.sh, FLEET.md §1.
