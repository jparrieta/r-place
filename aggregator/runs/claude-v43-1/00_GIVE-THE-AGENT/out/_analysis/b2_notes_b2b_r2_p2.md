
## Leg B2b-r2-p2, check round 2, 2026-10-12

### QB2-005 and QB2-006, revisited

Both were applied at B2b-r2. The failed first dispatch is at `out/_analysis/fleet_B2_round2_failed/`, and it is never scored. No work of this leg rested on either assumption.

### Rounds 1 and 2 had different readers (J, 2026-10-12 07:34 Berlin)

- **Round 1:** deepseek/deepseek-v4-flash-0731, through `@preset/cheap`, at high reasoning effort on mixed providers.
- **Round 2:** deepseek/deepseek-v4.1-flash, called directly, at medium reasoning effort, with max_tokens 128,000.

J's reading: the preset refused even a 32-token probe with HTTP 400. So the part-6 failures of the first dispatch were most likely the preset or its provider pin, not the context window (OpenRouter lists V4.1 Flash at 1,048,576 tokens). The same readers serve B3 and B4. Every change from round 1 to round 2 below is partly a change of readers, not only of the scheme.

### The dispatch, in `fleet.py`'s counts

`_fleet_raw/B2/round-2/DONE` and `log.jsonl` record 5 packets, each sent to 3 fresh readers (15 readers, r1 to r3 inside each packet folder). There were 15 valid returns, 0 exhausted and 0 reissues. Calls took 67.6 to 235.7 seconds each. The round used 751,923 input and 489,651 output tokens, at a cost of 0.598 USD. All 150 lines came back.

One line mistyped its heading. In `P03-r2-5/r2`, position 7 returned AyyMD t02, where the packet holds AyyMD t08. Its concepts (c0037, c0041) are t08's, so it is scored as t08 by position.

### Round 2's three numbers

`out/_analysis/b2_score_r2.py` scores the round by the declared definitions, reusing `b2_score.py`'s Jaccard and alpha. `out/_analysis/b2_rechecked.py` builds the rechecked placements: each item's latest recheck, which moves 19 hard items. The next table gives the figures for the whole set and for its two parts.

| set | fidelity | primary match | fidelity vs rechecked | pairwise | primary pairwise | alpha |
|---|---|---|---|---|---|---|
| all 50 (the hard set) | 0.639 | 0.747 | 0.701 | 0.718 | 0.833 | 0.710 |
| the 40 round-1 items | 0.572 | 0.683 | 0.648 | 0.685 | 0.792 | 0.676 |
| the ten biggest bags | 0.911 | 1.000 | 0.911 | 0.850 | 1.000 | |

Round 1, on its 40 items, scored fidelity 0.594, pairwise 0.733 and alpha 0.726. On the same 40 items round 2 is lower on all three. 27 of 50 items have two readers differing; 24 of them are round-1 items.

The largest change is in how many themes a reader places. Round 2's readers placed more than one theme on 47 of 150 lines; round 1's placed more than one on 10 of 120. Most of round 2's divisions are a second or third theme added by one or two readers. Each comes with a `why_not_one` that reads "carry" as "cover every concept". Rule 0's words are the contract's and stay. The rate of second placements is a property of the reader model, and B3, which uses these readers, should expect it.

What these figures license, in FLEET.md's words: they support the claim "what you would have produced at a scale one analyst cannot reach". They do not support "what any competent reader would have produced".

**The ten biggest bags.** All 30 lines put my placed theme first (primary 1.000). Readers marked the six bags as bags on 11 of 18 lines. They also marked bags I did not: ainbowroad t11, dota2 t05, leagueoflegends t02 and theblackvoid t09 each drew one or two bag lines. `also_present` diverges widely. The themes a reader names, placed and also present, score a mean Jaccard of 0.283 against mine. On 2007scape t04 one reader named 85 themes (the other two 29 and 16). On sweden t01 the three named 34, 35 and 25; I named 5. QB2-008 asks J for a concept floor.

### The verdicts

The next table gives one verdict for each item that divided readers, and for each where all three readers left my placement. Stage B4's taxonomy names the kinds. "Rechecked" means my placement after round 1's rechecks.

