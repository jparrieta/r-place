# Head, claude-v43-1

Under 3,000 words, rewritten whole at every close. Last written at C1a-02, 2026-10-13 (UTC). Stage B is closed and frozen. Stage C1 (structuring) has closed two passes. Pass 1 applied J's class 2 ruling and the 30 re-reads. Pass 2 read the four weak sources and amended seven gates, with 304 rechecks, 38 moves and every gate pair confirmed.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stages A1, B1 (the third-order scheme, 197 themes in 21 families), B2 (the pilot), B3 (the fleet) and B4 (adjudication and the blind sample) are done. Stage C1 has closed two passes, each with `done.sh C1`. `scheme_v2.jsonl` exists, rebuilt by `out/_analysis/c1_scheme_v2_sync.py` from `scheme_final.jsonl` plus the C1 lines of `gate_history.jsonl`. It differs from the frozen scheme in five themes: T3-095, T3-023, T3-084, T3-011 and T3-062.

## Stage C1

**J's rulings for C1 (20:16 Berlin, through the PI's message of 18:17Z; carry them).**
- **Class 2.** The readers' list stands as the placement. The B1 themes no reader placed are a flagged record (`b1_themes_without_reader_support`), not placements. I may promote a flagged theme where its concepts support it, logged as my re-placement.
- **The re-reads.** First the five class 4 items where six readers converge against a re-rule, then the class 4 unresolved rulings resting on "the earlier reading".
- **No fleet re-read of class 2 now.** Fresh readers test the revised scheme after C1.
- My B4 defect list, the G14 proposals, bare event titles and whose act a visitor's words count for are mine to work through.

**QC1-001 (J, 21:12 Berlin, through the PI; carry it).** C1 rechecks place each item by the amended gates over the whole scheme. J's 13 October rulings govern B4 rulings and their re-reads, not C1 rechecks. **The guard:** every re-placement names its concepts and the amended clause, and each pass counts and reports the moves to a theme that neither the readers nor my B1 placed (`out/_analysis/c1_guard_report.py`).

**What the B4c interview held.** 32 of 53 sampled class 2 items keep a B1 theme no reader placed. The G14 proposals: narrow T3-010's `must_show`; rewrite the T3-010/T3-149 and T3-084/T3-062 discriminators to name visible evidence; add a T3-010/T3-011 discriminator and a family `decide_when_both`; no split.

**The stopping criterion** (`notes-C1.md`). I stop recutting when every source line has a recorded decision (revise, leave, or carry with its reason) and the last pass amended no gate whose rechecks moved more than one in ten. A later cut is preferred only if it decides a recorded source without making two gates contradict each other, or moves a boundary that split readers at B2 and again at B3 or B4 toward a merge or the rare tier rather than a third sentence.

**Three reading rules, declared in pass 2 (`notes-C1.md`).**
- **The visitor rule.** A theme names an act in the record of the room whose threads hold the words. Another room's act spoken there is placed by what it is for this room, never as this room's own act. It goes into `scheme_v2.md`'s gate block as a reading rule of every gate.
- **A bare mention of the event** holds no act. It stays unplaced, as the empties' kind "a bare mention of the event, no act".
- **How a recheck is read.** I place the item under the amended sentence and under the old one. It moves when the answers differ and the line follows the old answer. A line that differs from both answers is listed for review, not moved.

**Pass 1 (C1a-01).** Read the record: `scheme_edits.jsonl`, the pair table, transmission's rows. Applied class 2: 1,990 lines on the readers' list, 2,814 B1 themes flagged, snap `C1-class2-readers-list`. Re-read 30 rulings: 10 placed, 15 unresolved, 5 held.

**Pass 2 (C1a-02).**
- **The weak sources** (`out/_analysis/c1_weak_sources.json`). 22 themes sit in all four sources, in five clusters: the April Fools themes, call/offer/build, G14's requests, T3-005|T3-021, and G02 moderation. At a floor of one occurrence the measure tracks a theme's size.
- **gate:1, T3-095 `must_show`:** the April Fools condition. 102 candidates, 30 owed, 2 moved: hawks t07 to T3-023, samuraijack t07 to T3-048.
- **Gates 2 to 4, the T3-095|T3-023 line.** Both discriminators and T3-023's `decide_when_both` now send working out whether a change is an April Fools joke to T3-095, and asking what it shows to T3-023. 90 owed, 0 moved.
- **Gates 5 to 7, the visitor rule.**
  - T3-084 now counts a request between rooms in either room's record, an arriving one included: 30 owed, 0 moved.
  - T3-011 now counts only calls "by the room's own members": escalated to all 124, 35 moved.
  - T3-062 now counts only "the room's own call, made by its members": 30 owed, 1 moved.
  Every move takes an arriving request out of T3-011 or T3-062 to T3-084.
