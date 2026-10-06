# Lead notes — r/bulgaria

branch B; threshold 500; items_in_window 543; chars_by_people 75425

## What was hard

The difficult judgment was separating a sequence from a relation. Expansion advocacy, diplomacy, repair, and renewed expansion occur close together, but only passages that name a problem and answer it support a relation. The account therefore treats the room as containing contrasting speakers rather than claiming it collectively changed its mind.

The second difficulty was keeping the subreddit’s own First of April joke separate from r/place. Codes `c0002` and `c0010` remain in a concrete theme about the room’s joke, with notes that they are not canvas conduct.

The counter-reading exposed a real imbalance in the pooled codes: batch 01 coded one passage in each retained thread, leaving substantive expansion comments uncoded. I read all 34 returned items and added `c0094`–`c0097` for the strongest previously uncoded contrary passages.

## Data problems

Deleted and removed bodies hide diplomatic openings, script posts, the Lithuania request, and the attack alarm. The surviving titles and replies are used without reconstructing missing text. One batch-02 coordinate excerpt was malformed around whitespace and remained uncoded. Generic mentionhelper and sneakpeekbot output was treated as setting; AutoModerator’s NP-link enforcement remains a moderator-operated timeline fact.

Parts of coordination moved to Discord, a strawpoll, Google Drive, and pxls.space. The record shows invitations, returned plans, reported agreements, and coordinates, but not those venues’ internal decisions or whether the pxls.space restart lasted.

## Branch B limits

No reader held the whole week. One coder read each slice, so there is no agreement measure. The arbitrary boundary cuts through the late restraint-and-coat-of-arms episode. The forest makes sequence visible but does not repair divided reading. The one relation carried across batches 01 and 02 rests on the words in `dfrrl3h`, `dfry8sk`, and `dfrzb05`, not their adjacency.

Every time and interval in `case.md` was taken from `package/tree_index.json` through `_lead_times.py` or directly from a slice coder’s stated measurement. The case does not infer a causal link from reply structure alone.

## Facts-file review

No facts lines were struck. Batch 01 added five instrument-visible moderator/edit facts and seven unglossed terms with item ids. Batch 02 added four instrument-visible edit or moderator-post facts and four unglossed terms with item ids. The review and carry-forward decisions were recorded at collect time in `out/ledger.md` and `out/_lead_notes.md`.

## Grouping review

I grouped batch 01 first, then extended only four existing themes with batch-02 codes and opened four batch-02 themes for practices that were genuinely new. After the counter-reading I reviewed every grouping again. No pooled code was reassigned and no two themes were merged or split; the contrary late passages instead required the new step-5 theme “pushing the flag farther right and up.” The instrument records the original themes with `regrouped_from: null`, the incremental `theme_add` calls, and the new late theme.

The two themes that nearly merged were “making room and deals with neighboring pictures” and “stopping expansion and repairing relations with neighbors.” They stayed apart because the former negotiates coexistence before or alongside damage, while the latter answers expansion that participants say has already broken agreements or erased work.

## Code judgments

Hardest to defend: `c0058`, “blaming compatriot savages outside the subreddit for burying every start of the coat of arms.”

Thinnest kept: `c0015`, “raising the cube-and-flag relationship.”

## Anomalies and leads

The same flag is a shared object, a diplomatic boundary, and a source of what one coder called “mob mentality.” Participants repeatedly say that people outside the subreddit undo agreements; the corpus cannot identify those placers, so this remains participants’ explanation rather than an established cause.

The ending does not simply close conduct. Within the ending thread, contributors thank one another, criticize bots, and propose restarting RubikFlag elsewhere. That continuation is visible as a call and answer but unresolved as sustained work.

## How the reading held up

The lead did not work from memory of raw threads and did not reread a thread because it had been forgotten. Before consolidation, the lead read only the briefing, all openings, the facts files, and the ledger; raw corpus access remained closed. After grouping, selected items were read through the prescribed tools for the counter-reading and evidence checks.

Earlier material did not become indistinct relative to later material because the lead’s working memory was the ledger, slice cases, codes-by-thread file, forest, and `_lead_notes.md`, not an attempted whole-corpus recollection. The scheduler checkpoint interrupted the lead workflow after batch 02 collect, not a coder’s reading; on resumption I reread the ledger and lead notes, did not recollect, and continued with consolidation.

## Complaints

The scheduler-required checkpoint asked for an interim `notes.md`, which conflicts with the contract’s ordinary instruction to write it once at the end. I recorded that checkpoint as requested, then replaced the interim text with this complete final notes file; no append-only instrument record was edited.

The ledger’s copied episode lines are clipped mid-sentence in places. The complete slice cases were available and were read beside the pooled codes, so the clipping did not control the account. A shell heredoc was also rejected before the initial stage call ran; the stage was immediately recorded with a foreground one-line Python call and no corpus or journal mutation occurred in the rejected command.

## Completion review

All 86 threads were disposed by the two slices, all 54 coded threads had live codes at consolidation, and the forest audit passed with all 93 pooled codes on nodes. No read out-of-scope thread had ten or more in-window items requiring an exclusion citation; batch 02 explicitly reports that none of its exclusions reached ten, and the fleet preflights passed for both slices. After the final close, `python3 close_run.py . --role lead --preflight` passed all 10 checks.
