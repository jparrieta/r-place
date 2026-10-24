# Notes, stage D4

## D4a-01: the statistic, the sensitivity check, the first pass (one element), and the held proposals

Leg D4a-01, 24 October 2026 (UTC). The tree itself, its rules and its accounting are in `tree-D4.md`; the branches are in `branches.jsonl`, `forms/` and `crosslinks.jsonl`. This file records what was done and why. J stops the run after this leg (QD4-001), so this pass is the last one the run makes.

### J's message after the D3c interview, and what was done with each part

1. **D3 stays frozen at 46384686, with no further re-check.** Done. No labeler or reader was used.
2. **The amendments to P05 and A11.** They were made as recorded amendments under rule 11 (move 198 on P05, move 199 on A11; history lines 173 to 180), each marked not re-checked with the frozen version beside it. F-024 and F-017 were re-examined in the same act. P05 took the bound, not the widened revision. The reason: the bound keeps the words the 705 rooms were re-checked against and narrows where they hold, while the widened revision adds a route and a holder that no room was served and no re-check can test. A11 was withdrawn: it never beat its null; template first (98 rooms) is nearly as common as the transition (111) of the 228 rooms with both ends; the failure clause stands alone in 117 rooms (talk only 31, layout only 86); and 261 accepted restrict lines say that a template does not settle the design for good.
3. **Mark each amendment as not re-checked, beside the frozen version.** Done in the records. Since the revert, they appear as held proposals in `tree-D4.md`, here and in the head.
4. **If the close-check refuses the amendments, ask.** It did ('model/ and its tiers moved after D3 froze them'; `_analysis/d4a01_validate_D4_01.txt`). I asked (QD4-001) and did not work around it. **J chose option (b)** (24 October, 15:05 Berlin). Move 203 reverted both amendments: P05 and A11 are restored byte for byte from the snap of move 197 (`_analysis/d4_revert.py`, history lines 181 and 182). The model hash is 46384686 again. Both amendments are held proposals, stated in full with their rooms, lines and moves in `tree-D4.md` ("The held proposals"). F-024's and F-017's D4a-01 lines stay as written. Each finding has one later line that restores its earlier statement and records the held proposal (findings, now 42 lines).
5. **Do not rely on the kind of add-condition, add-step and restrict lines; run the distance once with kind collapsed for them.** Done (`_analysis/d4a01_kind_collapsed.py`). The combined distance hardly moves: Pearson 0.9965, mean absolute difference 0.0024, delta 0.4223 against 0.4227. The average-linkage trees agree with ARI 1.00 at 2 and 3 clusters, 0.886 at 5, 0.922 at 8 and 0.779 at 12. No branch takes its members from a per-kind view for those ops, and each branch's kind field is reported, not relied on. **Local validation is reported as not established:** prior.md section 3's measure was not computed.

### Section 1, read before any cut

The delta score is 0.4227 (Monte Carlo SE 0.0020). The average-linkage dendrogram is a chain with no partition: at 12 clusters one group holds 663 rooms. Every room holds a key, and none returned `none`. Shared corrections reach 5 rooms only at the bare target. The detail is in `tree-D4.md`.

### The pass

- **Candidates** (`_analysis/d4a01_candidates.py`, `.txt`). 274 change keys at level 3 are held by 5 rooms or more. The largest are restrict lines on arrows, which cannot key a branch. Keys that co-occur beyond chance mostly share one third-order node.
- **The cut rules** were logged and written into `tree-D4.md` before the first cut. The minimum group size is 5.
- **Cut 1, F01** (move 200, merging): the play administered, at the fourth order, key `add-step:K01:T4-001`, 103 rooms. Its 164 lines were read whole (`_analysis/d4a01_lines_K01_addstep.txt`).
- **Cuts 2 to 6, F01's subforms** (moves 201, 202, 204, 205 and 206, splitting), at the third order: F02, the takeover run as a temporary regime (33 rooms); F03, the joke tested (18); F04, the licence policed (13); F05, the styling ended (12); F06, the joke kept (8). Two level-3 groups were set aside, since their lines state several different steps.
- **Cross-links** (move 207, relating): 18 lines over 6 pairs of subforms.
- **The accounting.** 103 rooms in a branch, 0 unadapted, 602 adapted but in no branch, 0 unreturned: 705, the analysed set. `tree-D4.md` names each of the 602 rooms, with the number of shared change keys a later pass would read.

