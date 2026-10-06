# `out/_transcripts/`

A copy of every leg's session transcript, filed at its close.

## What it holds

`leg-<NN.LEG>-<session id>.jsonl`, the transcript as Claude Code wrote it, and `INDEX.md`, a table with one row per leg: leg, session, file, lines, closed.

## Who writes it, and when

`close.sh`, after it verifies the transcript (every line parses, at least one assistant turn) and before it builds the checkpoint.

## Why it exists

E1 checks the diary against the transcript for legs drawn by seed, "an entry the transcript does not bear out is a defect", and METHOD promises that "every prompt, input, output, transcript and model identifier is archived". It is closed to the analyst before E1 by the permission rules and the sandbox. The session files themselves sit in `CONTROL/.cc/`, whose retention `protocol_guard.py` sets to 36,500 days: "transcripts are the run's memory".

## Where

[out/_transcripts/](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/_transcripts/).

Checked against: harness/close.sh, harness/protocol_guard.py, harness/settings.template.json, METHOD.md, stages/STAGE-E1-formalizing-audit.md.
