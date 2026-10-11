
## Corrections written at B2b-r1, 2026-10-11

- "107 episode lines whose kinds none of their rooms holds" is wrong. Counted against `scheme_current.jsonl`, there are 106 (line, kind) pairs where no room of the line holds the kind, over 81 lines of `episodes-B1.jsonl` (`out/_analysis/b2_episode_kinds.py`). The PI pointed this out.
- F-001's grain bound does not hold across rooms. A room's mean concepts per theme does not predict its single-kind share (Spearman −0.08 over 633 rooms). Within a room, larger themes carry more kinds (mean Spearman 0.28, positive in 482 of 619 rooms). The sentence that grain separates canucks from turkey is withdrawn. `findings.jsonl` carries the superseding F-001 line (status bounded).
- The T3-005 and T3-021 gates contradicted each other on repair during a raid. T3-005's must_not_show said "with no attacker in view", while its discriminator said "with or without". B2b-r1 corrected the must_not_show (`scheme_edits.jsonl`, the T3-005 must_not_show line).
