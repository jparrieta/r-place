# Case-lead running notes

## Before gate

- Fresh run: `read state` reported cursor 0.
- Read `brief.md` and all of `openings.md` before the gate, as required.
- Orientation only: ordinary TWICE image, GIF, discussion, recurring member-thread, and subreddit April Fools material surrounds a smaller run of canvas-facing openings. Those openings include proposing a TWICE logo, reporting its appearance, coordination, a Denmark approach, completion claims, and a post-event PlaceTwo build. These are not evidence and will not be coded or cited by the lead during the fleet run.
- Briefing limitations retained: it describes a sampled prior week and explicitly leaves much of that source record unopened; unsupported or sample-bounded claims will remain orientation only.
- Operational difficulty: the shell attempted an external temporary file for a heredoc and was denied; no file was written outside the run directory. Subsequent Python calls use direct invocations.

## Gate and first dispatch

- Gate branch B: 1,006 in-window items against threshold 500; `chars_by_people` is retained in `out/_gate.json` as the second harness-computed count.
- Two slices: batch 01 has 77 threads and 492 items, from `62m2m4` through `62z0k8`; batch 02 has 75 threads and 514 items, from `62z41m` through `63fdci`.
- Dispatch batch 01 only with model `gpt-5.6-sol`; stop for the scheduler to run its coder.

## Batch 01 collect / before batch 02 dispatch

- Collected batch 01 after scheduler-reported PASS: 77 dispositions, 4 coded threads, 58 codes, and 3 pointers.
- Reviewed all appended facts: timeline had two substantive moderator-action lines plus its batch heading; lexicon had seven unglossed terms. No line was a reading, so none was struck. Preserve this no-strike decision for final `notes.md`.
- Carry forward the unresolved `62yvf2` coordination episode, r/TheBlueCorner offer `dfq4l34`, Discord pointer `dfql4jl`, and removed-post/comment-layer contrast. Do not infer causality from adjacency; check batch 02 for textual continuation and mark any supported boundary-crossing relation.

## Batch 02 collect / checkpoint before consolidation

- Collected the scheduler-reported passing final slice: 75 dispositions, 9 coded threads, 118 codes, and 8 pointers.
- Reviewed its additions in full: five substantive timeline lines plus the batch heading, and eight lexicon lines. None was a reading, so nothing was struck. The timeline additions state edits or moderator activity with item ids; the lexicon additions give terms and first-use ids without gloss.
- Preserve `Plageuis Project` exactly as the fact file records it; do not silently normalize participant wording.
- Carry forward: batch 02 marks its opening as inherited from the earlier logo planning and says the original r/place episode closes within this slice; PlaceTwo remains unresolved beyond the window. Later consolidation should test the cross-slice proposal-to-maintenance/redesign sequence, the “WE DID IT” versus unsettled-work layer contrast, Denmark accounts/negotiation/denials, Discord movement, and post-event PlaceTwo rebuilding.
- Stop here before consolidate, pooling, theming, or steps 4–5, per scheduler checkpoint instruction.

## Before consolidation

- Scheduler confirms batches 01 and 02 are collected and checkpointed. Do not collect either batch again.
- Next order: consolidate; first `emit.close()`; build forest from `package/codes.jsonl`; run audit gate; proceed only on PASS.

## Before step 4

- Consolidation pooled 176 codes, 152 dispositions, and 11 pointers from two batches. First close completed.
- Forest audit PASSED: all 176 live codes verified at offsets and on forest nodes; all pointers and exclusion quotes verified; all 152 threads disposed exactly once.
- Consolidate incrementally in slice order. For each theme, state the shared practice rather than grouping by vocabulary or reply adjacency; retain single-code themes where needed. Record founding batch and later extensions for saturation.

## Before step 5

- Step 4 produced 18 themes covering all 176 pooled codes exactly once. Batch 01 founded nine themes; batch 02 extended five of them and founded nine more.
- The five repeated practices are joining builds, looking for viable space, keeping work standing, deciding redesigns/extensions, and moving live talk to Discord. New batch-02 practices concern reading/explaining the canvas, celebrating completion, welcoming a new Once, calling for coordination, questioning permission, forming protection ties, arguing with Denmark, recounting the ending, and rebuilding on PlaceTwo.
- Theme grouping is based on common practice across passages, not shared nouns or adjacency. Revisit after the account and counter-reading; record whether any regrouping is warranted.
- Step 5 must distinguish descriptive contrast, participant explanations, and supported relations; use exact item ids and words, and use only tree-index measurements or figures quoted from slice cases for time/interval claims.

## Counter-reading stated before search

- Provisional reading: r/twice's canvas work was iterative; public “WE DID IT” moments reopened into redesign, Discord coordination, defense, negotiation, loss, and PlaceTwo rebuilding.
- Consequential competing account: completion was settled, while later coordination was confusion or unauthorized meddling rather than continuing group practice.
- If the provisional reading is wrong, the corpus should contain members explicitly abandoning further work, rejecting Discord-led changes as illegitimate, or treating the Denmark conflict as invented rather than as something requiring response.
- Search the case's own vocabulary for completion/abandonment, griefing or unauthorized change, and denials of attack. Read every returned item through `read item`; name the strongest contrary item and revise only what it actually unsettles.

## After counter-reading and account / before final close

- Three full-record searches were run and every returned item was opened through `read item`. Strongest contrary item: `dfrlez2`, the official-denial statement from a Danish speaker. It requires attack claims to remain attributed and contested; it does not overturn continuing defense and negotiation.
- The apparent abandonment hit `dfrlvy8` concerns Denmark abandoning a proposed color change; `dfrkjow` is unrelated weekly discussion; `dfss9uc` is an unrelated URL-fragment hit. No relevant hit rejects Discord coordination as illegitimate or shows r/twice abandoning defense. No late code was needed.
- Revisited all 18 themes against the completed account and counter-reading. No regrouping: every code remains under one shared practice. Closest boundary is location-changing (`t06`) versus maintaining an occupied work (`t07`); distinct actions and decisions keep them apart. Protection ties (`t15`) also remain distinct from arguing/negotiating with Denmark (`t16`).
- Case account completed with required headings, individually backticked ids, exact supporting words, and tree-index or coder-recorded time measurements.
- Final notes now complete; next action is final `emit.close(verdict="full")` only.
