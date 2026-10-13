# Notes, stage C1: structuring

Opened at C1a-01, 2026-10-13. Stage B is closed and frozen. The scheme readers held is `scheme_final.jsonl` (197 themes); the settled line is `assign_final.jsonl` at sha256 d3506a88…. Nothing in stage B's files is edited here. Every change lands in this stage's own files: `assignments_final.jsonl` with its overlay, then `scheme_v2`, `tier_history.jsonl` and the rest.

## J's rulings for stage C1 (20:16 Berlin, through the PI's message of 18:17Z)

J read my B4c interview answers and said "go ahead" on three proposals:
1. **Class 2.** The readers' list stands as the placement. The B1 themes no reader placed are kept as a flagged record beside it, not as placements. Where a flagged theme's concepts support it, I may promote it in C1 as one of my re-placements, logged as such.
2. **The re-reads.** In this first pass, re-read the five class 4 items where six readers converge against a re-rule resting on the earlier reading (chicago t01, armok t04, dmt t03, germany t08, smashbros t01), then the class 4 unresolved rulings that rest on that same sentence.
3. **No fleet re-read of class 2 now.** Fresh readers test the revised scheme after C1.

My B4 defect list, the G14 proposals from the interview, and the questions on bare event titles and on whose act a visitor's words count for are mine to work through in C1. J's other rulings stand.

