I answered the handler's seven questions with fresh checks in this interview copy. The check scripts are in `out/_analysis/` under names starting `iv_` and write nothing else; none of this reaches the run. Three of my B1e statements fail these checks; they are listed at the end.

## 1. The coder's grain, or larger themes about more things

**What I checked:**
- **Between rooms (676 rooms).** Rooms with more codes do have more themes (correlation 0.45). But a room's average concepts per theme does not predict its share of single-kind themes (correlation 0.00).
- **Within rooms (596 rooms with six or more themes).** Themes above the room's median size sit on one kind 43.9% of the time; themes at or below it, 56.9%. 407 of the 596 rooms go the same way. With bags left out, the shares are 29.0% against 55.6%.
- **How much of a theme an added kind rests on.** The median is 2 concepts in themes of 6 to 10 (25% of the theme) and 3 concepts at 11 to 40 (18%, then 12%). At 41 or more it is 4 concepts (7%).

**Answer.** It is not the coder's cut of a room. Hold the room fixed and bigger themes still carry more kinds. But the extra kinds are thin: 2 to 4 concepts, a shrinking share of the theme. Rule 0's bar is "a concept of its own", a fixed count, not a share. A longer list of concepts meets it more often. The record cannot separate "the room did more in that stretch" from "a fixed bar catches more side-doings in a longer list."

**A test for B2:**
1. Draw themes of 11 to 40 concepts that B1 placed on two or three kinds. Draw native themes of 1 to 5 concepts as controls.
2. Cut each large theme's concepts at random into sets of five.
3. Fresh readers place each set alone, with the gates and without the coder's label or note.
4. Read the outcome:
   - If the sets land on different kinds that together rebuild the theme's kinds, the theme holds several doings.
   - If the added kinds appear only in the one set holding their 2 or 3 concepts, they are side-doings the bar admits. Then rerun with a share bar, for example 20% of the theme's concepts, and count which kinds survive.
   - If the added kinds appear only when readers see the whole theme with its label, the coder's framing drives them.

## 2. Placements the shipped gates would change

**How I drew the sample.** The population is every second-order theme that scheme_current.jsonl places on two or three kinds and that is not a bag: 3,796. The script sorts them by room and theme id, shuffles with the seed "iv-b1e-q2" and takes the first 20 (`out/_analysis/iv_q2_draw.py`). I read each one in full with `mem.py codes --sub S --second tNN`, with no cut, next to the shipped gates of its kinds.

The re-check was not blind. The draw printed the current kinds before I read the concepts, and I wrote the gates.

**Result.** 11 of the 20 are unchanged. 5 change firmly, 3 probably and 1 is uncertain: 25 to 45% change, with a 95% interval of about 11% to 66%. The primary kind changes in 2 or 3 of the 20.

The next table lists the nine that change or may change, with the gate clause that changes each.

| Theme | Now | Under the shipped gates | Gate clause |
|---|---|---|---|
| nbaspurs t06 | T3-095, T3-032 | T3-001 alone | A member staged the fake in t05. T3-095's gate sends a room's own fake and the readers it caught to T3-001. T3-032 needs three objecting concepts; this theme has two. |
| bulgaria t01 | T3-021, T3-084, T3-141 | T3-005 primary | Alarms and calls to defend lead, four concepts against one concept of upkeep. |
| dallasstars t09 | T3-002, T3-017 | T3-017 dropped | T3-017 needs three concepts of usual talk; there is one. |
| starlightstage t09 | T3-004, T3-136 | T3-020 added | Three concepts weigh where to go: below vim, not near flags, not in corners. |
| flyers t03 | T3-006, T3-086 | T3-068 added | About five concepts take over rival logos to make the room's own. This line was written only at B1e. |
| belgium t12 (probable) | T3-028, T3-054 | T3-120 primary | One concept asks for 300 accounts for a script; another hands members another room's script. |
| floridagators t01 (probable) | T3-033, T3-020, T3-037 | T3-037 likely dropped | One of its two concepts is a proposal; the other is a joke about buying a billboard. |
| buffalowizards t05 (probable) | T3-022, T3-009, T3-031 | T3-009 does not fit | The concept cheers a return during the event, not a finished work. |
| sadboys t04 (uncertain) | T3-035, T3-150 | T3-150 in doubt | The shipped gate asks for an alliance "for defence or a fight"; the concept declares solidarity. |