- **All 38 moved** with `mem.py reassign`. The guard counts 33 moves to a theme no reader and not my B1 placed, 32 of them T3-084 carrying concepts the readers had counted for T3-011 or T3-062.
- **Every pair of the five amended themes is read and confirmed.** T3-002|T3-084 is a watch item for fresh readers.
- **The held re-reads, all decided unresolved:** canucks t25, monalisaclan t12, suomi t26, germany t08 and germany t19. The lone-B1 floor now keeps a fitting theme out of six items, three of them where an amended gate excluded the readers' theme.
- **The files.** `assignments_final.jsonl` 7,844 lines, 2,022 revised. `rechecks-C1.jsonl` 304. `validate.py C1`: 0 errors, 0 warnings.

**Found, owed.**
- **The visitor sweep.** 23 rechecked items hold other rooms' help given to this room under T3-011 or T3-062; the list is in `c1_guard.json`. The scheme has no theme for help a room receives.
- **Six lines for review,** where both readings differ from the line: brasil t01, hearthstone t08, europe t14, kingdomhearts t03, formula1 t02 and taiwan t01.
- **Themes now placed nowhere:** T3-140, T3-144, T3-161. Eleven more sit in one room. Each owes a decision: retire, the rare tier, or a promoted flagged record.

## J's rulings on how a ruling is made (13 October; carry them)

- **QB4-001 (J, 06:43 Berlin):** "Ask it to stop. The point is to try to adjudicate. I imagine that the additions are really just the analyst trying to be nice. And not go back on what others said".
- **J's rulings (06:45 and 06:47 Berlin):** (1) A ruling chooses among the placements (reading A, reading B, my B1) and adds no theme beyond them. (2) It takes the union only when it names, for each theme it keeps, the separate concept that carries it; otherwise it chooses. (3) Re-rule packets 1 to 4's rulings that held a theme no placement held. Done at B4a-05.
- **also_present (J, 09:09 Berlin) and QB4-002 (09:20):** `also_present` lists only themes a reader placed, a reader listed under its own `also_present`, or my B1 named.
- **QB4-003 (J, 11:29 Berlin):** "count them. Themes a reader listed under its own also_present count in the bag test."
- **Lone B1 themes (J, 12:28 Berlin):** "Whatever the agent feels more comfortable with." I chose: in class 4 a theme only my B1 placed stands against the two agreeing readers only with three concepts or more of its own.

**Rule 0 inside the placements.** A concept counts toward a placed theme when that theme's `must_show` takes it and no field sends it to another placed theme. Order by concept count, ties by placements; at most three; a one- or two-concept theme is kept only when it leads its level on placements; a tie at the top places all tied themes; a theme alone at its level is kept. **The bag test:** four themes with three concepts each make a bag.

## Stage B4, in short

- **The adjudication** (`adjudication_report.md`). 3,288 contested items ruled; unresolved 185. Fields that failed: `must_show` 252, discriminators 114, `must_not_show` 57, `decide_when_both` 28. `assign_final.jsonl` is stage B's settled line and stays as it is.
- **The blind sample** (`transmission-after-revision-B4.md`). Two arms, DeepSeek V4.1 Flash and OpenAI gpt-6-astra. Fresh against settled, mean Jaccard: uniform 0.657 and 0.622, adjudicated 0.544 and 0.554. G14 is among the three worst families in both arms. These figures bound whether the written instrument decides, not whether it is right.
- **Transmission's rows for C1.** Row 2 (split, I was confident): mariokart t04. Row 4 (readers agreed against me): nine items. In four of them (alberta t04, finland t06, korea t15, mit t01) a `decide_when_both` "under rule 0" did not transmit.

## Stage B3 and B2, in short

B3: fleet ids only; 1,212 batches, R = 2; `assign_raw.jsonl` 17,653 lines; gold fidelity 0.645; agreement Jaccard 0.786, alpha 0.782. B2: gold fidelity 0.624, pairwise 0.818; stability 0.807 is the floor every later figure is read against.

