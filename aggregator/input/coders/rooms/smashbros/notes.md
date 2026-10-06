# Case-lead notes

branch B; threshold 500; items_in_window 8519; chars_by_people 1287306

## What was hard

The central judgment was keeping two simultaneous practices separate: making and governing the r/place mural, and turning the subreddit into Amazing Crash Family for April Fools. Shared timing and joke language did not make them one practice. The mural themes were also easy to over-merge. Choosing a target, building it, maintaining it, moving coordination into Discord, enforcing Discord authority, negotiating with neighbors, and crediting finished work often occurred in the same thread but did different work.

Discord required equally careful language. The public record supports invitations, plans, repair instructions, access complaints, and retrospective credit. It does not expose internal deliberation or establish that Discord authority was accepted by the whole community. I therefore describe the work as increasingly Discord-directed and contested, not controlled by a consensual leadership.

The Goon material is irreducibly incompatible. Participants call it an ally that helped with Fox, a Discord way of life, unwanted lettering, or a target they proudly destroyed. I preserved these as participant positions. I likewise treated tournament authenticity during April Fools as competing claims rather than adjudicating which result was real.

## Fact-file review

I reviewed `out/timeline.md` and `out/lexicon.md` after every collection. Batches 01, 11, 16, 17, and 19 appended no fact entries. I struck no line from batches 02, 03, 06, 09, 10, 12, 13, 14, 15, 18, or 20 because their additions directly recorded cited moderator/edit actions or participant terms.

I struck these timeline readings and retained the strikethrough record:

- Batch 04: `dfojfo3`, because “triggering” asserted causation rather than recording the moderator item.
- Batch 05: `dfovysr`, because calling the EVO final “fake” adjudicated authenticity.
- Batch 07: `62svjw`, because it folded comment-layer doubt into a post fact; `62swzz`, because it called the result fake; and `62ttha`, because it called the result real.
- Batch 08: `62vnly`, because “apparent bamboozle to actual play” adjudicated authenticity.

No lexicon line was struck. Detailed per-batch reviews remain in `out/ledger.md` and `out/_lead_notes.md`.

## Branch-B limits

No reader held the whole week. Each slice had one coder, so there is no agreement measure. Slice boundaries are arbitrary with respect to ongoing threads; context openings let adjacent coders orient to continuations but do not make either a whole-week reader. The lead assembled relations from pooled codes, the generated forest, and slice cases. Relations carried across boundaries include the completed Fox effort giving way to Falco across batches 07–08 and the continued shift from public planning to Discord-directed coordination across batches 08–10. These are weaker than relations established by one continuous reader and are stated only where a passage names the link.

The forest shows reply structure, not causation. Every relation in the case rests on what the turns say; adjacency alone is reported only as sequence. Times and intervals in the account came from `package/tree_index.json` through `_lead_times.py`, not from remembered coder prose.

## Grouping review

All 397 pooled step-3 codes were read in slice order beside their slice cases and assigned once. Sixteen gerund-led practice themes were opened at their first slice and extended as later slices repeated them. The instrument records the review or split rationale in each theme’s `regrouped_from` field.

After the counter-reading, I reviewed the grouping again. I did not merge or split a theme. Late code `c0398` extended “showing, celebrating, and crediting the mural.”

The two themes that nearly merged were “moving canvas coordination into Discord and other channels” and “enforcing and contesting who gets to change the canvas.” They stayed apart because recruiting people into a venue is not the same practice as regulating decision rights, bans, repairs, and unscripted edits.

## Counter-reading record

Before searching, I wrote that the competing account would show Discord never becoming accepted coordinating authority: independent alteration, expansion, and destruction would instead be treated as the point of r/place, with public Reddit plans sufficient for successful work. I expected explicit rejections of Discord rules and alliances plus credit for unaffiliated or Reddit-only work.