**What the interview held** (the PI's note of 18:17Z; the interview ran in a copy of the leg, so its answers reached this conversation only through that note):
- **Class 2.** 32 of 53 sampled class 2 items keep a B1 theme no reader placed or listed; by estimate about 60% of the 1,990.
- **The 25 unanimous items the fleet got wrong.** In 18 of them, three or four fresh readings follow the deciding sentence.
- **The gap in the uniform stratum.** Most of it is class 2's settled line (+0.064) and the fresh readers' own disagreement on contested items (+0.067).
- **The G14 proposals.** Narrow T3-010's `must_show`. Rewrite the T3-010/T3-149 and T3-084/T3-062 discriminators to name visible evidence. Add a T3-010/T3-011 discriminator and a family `decide_when_both`. No split.
- **Two questions.** A bare mention of the event needs a defined outcome. Whether a visitor's act in a room's thread counts for that room is the same gap as T3-052's "whose picture".
- **The re-read order I proposed.** The five, then the rulings resting on "the earlier reading", then AcePlace t13, then the 18 items where one B3 reader and all four fresh readings agree.

## The passes

**Pass 1 (C1a-01)** does four things and changes no gate and no theme:
- reads the record of section 1: `scheme_edits.jsonl`, the pair table, and transmission's second and fourth rows;
- writes `assignments_final.jsonl` from `assign_final.jsonl` with J's class 2 ruling applied;
- re-reads the class 4 rulings that rest on "the earlier reading", the five first;
- declares the stopping criterion before any recut.

**The later passes** hold the rest of the stage:
- the four weak sources and the themes in three of them;
- the gate amendments from the defect list and the G14 proposals, with their rechecks;
- the revision rate;
- the pair test;
- the empties and the arguables;
- the form pass;
- the fourth-order themes;
- `scheme_v2` and the handback.

## How `scheme_edits.jsonl` is read

The file has 306 lines. Each line carries the whole field twice, as it was and as it is now. `out/_analysis/c1_edits_render.py` prints each line once: its number, round, leg, theme, field, kind and the items that caused it; the sentence added or the field as it now reads; and its reason. Every line is read. Only the duplicated "was" copy is left out, and the render says where a line has no `added` part.

## Class 2: J's ruling applied, declared before the write

`out/_analysis/c1_assignments_init.py` writes `assignments_final.jsonl` from `assign_final.jsonl`. Every line is carried through verbatim except the 1,990 class 2 lines (`source: "b1_grouping_kept"`). For each of those:
- `third_order` becomes the two B3 readers' list, from `b3_classes.jsonl`; for class 2 the two readers' lists are equal.
- `support_by_theme` stays as it is. It already holds the concepts behind the readers' themes, and the script stops if its keys are not the readers' list.
- `also_present` stays as it is.
- `b1_themes_without_reader_support` stays, as the flagged record J ruled.
- `source` becomes "readers".
- A `moves` entry records the move as `mem.py reassign` records one: from, to, stage C1, leg, time, the ruling as its why, and the concepts.
- Each changed line goes into `assign_revisions_only.jsonl`, and the line count into `assignments_final.count.txt`.
- One diary line records the application, with the record file `out/_analysis/c1_class2.json`, and a snap follows. J's batching rule (B1b-29) is why this is not 1,990 calls of `mem.py reassign`.
- No flagged theme is promoted in this pass. A promotion comes only after the item is read, as a logged re-placement with the concepts named.

## The re-reads, declared before the first

- **The list.** `out/_analysis/c1_earlier_reading.py` lists the rulings whose why rests on "the earlier reading": 30, all class 4 and all unresolved, the five J named among them. In each, the B4a-06 re-rule left my B1 theme out under the three-concept floor. It then took the readers' theme to carry no concept "by the earlier reading", without reading the item again.
- **How each item is read.** Whole, through `mem.py theme`, against `scheme_final.jsonl`'s fields; no gate is amended in this pass. J's rulings of 13 October still bind. The ruling chooses among the readers' list and my B1 grouping and adds no theme beyond them. A lone B1 theme in class 4 stands only with three concepts or more of its own. The readers' list stands where its `must_show` takes concepts and no field sends them elsewhere. Where nothing takes the material, the item stays unresolved.
- **The fresh readings** from B4c are shown with each item. Where they bear on the reading, the reason names them. They do not decide.
- **The record.** Each item placed is moved with `mem.py reassign`, with its concepts and the deciding clause. Each item kept unresolved is recorded with its reason. All 30 go into `out/_analysis/c1_reread-01.jsonl`.

## The stopping criterion, declared before the first recut

I stop recutting the third-order tier when two conditions hold:
- Every source line has a recorded decision: revise, leave, or carry with its reason. The sources are the lines of `scheme_edits.jsonl`, the recurring pairs of the pair table, transmission's second and fourth rows, the stage B4 defect list, the G14 proposals, and the themes that appear in three of the four weak sources.
- The last pass amended no gate whose rechecks moved more than one placement in ten of its sample.

I would prefer a later cut to this one only on two grounds:
- it decides a recorded source line this cut leaves undecided, without making two gates contradict each other (`mem.py gates` clean on the themes it touches);
- or it moves a boundary that split the readers both at B2 and again at B3 or B4 toward a merge or the rare tier, rather than adding a third sentence.

A cut is never preferred for moving the arithmetic of any figure, which rule 7 keeps shut.

## Pass 1 (C1a-01): the record

### The sources read

- **`scheme_edits.jsonl`, all 306 lines.** Round 1 (286 lines, B2b-r1) is mostly gate checks, discriminators copied so a pair asks the same question both ways, and questions written where a `must_not_show` named a theme with no discriminator against it. Round 2 (9 lines) and round 3 (11, made at the freeze under QB2-012) carry the substantive changes. Several boundaries moved at B2 and split readers again at B3 or B4. By section 1 they are candidates for a merge or the rare tier rather than a third sentence:
  - T3-005 against T3-021 (edits 21 and 46);
  - T3-009 against T3-043 (22 and 60);
  - the homeland flag, T3-065 against T3-026 and T3-002 (47, 72, 73, 287, 290, 293, 294);
  - the call, offer and build cluster, T3-002, T3-033 and T3-038 (291, 292, 296 to 301);
  - T3-038 against T3-070 (301 to 304);
  - T3-010 against seven G14 and G13 siblings (273 to 286).
- **The pair table** (`multiplacement_register-B3.md`): 20 recurring pairs, led by T3-009|T3-043 (114) and T3-005|T3-021 (114, and 59 the other way). Two themes are modifier candidates for folding: T3-089, placed as an addition 30 times and as a primary 6 times, and T3-152, 41 and 15.
- **Transmission's rows** (`transmission-B4.md`).
  - Row 2 holds one item, mariokart t04 (G14), which is to be revised.
  - Row 4 holds 20 items. In 11 I was wrong; these are recorded, and no wording is moved toward my answer. In 9 the scheme taught something unintended; their wording is mine to fix. In four of the nine (alberta t04, finland t06, korea t15, mit t01), a `decide_when_both` told readers to add a second theme "under rule 0" and they did not.
  - Row 3 (18 items) is kept as a finding.

### Class 2, applied

`out/_analysis/c1_assignments_init.py --write` wrote `assignments_final.jsonl` (7,844 lines) from `assign_final.jsonl`.
- **The class 2 lines.** All 1,990 now place the two B3 readers' list, with `source: "readers"`. The flagged record `b1_themes_without_reader_support` holds 2,814 B1 themes: 1,166 lines flag one and 824 flag two. Each line carries a `moves` entry with its concepts.
- **The checks.** Every check held on every line: the two readers' lists equal, the support keys equal to the readers' list, and the flagged themes equal to the record.
- **The other files.** `assign_revisions_only.jsonl` and `assignments_final.count.txt` (7,844) were written with it. The snap is `C1-class2-readers-list`.
- **No promotion yet.** No flagged theme was promoted in this pass.

### The re-reads (J's ruling 2)

All 30 class 4 rulings resting on "the earlier reading" were read again (`out/_analysis/c1_reread/`, the decisions in `out/_analysis/c1_reread-01.jsonl`).
- **Placed: 10.** chicago t01 on T3-002, armok t04 on T3-017, dmt t03 on T3-014 (arguable), smashbros t01 on T3-023, ireland t12 on T3-002, kingdomhearts t21 on T3-041 (arguable), kuwait t08 on T3-074 (arguable), lakers t16 on T3-035, sonicthehedgehog t07 on T3-022 (arguable), and survivor t28 on T3-023 (arguable). Each was moved with `mem.py reassign`, with its concepts and the deciding clause.
- **Unresolved on a fresh read: 15.** In each, the readers' theme fails its own gate on these words, and my B1 themes are under the three-concept floor or absent.
- **Held for a C1 rule: 5.** Four wait for the visitor rule: germany t08, germany t19, monalisaclan t12 and suomi t26. In each, another room's act or mark is spoken in this room's thread. canucks t25 waits for the T3-095 gate, whose `must_show` lacks the April Fools condition its name and family carry.
- **The five J named.** Four are placed where all six readers converged. germany t08 is held, because the restraint the readers placed is r/ainbowroad's, not r/germany's.
- **The floor.** In three of the 15, my B1 theme's gate takes the concepts and fresh readers place it, but the lone-B1 floor keeps it out: azerbaijan t02 (T3-043), livecounting t06 (T3-017) and monstercat t14 (T3-125). The floor is my own choice under J's answer of 12:28 and goes to review in a later pass.
- **The result.** `out/_analysis/c1_assign_check.py`: 2,000 lines moved against the settled line, every one in the overlay; every C1 move names its concepts; empties 175, down from 185.

### What I doubt

- **survivor t28** is placed on T3-023 by T3-017's own `decide_when_both`. The B4 ruling on python t04, a similar item, went to T3-017, so one of the two readings is inconsistent with the other. The gate pass decides which.
- **dmt t03 against shield t06.** dmt t03 is placed on T3-014 and shield t06 kept unresolved. The difference rests on whose work a named sub's Discord serves, which the frozen gate states only as "named for the room's canvas work". The visitor rule should settle both.
- **The fresh readings.** The re-reads saw them with their reasons. I gave them no weight in the decision, but having them in view is not blindness.

### Slips

- A command using a jq `test()` regex was refused, as the head's rules say it will be. A script replaced it.
- The last page of the scheme edits overflowed the screen. It was read again in smaller pages, and no line was skipped.

`validate.py C1`, at pass 1's close:

```
stage C1:
  assignments_final 7844 lines = assignment_items_expected
  revised lines 2000 of 7844 (moved placements 2000)
  empties 175 of 7844
  a pass closed; the full set (scheme v2, assignments, the fourth-order themes, the form pass) is owed at the last pass, with the handback

0 errors (0 distinct shapes), 0 warnings
```

## Pass 2 (C1a-02)

### Declared before counting or amending

- **The four weak sources (section 1).** A theme appears in a source as follows. Each count is reported beside the yes or no, and a theme that appears in three or four sources is listed as one not to defend.
  - `disagreements.jsonl`: the theme is the `theme` of at least one scheme-ambiguous ruling, the sentence that failed to decide.
  - `reassign.jsonl` (arm 1, DeepSeek): on at least one disagrees-contested reading, the theme is in the settled set and missing from the fresh set, or in the fresh set and missing from the settled set. Arm 2's file (`reassign-openai-astra.jsonl`) is counted the same way and reported beside it, never pooled.
  - `coder_conflicts.jsonl`: the theme is in a pair the conflict "may explain".
  - Transmission's fourth row: the theme is in my set or the readers' set on one of its 20 items.
  - The script is `out/_analysis/c1_weak_sources.py`, and its counts are recorded in `out/_analysis/c1_weak_sources.json`.
- **Placements after a gate amendment.** A recheck places the item by the amended gates, over the whole scheme. The stage gives every C1 re-placement to me: "apply the amended rule, yourself, never a reader". J's rulings of 13 October govern how a B4 ruling is made: choose among the readers' and my B1 placements, and keep a lone B1 theme only at three concepts. They bound the re-reads of B4 rulings (pass 1) and do not bound a recheck under an amended gate. This is my reading. It goes to J as a question, and I work on it meanwhile.
- **The visitor rule (the question J left to me), as a reading rule of the scheme.** It is written into `scheme_v2.md`'s gate block and carried into the gates whose words trip on it.
  - A theme names an act in the record of the room whose threads hold the words. Where a gate says "the room", it means that room.
  - Another room's act, spoken or reported in those threads, is placed by what it is for this room: a request it receives, a neighbour's work remarked on, an argument about covering. It is never placed as this room's own act.
- **A bare mention of the event (the other question).** A second-order theme whose concepts only name the event ("r/place" as a title, a bare link) holds no act. The scheme places acts, so such an item stays unplaced. It is recorded as the empties' kind "a bare mention of the event, no act" (section 6). That is its defined outcome, and no theme is made for it.

### How a recheck is read (written at gate:2, after gate:1's rechecks)

A recheck asks one question: does the amended sentence move this placement? I place the item under the scheme with the amended sentence and again with the old one. The item moves when the two answers differ and the current line follows the old answer. An item whose line differs from both answers is not moved by the recheck. Such a line is a reader's or a ruling's choice that the amendment did not touch. I list it for later review (the revision rate, or the promotion of flagged class 2 records). Without this rule, the moved share would count disagreements the amendment did not cause, and section 4's one-in-ten escalation would answer a question the amendment did not ask. Gate:1's two moves meet this rule: in both items the T3-095 concepts fail only the new April Fools condition.

### The gate amendments

- **gate:1, T3-095 `must_show`.** Added the April Fools condition: "The question asked must be whether it is an April Fools joke; a claim doubted for any other reason, such as a warning of an attack or a rumour of a plan, does not belong here." Source: the B4 scheme-ambiguous ruling on canucks t25 (held at C1a-01); T3-095 is in all four weak sources. It had 102 candidates, 30 owed by seeded sample, and 2 moved, so it did not escalate:
  - hawks t07 moved from T3-095 and T3-023 to T3-023. Members ask the context of a bread image inside the moderators' Breadman change.
  - samuraijack t07 moved from T3-095 to T3-048. Members ask whether the episode still airs after Adult Swim's April Fools Rick and Morty loop.
- **gates 2 to 4, the T3-095 | T3-023 line.** After gate:1, three sentences contradicted it: T3-095's discriminator against T3-023, T3-023's discriminator against T3-095, and T3-023's `decide_when_both`. All three sent "working out what the change is" to T3-095. The new wording sends working out whether the change is real or an April Fools joke to T3-095, and asking what the change shows to T3-023. Words were replaced and no sentence was added. Candidates were 986, 848 and 443, with 30 owed for each gate and 0 moved. cfb t04 and naruto t02 show the line: members ask what their hidden flairs or the sub's picture are. The old wording would have added T3-095. Their lines already follow the new wording.
- **Listed for review, not moved by a recheck:**
  - brasil t01 and hearthstone t08 (gate:3);
  - europe t14, kingdomhearts t03 and formula1 t02 (gate:4);
  - taiwan t01 (gate:2), a two-against-two tie.
  europe t14 and kingdomhearts t03 hold T3-095 as a flagged class 2 record whose concepts would carry it.
- **Gate pairs confirmed after reading:** T3-095 with T3-001, T3-016, T3-023 and T3-048; T3-023 with T3-001, T3-032, T3-048, T3-063, T3-064, T3-093, T3-097, T3-100, T3-133 and T3-185.
- **gates 5 to 7, the visitor rule in three `must_show` sentences.** Each replaces words and adds no sentence. The three wordings sent another room's request, arriving in a room's threads, to the asking side's theme:
  - both B3 readers placed monalisaclan t12 on T3-011;
  - both B3 readers and five fresh readers placed suomi t26 on T3-062.
  The three amendments:
  - **gate:5, T3-084.** A request for help between canvas rooms counts in the record of either room: the asking room's own, or another room's request or call for hands as it arrives, addressed to the room as a group or to its members. T3-084 already held such arrivals (egypt t04, kuwait t05, Northwestern t04). 56 candidates, 30 owed, 0 moved.
  - **gate:6, T3-011.** "Or called to" became "or called to it by the room's own members". 124 candidates. 5 of the first 30 moved, so all 124 were owed, and 35 moved.
  - **gate:7, T3-062.** "The room's call" became "the room's own call for hands, made by its members". 44 candidates, 30 owed, 1 moved (osu t05).
  Every move is an arriving request that leaves T3-011 or T3-062 for T3-084. Rule 0 then places T3-084 as a second or third theme, or first where arrivals outnumber the room's own help: kanye t17, suomi t28, afip t07, chicago t09, msu t05, fullcommunism t05, puzzleanddragons t04. Two placements lose T3-011 altogether:
  - in chicago t09, one concept is left and it loses its level to T3-041 on placements;
  - in utahjazz t08 and mylittlepony t06, it falls to fourth.
  All 36 were moved with `mem.py reassign`, by `out/_analysis/c1_reassign_from_rechecks.py`, which reuses each recheck's own themes, concepts and reason.
- **Gate pairs confirmed after reading:** T3-084 with 7 themes, T3-011 with 12, T3-062 with 9. Two pairs agree only under the visitor rule:
  - T3-084 | T3-062. The discriminator speaks from the asking room's side, and in a receiving room only T3-084's `must_show` takes an arriving call.
  - T3-084 | T3-002. A visitor's call to the room's members is the request the room receives, not the room's own call.
  T3-002's discriminator is a watch item for the fresh readers after C1.
- **The visitor rule's wider reach, found by the rechecks.** 23 rechecked items hold, under T3-011 or T3-062, another room's help given to this room: offers, pixels, a sticky. Examples are nyjets t11, naruto t04, wildhockey t04, twice t15, snsd t03 and the_pack t06; the full list is in `out/_analysis/c1_guard.json`. Under the old wording and the new alike, such help is not this room's act, so the rechecks did not move these items. The scheme has no theme for help a room receives. This is owed: a sweep of G14 placements for other rooms' acts, and a decision whether the corpus carries "help received" as a kind (a theme, the rare tier, or the empties). My diary line put the count at 25; the script counts 23.

### The held re-reads, decided under the amended gates

These are re-reads of B4 rulings, so J's 13 October rulings apply: choose among the readers' placements and my B1, and a lone B1 theme needs three concepts.
- **canucks t25 stays unresolved.** Both readers placed T3-095. A warning of a canvas takeover found to be "not kidding" fails T3-095's April Fools condition. My B1's T3-005 has two concepts.
- **monalisaclan t12 and suomi t26 stay unresolved.** The readers placed T3-011 and T3-062, and the visitor rule excludes them. My B1's T3-084 now fits, under gate:5's wording. It holds two concepts in monalisaclan t12 and one in suomi t26, below the lone-B1 floor.
- **germany t08 stays unresolved.** The readers placed T3-024. The restraint stated is r/ainbowroad's, spoken in r/germany's thread. For r/germany it is another room's argument about covering. My B1's T3-046 fits, but on one concept.
- **germany t19 stays unresolved.** The readers placed T3-038. "Finnish flag almost complete" is not r/germany's mark. My B1's T3-052 needs a picture next to the room's mark, and nothing shows the Finnish flag is one.
- **The lone-B1 floor now keeps a fitting theme out of six items:** azerbaijan t02, livecounting t06, monstercat t14, monalisaclan t12, suomi t26 and germany t08. In the last three, an amended gate has excluded the readers' theme. The floor weighs my B1 against two agreeing readers, and that weight is gone when the readers' theme fails the gate. The floor's review, owed, should decide whether the floor still applies in such items.

### J's guard on QC1-001, counted (`out/_analysis/c1_guard_report.py`, `c1_guard.json`)

J (21:12 Berlin, through the PI) confirmed that C1 rechecks place by the amended gates over the whole scheme. He set a guard: every re-placement names its concepts and the amended clause, and each pass reports the moves to a theme that neither the readers nor my B1 placed.
- Pass 2 moved 38 placements by recheck.
- 33 of them added a theme no reader and not my B1 had placed: 1 at gate:1 (samuraijack t07, T3-048), 31 at gate:6 and 1 at gate:7, all T3-084.
- In the 32 T3-084 cases, the concepts are those the readers had counted for T3-011 or T3-062 under the old wording. The amendment changed their theme, not the material read.
- 5 of the 33 are class 1 lines, where both readers agreed: samuraijack t07, afip t07, australia t14, bostonbruins t12 and kanye t17. 14 are class 2, 9 are class 3 and 5 are class 4.

### What I doubt (pass 2)

- **The one-concept rule.** Rule 0 keeps a theme "alone at its level", so one arriving request adds T3-084 as a third theme. This happens in aggies t07, sixers t06, rit t09, minnesotavikings t12, teslamotors t11, spacexmasterrace t07 and PlaceNL t14. These are the scheme's rules applied as written, and they make T3-084 grow by many thin placements. The pair test (section 5) should read T3-084's pairs with this in mind.
- **Whose words a concept is.** Many calls carry no speaker's sub, for example "Help out /r/wow!" or "r/tokyo needs some help." Where the words do not show a visitor, I read them as the room's own (hearthstone t14, ubc t03, placesnek t07, kilian t09). A different reading would move a few more items.
- **T3-084 now holds both sides of a request.** C2 cannot read the direction of a request from T3-084 alone. Direction stays recoverable from the concepts and from T3-062, which is now only the room's own call. I gave direction up to keep "a request it receives" placeable, as the visitor rule says.

### Slips (pass 2)

- The diary line for gates 5 to 7 says 25 items for the visitor sweep; the script counts 23.
- A Bash call that set shell variables was refused by the permission check; the rechecks were rerun with the commands written out.
- A write of 94 rechecks outlasted the two-minute foreground limit and finished in the background (exit 0). I read its output before writing again.

### Next pass

1. Transmission row 4's four "under rule 0" sentences: alberta t04, finland t06, korea t15 and mit t01.
2. Row 2's mariokart t04. My B1 placed T3-084; the readers placed T3-002 and T3-005; the line now places T3-084.
3. The G14 proposals, weighed against section 1's warning.
4. The visitor rule's sweep and the "help received" question.
5. The lone-B1 floor's review.
6. The themes placed nowhere or in one room.
7. The promotions of flagged class 2 records, among them europe t14 and kingdomhearts t03 (T3-095).
8. Then the revision rate, the pair test, the empties and arguables, the form pass, the fourth-order themes and `scheme_v2.md`. The visitor rule goes into `scheme_v2.md`'s gate block as a reading rule of every gate.

### validate.py C1 at pass 2's close (before `done.sh`)

```
stage C1:
  scheme_v2: 197 themes (14 rare), frozen 197, retired 0, new 0
  assignments_final 7844 lines = assignment_items_expected
  revised lines 2022 of 7844 (moved placements 2019)
  empties 175 of 7844
  a pass closed; the full set (scheme v2, assignments, the fourth-order themes, the form pass) is owed at the last pass, with the handback

0 errors (0 distinct shapes), 0 warnings
```