| item | readers | verdict |
|---|---|---|
| guatemala t02 | all three T3-002, T3-167, T3-026; none T3-065 | scheme-ambiguous: the concepts say only "a flag" in r/guatemala, and two readers never opened G17. Edits 287, 290, 293, 294 |
| nVade t04 | T3-195, T3-195, T3-005 | scheme-ambiguous: a pledge honoured by defending had no T3-195 question against T3-011 or T3-005. Edits 288, 289, 295 |
| n64 t02 | T3-033+T3-002, T3-033+T3-038, T3-038 | scheme-ambiguous: no question between T3-033 and T3-038. Edits 291, 292 |
| dofus t01 | T3-033 in all three, seconds T3-092, T3-038 | the same pair; edits 291, 292 |
| AyyMD t08 | T3-001, T3-023, T3-023 | author-error: the moderator's takeover and CSS change (c0041, c0042) make it T3-023, as T3-023's question asks |
| nyu t01 | T3-070, T3-070, T3-004+T3-020 | author-error: coordinates, a moved spot and a template handed out are T3-070 |
| cubers t12 | T3-038, T3-044+T3-005, T3-044+T3-005+T3-021 | author-error: the tag is made to send lost cubers to the sub (c0075), so T3-044, not T3-169 |
| harrypotter t08 | T3-159, T3-031, T3-017+T3-159 | author-error: house points awarded for r/place work are a reward to helpers (T3-159) |
| farmcarrots t15 | T3-031 in all three, T3-050 in two | author-error: the room's carrot-joke replies lead; the taunt is the provocation |
| parabola t02 | T3-010 in all three, T3-150 in two | author-error: the border settled leads; my single T3-150 missed it |
| redhotchilipeppers t09 | T3-009, T3-009+T3-072+T3-073, T3-009 | author-error on my second theme, T3-043, which the readers do not need; T3-009 is primary in all three |
| Slovakia t07 | T3-065+T3-024, T3-024+T3-060, T3-024 | primary T3-024 matches all three; my second, T3-079, was drawn by none: author-error (Slovak hearts in the placehearts grid join no flags) |
| kpop t04 | all three T3-033, T3-066, T3-136 | genuine-joint: three readers agree on three themes; the vote proposal (c0024) and the turnout doubt have concepts of their own |
| floridagators t09 | T3-014+T3-152 in all three, T3-153 in two | genuine-joint: my original pair, plus the alliance meeting in the chat (c0124) |
| 4chan t07 | T3-010 in all three, T3-149 in two | genuine-joint: peace asked of the blue box (c0136, c0143) |
| anarcho_capitalism t12 | T3-149 and T3-010 in two, T3-149 alone in one | genuine-joint, as I placed it; one reader's T3-153 is a reader-error |
| simonfraser t08 | T3-084, T3-011+T3-084, T3-011+T3-084+T3-170 | genuine-joint: help sent (c0029, c0043) beside help asked |
| korea t15 | T3-015 in all three, T3-075 in one | genuine-joint by one reader, my original second |
| Goodboye t03, acecombat t05 | divided across T3-084, T3-151, T3-011; T3-010, T3-014, T3-062 | item-is-a-bag, as at round 1 |
| flashtv t13 | T3-009, T3-073, T3-073+T3-009 | two readers hold my rechecked T3-073; round 1's question holds; reader-error for the third |
| drumcorps t07, furry t10, placestart t15, stardustcrusaders t19, orderofthebluecorner t08 | one reader adds themes; the others hold my rechecked placement | reader-error: unneeded second placements |
| dota2 t05, leagueoflegends t02, theblackvoid t12 | all hold my primary; one or two add the themes I left in `why` | reader-error by rule 0, read strictly |

GreenCorner t03, WisconsinBadgers t04, england t03, megaman t11 and signal t01 are unanimous. Each falls on my rechecked placement: round 1's author-error verdicts, confirmed by new readers. There are eight author-error verdicts this round: AyyMD t08, nyu t01, cubers t12, harrypotter t08, farmcarrots t15, parabola t02, redhotchilipeppers t09 and Slovakia t07. They change no sentence, so they are listed here and not in `scheme_edits.jsonl`. `author_items.jsonl` stays as written.

### The edits

`out/_analysis/b2_edits_r2.py` wrote `scheme_edits.jsonl` lines 287 to 295, all scheme-ambiguous, with tier_history lines 373 to 381. They change 9 fields over 8 themes:
- T3-065's gloss now says a flag built in a room named for a land is that land's flag, unless its concepts name another.
- The T3-002/T3-065 and T3-026/T3-065 questions say so in both gates.
- A new T3-033/T3-038 question asks whether an idea is offered or a mark placed and reported. For a proposal followed by its placing, the side with more concepts is primary.
- New T3-195/T3-011 and T3-195/T3-005 questions ask whether an agreement is invoked, or the work helped or defended with the pledge only the reason.

No edit narrows a theme. `b1e_assemble.py --write` rebuilt `scheme.jsonl`, `families.jsonl` and `scheme.md`. `mem.py gates` finds no defect.

**The rechecks.** The nine edits owed 133 records over 59 items in the hard and gold sets. `out/_analysis/b2_rechecks_r2b.py` read each against its edit's sentence; none moves. `rechecks-B2.jsonl` holds 887 records, and none is owed.

**The gates.** I read ten pairs and confirmed them (`out/_analysis/b2_confirm_r2.json`): the five new or reworded pairs, and five whose confirmation the edits had made stale. 31 pairs are confirmed, 0 are stale and 464 are unconfirmed.

### Section 4

Round 2's packets hold 3 to 15 items, so round 1's curve (first ten items against last ten) cannot be drawn. Within the four packets of 9 or more items, I compared each reader's first half with its last half. The arguable rate falls in 8 of 12 readers and rises in 3. Agreement with the other two falls in 9 and rises in 2. The curve shows no sign that agreement grows with position. The B3 batch cap stays as declared: 40 items, the first 10 a warm-up block.

### Stopping (QB2-007)

Section 5 stops the rounds when pairwise agreement on the hard set clears the threshold. Round 2's figure on the 50-item hard set is 0.718, above 0.70. The PI's round-2 rule holds: the ten biggest bags have now been read once. But the 40 items both rounds share fell from 0.733 to 0.685, with new readers, and the ten bags lift the whole. QB2-007 asks J whether the rounds stop and the scheme freezes, or round 3 opens. Meanwhile the rounds stop under the declared rule, with the 40-item figure reported beside it. This leg does not freeze: the freeze needs the 464 unconfirmed pairs read and the decide_when_both clusters checked. The leg closes with `done.sh B2`.

**Questions open:** QB2-007 (stopping), QB2-008 (a floor for `also_present`).