Searches used the corpus’s own terms: “lone actor,” freedom outside Discord, bans and kicks, alliances and control, work without Discord, and Reddit-credited completion. I opened the relevant returned items with `read.py item`. The strongest contrary item was `dfs4gfe`, which asserts freedom to stay outside Discord and affect the canvas independently. `dfs2m15` describes lone action; `dfs5vwh`, `dfqdz7c`, and `dfqunre` connect bans or kicks to helpers lacking plan knowledge. The search also found uncoded `dfomast`, “WE DID IT REDDIT”; I emitted it as step-5 code `c0398` and placed it in the existing completion/credit theme.

No relevant returned item explicitly called Discord unnecessary or denied that it coordinated work. That null result is limited to the searched vocabulary, the public corpus, and triaged late threads. The result qualified rather than overturned the reading: early success was publicly coordinated and Reddit-credited, while later Discord direction was important but contested. All relevant hits belonged to threads coders had read whole, so step 5 did not require a new whole-thread read and no disposition changed.

## Data problems

Deleted and removed bodies interrupt plans, disputes, and ordinary threads; they were never reconstructed. External images and videos were not treated as observed content. Off-platform Discord decisions, labor allocation, bans, and treaty-making remain unavailable even where their effects return to Reddit.

Several coders reported shell-display clipping despite logged whole-thread service. Materially relevant instances include `62sb3j` (one item later recovered through the item reader), the repeated copypasta in `62ydgb`, the large final-canvas thread `638442`, and the tier-list thread `63adsz`. The final account uses only displayed, cited passages and does not claim exhaustive passage-level coverage of those threads. Other context-heavy clipped threads had only visible deleted or out-of-scope in-window material.

Late absence is bounded. Some long out-of-scope threads in batches 16–20 were assessed through prescribed triage windows rather than read whole, and some after-window replies continue beyond the study window. The absence section does not turn that partial exposure into proof that no buried mention existed.

## Anomalies and leads

Early construction repeatedly receives “WE DID IT REDDIT” credit, while later repair and expansion instructions increasingly route helpers into Discord. The contrast is a development in venue use, not proof that Reddit stopped mattering. The final discussion preserves both Discord-backed alliance claims and a lone actor’s defense of independent change.

The subreddit-specific prank outlasts April 1: moderators prolong altered flairs, stage a second-day lost-sheet bamboozle, and a tier-list author discloses and republishes a “dank prank” after placement ends. No textual relation connects this prank practice to the canvas work.

## Complaints

A logged whole-thread service can still exceed the shell display, so “read in full” is operationally true without every returned passage being inspectable. Paginated whole-thread output would make that boundary clearer. Branch B also makes cross-slice relations laborious to audit because the forest, slice cases, and pooled code reading must be held together without a continuous reader.

The counter-reading command is implemented as `cite.py --find`, although the prose contract calls it `find`; the help text resolves this, but a named wrapper would reduce avoidable ambiguity. The first attempted item reads used the JSONL record and correctly failed because `read.py` expects rendered `corpus.txt`; all successful raw reads used the prescribed rendered corpus afterward.

## Code judgments

Hardest-defended code: `requiring repairers to join so they do not set Discord back` (`c0248`).

Thinnest kept code: `asking what goon is` (`c0358`).

## How the reading held up

The fleet phase was interrupted by scheduler checkpoints after every batch, as designed. The lead turn itself was explicitly checkpointed after batch 20 and later resumed. On resumption I read `out/_lead_notes.md`, the contract sections, and the preserved ledger before consolidating; I did not recollect or recode a slice.

I did not substitute memory of raw threads for served text. Before step 5 I had not read raw threads at all; step 4 used the pooled code reading and slice cases. During the counter-reading I opened every relevant search hit with `read.py item`. I did not return to an item because I had forgotten it, and no earlier pooled slice became indistinct relative to a later one because grouping was recorded incrementally by batch. The coders’ own memory and truncation reports remain preserved in their slice notes and the ledger.

## Completion review

The full run—not only the last slice—was checked. The required case headings are present and ordered; cited item and thread ids are individually backticked; supporting words accompany material claims; times come from the instrument; the counter-reading states the competing account, strongest contrary item, search result, and change to the reading; and branch-B limitations are explicit. The complete-record preflight result is recorded by the command output at close.
