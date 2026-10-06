# Case-lead notes

branch B; threshold 500; items_in_window 2000; chars_by_people 242958

## Facts-file review

Batch 05 added three timeline lines and three lexicon lines. I reviewed each line and struck none: the timeline entries are limited to one participant edit and two moderator rule-6 removals, each with a time and item id; the lexicon entries reproduce unglossed participant terms with item ids. The collect command warned that batch 05 rewrote `timeline.md` rather than appending, but full inspection showed that every earlier entry remained and the three new entries appeared in time order, so no fact was lost. Batch 04 produced the same warning with no loss on inspection. Reviews for batches 01–04 and their carry-forwards are recorded under their entries in `out/ledger.md` and in `out/_lead_notes.md`.

## Fleet and checkpoint

All five slices were collected before the scheduler checkpoint. The checkpoint write to `notes.md` preceded the contract's normally final-only notes write because the scheduler explicitly required the batch-05 review here before continuation. On resumption I reread `out/_lead_notes.md`, `out/ledger.md`, and this file, then consolidated without recollecting batch 05. The first `emit.close()`, forest build, and fleet audit followed in the prescribed order; the audit passed.

Branch B means no reader held the whole week. One coder read each slice, so there is no agreement measure. Slice boundaries are arbitrary with respect to exchanges, and the forest shows reply sequence without turning adjacency into causation. Relations assembled across slices would be weaker; the final case therefore does not assert a causal relation across a slice boundary. Discord and r/placeTexas movement also mean falling activity in r/texas cannot establish that practice ended.

## Grouping review

I read `package/codes_by_thread.md` one slice at a time beside the corresponding slice case, opening themes when their practice first appeared and extending them in order. `_lead_theme_plan.md` records the practice holding each group together and variation within it. I reconsidered boundaries after the counter-reading and did not regroup any already-emitted code. Moving venues stayed apart from the bargains brought back; relocation stayed apart from maintaining an existing position; scripts stayed distinct because participants exchanged, modified, ran, troubleshot, and contested the tool.

The two themes that nearly merged were **Celebrating what the flag became** and **Arguing over what the Texas–Norway fight meant**. They stayed apart because good games, thanks, affection, insults, and memorials close socially with other participants, while explanations, corrections, blame, symbol interpretation, and naming the war make an account of what happened.

The code I would defend hardest is `c0252`, **denying r/Texas can command flag workers and sending authority to Discord**. The thinnest I kept is `c0138`, **showing r/place right now**, which rests on a terse surviving title and contributes only a bounded status-post practice.

## Counter-reading record

Before searching, I recorded the competing account that r/texas mostly relayed or watched work controlled by Discord users, scripts, and placers outside the room. If that account were right, explicit denials of subreddit authority, reports of decisions elsewhere, and failed public instructions should be present. The strongest contrary item was `dfrp3jf`, which says r/texas indicated the “mood of Texans, not the community as a whole,” estimates only 10% of workers were prior subscribers, and redirects official authority to Discord.

The targeted searches covered the complete record's vocabulary around mood, authority, control, Discord, coordination, scripts, bots, missed memos, undoing work, and official designs. Every returned item was opened with `read item`, including false-positive `undo` matches in immigration discussions. Three relevant returned passages lacked codes: `dfpswkt`, `dfqf7gf`, and `dfqs4xq`. They were cited, coded at step 5 as `c0287`–`c0289`, and added to the existing venue-movement theme. The contrary evidence narrowed the account from command center to recruiting, relay, bargaining, and reflection venue; direct evidence of building, repairing, negotiating, and handing off survived.

## What was hard

The hardest distinction was between a neighbor's accusation, a Texan's reply, and a fact about what happened on the canvas. Claims about “rogues,” spies, bots, erasure, and who began attacks conflict. I retained them as blaming, rejecting, reporting, or explaining rather than resolving them. Another difficult boundary was between defending an existing flag and bargaining to abandon it for a rebuilt flag elsewhere. The late Norwegian article invited a story of reconciliation, but affection and jokes coexist with grievance; different speakers do not establish that the community changed its mind.

## Data problems

Removed and deleted bodies obscure initiating claims in many short event threads. Link and image posts often leave only titles, and unavailable images were never interpreted as evidence. Some replies continue beyond the window, especially `63a5b7`. Four off-platform routes—Discords, a panning sheet, another subreddit thread, and r/placeTexas—show that coordination moved or partly moved, but their internal deliberation is absent.

Batch 04 and batch 05 each rewrote their seeded `timeline.md` rather than appending. Collection warned about both; full inspection showed all earlier facts retained and the new lines inserted in time order, so no repair or strike was needed. The ledger's copied unresolved-episode summaries are visibly clipped at line ends; I used the complete slice `case.md` files during consolidation rather than completing clipped text from memory.

## Anomalies and leads

The same room uses Texas history and ordinary sayings as both tactical instructions and retrospective labels: the Alamo and San Jacinto mobilize defense, while “The Texan-Norwegian War” names the finished episode. The explicit claim that r/texas represented a mood rather than the workers is the strongest lead for comparison with other place communities. Moderator redirection to r/placeTexas is also important because disappearance from the source venue may reflect relocation of talk rather than declining engagement.

## Complaints

The contract's final-only instruction for `notes.md` conflicted with the scheduler's explicit checkpoint requirement to write batch-05 review remarks here before consolidation. I followed the checkpoint instruction and completed the same file at the final writing stage, preserving rather than replacing the earlier record. The fleet ledger truncates some copied edge-tag passages, which makes it unsuitable as the sole memory despite the contract describing it that way; complete slice cases remained necessary.

A root-level `read.py ... audit` diagnostic reports the pooled fleet dispositions as unread because the lead's own read log contains only step-5 item reads; it does not merge the slice read logs. The role-specific fleet audit had already verified all staged slice logs and passed. I therefore treat the root diagnostic as inapplicable to branch B and leave final validation to the required lead preflight.

## How the reading held up

I never substituted memory of a raw thread for served material. Before step 5, branch B correctly prevented the lead from reading raw threads; I worked from the openings overview, pooled code reading file, complete slice cases, facts files, ledger, and forest. I did not reopen a slice because I could not remember it; I read every slice in order during consolidation and reopened only targeted items returned by the required counter-reading or needed for exact final support. Earlier slices did not go indistinct because the incremental theme plan and lead notes carried their boundaries forward.

The run was deliberately interrupted by the scheduler checkpoint after batch 05 collection, not by a tool failure. I resumed at consolidation after rereading the three lead-memory files and did not repeat collection. No external memory, atlas, web source, or unserved project file was used.
