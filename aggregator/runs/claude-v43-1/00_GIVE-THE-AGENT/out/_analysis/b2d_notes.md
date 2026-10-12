
## Leg B2d, the gold round and the stability check scored, 2026-10-12

### The dispatches

J ran the three dispatches on the frozen scheme. `fleet.py`'s counts come from each round's DONE record. The next table lists them.

| round | packets | readers | valid returns | exhausted | cost (USD) | input tokens | output tokens |
|---|---|---|---|---|---|---|---|
| gold | 3 | 3 a packet | 9 | 0 | 0.231 | 288,978 | 225,436 |
| stab-1 | 3 | 3 a packet | 9 | 0 | 0.178 | 46,041 | 211,978 |
| stab-2 | 3 | 3 a packet | 9 | 0 | 0.220 | 132,118 | 276,244 |

`validate.py B2` checked the 360 return lines with no error. `out/_analysis/b2_translate_fleet.py` translated each round to room ids, 120 lines a round with 0 id problems (copies in `out/_analysis/b2_r<round>_returns/`).

### The scores

`out/_analysis/b2_score_final.py` scored the three rounds. Its outputs are `b2_final_score.json` and the per-item table `b2_gold_items.tsv`. The rounds' lines are lines 4 to 6 of `pilot_rounds.jsonl`, and the gold line is flagged gold (`b2_round_lines_final.py`). Gold items are not exported to `exemplar_candidates.jsonl`, because B3 seeds the gold set unannounced. The next table lists the figures.

| round | fidelity | against rechecked | primary | pairwise | alpha | items differing |
|---|---|---|---|---|---|---|
| gold | 0.624 | 0.661 | 0.800 | 0.818 | 0.809 | 14 of 40 |
| stab-1 | 0.636 | 0.674 | 0.800 | 0.800 | 0.789 | 14 of 40 |
| stab-2 | 0.631 | 0.669 | 0.800 | 0.756 | 0.743 | 18 of 40 |

**Stability: 0.807.** This is the mean Jaccard of stab-1 readers against stab-2 readers, nine pairs per item. Primary placements matched in 0.853 of those pairs. Alpha over the six stability readers is 0.784. The figure sits level with the pairwise agreement inside each stability round, so the rewording of the brief adds no disagreement (`stability-B2.md`).

**The gold gap.** Gold fidelity (0.624) is lower than round 3's (0.682), while gold pairwise (0.818) is higher. On ten gold items the readers keep only my primary of two placements. The gold set was placed at B2a-r1, before round 1 showed this author-error. Primary match is 0.800, as at round 3.

### The blind re-placement

The ten hard items were drawn by seed b2d:blind: guatemala t02, harrypotter t08, ice_poseidon t16, ainbowroad t04, parabola t02, ainbowroad t03, megaman t11, anarcho_capitalism t12, dota2 t05 and theblackvoid t09.
- **The window.** I read each item whole through `mem.py codes` inside a blind window (14:01:06 to 14:02:36 in the read log). I placed them in `out/_analysis/b2_blind_replace.jsonl` before closing the window.
- **Self-agreement** (`b2_blind_score.py`): against `author_items.jsonl` 0.883, against the rechecked placements 0.900, primary 0.90. On the same ten items, the round-3 readers' fidelity was 0.806.
- **Caveat.** Earlier legs showed me several of these placements in round tables, so 0.883 is an upper bound.

### The predicted confusions

Of the nineteen pairs in `confusions.md`, four split readers in any round and three more than once:
- T3-004/T3-070: 6 splits in 55 reader pairs;
- T3-009/T3-073: 5 in 65;
- T3-001/T3-023: 3 in 58.

The hardest pair, T3-005/T3-021, never split. I had estimated 15 to 20%, and the observed rate is 0 in 64 reader pairs.

### The reports

- **`pilot_report.md`** covers the rounds, the gold number and its gap, stability, my consistency, every edit by theme (a generated table), the author-error verdicts, the themes that did not stabilise, the scorecard, the cost and the least-sure sentence.
- **Author-error verdicts:** 32 items (21 hard, 11 gold).
- **Wording defects carried to C1:** four gold items where readers missed what I placed (uofmn t01, cuboulder t04, mariokart t04, ireland t12).
- **`stability-B2.md`** and **`handback-B2.md`** are written.

### The close-check, B2d

`validate.py B2` reported:

```
stage B2:
  leg: check (6 dispatch folders with DONE)
  _fleet_raw/B2/round-1: 3 readers, 120 return lines
  _fleet_raw/B2/round-2: 15 readers, 150 return lines, 16 waived by J (return_waivers.jsonl)
  _fleet_raw/B2/round-3: 15 readers, 150 return lines, 4 waived by J (return_waivers.jsonl)
  _fleet_raw/B2/round-gold: 9 readers, 120 return lines
  _fleet_raw/B2/round-stab-1: 9 readers, 120 return lines
  _fleet_raw/B2/round-stab-2: 9 readers, 120 return lines
  author items 50, gold items 40, rounds scored 6, edits 306 (author-error 4), scheme ids 197 (scheme_final.jsonl), frozen


0 errors (0 distinct shapes), 0 warnings
```

The leg closes with `done.sh B2`.
