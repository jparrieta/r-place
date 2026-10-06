# Case-lead notes

branch B; threshold 500; items_in_window 10209; chars_by_people 934837

## What was hard

The principal difficulty was separating three contemporaneous strands: r/place canvas work, the subreddit-wide Laine/Jets April Fools takeover, and ordinary hockey discussion that remained inside a selected thread and therefore still required coding. Claims about completion, attacks, borders, and image quality had to remain participant reports because linked images and the canvas itself were not read.

The other difficult boundary was between reply structure and evidence of response. I used a relation only when the later words answered, named, recalled, or explicitly explained the earlier passage. The post-event run of ordinary hockey is reported as sequence, not as a change caused by the canvas ending.

## Facts-file review

Every collected addition to `timeline.md` and `lexicon.md` was read. I struck timeline lines when they paraphrased what an edited or moderator item was doing, characterized an exchange, inferred a prior position, or added contextual interpretation beyond exact participant words and metadata. This affected batches 01, 02, 03, 05, 07, 08, 09, 10, 11, and 12. Batches 04, 06, and 13–17 added no timeline lines. All unglossed lexicon additions were retained. The collect tool reported that batches 01, 02, 03, and 09 rewrote `timeline.md` rather than appending; each replacement was reviewed, and prior harness seeds and lead strikes remained present. The batch-by-batch reasons and carried questions remain in `out/ledger.md` and `out/_lead_notes.md`.

## Fleet and evidence limits

No fleet coder read the whole week, and one coder read each slice, so there is no agreement measure. Slice boundaries are arbitrary. The Viking bargain is the only relation carried directly over a slice boundary; it is retained because the batch-08 megathread repeats the move-for-leaving-the-sail exchange recorded in batch 07. The forest makes the sequence visible but does not make the fleet a single reader.

Deleted and removed bodies interrupt exchanges. Images, linked posts, and the canvas were not inspected. Discord carries planning and negotiation outside the visible record; only requests, instructions, and reports returning to Reddit are available. A proposed drawing script is not evidence that automation was adopted. Visitors from neighbouring projects sometimes speak inside r/leafs, so venue does not establish Leafs authorship.

## Counter-reading search

Before searching, I recorded the competing account and its expected evidence in `out/_lead_notes.md`. After staging `step5_counter`, I searched the full corpus for the case's own destructive vocabulary and read each event-relevant returned item with `read item`. All returned event items sat in threads a fleet coder had read whole, so no lead `read thread` was required. Nine late codes were appended and added to existing themes. The strongest contrary item remained `62w16l`; the search also found explicit redirection from rival attacks toward the Leafs build. The initial attempt to call `read item` against `coder_corpus.jsonl` produced “wrong file” errors; I corrected the invocation to the instrument's rendered `corpus.txt` and then read the items through the prescribed tool.

## Grouping review

After writing the within-case account, I reviewed every theme boundary against the pooled codes and the nine step-5 codes. I did not regroup: the practices remained distinguishable, and the late codes extended existing themes rather than opening or splitting one.

The two themes that nearly merged were “defending and repairing the Leafs picture” and “bargaining for space and help with neighbours”; they stayed apart because replacing damage and negotiating another group's future conduct are different practices even when one bargain reduces repair work.

Hardest-defended code: `c0327`, “redirecting a Habs attack into finishing the Leafs logo.”

Thinnest kept code: `c0247`, “asking whether an image is r/place 2.0.”

## How the reading held up

As a branch-B lead I did not hold or reconstruct raw threads before the counter-reading stage; I worked from the ordered pooled-code reading file, slice cases, ledger, facts files, and forest. I did not substitute my memory of a raw thread for served text. When the run resumed after the scheduler checkpoint and conversation compaction, earlier slices were less sharp than later ones. I recovered by rereading `out/_lead_notes.md`, the relevant ledger record, `package/codes_by_thread.md` from the beginning in slice order, and each coded slice case beside it. I returned to batches 05–12 specifically because their detail was no longer reliable from memory. During step 5 I reread every search hit as an item because the search snippets and memory were insufficient for coding. The run was interrupted and resumed once at the prescribed post-collection checkpoint.

## Anomalies and leads

Batch 04's notes unexpectedly repeated the lead's earlier shell here-document difficulty; this is a provenance anomaly, not case evidence. The lead's own initial here-document attempts failed without writing because the shell could not create a temporary file under the sandbox; in-directory helper files or `python3 -c` were used afterward. Several `timeline.md` additions were interpretive despite the facts-only instruction and were struck rather than silently revised.

## Complaints

The branch-B division usefully bounded reading but makes the required whole-case relations structurally weaker: the lead must adjudicate slices without having read their full threads, while the only coder who did read a slice never sees the adjacent one. The contract's explicit cross-boundary marking and late counter-reading access made that limitation visible, but cannot remove it.
