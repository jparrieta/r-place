# `CLAUDE.md`

The rules Claude Code loads into every analyst session, binding on every turn.

## What it holds

The reading order at a leg's start: AGENT.md, then `out/_head.md`, the stage file, `mem.py diary --last 5` and `validate.py --open NN`, and nothing else by default. Then the rules for every turn: write as you work with `mem.py log`, never to `out/diary/` by any other route; read through the verbs, since a raw file above about 25,000 tokens is paged; `out/_probe/` and `out/_transcripts/` are the harness's until E1; never delete a file; log and snap every categorization move; close with `done.sh NN`, with `--cut` only where a stage file names one; the head is at most 3,000 words. Last, what the compactor must preserve, in order: the method question in one sentence, the current account, the reasons for the last revisions, the contrary rooms, the next comparison.

## Who writes it, and when

Written with the instrument; `build.sh` copies it to the analyst's root, where Claude Code reads it at the start of each session.

## Why it exists

Contract, "Think on disk, and never rely on having read", and rule 20: the diary is written as you work, through `mem.py log` only. STANDING-INSTRUCTIONS §2 says the harness owns compaction and names this file as the list the compactor keeps.

## Where

[CLAUDE.md](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/CLAUDE.md); source [aggregator/instrument/CLAUDE.md](../../../aggregator/instrument/CLAUDE.md).

Checked against: CLAUDE.md, STANDING-INSTRUCTIONS.md §2, CONTRACT-aggregator.md rule 20, harness/build.sh.
