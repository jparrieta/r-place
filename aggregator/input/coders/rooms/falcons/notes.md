# Case-lead notes — r/falcons

## Gate and fleet

The recorded gate used branch B: 762 in-window items exceeded the threshold of 500, producing two whole-thread slices. Batch 01 disposed 51 threads and batch 02 disposed 32; both passed their read audits and were collected once. No timeline or lexicon additions were struck. The timeline additions were concrete descriptions of edited items with times and item ids; the lexicon additions were participants’ terms with first-use item ids and no gloss.

The branch-B limitations are substantive. No reader held the whole week, one coder read each slice, and there is no agreement measure. Slice boundaries were arbitrary with respect to the case. The scoreboard campaign crossed the boundary: batch 01 left it unresolved, while batch 02 inherited it and supplied an explicit “blitz the board” proposal. Relations across that boundary were reconstructed from the two slice cases, pooled codes, and forest, not from a single reader’s continuous experience.

## What was hard

The hardest distinction was between arguing that the canvas fight was not worth caring about and arguing that manual placement could not beat reported bots. Both can sound like dismissal. I kept them apart because the first disputes the value of the fight, while the second debates practical capacity and includes participants who still enjoyed or supported r/place elsewhere.

Claims about bots, alts, scripts, and alliances were unusually detailed but remain participants’ reports. A participant describes blocks being replaced within twenty seconds and recounts six hours of placement; that supports their own explanation for stopping, not independent proof of automation. Similarly, a Patriots visitor reports Slack circulation, but the Slack’s ownership and decisions are unavailable.

The April Fools material required keeping two jokes apart. Fake trades, reversed loyalties, and fake Super Bowl news are this subreddit’s own April 1 conduct, explicitly not conduct about the canvas. The notes and themes preserve that separation.

## Data problems

Removed opening bodies affect several central event threads: `62vj87`, `62vj9v`, `62vzz7`, `62x702`, and `63afop`. Their surviving titles and replies support limited claims, but the initiating bodies cannot be reconstructed. Deleted comments interrupt personal and bot arguments in `634x6u` and `637anh`.

The record shows only what people in r/falcons said about the canvas, Slack, other subreddits, 4chan, bots, scripts, and pixel users. It does not expose those external venues or verify canvas outcomes. Both fleet coders reported no transport truncation.

Every Python invocation printed a macOS warning that a cache file could not be created under `/tmp`; the tools nevertheless completed. One attempted `python3` here-document failed before Python ran because the shell could not create its temporary file. It produced no journal action; the required first `emit.close()` was then run successfully as a direct foreground invocation. Working scripts and state remained inside this run directory.

## Anomalies and leads

The first erase thread says the post was sent into “our slack,” a lead about off-Reddit circulation but not evidence of what occurred there. A human names a bot account as an example of automated pixel placement, but that account’s activity is outside the corpus.

An ordinary April 2 Daily Discussion carries one direct r/place recruitment amid baseball and football talk, showing that the event recruited the room’s existing catch-all format without taking it over.

The Eagles anti-Nazi-flag appeal becomes conditional bargaining over the Falcons’ Pats target. The Georgia-G request becomes Tech–UGA rivalry and cross-subreddit familiarity. r/Braves and r/cfb are pointers within an event thread, not evidence that organising moved to them.

The counter-reading’s strongest contrary item proposes Manningface over 3-28 as “Creation instead of mindless destruction” and reports “a little progress.” Searches found no report that a Falcons-created image was completed or held. The scoped null says nothing definitive about the external canvas.

## Complaints

The branch-B contract correctly requires facts-file review after each collect, but the scheduler also required a checkpoint version of `notes.md` before consolidation even though the base contract says `notes.md` is written once at the end. I followed the scheduler’s explicit checkpoint instruction and replaced that provisional note with this final account of the run.

The fact that edited-item timeline lines describe an item’s content does not reveal what the edit changed; the record supplies only the edited flag and final body. I retained the lines as facts about edited items, not edit histories.

After the final required branch-B fleet audit passed, I also invoked the standalone root `read audit`. It compared pooled thread dispositions with the case lead’s intentionally empty pre-step-5 raw-thread log and therefore labelled all 83 dispositions “overstated.” This diagnostic is not branch-B aware: the required `audit_fleet.py` check used the staged coder read logs and passed all slices, dispositions, offsets, pointers, and forest nodes. I did not alter the pooled record in response.

## Grouping boundary

“arguing whether the canvas fight is worth caring about” and “arguing whether five-minute placements can beat bots” nearly merged; value judgments kept the former apart from practical-capacity claims and the dispute over whether to continue by hand.

The grouping was reviewed after both slice cases. I split tactical instructions from rallying calls, conditional answers from general ally recruitment, and post-placement result talk from live-thread taunting. Those decisions are recorded in `regrouped_from`; other themes explicitly record that review produced no regrouping. The Slack-circulation code remained a single-code theme because it shared no practice with another code.

## Code judgement

Hardest to defend: `making help conditional on erasing the Pats meme` (`c0173`).

Thinnest kept: `agreeing they have way too much time` (`c0167`).

## How the reading held up

I did not work from memory of a raw thread. Under branch B I read no raw threads before consolidation and theme construction; I worked from the ledger, the two slice cases, the pooled codes in slice order, and the forest. At the scheduler checkpoint I reread `out/ledger.md` and `out/_lead_notes.md` rather than relying on conversation memory.

I went back to the slice cases, forest, and selected items whenever exact wording, an endpoint, or a relation was needed. This was because the instrument requires checkable wording and measured intervals, not because I had forgotten a raw thread I had previously read. The counter-reading hits were all opened with `read item`; no returned hit was treated as a count-only result.

Earlier material did not become indistinct relative to later material in my own thread memory, because no single-reader raw-thread memory existed in this branch. The batch 01 account was less immediate after reading batch 02, so I used the ledger and the batch 01 case beside the batch 01 pooled codes before grouping. The planned scheduler checkpoint occurred after both collects; this was not an interrupted failed run, and I resumed from the recorded ledger and lead notes without recollecting or restarting.
