# `out/diary/`

The running log of the run, written as the analyst works.

## What it holds

Files `NN-k.jsonl`, one series per stage. Each line: `t` (UTC time), `stage`, `leg` (from `.leg`), `kind`, `ids`, `text`. A part rolls to the next number at 1,500 words. The kinds: opened, dropped, merged, split, kept, move, abductive, question, comparison, note, helper, minted, placed, unplaced, pause, and any kind a stage file names in a `log --kind` line. A leg's closing line summarises it in three sentences.

## Who writes it, and when

The analyst, only through `mem.py log`; `mem.py mint`, `place` and `unplace` log their own kinds. `pretool_guard.py` blocks Write, Edit and shell writes into `out/diary/`. Read with `mem.py diary --last N` (default 5) or `--grep <id>`.

## Why it exists

Rule 20: "A diary written at the close from memory is a reconstruction and is not a diary." STANDING §2: "The diary is not read whole by anyone"; the last five entries start every leg, and E1 computes over it and checks it against the transcripts.

## Where

[out/diary/](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/diary/).

Checked against: tools/mem.py, harness/pretool_guard.py, CONTRACT-aggregator.md rule 20, STANDING-INSTRUCTIONS.md §2, stages/STAGE-E1-formalizing-audit.md.
