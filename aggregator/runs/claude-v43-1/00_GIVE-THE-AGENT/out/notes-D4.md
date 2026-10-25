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

## D4a-03: the comparison, the projections, the handback

Leg D4a-03, 25 October 2026 (UTC).

### A departure: the comparison engine is chunk-comparison-v1.1 (QD4-002), declared before it runs

J answered QD4-002 with option (a) (25 October, 19:48 and 19:54 Berlin). The harness owner patched `tools/chunk_compare.py` and its trusted copy identically to `chunk-comparison-v1.1` (sha256 c8d2eb8c7c309c02de9bb04e10efeaa91071ee2a469823f569a9ab64a42c059f). A second-order theme placed only on third-order residue that no fourth-order theme gathers (T3-017, T3-133) is now counted with the unplaced concepts and reported apart, in the fields `residue_themes` and `residue_concepts`. A theme also placed on a gathered node keeps that node. The stage file names `chunk-comparison-v1`, so this is a departure, declared in `departures.jsonl` (line 10) before the run. The method declared at D4a-02 stands otherwise: the stage file's command and defaults (a = 1.0; seeds 0 and 1; 200 bootstrap draws and 100 permuted copies per seed; k from 2 to 12). The cuts are final (F35, move 236), and no branch is recut after the comparison is seen. Beside the comparison I report each room's residue share, as J asked: the share of its placed and residue concepts that sit on residue.

### The comparison read (detail in `tree-D4.md`)

- **The two verdicts by number.** The tier verdict: at the carried k 4, dimension ARI 0.110 and third-tier ARI 0.170. The volume verdict: the cluster labels explain 0.255 of the variance in log concepts, at the 100th percentile of the permutation null (null maximum 0.026).
- **The k carried.** 4 over all 705 rooms (worst margin +0.052, silhouette 0.024). 2 over the 626 rooms without the 79 low-information rows (worst margin +0.099, silhouette 0.097). Every k from 3 to 12 clears over all rooms, but no silhouette exceeds 0.051. So the null is beaten while the clusters barely separate.
- **The sensitivities.** Against the Ward/CLR labels at k 4, the Jaccard and Hellinger partitions give ARI -0.007 and -0.008, and a/10 and 10a give 0.145 and 0.164. The partition does not survive a change of distance or of smoothing. The median own-data weight is 0.990, so the smoothing touches the profiles little.
- **The empties.** None. a = 1.0. The third tier is sparse: 13.52 nonzero of 195 columns per room.
- **The clusters.** VA 176, IT 292, TX 155, CH 82. They differ mostly by their Keying share (T4-001) and by size: IT holds 137 of the 176 rooms of the smallest quartile. Best-match Jaccard with a branch is 0.096 to 0.187. The coding-structure clusters and the adaptation branches do not match.
- **The residue.** 199 rooms hold residue concepts. The share per room has a median of 0, and 39 rooms are at 0.10 or more and 7 at 0.30 or more. In these rooms the composition leaves out the room's own ordinary business.

### The projections read

The single does-not-compose room (picturegame) lies in F21 and F25. The canvas percentiles follow room size: 11 of 35 branches have a median room size at or above the 95th percentile, and the large-room clusters have the large areas. No difference in what rooms kept on the canvas is read as independent of size. No cut rests on the projections; every cut was snapped before them.

### What D4 shows, for D5

- **The adaptation tree is a set of facets.** The 35 branches overlap (759 cross-links). The comparison's partition, built without the ledger, is weak, unstable across distances, and largely a size partition. Neither gives exclusive forms.
- **What the branches say.** Rooms add work the model does not state: the play administered (F01), deals carried out (F10), machine targets and plans kept current (F08, F15, F33), chats kept open (F16), help made conditional (F22, F28), and carrying on renewed elsewhere (F11). They limit P05's added clause where informed members reject a planned change (F07, F26, F27). And they show two links the model lacks (F09, F32).
- **Local validation** remains not established. prior.md section 3's measure was not computed.

### Slips

- Three Edits to the handback's script (`_analysis/d4a03_handback.py`) ran in one turn, and later three Edits to the head ran in one turn, against the rule. Each landed on a separate string.
- One figure in the handback's script was typed (102 rooms for F07, F26 and F27). It was replaced by the computed figure (108) before the handback was written.

### Close-check, D4a-03

`validate.py D4` reports 0 errors and 0 warnings (`_analysis/d4a03_validate_D4_01.txt`), including the trusted replay of the comparison engine. Section 4: 476 in a branch, 0 unadapted, 229 adapted in no branch, 0 unreturned; 705.
- **Written at D4a-03:** `departures.jsonl` line 10; `chunk-share-D4.result.json`, `.jsonl`, `.md` and `.py` (by the engine); `projections-D4.jsonl` (by `tools/projections.py`); the D4a-03 sections of `tree-D4.md` and of this file; `handback-D4.md`; `interview/D4a-03.md`; the head. Helpers in `_analysis/`: `d4a03_departure.py` (writes the departure), `d4a03_read_comparison.py` and `d4a03_volume.py` (read only), `d4a03_tree_append.py` (appends to `tree-D4.md`) and `d4a03_handback.py` (writes the handback).
- **Unchanged:** the branches (35), cross-links (759), tier history (944), the model at 46384686… (history 182, findings 42), the ledgers, the verdicts and every view.
- **Questions.** QD4-002 is answered. None is open. The stage closes at its interview cut.

