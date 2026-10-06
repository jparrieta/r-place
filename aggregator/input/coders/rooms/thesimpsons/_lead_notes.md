# Case-lead running notes

## After collecting batch 01

- Reviewed `out/timeline.md` and `out/lexicon.md`; struck no lines. The three lexicon additions are factual participant terms tied to item ids and have no gloss. Preserve this review for `notes.md`.
- Carry forward the unresolved Flying Hellfish proposal and Homer-defense call against “THE VOID”; later evidence must establish any outcome.

## Batch 02 collect review

- Struck no appended facts. Timeline additions are edit-marker facts with instrument times and ids; lexicon additions are unglossed participant terms with first-use ids. State this in final notes.md.
- Carry to step 5: test later evidence for the claimed settlement with Smash participants versus renewed conflict. Keep Reddit-visible answers separate from unseen Discord negotiation, and treat unsupported order as sequence only.

## Batch 03 collect review

- Struck no appended facts. Both timeline additions are edit-marker facts with instrument times and ids; all four lexicon additions are unglossed terms with first-use ids.
- Carry to step 5: no assigned thread in the final slice showed r/place practice or continued the inherited Homer-damage opening. This is a scoped later absence, not evidence of a community-wide change of mind. `63f358` names a general Simpsons Discord without linking it to r/place.
- Scheduler checkpoint: all three slices are collected. Do not consolidate, pool, theme, or begin steps 4–5 until instructed.

## Step 4 grouping review

- Consolidated 73 codes incrementally in slice order into eleven themes. Later slice 02 codes extended `calling for keeping Homer alive`; distinct themes were opened for proposing other pictures, negotiating the mile-long-nose collision with Smash, and asking allies to fight red. Slice 03 added no codes or themes.
- The broad provisional grouping “defending Homer” was split because repair work, negotiating borders/blame, and reciprocal defense against red are different practices. Single-code themes were retained for selling a patch and cheering THE VOID.

## Step 5 counter-reading set before search

- Main reading to test: after using familiar show material for the room's own April Fools joke, r/thesimpsons moved from scattered picture proposals into repeated Homer repair calls, border negotiation with Smash participants, and a claimed joint defense; the final slice shows ordinary fan talk rather than a documented post-event settlement.
- Competing account: the canvas conduct remained scattered picture-posting, and the apparent Homer coalition was only a brief settlement inside one comment thread.
- If the main reading is wrong, the corpus should contain explicit refusals to defend Homer, renewed attacks on Smash after the claimed agreement, or later statements that the repair effort was abandoned or failed.

## Final preflight

- Repaired orphan `c0029` by appending it to `t01` and reran the final close; C4 then passed.
- C5 remains failed on 21 false positives. Openings counts verify every named thread has fewer than ten in-window items, while the preflight appears to trigger on whole-thread items in `_read_index.json`. Duplicate `emit.thread` calls are refused by the documented append-only API. Recorded the full list and conflict in `notes.md`; no coder directory or generated JSON was altered.