The changes come from four sources:
- the three-concept bars written into the T3-032 and T3-017 gates;
- the "room's own fake" rule for April Fools;
- the "which act leads" rule for defending against repairing;
- a line written only at B1e (T3-068 against T3-006).

Scaled up, that is about 950 to 1,700 of the 3,796 themes, and 380 to 570 primaries. I did not sample the 3,977 single-placed themes. The B3 fleet places from the gates, so this weakens B1's own figures, F-001 included, more than the shipped scheme.

## 3. The 100-character cut

**What I checked:**
- **The read log.** `_mem_reads-B1.jsonl` logs each mem.py call, not the shell pipe after it. The only `cut` in out/ is the A1 reader's own script, `read_room.sh`. The notes record one truncated display, at B1b-19: an episode quote (E229) that was turned into a paraphrase.
- **What the cut removes.** In a concept line the label starts at about column 80. A cut at 100 leaves about 21 characters of the label and none of the participants' words.
- **Page cuts are ruled out.** Every room had its concepts served before its first placement. In the first pass, 7,773 of the 7,786 placed themes were read one theme at a time, and the log's own totals show every line of those reads was served. Two room-level `codes` reads (smite, rhythmheaven) stopped at 80 lines, but their themes were also read one by one.
- **An indirect test** (`iv_q3_beyond100.py`). It asks whether a rule 0 line's reason uses a word found only past column 100 of a concept it cites. 4,649 of 5,754 lines (81%) do. With the cited concepts swapped for another room's, 4% do, which is the chance level. No leg with more than ten lines falls below 55%.

**Answer.** I cannot name the truncated reads from this copy. The transcripts can, and they are closed to me until stage E1. Most second and third placements were written by someone who saw past column 100. Primary placements have no reason text, so the test cannot reach them, and those are the ones that could rest on a truncated line.

**How to find them:**
1. In the transcripts, list every command that piped `mem.py theme`, `codes` or `room` through `cut -c1-N` with N under about 140.
2. Match each command to its line in `_mem_reads-B1.jsonl`.
3. Join with the place events in `kinds-B1.jsonl`. A placement is at risk when every read of its theme before it was cut.
4. Reread those themes in full under the gates, as in question 2, and count the changes.

## 4. Truces, alliances, bartering and border deals

**What I checked** (`iv_q4_deals.py`):
- 74% of the 444 border-deal themes hold none of the other three kinds. Truces (94 themes), alliances (134) and bartering (170) sit alone 49%, 51% and 49% of the time.
- Of the 674 themes holding any of the four, 147 (22%) hold two or more.
- The overflow lines show more: 151 keep border deals and name truces, 122 name alliances and 114 name bartering.

**The strongest case for one kind.** The rooms make these deals in one negotiation. What separates the four is what is traded: space, peace, defence or help. That is the content of one doing. The three-kind cap now drops them, as question 6 shows. A reader holding family G14 alone sees the other kinds only through discriminators.

**The strongest case against.** About half of each kind sits apart, in 46 to 315 rooms. Readers can tell what each one commits a room to:
- a border deal divides space;
- a truce ends a fight already begun;
- an alliance promises defence against third rooms;
- a barter swaps help case by case.

Those differences bear on the theory question of which forms keep the work alive. An alliance brings defenders to a raid; a border avoids one. Merging later is arithmetic; splitting later means rereading about 840 members.

