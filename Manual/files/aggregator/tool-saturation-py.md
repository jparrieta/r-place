# `tools/saturation.py`

The stopping rule: when a stage may stop reading, and the proof that going on would have found nothing.

## What it holds

Verbs: `order --stage B1` (B1's seeded order printed, each room read or unread, for the second pass); `status --stage B1` (the rule replayed from the files: rooms read, share of the words, kinds seen, coverage, unseen kinds estimated, the open round, the markers, the next room); `report --stage B1` (`out/stopping-B1.md`); `decide --stage B1 finish|stop --why "..."` (the PI's decision after the report).

The rule, as the PI set it on 29 September 2026: material is counted in words, in units of the average room. No estimate is made before 50 average rooms, and 25 rooms, are read. No round is longer than 25 average rooms. If 60% of the words are read before marker 3, B1 reports and pauses (the check-in), and the PI decides to continue, finish or stop. While a new kind has come in the last 10 average rooms, and the last 10 rooms, reading goes on. After 10 without one, a round begins: the estimate (Chao et al. 2014, incidence data) predicts how far the next new kind is, and the round reads that far, never more than has been read. A new kind inside a round, or inside the draw, resets everything. At B1 a kind is a third-order theme as met: `mem.py mint` and `place` append it to `out/kinds-B1.jsonl` with the room being read, which says when a kind is new, and the room whose theme was placed, where the estimates count it (Chao's incidence assumption; J, 29 September 2026), a logged merge or split is a new kind, and the file is never rewritten, so a later regrouping leaves the rule's past as it was read. Three empty rounds are marker 1, where the literature would stop; three more are marker 2; then a draw of rooms taken at random from those unread, as many words as the three rounds between the markers, whose reading is marker 3. The report states what the draw rules out (Callaghan and Müller-Hansen 2020). The stage then pauses and the PI decides. The rule is B1's alone: A1 reads every room and counts no kinds (J, 29 September 2026).

## Who writes it, and when

Shipped in the analyst's `tools/`. The analyst runs `status` at will, and `report` at B1's marker 3; `mem.py next --stage B1` follows the rule, and `mem.py mint` and `mem.py idea` stamp words read with it. The seed is the sha256 of the store's `rooms.jsonl`, frozen in `out/seed.txt` at B1's first draw, so no one chooses the order. Stage A1 declares its own order and counts no kinds (J, 29 September 2026).

## Why it exists

An earlier run stopped after 127 rooms with its curves still climbing, and the tier it froze collapsed; runs of "nothing new in N" miss badly (Callaghan and Müller-Hansen: 39% of runs after 50 in a row). The rule stops only by an estimate, goes past where the literature would stop, and ends with a random draw that states what could have been missed.

## Where

[tools/saturation.py](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/tools/saturation.py). The research behind it: `aggregator/handler/memory/research/stopping-rules-2026-09-29.md`.

Checked against: tools/saturation.py, stages/STAGE-A1-reading-room-notes.md, stages/STAGE-B1-coding-third-order-scheme.md.
