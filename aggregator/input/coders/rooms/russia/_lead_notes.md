# Lead notes

## Batch 01 collect

- Reviewed all 12 appended timeline lines and all 5 appended lexicon lines. No lines were struck: the timeline lines are dated edit/moderator facts with item ids, and the lexicon lines contain only terms and first-use item ids.
- Carry forward the edited r/place coordination sequence and repeated moderator-operated NP-link notices. Reply adjacency and “followed by” wording will be treated only as observed sequence unless the passages themselves establish a relation.
- Final `notes.md` must state that no batch-01 facts lines were struck and why.

## Batch 02 collect

- Reviewed the one appended timeline line and two appended lexicon lines. No lines were struck: the timeline line reports the edited post's announcement without treating Bagration44 as a verified moderator; the lexicon lines are unglossed terms with their item id.
- Collector warned that batch 02 rewrote rather than appended `timeline.md`; inspection confirmed the lead copy retained all seeded and batch-01 lines and added the batch-02 line.
- Carry forward the move directing r/place posts to r/russiaclan, while distinguishing the participant's claim to speak for moderators from a verified moderator mark. Preserve the inherited and unresolved episode edges for the cross-slice account.
- Final `notes.md` must state the batch-02 facts review and the rewrite warning.

## Batch 03 collect

- Reviewed all three appended timeline lines and both appended lexicon lines. No lines were struck: the timeline lines are dated moderator-operated NP-notice facts with item ids; the lexicon lines preserve participant wording and first-use item ids. The metro-attack timeline entry is retained only as a moderation fact, not as r/place practice.
- Carry forward the two late flag-building calls after the redirection as sequence only. The slice explicitly does not support a causal relation to that redirection. The ending edge is closed; r/russiaclan activity is outside the supplied evidence.
- Final `notes.md` must state the batch-03 review, the no-strike decision and reasons, and the coder's generic-close warning.
- Instruction conflict at checkpoint: the scheduler asked for this review to be written into `notes.md` now, while the controlling contract says `case.md` and `notes.md` are written once at the end. Per the initial direction to resolve conflicts in favour of the contract, `notes.md` was not started; this text is preserved for its final write.
- Stop after collection and facts review. Do not consolidate, pool, theme, or begin steps 4 and 5 until the scheduler continues the run.

## Consolidation, first close, forest and audit

- Scheduler resumed the checkpoint. Consolidated all three batches: 109 codes, 266 thread dispositions and 26 pointers.
- Called the first lead `emit.close()` before themes, then built the forest from `package/codes.jsonl`.
- `tools/audit_fleet.py` passed: 109/109 live code offsets, 26/26 pointer offsets, 22/22 exclusion quotes, 34 coded threads represented, and all 266 slice threads disposed once.
- Beginning step 4 incrementally in slice order, reading each portion of `package/codes_by_thread.md` beside its slice case.

## Step 4 grouping and counter-reading test

- Incremental consolidation opened themes from slice 01, extended recurring practices in slice 02, opened two practices first found in slice 02, and assigned both slice-03 codes to the existing flag-recruitment theme. Thirteen themes cover every live code exactly once; one is deliberately a single-code theme.
- Provisional case reading before search: r/russia participants improvised flag work through recruiting, tactical help, territorial disputes, allies and repeated redirection after losses; they openly described small numbers and zero coordination, while a post speaking for moderators moved event talk to r/russiaclan and late flag calls still appeared in r/russia.
- Consequential competing account: participants achieved effective, stable teamwork rather than improvised work marked by small numbers and losses, and the move to r/russiaclan successfully contained later coordination. If the provisional reading is wrong, the supplied record should contain repeated claims of coordinated plans, completed or securely held flags, and visible participant uptake that contradicts the claim of isolated late calls after redirection.

## Completion check

- Final integrity at verdict close: 111 live codes, all under exactly one of 13 nonempty themes; 266/266 threads disposed; every coded thread has a live code; literal branch-B gate line present in `notes.md`.
- Preflight passed C1, C3, C4, C6, C7, C8, C9, C11 and C12. C5 alone reported eleven missing exclusions.
- The eleven C5 threads have 0–8 in-window items according to `openings.md`, so none reaches the contract's ten-in-window citation trigger. Exact title citations for all eleven were resolved as one batch; the first attempted `emit.thread` repair was refused because the disposition already exists and the record is append-only. No repair event was written. This appears to be a preflight defect using total-thread size rather than in-window size; it cannot be made to pass without changing the checker or bypassing append-only recording.
