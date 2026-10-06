## Gate and fleet

Branch B was fixed by 939 in-window items against the 500-item threshold; the manifest also records 938 items and 138,605 characters by people. Batch 01 and batch 02 were read by separate coders, collected in order, and pooled only after the scheduler checkpoint. No reader held the whole week, slice boundaries were arbitrary with respect to practice, and there is no agreement measure. I carried one cross-boundary sequence—the original event closing before the PlaceTwo sequel—and did not claim it was causal.

At each collect I reviewed every appended fact line. I struck none: all seven timeline lines identify visible edits, stickies, or moderator conduct with item ids and times, and all ten lexicon lines are unglossed terms with first-use ids. The decisions and carry-forward remarks are recorded under each batch in `out/ledger.md` and in `out/_lead_notes.md`.

## Grouping review

I reviewed all 113 codes in slice order beside each slice case. Shared vocabulary or reply position was not enough to group them. I split “working out what and where to build” from “joining in and getting Buffalo marks built” because selecting coordinates, designs, colours, and borders is a different practice from recruiting, placing, thanking, and reporting progress. I also split “using and contesting scripts and placement glitches” from “repairing and defending Buffalo space” because the former concerns the means and fairness of pixel placement while the latter concerns holding or restoring a mark. Both regroupings are recorded through `regrouped_from` on the resulting themes. I then reviewed the grouping against the forest and counter-reading; no further regrouping was warranted.

The two themes that nearly merged were “repairing and defending Buffalo space” and “using and contesting scripts and placement glitches.” What kept them apart was that participants could defend without discussing a placement tool, while scripts and glitches were also used to attack or clean rather than simply defend.

## What was hard

The hardest interpretive boundary was preserving three simultaneous practices in the same threads: building Buffalo marks, attacking rivals, and negotiating help. The contrary cooperation passages are substantive, but they do not demonstrate that accepted peace displaced recurrent attacks. I therefore described a contested practice rather than a change of community mind.

The r/716Place evidence is also narrow. “Join us” and “Our stuff has been organized” support movement of organizing, while continued local defense talk supports a division of venue. They do not expose decisions or labor inside r/716Place, and the 12-hour-36-minute sequence does not establish that the first post caused the later arrangement.

The successor-canvas title says “6 hours later,” but the instrument places the post 11 hours 45 minutes after original placement ended. I kept the former as participant wording and the latter as the measured interval rather than silently equating them.

## Data problems

The deleted body of `62su6n` and deleted comments in selected threads cannot be reconstructed. Images and linked canvases were unavailable as text. r/716Place and PlaceTwo are visible only through local references. The forest reports no moderator-removed node among coded threads, but that narrow absence cannot rule out moderation elsewhere in the 64-thread record.

Batch-02 pooled pointers `p0008`–`p0011` retain slice-local `code_ids` (`c0001`, `c0002`, `c0005`) rather than the pooled code ids beginning at `c0108`, even though their item offsets are correct and the fleet audit passed. The final account does not rely on those pointer-to-code fields.

## Anomalies and leads

The corpus places explicit rival-targeting beside calls that “all NHL teams should help each other,” truce offers, and reciprocal maintenance. A comparative reader should not collapse either side into a stable community position.

The Red Wings appear first in participants’ accounts as scripting over Buffalo space and later through a direct offer of help “as a thanks” for being allowed space. The offered reason supports reciprocity; the unseen negotiation and actual pixel consequences remain open.

The final slice adds a 45-by-45 PlaceTwo logo described by one author as made “one pixel at a time.” The passage does not settle whether the work was strictly solitary or only describes that author’s contribution.

## Counter-reading record

Before searching, I recorded this alternative: cross-team cooperation may have been the organizing center, with rival attacks only side episodes; if so, sustained mutual help, accepted truces, and maintenance should displace or reverse attacks. The strongest contrary item was `dfqu86q`. Narrow whole-word and proximity searches returned relevant truce or help passages at `dfqud4x`, `dfrssu2`, and `dfrzdif`, all already coded, plus ordinary hockey false positives. No late code was needed.

One initial query used the substring `ally` and returned 148 noisy matches because it could occur inside unrelated words. I did not treat the count as evidence; I narrowed the expression to word boundaries and read the returned items. The relevant evidence changed the account to contested coexistence of rivalry and cooperation but did not overturn it.

## Code judgments

Hardest to defend: `moving r/place talk out of r/sabres and into r/716Place`.

Thinnest kept: `mentioning r/place in a post whose body is gone`.

## How the reading held up

As case lead, I did not read raw threads while the fleet ran. I worked from the openings for orientation, then the ledger, two slice cases and notes, pooled codes in slice order, and the forest. I did not substitute memory for served text or reopen an item because I had forgotten it. During the permitted counter-reading stage I used `find` and `read item`; earlier slice material did not become indistinct relative to later material because the ledger and ordered pool kept their boundaries visible.

The scheduler checkpoint interrupted the case-lead workflow after both batches were collected. On resumption I reread `out/ledger.md` and `out/_lead_notes.md` before consolidation. This was a planned checkpoint rather than a failed reading attempt. No raw corpus reading had occurred before that point.

## Complaints and instrument record

The shell refused a here-document because it could not create a temporary file, so that Python close invocation never launched. The forest and first audit nevertheless ran; I then performed the required initial close with a one-line foreground invocation, rebuilt the forest, and reran the audit, which passed.

I accidentally called non-verdict `emit.close()` again after themes, producing a third total close once the required verdict close is included. The journal exposes this; it does not alter codes or themes, but it departs from the prescribed two-close order. The first theme script also tried to assign `c0069` twice; `emit` refused before writing the conflicting theme. The four already written themes stood, and a resume script recorded only the remaining corrected themes.

The scheduler required a checkpoint version of `notes.md` before consolidation, while the base contract says to write it once at the end. I obeyed the explicit checkpoint instruction and replaced that preliminary checkpoint text with this final notes account after step 5; this departure is recorded here rather than hidden.

Finally, the pointer vocabulary requires subreddit pointers to retain `moved="no"`, even when the text explicitly directs organizing to r/716Place. The structured pointer therefore cannot express the relocation; the code, theme, and case account do.