## D4a-04: can the 25 top-level branches be joined into fewer parents?

Leg D4a-04, 25 October 2026 (UTC), an extra leg on J's instruction (25 October, 21:39 Berlin, through the handler). J finds 35 branches a lot and asked whether the 25 top-level branches can be joined into a smaller set of parents, on grounds the stage and the contract allow, decided from the record. If not, the reasons go here, nothing changes, and D5 runs one leg per branch. J will not be asked again.

### The test, written before any computation

A parent is a branch, so it must meet what the stage asks of a branch:
1. **Keys.** Every member holds every key of the parent at its level (section 2). Members' material can stand beside the keys as a declared ground, never alone.
2. **Nesting.** A subform nests by adding keys. `stage_D4.py` accepts a child only if each parent key has the same op and the same target as a child key, and the child's node lifts to the parent's node. So one parent can hold only branches of one element and one op.
3. **The level.** A group that meets only at the dimension or the bare target is a grouping, not a branch, since the aggregation does the work (section 2; cut rule R4).
4. **The source.** No list of rooms that belong together may come from anywhere but the ledger (section 2's Forbidden). Rooms that happen to share branches therefore ground no parent.
5. **The shared change.** A parent, like any branch, needs lines that state one shared change (cut rule R2). Rooms that the parent brings in, beyond its children, must have lines read for that change.

### What the record shows (`_analysis/d4a04_joins.py`, `d4a04_joins.txt`)

- **The handler's facts, checked.** 25 top-level branches on 14 elements: yes. By the elements' own dimension field they fall in six dimensions, D02 9, D07 5, D03 4, D04 4, D06 2 and D01 1, as the handler says. But the ladder joins a branch by the node its key lifts to, not by the element's field, and by that lift the count is D02 9, D04 6, D07 6, D06 2, D01 1 and D03 1. F07 lifts to D02, F26 to D04 and F32 to D07, although P05's own field is D03. The Jaccard distance between member sets has median 0.977 and minimum 0.870 (F10 and F26): yes. Average linkage first merges at 0.870 (F10 with F26), not above 0.89. At 0.95 it gives 13 groups, six of which join branches of different elements: yes.
- **Joins under rule 2, one element and one op.** Only three sets of top-level branches share both.
  - **P04 add-step (F15, F33).** Their nodes, T4-008 and T4-006, meet first at the dimension: `add-step:P04:D02`, 85 rooms, 20 of them in neither child.
  - **P16 add-condition (F22, F28).** T4-017 and T4-016 meet at the dimension: `add-condition:P16:D04`, 65 rooms, 13 in neither child.
  - **P05 restrict (F07, F26, F27).** T4-006, T4-016 and T4-013 lie in three dimensions, so they meet only at the bare target: `restrict:P05:*`, 214 rooms, 106 in none of them.
  Each parent would sit at the dimension or the bare target, a grouping under rule 3. Each would also take in rooms (20, 13 and 106) whose lines were never read for the shared change, so rule 5 fails too. Reading them would not cure rule 3.
- **Families across elements or ops.** These are the families named at D4a-02: P05's clause and the marking (F07, F26, F27, F32); the shared instruction kept current (F08, F15, F33); carrying on (F11, F23, F25); the chat (F16, F29, F30); machine hands (F08, F24); the frame (F01, F21); help (F22, F28). None has a key common to its branches, and the rooms in all of a family's branches number 0 to 5. No parent can be grounded on keys under rule 1, and the check refuses the nesting under rule 2. Co-membership alone cannot ground one under rule 4.
- **The membership distances.** These say the same thing from the other side: the branches hold almost disjoint sets of rooms, and the groups that average linkage forms at 0.95 join different elements with no shared change.

### Decision

**No join is defensible on grounds the stage and the contract allow. Nothing changes:** 35 branches, 25 top-level and 10 subforms, 759 cross-links. D5 runs as the stage says, one leg per branch. The subforms already nest inside their parents (F02 to F06 in F01, F12 to F14 in F11, F18 and F19 in F17), so a parent's leg can hold its subforms' accounts. The families named at D4a-02 are a reading aid for D5's accounts: they state one change across elements or nodes, and each D5 account can cite its family. They are not parents, since nothing in the ledger joins them.

**What would have made a join defensible.** Either a key held by every member of the branches to be joined, at the third or fourth order (none exists), or a stage rule that accepts parents at the dimension or the bare target (the stage forbids them). Neither holds, so 35 is the number the keys support.

### Close-check, D4a-04

`validate.py D4` reports 0 errors and 0 warnings (`_analysis/d4a04_validate_D4_01.txt`), including the trusted replay of the comparison engine. Section 4: 476 in a branch, 0 unadapted, 229 adapted in no branch, 0 unreturned; 705.
- **Written at D4a-04:** this section; the head; one read-only helper, `_analysis/d4a04_joins.py`, with its output.
- **Slip:** two Edits to the head ran in one turn, against the rule; each landed on a separate string.
- **Unchanged:** the branches (35), cross-links (759), tier history (944), forms, the comparison and the projections, the handback, the model at 46384686…, the ledgers and every view.
- **Questions.** None is open.
