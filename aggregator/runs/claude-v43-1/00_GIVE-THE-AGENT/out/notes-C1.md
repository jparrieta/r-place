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
