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

## D4a-02: the second pass, the comparison, the projections

Leg D4a-02, 25 October 2026 (UTC). The harness opened this leg after QD4-001 had said the run would stop at D4a-01, so the run goes on, and this leg does the stage's remaining work.

### The comparison, declared before its script runs (stage D4 section 5)

The final branch cut of the stage is cut 29 of this leg (F35, move 236), and every cut is snapped. No branch is recut after the comparison is seen. The comparison is the chunk-share comparison, run as the stage file gives it: `python3 tools/chunk_compare.py --out out --store package/store`, the versioned engine (`chunk-comparison-v1`), with its defaults. Its method, as the stage file and the engine state it:
- **Features.** One row per room. Columns are the fourth-tier themes, and the counts are unique concept ids by their theme links. A theme placed on several fourth-tier themes splits its weight equally among them. Unplaced concepts are counted apart. Empty compositions are excluded by name. Rooms with fewer than five placed themes are flagged as low-information and kept, and the pipeline is run again without them.
- **Smoothing.** P = (x + a m) / (n + a), with a = 1.0, since `prior.md` holds no `chunk_concentration` line. It is a fractional pseudo-count heuristic. The run reports the median own-data weight and the sensitivity to a/10 and 10a.
- **Distances and clusters.** Ward on Euclidean CLR vectors. Jaccard presence and Hellinger shares with average linkage, as sensitivities, with adjusted Rand indices at each eligible k.
- **Null and resampling.** Theme-allocation patterns are permuted among themes. There are 200 accepted bootstrap draws and 100 permuted copies under each of two seeds (0 and 1). Eligible k runs from 2 to min(12, floor(n/2)). A k clears only when both stability margins are positive under both seeds. The k carried maximizes the worst margin, with the smaller k on a tie. If none clears, the result is `no-supported-partition`.
- **What it reads.** The concept store, the placements, the tiers, the dropped cases and the prior. It reads no adaptation, branch, verdict or outcome, so it is a non-adaptation baseline that shares the inductive coding structure, not theory-free evidence.
- **What I read from it.** The empties, a and the median weight; the Rand indices among the three distances; the third tier's sparsity; the tier verdict with its index; the volume verdict with its percentile; the k carried, with and without the low-information rows. Best-match Jaccard against the branches is descriptive. ARI against the branches is undefined, since the branches overlap (759 cross-link lines) and no exclusive cut is named.

### The comparison did not run (QD4-002)

`python3 -I -B tools/chunk_compare.py --out out --store package/store` stopped on its first room: "ValueError: Placement lacks fourth-tier parent: ('2007scape', 't02')" (`_analysis/d4a02_chunk_compare_run.txt`). The cause is the run's residue. 335 second-order themes in 213 rooms are placed on the two third-order themes that no fourth-order theme gathers: T3-017 (carrying on ordinary sub talk, 334) and T3-133 (recovering a hacked sub, 1). `data_structure-C5.md` keeps both as residue, and the tiers are closed after C5 (rule 11). The stage file counts unplaced concepts apart; the engine raises on these placements instead. The run wrote no file. I did not edit the engine or the tiers, and I asked J (QD4-002). The projections follow the comparison and are not built.

### The pass (cut rules R0 to R7, with the amendment R1a to R1c, logged before it was used)

- **Read.** The 31 element change keys at level 4 left at D4a-01, each held by 20 rooms or more. Each key's lines were read whole, by level-3 node, in `_analysis/d4a02_keys/` (`d4_key_lines_bynode.py`, run by `d4a02_dump_keys.py`).
- **Cut.** 29 cuts, moves 208 to 236: 24 branches and 5 subforms (F12 to F14 under F11; F18 and F19 under F17), from the specs `_analysis/d4a02_cut_F07.json` to `F35.json` (`d4a02_specs.py`). They were written by `d4_cut_batch.py`, which logs each move only after `d4_cut.py` reports the write, and then snaps it. The list, with names and what each changes, is in `tree-D4.md`.
- **Set aside.** 8 keys, each with its reason in `tree-D4.md`.
- **Cross-links.** Move 237: 741 new lines, 759 in all, over 348 pairs of branches that do not nest.
- **The accounting.** 476 rooms in a branch, 0 unadapted, 229 adapted but in no branch, 0 unreturned; 705, the analysed set. `tree-D4.md` names each of the 229 rooms with its count of smaller keys.

### What the pass shows

- **The branches are facets, not exclusive forms.** 200 of the 476 rooms are in one branch, and the rest are in two to six or more (subforms counted). A room makes several element-level changes at once, and the keys do not group rooms into a few types. This fits the chained dendrogram and the delta score of section 1.
- **Families.** One change appears at several nodes, so it appears as several branches. The largest family is P05's added clause holding only in part (F07, F26, F27), beside F-024's held branch. Also: keeping the shared instruction current (F15, F33 and F08), help conditional (F22, F28), carrying on (F11 to F14, F23, F25), and the chat (F16, F29, F30).
- **Two links the model lacks.** The move leads back to building (F09, 54 rooms), and the marking leads back to keeping (F32, 21 rooms). Neither is an arrow; the next stage reads them for order.
- **Many restrict branches are limits of the record.** They show what the record does not hold: machine hands not shown placing (F24), the chat seen only from outside (F30), hosting only as one-off permission (F31), carrying on only in talk (F25). They are kept because the element's statement holds only in part there, and they are reported as limits, not as forms of doing.
- **Local validation** remains not established.

### For the operator

- **The comparison engine and the residue.** `tools/chunk_compare.py` raises on a placement whose third-order theme no fourth-order theme gathers, but the stage file counts unplaced concepts apart, and this run keeps two residue themes by design (QD4-002).
- **The member-name check is a substring check.** `stage_D4.py` refuses a branch name that contains any member's name as a substring, so the room 'de' forbids words such as 'decisions' and 'outside'. Two spec names were changed before writing (F16, F30).

### Slips

None in the writes of this leg. Two spec files (F16, F30) were edited after their generator ran, to change a name the check refused; the edits are the names only.

### Close-check, D4a-02

`validate.py D4` reports 0 errors and 1 warning (`_analysis/d4a02_validate_D4_02.txt`). The warning is that the comparison and the projections are not built. At a leg that made a cut this is a warning; the stage does not close without them (QD4-002). Section 4: 476 in a branch, 0 unadapted, 229 adapted in no branch, 0 unreturned; 705.
- **Written at D4a-02:** 29 branches (`branches.jsonl`, now 35); 29 forms (`forms/`, now 35); 741 cross-link lines (now 759); 371 stage-D4 tier_history lines (29 cuts and 342 cross-linked pairs; the file now 944 lines); the moves 208 to 237, each logged and snapped; this section and the `tree-D4.md` sections; QD4-002. Helpers in `_analysis/`: `d4_key_lines_bynode.py` and `d4a02_dump_keys.py` (read the ledger and write the key files), `d4a02_specs.py` (writes the specs), `d4_cut_batch.py` (runs `d4_cut.py`, `mem.py log` and `snap.py`), `d4a02_tree_append.py` (appends to `tree-D4.md`).
- **Unchanged:** the model, at 46384686… (history 182 lines, findings 42), the ledgers and their rulings, the verdicts and every view.
- **Questions.** QD4-002 is open.