### What this pass shows, and what it does not

- The ledger's form signals are weak. The D3 revisions absorbed the shared corrections, and the dendrogram shows no partition. The groups that remain are elaborations of single elements.
- The one element cut, K01, gives a branch about the sub's own April Fools play, not about canvas work. It says that members organized the play itself: they tested it, policed it, ended it and kept parts of it.
- The pass reached one element. 31 element change keys at level 4, held by 20 rooms or more, were not read (`tree-D4.md`, "Where the pass stopped"). So the tree is a first pass, not a taxonomy of the rooms' forms.
- **Not built.** The comparison (section 5) and the projections (section 6). They come after the final branch cut, and this is not the final cut of the stage's design. The close-check warns about them at a leg that made a cut. No verdict, canvas field or branch entered any computation of this leg.

### For the operator

- `validate.py --open D4` reads the startup packet's pattern name `rooms-x-adaptations.<level>.<kind>.tsv` literally and reports it missing; the sixteen matrices are present.
- `stage_D4.py` resolves a branch key's target against the elements only, so no branch can be keyed on an arrow, though the largest change keys in this ledger are on arrows.
- `stage_D4.py` refuses any model move after the D3 freeze, while J's instruction asked for amendments at D4. The two did not meet, and QD4-001 settled it for this run.

### Slips

- **A tool interruption.** The session ended during the command that logged and snapped move 202 and dry-ran F04. The log line and the snap were written. F04's dry-run file was empty, so the dry run was repeated before F04 was written.
- **The forms' list of unchanged elements counts arrows.** `d4_cut.py` reads instantiate keys at the bare target, and those include arrows, so F06's list names A12 among "elements". The forms are written once and are not regenerated. Read that line as elements and arrows.
- **The amendments were made, then reverted.** The two model moves of this leg (198, 199) were undone by move 203 at J's ruling. Each stays on record.

### Close-check, D4a-01

`validate.py D4` reports 0 errors and 1 warning (`_analysis/d4a01_validate_D4_03.txt`). The warning: the comparison and the projections are not built; at a leg that made a cut they are built after the last cut. Section 4: 103 in a branch, 0 unadapted, 602 adapted in no branch, 0 unreturned; 705, the analysed set. The first run (`d4a01_validate_D4_01.txt`) gave the model:moved error, now gone with the revert. The second (`d4a01_validate_D4_02.txt`) gave the missing notes and the unnamed rooms, now written.
- **Written at D4a-01:** `branches.jsonl` (6 branches), `forms/` (6 files), `crosslinks.jsonl` (18 lines), `tier_history.jsonl` (now 573 lines; 12 stage-D4 lines: 6 cuts and 6 cross-linked pairs), `tree-D4.md`, this file; model history (now 182 lines: 8 amendment lines and 2 revert lines); findings (now 42 lines: 2 re-examination lines and 2 lines after the revert); the moves 198 to 207, each logged and snapped; QD4-001. Helpers in `_analysis/`: `d4a01_key_freq.py`, `d4a01_kind_collapsed.py`, `d4a01_candidates.py`, `d4_key_lines.py`, `d4a01_a11_classes.py` and `d4a01_amend_specs.py` (read or write their own outputs only); `d4_amend.py`, `d4_revert.py`, `d4a01_findings.py`, `d4a01_findings_revert.py`, `d4_cut.py`, `d4a01_specs_K01.py`, `d4_crosslinks.py` and `d4a01_tree_append.py` (write the files named in their docstrings).
- **Unchanged:** the model, at 46384686… (elements 45, arrows 21, the tiers), the ledgers and their rulings, the verdicts and every view.
- **Questions.** QD4-001 is answered. None is open.
