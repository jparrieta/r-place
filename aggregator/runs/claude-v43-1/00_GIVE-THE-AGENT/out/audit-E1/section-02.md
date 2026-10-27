# Audit, section 1, part 2: the orderings, the counts, coverage and the canvas (E1b-02)

Written at E1b-02, 27 October 2026. This part covers four items of stage E1 section 1: the orderings proved by snaps, the counts rule, coverage, and rule 7's uses of the canvas. It also reports J's answer to QE1-001. Every figure comes from a script in `audit-E1/`, with its output beside it, or from a reading by hand that the diary logs. The scripts written at this leg are `prior_sections.py`, `snap_order.py`, `counts_phrases.py` and `counts_sample_check.py`; E1a's `orderings.py`, `counts_rule.py`, `coverage.py` and `canvas_uses.py` are read here. Each script states its rule in its docstring, written before it ran. A first run with a fault is kept under a `.superseded-N` name.

## 1. Orderings proved by snaps

A snap (`out/_snap/<name>.sha256`) holds the hash, size and time of every file in `out/` at one moment. At E1a's count there were 658 snaps with a header, from 6 October 12:29 to 27 October 15:33. For each ordering the stage names, the table says whether the snap's hash equals the file's as it stands, or whether the file moved after the snap, and which.

| ordering | result | what the snaps show |
|---|---|---|
| The scheme frozen before B3's first batch | **held** | `scheme_final.jsonl` has two hashes in all snaps. `fb8b543a9898` is at B2b-r3-p3's close (12 October 12:43:18Z). `4b471d29dd41` is in 541 snaps, from B2c's packets-out (13:10:24Z) to now. B3's first fleet call was at 15:17:38Z. The file has not moved since. |
| `prior.md` sections 1 to 6 sealed before B1's first `theme_discovery.jsonl` line | **held**, proved by rebuilding the text | `prior.md` has two hashes in all snaps. `7aa5240047ce` is in 321 snaps, from B1a's close (7 October 13:16:39Z) to C5. The first theme line is at 13:56:08. `prior_sections.py` rebuilt the file from the analyst's writes in the transcripts: a Write at 13:13:59Z and an Edit at 13:15:03Z give `7aa5240047ce`. Two Edits at D1a (15 October 15:56Z) give `720068eeaf87`, the file as it stands. Section by section, the preamble and sections 1 to 6 are the same, byte for byte, then and now. Only sections 7 and 8 changed: at B1 both held the same placeholder text, and now each holds its own. No shell command wrote `prior.md`. |
| Sections 7 and 8 sealed at D1 before `DROPS/D/` was ingested | **held** | `720068eeaf87` is first snapped at D1a's packets-out (15 October 19:44:16Z). The first snap that lists `adaptations.jsonl`, the ingested return, is D2a's adaptations-in (16 October 10:17:19Z). The file has not moved since. |
| The model hashed at C5's close before D1 | **held; the model moved after, by declared amendments** | `e15f96470271…` is at C5c-13's close (15 October 14:42:06Z), and D1's first snap is at 19:44:16Z. The model moved at D3, to `46384686d617…`, by the return's rulings (moves 172 to 197). That is the model at D6 and now. |
| Every D4 move snapped before `projections-D4.jsonl` and the chunk-share tree | **held for the branch cuts; the room forms came after, by J's ruling** | 34 D4 move snaps changed `branches.jsonl` from the snap before (moves 201 to 236). The last, `D4-move-merging-236`, is at 25 October 16:21:31Z. The first snap that lists the projection is D4a-03's interview cut at 19:16:07Z. 82 D4 snaps list the projection or the chunk-share files, and none of them changed `branches.jsonl`. `branches.jsonl` as it stands equals its last D4 snap. |
| Every move snap at C2 to D3 | **held** | 198 move snaps carry the move numbers 1 to 197, with none missing. Sorted by number, they are sorted by time, but for one pair. `D3-move-181-1` (21 October 09:31:59Z) is a second snap of move 181's state, 24 seconds before `D3-move-developing-181`. The diary named it as wrongly named and unused at D3a-53. |
| Every D6 proposal against its evidence and status | **status held**; evidence in part 3 | `proposals-D6.jsonl` holds 11 lines, all `unvalidated`, all on base `46384686d617…`, the D3 freeze. `amendments-D6.jsonl` holds 0 lines. The file has 6 hashes in 19 D6 snaps, and each change falls at the leg its new lines name (D6a-01 to D6a-07). It is unchanged from D6a-07's close to D6a-18's. |

A hash shows a whole file, not each of its lines. So these are self-reported:
- that the earlier lines of `proposals-D6.jsonl` stayed as written while lines were added;
- every other claim the run makes about the order of its work.

