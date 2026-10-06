# Case-lead notes — checkpoint after fleet collection

branch B; threshold 500; items_in_window 1636; chars_by_people 106297

## Facts-file review

- Batch 01: retained ten timeline additions and seven lexicon additions; none was a reading.
- Batch 02: struck `H+24.40 ... begins applying ... across image posts (dfp2zoj)` because it generalized from one moderator item into a cross-item practice reading. Retained the other seven timeline additions and all seven lexicon additions.
- Batch 03: retained two timeline additions and one lexicon addition; none was a reading.
- Batch 04: retained four timeline additions and two lexicon additions; each timeline line stays within one tagged item and both lexicon lines are unglossed terms with item ids.

## Checkpoint

All four slices have been collected. Consolidation, pooling, themes, and steps 4–5 have not begun, as required by the scheduler checkpoint.

## What was hard

The canvas and the subreddit's own April Fools joke overlap in clock time and sometimes in the same moderator post. I kept them separate by coding the real-animal rule turn explicitly as local subreddit conduct, not as r/place strategy. Attack attribution was also difficult: posts blame named groups, while visitors blame “randomers,” blank accounts, or unrelated accounts. I preserved these as contrasting participant accounts and did not decide who caused the pixels.

Several retained titles and comments describe images that are not present as text. I attributed “furby,” “furay_irl,” “Yiff Me Daddy,” and other visual descriptions to the speakers who used those words rather than treating them as my own inspection.

## Data problems

Deleted and removed bodies hide some plan and thanks posts, including `62qu73`, `62xcr5`, `6308m7`, and `631d90`. Linked images, the live canvas, PlaceTwo, pxls.space, and Discord are outside the textual record. Discord voting, negotiation, and permission therefore appear only through reports brought back to Reddit.

Branch B divides the room among four readers. No reader holds the whole week, there is no agreement measure, and slice boundaries are arbitrary with respect to exchanges. Cross-slice relations were assembled from pooled codes, slice cases, facts, and the forest; the forest shows reply sequence but does not itself establish cause. The relations explicitly carried across boundaries are the 621,621-to-final-location relocation `[crosses 01|02]` and the defense-to-rebuilding/thanks account `[crosses 02|03]`.

The timeline file was rewritten rather than appended by batches 01–03. Earlier facts survived, but batch 02 left two H+24 lines out of chronological line order. The account used measured item times rather than file order. The batch-02 line claiming the moderator “begins applying” a removal explanation “across image posts” was struck because it generalized one item into a cross-item reading; all other collected facts lines were retained.

## Anomalies and leads

The shared words repeatedly mutate—`furby`, `r/forry`, `furay_irl`, `FURPÏ`, and `Touaoii`—and participants alternately repair, accept, or celebrate them. Later comparative work could ask when alteration becomes damage and when it becomes a valued name, but this case does not impose one answer.

The room reports giving its former 621,621 place to Wales without explaining why. A self-described `/place` representative reports destroying the PlaceTwo banner, but another participant disputes that person's authority. The pxls.space invitation arrives near the end of the window and continues beyond it.

## Complaints

The collected ledger truncates several copied episode and facts lines, so the slice cases and full facts files had to be read beside it. The facts-file “append” process sometimes replaced the timeline and disturbed chronological line order. The first attempted lead `emit.close()` used a shell here-document; the sandbox refused the temporary file before Python started, while later commands in that shell invocation still ran. I repaired the prescribed order by running `emit.close()` with `python -c`, then rebuilding the forest and rerunning the audit, which passed before thematic work began.

## Grouping review

After writing the within-case account, I reviewed every theme against the practices in other exchanges and made no regrouping. Shared adjacency or shared words were not enough to merge practices: coordinating locations differs from sustained defense; naming altered lettering differs from repairing it; and present-tense completion claims differ from keeping and looking back at the finished canvas.

The two themes that nearly merged were “celebrating what the furries did on the canvas” and “keeping and looking back at the finished canvas.” I kept them apart because the first claims completion and collective credit while work is active, whereas the second accepts imperfections, preserves copies, and recounts labor after placement ends.

## Code judgments

Hardest-defended code: “following a Discord vote to abandon two locations and coordinate efforts.”

Thinnest kept code: “asking to expand in place.”

## How the reading held up

As branch-B lead, I did not read raw threads during fleet coding or thematic consolidation. I worked from each slice's codes and case in order, plus the facts ledger and forest, and opened raw items only after `step5_counter` was recorded. I did not substitute memory of a thread for served text. I returned to items to verify exact passages and instrument times, not because I had forgotten them. Earlier slices did not become indistinct in favor of later ones because the running lead notes and ledger carried their unresolved edges; the main limitation is structural, since no one reader held the whole week.

This lead run resumed after the scheduler's explicit checkpoint following collection of batch 04. I continued from `out/_lead_notes.md`, `out/ledger.md`, the collected facts files, and the on-disk journal rather than recollecting or restarting any slice. This was a planned checkpoint, not a lost reading. The only execution interruption was the failed here-document described above; no Python close call occurred in that failed command, and the close→forest→audit sequence was rerun successfully.
