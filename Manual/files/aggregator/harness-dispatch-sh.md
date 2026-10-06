# `harness/dispatch.sh`

Sends a fleet stage's packets to readers, outside the analyst's session.

## What it holds

`dispatch.sh NN [--round K] [--only ...] [--dry-run] [--recheck]`. It refuses while an analyst launch is active or when `DONE` already exists; reads the readers (route, model, n, shared pages) from `arm.json`; runs the trusted `fleet.py` over `out/_packets-NN/` (B2 by round; D2 over `out/verdict-D/`); logs to `handover-events.log`; prints the check leg to open. At D2 it also names the handler's brief for Codex; with `--recheck` at D3, the re-check brief.

## Who writes it, and when

The handler, in a Terminal on the Mac (the OpenRouter key is in the Keychain), after `close.sh` has checkpointed the build leg.

## Why it exists

Contract §4: the dispatch runs "outside your session", and "nothing in it reads your files". It "analyses nothing".

## Where

[harness/dispatch.sh](../../../aggregator/runs/claude-v43-1/CONTROL/harness/dispatch.sh).

Checked against: harness/dispatch.sh, tools/fleet.py, CONTRACT-aggregator.md §4.