**QE1-001.** Stage E1's close-check first counted as errors the 82 D4 snaps that list the projection. J ruled on 27 October (18:45 Berlin, through the principal investigator): "Yes. I would not change the structure of the journey for bookkeeping." The handler amended the check. A D4 snap now counts as a branch cut only where it changed `branches.jsonl`, and the 82 are printed as findings. `snap_order.py` confirms that none of the 82 changed the branches. They are the six room forms, made after the projection at J's instruction: the D4a-03 interview cut, the closes of D4a-04 to D4a-08, and moves 238 to 313. They are not a recut of the branches.

## 2. The counts rule (rule 19)

**The census, stated twice** (`counts_rule.py`):
- `package/store/rooms.jsonl` lists 705 rooms, and 705 room folders hold a case account. They are the same set.
- `dropped.jsonl` holds 0 lines, so there is no drop and no reason to give.
- `tools/counts.py` gives 705 analysed rooms, 115,388 concepts and 7,844 second-order themes.

**Stage D4 section 4's four counts:** 476 in a branch + 0 unadapted + 229 in no branch + 0 unreturned = 705, which is `n_analysed`.

**The head's ledger figures**, against the ledgers as the head stands now (`counts_phrases.py`). All seven agree: adjudications 96,568, verdicts 1,029, tier history 1,026, model history 182, findings 45, elements 45 and arrows 21. E1a's `counts_rule.json` shows tier history 1,020 against 1,026. That is no longer true: it read the head before E1a's own Edit.

**Every count in every handback.** `counts_rule.py` found 361 phrases of a number and a counted noun in the 18 handbacks.
- `counts_phrases.py` sets aside 32 that are not counts: 26 whose number is followed by a comma (an id, a move number or a list item) and 6 decimals. That leaves 329 counts.
- Checking 329 by hand is more than one leg can do, so a seeded sample of two per handback, 36, was checked by `counts_sample_check.py` and by hand. The sample is drawn by `out/seed.txt`, and its rule was written before the run.

| result | counts | which |
|---|---|---|
| recomputed from the governing file, and agree | 27 | One of them, handback-A1's "7 lines" of defects, became 8 later in A1, as the same handback's line 72 records. |
| agree with a stated parameter or list | 4 | 500 shuffles (twice) is `c2_arrow_evidence.py`'s default; the 6 items are `field-C4.md`'s list 3; the 20 arrows are the 20 drawn in `figure-C5.md`, where A21 is not drawn. |
| rest on a judgment by hand that no file lets me recompute | 3 | A1's "79 of 100 concepts" (`coordinating-rule-A1.md` line 85); C4's "78 rooms" (`field-C4.md` line 115); D3's "48 rooms" (`notes-D3.md` line 6965). |
| **disagree** with the governing file | 2 | See below. |

- **handback-B1.md line 20** says "107 episode lines" whose kinds none of their rooms holds. `notes-B1.md` line 3108, written at B2 with `_analysis/b2_episode_kinds.py`, counts 106 (line, kind) pairs over 81 lines and says the 107 is wrong. The handback was not corrected. The handback is wrong.
- **handback-C5-p14.md line 45** says the model's history holds "31 lines (12 element, 12 arrow, 5 condition, 1 role, 1 claim)". `model/history.jsonl` holds 45 lines of stage C5 up to pass 14's leg, C5c-11: 16 element, 21 arrow, 5 condition, 1 role and 2 claim, over 30 distinct ids. 31 matches neither count, and the handback does not say how it counted. The handback is wrong.

My checking scripts had faults; the outputs of each first run are kept:
- `counts_phrases.py` first took any comma into the number and set aside no phrase.
- `counts_sample_check.py` first read a key the B3 defects lack.
- It also first read the analyst's D3 rulings in place of the re-check readers' verdicts.
- It then grouped those verdicts by the readers' own spelling of the room ("LAX" and "lax", "The R" and "The_R") until the room's folder was used.

The final message of each stage is in its transcript and is read with the diary in part 5. **293 handback counts were not checked.**

## 3. Coverage

Rooms read whole, counted from the read logs (`coverage.py`), one record per read. A log names the log that was open, not the stage the reading served.

| log | `mem.py room`: reads (rooms) | `mem.py forest`: reads (rooms; read whole) | case account: reads (rooms) | `cite.py`: reads (rooms cited) |
|---|---|---|---|---|
| A1 | 1,936 (705) | 205 (155; 1) | 887 (705) | 4,681 (663) |
| B1 | 1,873 (705) | 305 (110; 110) | 0 | 2,562 (455) |
| B2, B3, B4 | 0 | 0 | 0 | 0 |
| C1 | 0 | 1 (1; 0) | 0 | 71 (111) |
| C2 | 343 (67) | 498 (67; 67) | 0 | 1,144 (364) |
| C3 | 0 | 0 | 0 | 36 (30) |
| C4 | 0 | 0 | 0 | 14 (12) |
| C5 | 261 (218) | 32 (32; 32) | 0 | 2,254 (431) |
| D1, D4 | 0 | 0 | 0 | 0 |
| D2 | 0 | 0 | 0 | 2 (2) |
| D3 | 4 (4) | 14,054 (703; 703) | 0 | 77,047 (705) |
| D5 | 10 (8) | 0 | 0 | 6,848 (470) |
| D6 | 0 | 0 | 77 (40) | 845 (372) |
| **in all** | **705** | **705; 704 read whole** | **705** | **705** |

