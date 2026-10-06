# Case-lead notes

branch B; threshold 500; items_in_window 3308; chars_by_people 534633

## Fleet facts-file review through batch 07

Every batch's additions to `timeline.md` and `lexicon.md` were read after collection. The detailed decisions and carry-forward remarks are recorded under the corresponding entries in `ledger.md` and `_lead_notes.md`.

For batch 07, `collect` warned that the coder rewrote `timeline.md` rather than appending. Inspection showed that the earlier timeline entries and every prior lead strikethrough were preserved, with the fifteen new entries inserted chronologically. The three lexicon additions (`pels`, `FAGTORIO`, and `banding`) were retained. All fifteen timeline additions were retained because they give surface descriptions of edited or moderator-marked items without asserting an inferred relation or outcome; no batch-07 line was struck.

Earlier review struck interpretive action glosses where they went beyond metadata, exact titles, or direct surface description. Those strikes remain visible in `timeline.md`: four from batch 02, five from batch 03, seven from batch 04, and two from batch 05. Batch 01 added no facts lines; batches 06 and 07 required no strikes. Batch 06 also rewrote the timeline, and inspection likewise confirmed preservation of prior entries and strikes.

## What was hard

The hardest distinction was between a canvas relation and a participant's report about one. Catalunya appears as a warned-about takeover, a denied threat, a peace proposal, and an ally in the retrospective. I preserved those positions rather than choosing one stable label. Likewise, the proximity of several defence warnings does not establish that they concern one attack.

The room's own April Fools conduct overlaps the canvas in time. Codes on the oldschool redesign, fake release, fake patch notes, and community-map trap explicitly mark them as subreddit jokes rather than canvas conduct. The late community-map correction remains in the case because it is conduct, but it is not evidence about r/place.

Automation was another boundary problem. Script-writing, overnight running, and “spirit of automation” praise are visible practices, but so are “ruins the point” and “bots are what is ruining r/place.” I kept these together as the room deciding how automation belongs, not as evidence of consensus or a change of mind.

## Data problems

Deleted and removed bodies are common in short proposal, warning, and defence posts. Surviving titles support narrow acts but not reconstructed arguments. Image links do not make their contents textual evidence. The canvas itself, Imgur images, Pastebin source, Discord discussion, and pxls.space pixels are outside the record.

The forest reports 51 uncoded stretches of at least forty characters and mean coverage 0.85 for coded items. These are visible analytic choices, not hidden corpus loss. The retrospective continues beyond the final slice, and two comments inside it are deleted.

Branch B divides the week among seven readers. No reader held the whole record, there is no coder-agreement measure, and slice boundaries are arbitrary with respect to exchanges. I used cross-slice relations only where later words name or answer the earlier practice; otherwise I reported sequence. Batch 06 and batch 07 rewrote `timeline.md` rather than appending, but post-collect inspection confirmed that earlier lines and lead strikes survived and the new lines were inserted chronologically.

## Anomalies and leads

One canvas visitor says the r/place banner led them to try and buy Factorio. The retrospective's ally list is unusually broad compared with the earlier mixture of treaties, neighbour objections, attack reports, and disputed threats; it should be read as a participant's closing account rather than a neutral map.

The moderator ban does not immediately end local r/place talk. Posts continue to propose, defend, and negotiate, even as replies redirect them to the sticky or Discord. After closure, participants quickly propose a copy, while others say it has lost or never had novelty.

## Grouping review

All 232 live codes were assigned exactly once across 15 themes after reading the pooled codes slice by slice beside their cases. I reviewed the grouping again after the counter-reading. No regrouping was required: objections to bots are meaningful variation within “automating pixels and arguing whether bots ruin the point,” and scepticism toward pxls.space is meaningful variation within “starting again on a replacement canvas.” The single-code theme “seeing Factorio biters in r/bluecorner” stayed single because no other code shares its supported practice.

The two themes that nearly merged were “designing and extending the conveyor belt” and “bargaining with neighbours over space, crossings, and help.” I kept them apart because one makes and corrects the artefact, while the other negotiates permission, coexistence, or assistance with other groups; shared belt vocabulary alone does not make those the same practice.

The code I would defend hardest is `c0058`, “proposing a new logo twice as big after finishing one.” The thinnest code I kept is `c0065`, “bringing out an old post because it is a good day for it.”

## Counter-reading search

Before searching, I recorded the alternative that this might be a narrow, automation-heavy effort resisted by the wider comment layer. Searches used the case's vocabulary for giving up or abandoning, bots or scripts ruining the point, too few people helping, and lost novelty. I read each relevant returned item through `read item`.

The strongest contrary item is `dfrjez5`, “bots are what is ruining r/place.” `dfr2tgs` says automation “ruins the point,” `dfsl62i` says the copy has “lost its novelty,” and `dfs6j52` and `dfsaafv` admit not helping. The apparent abandonment item `dfpqtg0` instead proposes focusing from an “outpost” onto a “megabase.” No searched item collectively calls for abandoning all Factorio drawings. That null is scoped only to these complete-record regex searches; removals and off-platform activity limit what absence establishes. No late code was needed because every relevant contrary item was already coded.

## Complaints

The facts-file instruction distinguishes facts from readings but gives no syntax for retaining edit/moderator metadata while striking only a descriptive clause. I struck whole lines when the gloss was interpretive and documented each decision. The repeated rewrite warnings were alarming but inspectable and did not lose prior work.

The fleet ledger truncates some copied episode lines mid-word. The underlying slice cases remained available and were read in full, so the truncation did not control the account, but the ledger alone would not have been sufficient after compaction.

## How the reading held up

I did not work from memory of raw threads. As branch-B lead I did not read raw threads before step 5; I worked from `openings.md`, the pooled code reading file, all seven slice cases, the forest, the ledger, and the facts files. During the counter-reading I used `find` and then `read item` on the returned relevant items as prescribed.

I went back to slice cases and pooled codes because the combined case output was once transport-truncated, not because I was trying to reconstruct a forgotten raw thread. Earlier slices became less vivid than later ones during the multi-checkpoint run, so I reread `ledger.md`, `_lead_notes.md`, and each slice case during consolidation rather than relying on conversational memory.

The run was intentionally checkpointed and resumed after each scheduler-run coder, and once after all seven slices were collected. At each collect I recorded facts review and carry-forward issues in the ledger and lead notes. On the final resume I read those records, consolidated once, closed once, built and audited the forest, then proceeded to themes and the account. No crash-resumption cursor affected corpus reading; the original lead state began at cursor 0.

## Final completeness review

The gate values above were copied from `out/_gate.json`. All 275 threads are disposed; every coded thread has live codes; the audit verified 232 live code offsets, 71 pointer offsets, 76 exclusion citations, seven slices, 63 coded forest threads, and all codes on forest nodes. The required case headings are present in order, episode endpoints and textual evidence use individually backticked ids, and relations distinguish explicit answers from sequence. The ordinary opening, separate subreddit jokes, off-platform limits, post/comment contrasts, counter-reading, selection, named communities, and removals are all accounted for.