## J's rulings that bind (carry them)

- **Bags.** No one cuts the bags (J, 12:24 Berlin). A bag stays one item: one theme placed, its others under `also_present`, each with three concepts of its own and named by a reader or my B1.
- **The bound (J, 13:47).** `also_present` names "twenty themes at most", each with three concepts of its own.
- **The not-flagged bag (J, QB2-013).** With no other theme at the three-concept floor, `item_is_a_bag` is false and `also_present` `{}`.
- **Fleet ids (J, 09:14 and 12:15).** Packets carry only fleet ids; my files keep room ids.

## Standing words from J and the PI (carry into every head)

**J's words for B1 (7 October 2026):** "national elements are very important here"; "we need to get as much variance on organizing behavior early on so that later we have enough to create the model". National, political and conflict content is study material, named as plainly as any other. **The handler's rule:** a choice to leave out or soften content for any reason other than the study's goes to J first with `mem.py ask`, and the content stays meanwhile.

**J on reading (11 October, 16:54 Berlin).** Stop cutting room reads to a line length. Read room lines whole. Page a long read by line ranges or offset, never by truncating lines. Use `--width N` on a `mem.py` read if a clip is ever needed.

**J on asking (11 October, 17:01 Berlin).** Ask J with `mem.py ask` whenever a question is needed; asking does not stop the run.

**The PI's clarifications (8 October, approved by J):** the thresholds are the design's heuristic; the rule is unchanged.

**How to work, from J (8 October, 23:45 Berlin, "can you do a hot change for the batching?"; relayed by the handler at 22:03Z; carry this paragraph into every head).** A change in how I work, not in what I read or decide. Fewer turns. When two or more tool calls do not depend on each other's output, make them in one turn. Chain ordered commands in one Bash call with &&, so that a failure stops the rest; for example, the `mem.py log` or note just decided, then the next `mem.py codes`. Never put a write in the same turn as the read it depends on. Never run two writes to the same file as separate parallel calls. Keep one room's material per read, as now. Every tool still writes its own record; nothing about what I read or decide changes.

**Two rules from J at B1b-29 (through the handler, 20:10Z; carry them into every head).** Write rule 0 lines and bags with `b1_multiplace_write4.py` and `b1_bags_from_file2.py`, not the old scripts, which made one `mem.py` call per row of the whole table and grew to 8.5 minutes a write. Never end a turn while a job runs in the background; run every write and check in the foreground.

## The pilot's declarations (from `notes-B2.md`)

- **Agreement:** Jaccard on placement sets (`["T3-004"]` against `["T3-004","T3-011"]` scores 0.5). Alpha uses distance 1 − Jaccard. Primary exact agreement is reported beside, never in place.
- **Gold:** 40 items in `gold_items.jsonl`, never shown to a reader.

## The scheme

`scheme_final.jsonl` holds 197 themes (183 main, 14 rare) in 21 families, frozen. Stage C1 writes `scheme_v2.jsonl`, field for field (the 14 rare themes carry `floor: null`), with every change logged in `tier_history.jsonl` and every gate amended through `mem.py gate` with its rechecks.

## Open, carried

- **From B1.** The ruling on testing G13, G14 and G15 as one index page. Seven pairs of lines telling one event; the cfb and finland records; the 76 themes holding both T3-005 and T3-021 acts. The second-order theme the scheme handles worst: argentina t06.
- **The bag count.** J counts 841 B1 bags; an older head said 846. Not reconciled.
- **Defects for stage C1** (in `adjudication_report.md`), not yet worked: T3-017's and T3-001's discriminators against T3-031's canvas condition; T3-033's "first"; the homeland flag in the siblings' `must_not_show`; T3-018's "whose character"; T3-052 presumes a mark and an owner; T3-086 against T3-050; T3-003's and T3-043's discriminators on parts claimed after the work; "the work" in T3-073 and T3-058; T3-054 against T3-038 and T3-002; T3-111 and a standing community; T3-087 against T3-058; T3-117's regret; T3-021 and a cleaned copy; T3-164's reach; T3-009 against T3-073. From B4c: G14's request siblings; fleet unanimity resting on a field it contradicts. From C1a-01: whose chat a named sub's Discord is (dmt t03 against shield t06); survivor t28 against the B4 ruling on python t04.
- **My doubts.** The three-concept lone-B1 floor is my choice and keeps a fitting theme out of six items. Rule 0's "alone at its level" adds T3-084 on one concept in seven items. Where words carry no speaker's sub I read them as the room's own. T3-084 now holds both sides of a request, so C2 cannot read direction from it alone.

