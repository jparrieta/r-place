# `arm.json`

Which model serves each stage, and which readers each fleet uses.

## What it holds

One entry per stage A1 to E2: `analyst` (claude-opus-5-5 throughout) and `effort` (medium for A1, B2, B3, D1, D2, E1; xhigh for the rest). Fleet stages add `readers`: B2 gateway `@preset/cheap` n 3; B3, B4 and D2 gateway `@preset/cheap` n 2; E1 gateway `@preset/cheap` n 1; C2 and C5 cli route, claude-opus-5-5, n 1, `allow_anthropic` true. D2 also names the labelers: GPT in OpenAI Codex, one fresh session per room. A leg may override its stage.

## Who writes it, and when

Written with the instrument; `build.sh` copies it to `CONTROL/arm.json`.

## Why it exists

Its note: read by `step.sh` (model and effort), `close.sh` (the model audit) and `dispatch.sh` (the readers). HOW-TO-RUN: "You never change route inside a session." FLEET §1 sets R = 2 readers per item at B3 and B4, and three at the pilot, B2. At C2 and C5 `n` is per packet: C5 builds three packets, one reader each, so three readers.

## Where

Source [aggregator/handler/claude/arm.json](../../../aggregator/handler/claude/arm.claude.json); in a run, `CONTROL/arm.json`.

Checked against: harness/arm.json, harness/build.sh, harness/close.sh, harness/dispatch.sh, HOW-TO-RUN.md, FLEET.md §1.
