# `tools/mem.py`

The store and the analyst's own files, one page at a time, and the only writer to the diary.

## What it holds

Reading verbs in groups: one room (`room`, `case`, `brief`, `forest`, `when`, `canvas`, `compare`, `note`); concepts and themes (`codes`, `theme`, `themes`, `after`, `pairs`); room facts (`facts`); the analyst's files (`notes`, `progress`, `neighbours`, `scheme`, `where`, `rooms`, `contrast`, `adaptations`, `finding`, `question`, `table`, `view`, `wiki`, `shelf`, `contract`, `diff-scheme`, `diff-model`, `diary`). Writers: `log`, at any stage (a logged merge or split at B1 is a new kind for the stopping rule); `mint`, refused outside B1, C1 and D3 (after B1 it stamps the discovery only, and the theme is written into `scheme_v2.jsonl`); `place` and `unplace`, B1 only; `reassign`, which re-places a second-order theme in `assignments_final.jsonl` after a recut, C1 to D6; `idea`, B1, C1 and D3; `adjudicate`, refused outside D3. At B1, `mint`, `place` and a logged merge or split append to `out/kinds-B1.jsonl`, the stopping rule's record. Pages are 80 lines, each ending with a marker; a wrong room or id is refused with the nearest name.

## Who writes it, and when

Shipped in the analyst's `tools/`. Every call appends a line to `out/_mem_reads-NN.jsonl`. It overlays the analyst's placements, fourth-order themes and dimensions from `out/` at query time; nothing in `package/` is rewritten.

## Why it exists

Rule 1: every read of the store or the analyst's own files goes through it, and "Where your account of your reading and the log disagree, the log is right." Rule 20: the diary is written "through `mem.py log` only". CLAUDE.md: read files through the verbs.

## Where

[tools/mem.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/mem.py).

Checked against: tools/mem.py, tools/NEW-VERBS.md, STANDING-INSTRUCTIONS.md §1, CONTRACT-aggregator.md rules 1 and 20, CLAUDE.md.