## Ledgers at this close

- B1 to B3: `scheme_current.jsonl`, `families.jsonl` (21), `confusions.md` (19 pairs), `episodes-B1.jsonl` (1,341); `notes-B2.md`, `gold_items.jsonl` (40), `scheme_final.jsonl` (197); `notes-B3.md`, `assign_raw.jsonl` (17,653), `multiplacement_log.jsonl` (3,171), `b3_classes.jsonl` (7,844), `defects.jsonl` (63).
- B4: `notes-B4.md`; `transmission-B4.md`; `coder_conflicts.jsonl` (72); `disagreements.jsonl` (3,288); `assign_final.jsonl` (7,844); `adjudication_report.md`; `reassign.jsonl` (999), `reassign-openai-astra.jsonl` (1,000); `transmission-after-revision-B4.md`; `handback-B4.md`.
- C1: `notes-C1.md`; `assignments_final.jsonl` (7,844), `assign_revisions_only.jsonl`, `assignments_final.count.txt`; `scheme_v2.jsonl` (197); `gate_history.jsonl` (7); `rechecks-C1.jsonl` (304); `gate_checks.jsonl`; `out/_analysis/c1_*.py` with `c1_rechecks/` (packets and decisions per gate), `c1_guard.json`, `c1_weak_sources.json`.
- Asks QB2-001 to QB2-014, QB3-001 to QB3-005, QB4-001 to QB4-003 and QC1-001 are answered.

## Rules kept

- Never type an id, an order or a name from memory; check with `jq` or a script. Never log a write before the tool answers. Count a ledger's lines after appending.
- There is no `--kind close` and no `--kind episode`; log those as notes.
- A question to J is `mem.py ask "<question>" --assume "<meanwhile>"`. Read an answer with `mem.py asks <id>`.
- Never put a placeholder or a no-op in a command or a log line. Never put an Edit or Write and the read, dry run or validator run that checks it in one turn. Count the head's words before the closing line.
- Never write an id-like token the run does not define in the head, such as a D or a P followed by digits: `done.sh` reads it as an unresolved link.
- The permission check refuses: shell variables set and expanded in a command; shell loops and words beginning "for_"; shell functions, brace groups and heredocs; awk with system() or `$` fields; env-var prefixes; cat or jq on `out/diary/`; `cut -c` after `mem.py` or a helper; `head -n -N`. Write a script file in `out/_analysis/` instead. `.git` is read-denied, and so are reads outside the run folder.
- `mem.py` pages long output; fetch the rest with `--offset`. A Bash output over about 30 KB is saved where I cannot read it; page it. A Bash call over two minutes moves to the background: set `timeout` up to 600000 for long writes, and read the output before the next write.
- After a compaction the guard requires the head and stage file read again and the exact line "compacted; head reconciled" through `mem.py log --kind note`, in a call of its own, before any other step.
- In C1: every re-placement goes through `mem.py reassign` with `--codes`; a recheck first, then the reassign. Rechecks go through `out/_analysis/c1_recheck_apply.py` from a decisions file (`--check` runs them through `mem.py --dry-run`), and moves through `c1_reassign_from_rechecks.py`. After any `mem.py gate`, run `c1_scheme_v2_sync.py --write`, then read and confirm every pair of the amended theme with `mem.py gates`. A C1 move to an empty placement cannot carry concepts. Every move of a theme (split, merge, retire, rare, a fourth-order cut) is logged `--kind move` and snapped.

## The next comparison

Pass 3 (C1a-03) first reads the views after pass 2's close. Then it works through four items:
1. Transmission row 4's four "under rule 0" sentences (alberta t04, finland t06, korea t15, mit t01) and row 2's mariokart t04.
2. The G14 proposals, weighed against section 1's warning about third sentences.
3. The visitor sweep: G14 placements that hold another room's act, and whether "help received" is a kind the corpus carries.
4. The lone-B1 floor's review, where an amended gate has excluded the readers' theme.

Then come the themes placed nowhere or in one room, the promotions of flagged class 2 records, and the revision rate, 200 placements re-decided by seed.