**My choice.** Keep the four kinds. Put border deals and the G13 and G15 deal kinds on one index page, and write the shared deal variation into each gate.

**What would reverse it at B2.** On themes B1 placed on exactly one of the four, fresh readers might agree it is a deal above 85% of the time but agree on which one below 60%. Then merge. Above 75% agreement on which one, keep the four. In between, rewrite the gates and test again.

## 5. T3-005 against T3-021

**The gates contradict each other.** T3-005's must-not-show line gives T3-021 repair "with no attacker in view". T3-005's own discriminator gives T3-021 repair "with or without an attacker in view". Repair during a raid falls on both sides.

**The theme to put before a fresh reader: vegan t08**, "defending vegan signs from repeated overwriting" (47 concepts). It sits right on that case:
- alarms against a named attacker: "We're under attack by evil Mona Lisa";
- repair beside the fight: "I'm working on saving it!" and "I'm still trying to keep the old one alive".

B1 placed it on T3-005 alone, and I hesitated over T3-021 in the stranger test. bulgaria t01 flips on this line in the question 2 sample.

**When I would merge.** First fix the contradiction: repair during a raid goes by whichever act its concepts lead with. Then test on themes B1 placed on only one of the two:
- disagreement above one third (chance-corrected agreement below 0.4): merge;
- disagreement below 15%: keep;
- in between: draw the line at the concept (alarm, call or counter-attack against fixing pixels) and test again.

## 6. The unplaced themes and the episode leftovers

**The 58 unplaced themes.** Nearly all are records whose content is gone: deleted bodies, bare titles, link-only posts, one-word replies. They hold no kind the scheme misses. A few are traces of organising whose words were deleted:
- a strawpoll link with no question (ssbpm t09);
- "Help needed" (python t09);
- a named operation (malta t08);
- a request to Purple Pixels (PurplePixels t13).

They measure how much organising the deletions hid. That belongs with the prior's "deliberation off the record", not with a new kind.

**The episode lines.** My "107 episode lines" was wrong. The B1b-30 count was 107 (line, kind) pairs. Today it is 106 pairs over 81 lines. In 61 of those 81 lines, a room's overflow record names every missing kind: the room did it, and the three-kind cap dropped it. The missing kinds are mostly deals: truces in 18 lines, alliances in 11, help in 9 and yielding space in 7.

So the scheme has the kinds, but the placements lose deals between rooms. For some truces and alliances, the episode file is the only record. Those relations are what stages C and D must compose.

## 7. What B2 readers should see, and what would bias them

**What I did not have:** gates while placing, a second reader, a blind read, and placement concept by concept.

**B2 readers should see:**
- the index page, so they can find kinds outside their family;
- their family's full tests, with the deal kinds on one page;
- the theme's concepts with the participants' words in full;
- in one test arm, no coder label or note, to measure the framing effect from question 1.

**They should not see** my placements, my rule 0 lines or my counts.

**What would bias them:**
- **Exemplars** anchor readers on surface words: after seeing "under attack" quotes, a reader sends every alarm to T3-005. Keep them withheld, as the packet script does by default.
- **Families** narrow the search: a reader holding G14 will file truces under border deals.
- **Confusion pairs**, if shown, turn B2 into a test of my discriminators. Use them to score and to pick items, not as reading.
- **My hard set** reflects my own expectations, so draw part of the items at random.

## Corrections to my B1e record

These sit in the run's files. Nothing in this copy changes them.
- The grain claim in F-001 and in my final message is wrong. Across rooms, a room's grain predicts nothing; within a room, theme size does. F-001 needs a superseding line.
- "107 episode lines" in the head, handback and notes should read "106 unplaced (line, kind) pairs over 81 lines".
- The T3-005 and T3-021 gates contradict each other on repair during a raid.
- F-001's 51.1% rests on placements the shipped gates would partly redo: 25 to 45% of multiply placed themes in the sample.
