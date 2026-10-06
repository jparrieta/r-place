branch B; threshold 500; items_in_window 3115; chars_by_people 476305

## What was hard

The hardest distinction was between practices that shared April Fools or r/place vocabulary but did different things. The helicopter refrain, lake-shark prank, Lucas Museum headline, mock “CHICAGO SUCKS” reversal, Weiner’s Circle translation, and Rainforest Cafe meetup remained separate themes or theme candidates because a common date and joking register did not make them one practice. The Rainforest Cafe outing was the subreddit’s own joke carried into an offline meetup, not canvas conduct.

The central flag thread was an edited post containing retrospective updates. Its update order is visible, but their individual posting times are not. I therefore did not assign clocks to internal updates. The flag episode’s externally measurable endpoints and reply intervals came from `package/tree_index.json` or figures in slice cases.

Cross-slice interpretation was also difficult. No reader held the whole week: one coder read each arbitrary slice, there is no agreement measure, and an exchange near a boundary could be divided across readers. The move from `dfqabhm` in batch 03 to `6307cp` in batch 04 was carried across the boundary because the earlier passage explicitly points to the “official proposal,” not because the items are adjacent. Other cross-slice continuities were stated as sequences unless participants named the same flag or thread.

Two tentative umbrella groupings were rejected. “Doing April Fools jokes” concealed different local practices. “Doing canvas work” concealed building the Chicago flag, negotiating help and space, rallying around sports designs, explaining Place, and arguing over whether Place belonged in r/chicago.

## Data problems

Deleted and removed bodies limit several important threads. `62xbmp` preserves a flag-call title but no plan; `634dqx` preserves the r/kanye request but not its body; `63822o` preserves the overrun warning but no coordinates or detail; and the final celebration has a deleted reply. Removed text was not reconstructed.

Linked images were not available as textual evidence. The account can report what participants said an image showed, that an image was “axed,” that a linked result was called the Chicago flag, and that an organiser claimed it reached the final image. It cannot independently verify the visual state of the canvas. Google Sheets, Imgur, Discord-hosted images, Meetup, and other linked material are visible only through what returns to Reddit.

The fleet record is complete for the assignment but methodologically partial: seven coders each read one slice, and their case accounts differ in emphasis. Slice boundaries are arbitrary relative to episodes. Relations assembled across those boundaries are weaker than relations read by one person, and there is no coder-agreement statistic.

No served tool output used for the final account remained clipped. A `tree_index.json` schema probe produced a deliberately truncated diagnostic dump; I replaced it with the bounded `_lead_times.py` helper and used only its selected measurements. The prescribed forest predates the seven counter-reading codes; their citations and theme assignments are carried by the append-only journal and checked in the final outputs.

## Anomalies and leads

The organiser’s edited post claims the flag survived on the final image, yet `63822o` warns two minutes before closure that it was being overrun and receives no visible defense after closure. This is not necessarily a contradiction—the flag could have remained or been restored—but the record does not show the visual resolution. The account therefore preserves both participant claims.

The room’s internal resistance is not marginal noise: members ask to ban Place posts, tell posters to stop, dismiss the late warning, and disparage the completed image. Those passages coexist with building, repair, explanation, and celebration. Different speakers express contrasting positions; the record does not establish that r/chicago changed its collective mind.

The r/MysteryDungeon overlap is the cleanest negotiated reversal. The other community says its four pixels are not random vandalism; the organiser recognizes that Chicago expanded into the earlier plan and permits completion. The Buffalo/716Place proposal ends differently: Chicago declines further expansion and says it would reclaim Link’s hair.

## Fact-file review

At each collect I read the timeline and lexicon additions. I struck two timeline lines as readings rather than facts: batch 02 characterized an AutoModerator response as a “meetup joke,” and batch 07 characterized a later response as the recurring r/chicagohelicopters “meetup joke.” Batch 07’s d4 03:39 and 04:15 timeline entries were restored to chronological order. All retained lexicon entries are verbatim terms with item ids and no gloss.

