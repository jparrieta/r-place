# `READ-ME-FIRST.md` (the run's)

The first page for the person who runs the study: three parties, how a leg works, and the lines to type.

## What it holds

The run's shape (sections, stages, steps, leg ids); how a leg works (it continues the last close's conversation, runs in `dontAsk`, may ask the principal investigator, may start helpers, never runs readers, and closes with five recall questions, a model audit and a checkpoint); the acceptance tests once before A1 and the leg handler's live check; every leg, through `legs.py` or by hand (`step.sh`, then `close.sh`); a dispatch; pausing; interviews, both ways; stage E2's proposal; and who talks to the analyst: only the principal investigator, through `legs.py`, recorded in `CONTROL/messages-to-legs.jsonl`.

## Who writes it, and when

Written with the instrument; `build.sh` copies it to the run's root, where the analyst's sandbox denies reading it.

## Why it exists

It names the three parties: the analyst, "a Claude session that lives in `00_GIVE-THE-AGENT/` and sees nothing else"; the handler, who builds the run and answers questions in files; and the reader of the page, "you, who own the study and decide".

## Where

Source [aggregator/handler/claude/READ-ME-FIRST.md](../../../aggregator/handler/claude/READ-ME-FIRST.md).

Checked against: harness/READ-ME-FIRST.md, harness/build.sh, harness/settings.template.json.
