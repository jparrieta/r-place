## The sensitivity of the form lines to the rule's thresholds

Written at D6a-09 on J's ruling 1b (27 October, 09:27 Berlin) by `_analysis/d6a09_sensitivity.py`, which re-runs the rule of D6a-01 on the same facts files. The rule names a cell changed where an op is held by at least the floor (the larger of 5 and a share of the form's defining rooms) at the ratio threshold or more times the 558 defining rooms' share. Run at the rule's own thresholds (ratio 1.2, floor 10 per cent), the script gives back all 396 written relations. The table counts the changed cells at each setting, all forms first, then by form.

| ratio threshold | changed cells, floor 10 per cent | changed cells, floor 15 per cent |
|---|---|---|
| 1.0 | 99 (A 19, B 12, C 15, D 22, E 16, F 15) | 67 (A 11, B 8, C 9, D 16, E 10, F 13) |
| 1.1 | 82 (A 14, B 7, C 12, D 20, E 14, F 15) | 53 (A 8, B 4, C 6, D 14, E 8, F 13) |
| 1.2 (the rule) | 72 (A 11, B 7, C 10, D 17, E 13, F 14) | 45 (A 5, B 4, C 5, D 12, E 7, F 12) |
| 1.3 | 57 (A 6, B 7, C 6, D 15, E 11, F 12) | 36 (A 3, B 4, C 2, D 11, E 6, F 10) |
| 1.4 | 42 (A 4, B 4, C 3, D 9, E 10, F 12) | 29 (A 2, B 2, C 1, D 8, E 6, F 10) |
| 1.5 | 27 (A 1, B 3, C 2, D 6, E 6, F 9) | 20 (A 0, B 2, C 1, D 6, E 4, F 7) |

Raising either threshold only removes cells: at every setting stricter than the rule, each cell still changed keeps its written relation. Lowering the ratio adds cells the rule leaves untouched (27 more at 1.0 with the 10 per cent floor).

**The cells kept at the stricter rule.** J's ruling names two marks. A changed cell is marked "robust" if it keeps its written relation at ratio 1.5 and floor 15 per cent, and "marginal" otherwise. Of the 72 changed cells, 20 are kept and 52 are marginal. Each cell's mark, holders, ratio and relation at the stricter settings are in `form-cells-sensitivity-D6.tsv`.

- **A, Border terms and the announced plan:** 0 of 11 kept.
- **B, Behind the thread: chat, scripts, raids:** 2 of 7 kept: P14 (specifies), P23 (specifies).
- **C, The design reopened:** 1 of 10 kept: P02 (specifies).
- **D, Keeping, with help or carrying on:** 6 of 17 kept: P01 (specifies), P14 (restricts), P05 (specifies), P20 (specifies), P13 (specifies), A09 (restricts).
- **E, The sub's play, run as work:** 4 of 13 kept: A01 (restricts), K01 (specifies), A07 (restricts), A15 (restricts).
- **F, Moving for the spot:** 7 of 14 kept: P01 (specifies), P03 (specifies), P04 (specifies), A06 (restricts), P19 (restricts), A04 (restricts), A07 (restricts).

Most single cells do not survive the stricter rule, though D, E and F keep their central changes: D its keeping and carrying on (P05, P13), E the play run as work (K01), F building again after a move and border talk before keeping (P03, A04). B keeps its scripts and its chat (P14, P23), and C keeps the design (P02). A keeps none of its changes at ratio 1.5 and floor 15 per cent, and 1 of 11 at ratio 1.5 with the 10 per cent floor, so A's telling (terms, plans and their reach) rests on cells that do not survive a stricter rule. A cell marked marginal is a lean of the form at the rule's thresholds, not a finding that survives a change of rule.