Batch 01 rewrote `timeline.md` rather than appending; the collector replaced the lead copy and I reviewed it in full. The same happened for batches 04 and 05, and the replaced lead copies were reviewed in full.

## Grouping review

Themes t01–t04 first appeared in batch 02, t05–t09 in batch 03, and t10–t12 in batch 04. Batches 05–07 extended existing themes. After the counter-reading search, seven late codes (`c0102`–`c0108`) extended building the flag, negotiating overlap, and proposing sports designs; no new theme was required.

The two themes that nearly merged were “building, repairing and showing the Chicago flag” and “exchanging help and making room with other communities.” They stayed apart because the first acts on the flag itself, while the second manages reciprocal help, overlap, or refusal between named groups.

I reviewed all twelve groupings again after the counter-reading. No theme was merged or split. The `regrouped_from` fields record the earlier separation of broad joke and canvas groupings, and the late codes were assigned through `theme_add`.

The code I would defend hardest is `c0056`, “taking clean-up duty while others build the flag core.” The thinnest code I kept is `c0024`, “announcing the Lucas Museum's return as an April Fools headline,” because only the surviving title remains.

## Counter-reading work

Before searching I fixed a competing account: the apparent sustained flag effort might be retrospective compression around one edited post, while the wider room mainly showed fragmented calls and hostility. I expected repeated failure or abandonment claims, dismissals replacing repair, or a post-event dispute that the completed image was not the Chicago flag.

The first broad query returned 32 matches; event-relevant items were opened through `read item`, while ordinary uses of “failed,” “destroyed,” “abandoned,” and “who cares” were inspected and rejected as out of scope for the counter-reading. A second query was overbroad because `r/CHICAGO` matched ordinary subreddit references; I inspected its returned snippets, opened the relevant flag items, and ran a narrower flag-failure query. The strongest contrary item was `63822o`, the late “getting overrun” warning. No searched in-scope item disputed the later textual identification of the linked image as the Chicago flag, but that null is limited to this supplied, partial record and does not verify unseen images.

The search exposed seven meaningful uncoded passages in the already fully read central flag thread. All citations were resolved before emission, and the codes were added at `step5_counter` to existing themes. Machine-generated crosspost summaries and unrelated search hits were not coded.

## Complaints

The scheduler checkpoint explicitly required `notes.md` before the contract’s final writing stage, conflicting with the contract’s instruction to write it once at the end. I recorded that conflict in the checkpoint draft, then replaced the draft with this complete final notes file after the remaining prescribed work.

The fact-file collector counts inserted Markdown headings as added timeline lines, so reported “+N lines” can exceed the number of substantive facts by one. I reviewed substantive entries rather than treating the count as content.

The broad counter-reading query’s false positives were predictable because ordinary Chicago discussion also uses “failed,” “destroyed,” “abandoned,” and “who cares.” The narrower follow-up was necessary to establish the scope of the null result.

## How the reading held up

I did not work from memory of raw threads while the fleet ran; branch B prohibited the lead from reading them. The openings file, `out/ledger.md`, `out/timeline.md`, `out/lexicon.md`, pooled codes, forest, and slice cases were the working memory.

I did not go back to a raw item because I had forgotten it. Raw items were opened only after `step5_counter` for the planned counter-reading, to inspect search hits and obtain the supporting words required by the account.

Earlier slices did not become indistinct relative to later ones because I reread the ledger before consolidation and then read codes and cases in prescribed slice order. What remained weaker was cross-slice relation evidence, a property of the fleet design rather than a memory lapse.

The run paused at the scheduler’s required checkpoint after batch 07 and then resumed with consolidation; no failed or partial coder run was resumed. I picked the lead work back up by reading `_lead_notes.md` and the ledger, verified all seven batches were already collected, and did not recollect batch 07.

The only re-reads were purposeful: selected counter-reading items, the central edited flag post, and relevant inter-community replies were opened again to test the competing account and recover exact supporting words. This occurred during step 5, after all slices and themes were in hand.
