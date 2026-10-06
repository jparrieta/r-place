# Notes

## Gate and fleet limits

The gate selected branch B: 1,159 in-window items against a threshold of 500, with 159,155 characters written by people. Three coders each read one whole-thread slice. No reader held the whole week, there is no agreement measure, and slice boundaries are arbitrary with respect to exchanges. Relations crossing 01|02 or 02|03 are marked in `case.md` and rest on the pooled forest, exact item passages, and the two slice accounts rather than on one reader's memory.

The run was deliberately checkpointed after batch 03 was collected. On resumption I read `out/_lead_notes.md` and the checkpoint `notes.md`, did not collect the batch again, and continued with consolidation.

## What was hard

The event and the room's own April Fools conduct occupy the same days and reuse Dome, Helix, voting and flair. I kept the distinction at passage level: the two-day election, candidate AMA, request bamboozle, potato/flair/song bits and Ash Gray hydro-electric-plant joke are community conduct but not conduct on the canvas.

The hardest interpretive boundary was between doing pixel work and later telling a morally satisfying story about it. Calls, templates, coordinates, repairs and relocations are direct operational conduct. Claims that attackers received “bad endings” and allies stayed clean are attributed participant recollections; they are not treated as verified canvas history or causal evidence.

The counter-reading also required preserving disagreement without inventing a change of mind. `dfqc74d` says the redraw will get nowhere and the subreddit is “deader”; `dfpva8b` says Dome cannot be saved from r/Space. Other speakers continue repairing, relocating and rebuilding. These are contrasting positions and constraints, not a demonstrated community conversion from effort to abandonment.

## Grouping review

The first grouping review split “turning alliances and land claims into Chatot lore” from “making, losing, moving, and cleaning up Chatot”: the former retells relations through art, jokes and documentation, while the latter coordinates pixels. It also split “trying to rebuild Dome before place locked” from “calling people in to defend and redraw familiar figures,” because the rebuild repeatedly scouts new sites and ends at the lock rather than maintaining an existing figure. Both regroupings are recorded in the themes' `regrouped_from` fields.

After the counter-reading search I reviewed all nine themes again and made no further regrouping. Contrary items `dfqc74d`, `dfpva8b` and `dfp588u` remain meaningful variation inside defending/redrawing and running the vote rather than separate practices.

An incremental `theme_add` initially refused a numeric range because it included election codes `c0112`–`c0115` already assigned to the vote theme. The refusal occurred before that addition was written. I resumed append-only, excluded those four codes from the April Fools-bits range, and the final grouping assigns every code exactly once.

The two themes that nearly merged were “making, losing, moving, and cleaning up Chatot” and “turning alliances and land claims into Chatot lore”; operational pixel coordination versus retrospective relation-making kept them apart.

## Judgement calls

The code I would defend hardest is `spending all day talking with and helping neighbours around Chatot` (`c0211`). The thinnest kept code is `adding another power-plant image gag` (`c0247`), which rests on a surviving title because the body is deleted.

The duplicated alliance-art title appears first with a deleted body in `63clpw` and then as an intact linked post in `63cmz7`. Both surviving publication acts remain coded; the record cannot establish why the first copy was deleted.

The facts-file review struck two batch 02 timeline lines: `dfp4xkb` used “complaint” and `dfqgtbf` used “hint,” both readings rather than bare edit facts. No lexicon lines were struck, and no batch 01 or batch 03 timeline additions were struck. Batch 02 and 03 collection warned that the coder rewrote rather than appended its timeline copy; inspection showed that the lead file preserved earlier facts and strikes and merged new facts in time order.

## Data problems

The first coder's full display of inherited thread `5yznv4` was transport-truncated in its middle even though the instrument logged the thread as served whole. The visible beginning and end support its retained codes, but unseen middle turns limit the account of that discussion. Batch 02's long `62u073` AMA display was also initially clipped; that coder re-served and paged it, so its missing middle was recovered.

Deleted bodies occur in relevant election, Chatot, SaveDome, logo, plant and alliance threads. They were not reconstructed. Title-only image and link posts support publication acts and participants' names for artifacts, not independent visual descriptions.

Coordination partly moved to Discord, imgur and an external wiki. Reddit shows what returned—flair, templates, calls, coordinates and documentation requests—but not full off-platform deliberation, visual plans or resulting wiki edits. This limits claims about decisions and about absence.

macOS/Python repeatedly attempted to create an xcrun cache under `/tmp`; the sandbox denied it and the instrument calls completed. Subsequent calls set `TMPDIR` to `out/tmp`. An early lead heredoc also failed because the shell attempted an external temporary file; it ran no Python. Working scripts and state remained in the run directory.

## Anomalies and leads

The reported Helix vote surge combines a concrete participant explanation—a Discord request and repeated clicking—with jokes about hackers, fraud and impeachment. Both the claimed mechanism and comic register matter; neither proves an audited election process.

The redraw argument recruits a broader dispute over whether the subreddit is “dead,” contrasting subscriber totals, current attendance and a returner's story. It is retained only where speakers use that dispute to assess whether enough people can change the repair template.

The Ash Gray plant joke persists after the canvas closes and produces a claimed gameplay consequence in CC's final form. It shows what this room returned to inside the window rather than an r/place aftermath.

## How the reading held up

I did not work from memory of raw threads. Before step 4, I had read only the brief, openings and lead records; the fleet held the raw slices. Theme consolidation used `package/codes_by_thread.md` one slice at a time with that slice's case beside it. I did not go back because I could not remember a thread. During step 5 I opened every counter-search hit and the individual items needed for checkable quotations, as the contract permits.

Earlier material did not become indistinct relative to later material because the ledger and `_lead_notes.md` carried each boundary, fact review and unresolved edge across the checkpoint. The run was interrupted only by the scheduler's planned checkpoint after batch 03; I resumed from those files and did not repeat collection.

## Complaints

The contract says `case.md` and `notes.md` are written once at the end, while the scheduler explicitly required a checkpoint entry in `notes.md` before consolidation. I followed the scheduler's checkpoint instruction and replaced that provisional entry with this final notes account; the conflict is recorded here.

The full-thread tool has no documented paging remedy when a response is transport-truncated. That left batch 01's `5yznv4` middle genuinely unseen, unlike the later AMA where the coder found a compliant re-service route. A native bounded-page option for `read.thread` would remove this ambiguity.