- **No room is unread.** Every one of the 705 analysed rooms was read by `mem.py room`, by `mem.py forest` and through its case account. 704 forests were read whole. The one short is r/COSI. Its forest was read once, at A1, from line 11 to line 18 of 18, so the ten header lines were skipped and every line of its tree was read.
- **A log that reads nothing is no gap.** B2, B3, B4, D1, D2 and D4 read no room through `mem.py`, because the fleets read for those stages. Readers and labelers leave no read log. Their reading is in `_fleet_raw/`:
  - B2: 6 rounds;
  - B3: 1,223 entries;
  - B4: 51 entries, and 55 for the OpenAI arm;
  - D2v and D3v: 708 entries each;
  - `DROPS/D/` holds 706 room entries.
- **Reported apart:** the hostile reader at C2 (`_fleet_raw/C2/C2-reviewer`) and the three readers at C5 (`readers-C5/`, one line each).
- **Refusals:** the read logs hold 3 refused room reads, 1 at B1 and 2 at D5.

## 4. Rule 7's uses of the canvas, stage by stage

Rule 7 lets me read the canvas with every room. It asks that wherever a canvas figure shaped a reading, a cut, a placement, a name or an element, the record says so, with `canvas` among its grounds or in its note. The fleets are never served the canvas. `canvas_uses.py` counts the uses in the logs, and I read the model's and the tree's files for canvas figures.

| stage | use in the logs | declared? |
|---|---|---|
| A1 | `mem.py room` with the canvas, 715 reads; `mem.py canvas`, 722 calls over 705 rooms | Yes: the `made` line and the reading route (`departures.jsonl` line 5). |
| B1 | 1,874 room reads showed the canvas (with `--size`) | The reads are allowed. No placement carries a canvas ground, and the record names nothing they shaped. |
| C2 | 22 room reads with the canvas (19 rooms); 321 with `--no-canvas` | The same as B1. |
| C5 | 218 room reads with the canvas; 43 with `--no-canvas` | The same as B1. |
| D3 | 4 room reads with the canvas | The same as B1. |
| D4 | the projection (`projections-D4.jsonl`, the chunk-share tree), after the branch cuts | Yes, and in order (part 1). The 75 D4 tier-history grounds that name the canvas all say that no canvas field was used. |
| D5 | 5 room reads with the canvas; `mem.py canvas` twice (D5a-40, D5b); the canvas fields of `branches-D5.jsonl` (35 branches) | Yes: `survival-D5.md` reads them after the record. |
| D6 | D6b read D5's survival output | Yes: `notes-D6.md` says the survival reading by form comes from the record and that the canvas is not read. |

**Undeclared uses found: none.** No element, arrow, proposition, finding or branch carries a canvas figure. The passages that name the atlas, artwork or survival are members' own acts or the coded record:
- P12's "atlas entries" are entries members wrote;
- "artwork" in A05's support is in a member's quote;
- F-021's bound says "The canvas is not evidence (rule 7)";
- in F-023, F-027, F17 and F18, what "survives" is in the coded record or in the rooms' own judgment.

The B1, C2, C5 and D3 reads are the open question. The canvas was on the page while I placed and ruled, and the record names nothing it shaped. The logs cannot tell whether it shaped nothing or shaped something undeclared, so that is self-reported.

**Where the canvas may have shaped the work without a declaration**, for a reader to look:
- **Elements argued mostly from what rooms kept:** P12 (records), P13 (carrying on), P22 (which version is kept), A09 (the record carried on), and the account's survival paragraph, which rests on the `work_remained` field (defects line 100).
- **Branch names that say what rooms did with their work:** F09 (rooms rebuild after moving), F12 (the spine restarted on another canvas), F17 and F18 (success judged by what survives), F23 (the close scoped to the original canvas) and F32 (rooms keep after marking).
- **The cuts made after the projection:** the six room forms, cut with `projections-D4.jsonl` and the chunk-share tree in the folder (the 82 snaps of QE1-001). Their grounds say no canvas field was used.

## 5. Defects named at this leg

Two lines were appended to `defects.jsonl` (lines 110 and 111, stage E1, leg E1b-02) by `_analysis/e1b02_defects_lines.py`. They are the two handback counts that disagree with their governing files (handback-B1.md line 20; handback-C5-p14.md line 45). Both are the instrument's. No earlier file is changed.

## What this part cannot say

- Whether the 293 unchecked handback counts agree with their files. The sample of 36 found 2 that do not.
- Whether the earlier lines of `proposals-D6.jsonl`, or of any other file, stayed as written while the file grew. A hash covers the whole file.
- Whether the canvas, on the page in 2,118 of my room reads at B1, C2, C5 and D3, shaped a placement, a ruling or a name that the record does not declare.
