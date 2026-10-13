# Head, claude-v43-1

Under 3,000 words, rewritten whole at every close. Last written at C1a-07, 2026-10-13 (UTC). Stage B is closed and frozen. Stage C1 (structuring) has closed seven passes. Pass 7 called the pair test's 76 pairs; it amended no gate and moved no placement.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## The current account, and the contrary rooms

The settled line is mostly right on the primary act and drops second acts. In the revision rate's 200 items, my re-decision agreed with the current line's primary in 0.845; in 29 (14.5%) I would add a second act of three concepts or more, the lean J ruled to keep. Pass 6's T3-043 gates moved 23 of 183 placements: members telling their own part had been counted as credit. Pass 7 found a seam in all 76 frequent pairs (75 joints, 1 unresolved, no lump); where two themes sit closest, placements follow a label's words, not the written line's fact. The room that best supports the account is naruto t04: one theme for help that arrives from other rooms. The room that most threatens it is greenlattice t03: more than ten concepts ask for peace or a pact, and the line places T3-010 alone with T3-149 under `also_present`, a bag J ruled must not be cut.

## Where the run stands

Stages A1, B1, B2, B3 and B4 are done. Stage C1 has closed seven passes. `scheme_v2.jsonl` is rebuilt by `out/_analysis/c1_scheme_v2_sync.py` from `scheme_final.jsonl`, the 35 lines of `gate_history.jsonl` and `out/_analysis/c1_tier_ops.jsonl`. It differs from the frozen scheme in 19 themes: T3-001, T3-002, T3-004, T3-010, T3-011, T3-015, T3-017, T3-023, T3-025, T3-043, T3-050, T3-062, T3-063, T3-075, T3-076, T3-084, T3-095, T3-140 (rare; 15 rare in all) and T3-149.

## Stage C1

**J's rulings for C1 (carry them).**
- **Class 2.** The readers' list stands as the placement. B1 themes no reader placed are a flagged record (`b1_themes_without_reader_support`). I may promote one where its concepts support it, logged as my re-placement.
- **No fleet re-read of class 2 now.** Fresh readers test the revised scheme after C1.
- My B4 defect list, the G14 proposals, bare event titles and whose act a visitor's words count for are mine to work through.

**QC1-001 (J, carry it).** C1 rechecks place each item by the amended gates over the whole scheme. **The guard:** every re-placement names its concepts and the clause, and each pass counts the moves to a theme neither reader nor my B1 placed (`out/_analysis/c1_guard_moves.py`).

**QC1-002 (J, carry it).** Lean to one placement. A second theme needs three concepts or more of its own, the same floor as `also_present` and the lone-B1 rule. No corpus-wide sweep; the revision rate measures the lean.

**QC1-003 (the handler's ruling under J's delegation; carry it).** Five revision-rate errors no C1 verb can apply stay as found; no verb is opened in C1, since a new verb changes the instrument and that is J's call. They are in `out/_analysis/c1_unapplied.jsonl`: harrypotter t11 and tampabaylightning t08 to be emptied; radiohead t04, heroesofthestorm t11 and stevenuniverse t02, bags whose placed theme and `also_present` should swap. List them in `notes-C1.md` and `handback-C1.md` from that file; all 34 errors count in the rate. If J opens a verb, the file is what it applies.

**The stopping criterion** (`notes-C1.md`). I stop recutting when every source line has a recorded decision (revise, leave, or carry with its reason) and the last pass amended no gate whose rechecks moved more than one in ten. A later cut is preferred only if it decides a recorded source without making two gates contradict each other, or moves a boundary that split readers at B2 and again at B3 or B4 toward a merge or the rare tier rather than a third sentence. **At pass 7:** it holds, trivially, since pass 7 amended no gate. Recutting stops; a gate the empties and arguables pass needs owes its rechecks and reopens the criterion.

**Reading rules (`notes-C1.md`), all for `scheme_v2.md`'s gate block.**
- **The visitor rule.** A theme names an act in the record of the room whose threads hold the words. Another room's act spoken there is placed by what it is for this room.
- **"The work"** in a field is the room's own work unless the field names another's.
- **A bare mention of the event** holds no act; it stays unplaced.
- **How a recheck is read.** The item moves when the old and amended sentences give different answers, J's floor applied to both, and the line follows the old one; a line that differs from both is listed for review.
- **J's floor in every pairing sentence.** "When it has concepts of its own" is read as three concepts or more.
- **The named words of T3-010 | T3-149** (and since gates 33 and 34, of T3-149 | T3-025). Attack, war, fight, battle, invasion, raid and conquest name an attack. Verbs acting on a work without them are a work asked to be spared (T3-010). A pledge to leave each other alone that names no lines or space is a non-aggression pact (T3-149). A greeting "in peace", or an adverb or adjective on border talk, names no pact.
- **Help between rooms is read from either room's record** (gate:5 for T3-084, gate:27 for T3-011).
- **Credit and own part (gates 30 to 32).** A member's own part, during the work or after, is T3-003; T3-043 is credit to others and disputes over who made it. A plural claim of who made it stays T3-043. A mixed concept goes by the act its label leads with.

**Passes 1 to 6, in short.**
- Pass 1: class 2 applied; 30 re-reads. Pass 2: gates 1 to 7 (April Fools; the visitor rule). Pass 3: gates 8 to 26 (who calls; J's floor; the named words). Pass 4: the held lines, gate:27, the lone-B1 floor revised, T3-140 to rare.
- Pass 5: the revision rate (`out/_analysis/c1_revision/`, seed 20261013): against the current line 73 of 200 placed differently (36.5%), mean Jaccard 0.786, primary agreement 0.845; against the settled line 99 (49.5%). 34 errors (29 moved, 5 in `c1_unapplied.jsonl`). 28 source lines decided (`c1_source_lines_pass5.json`).
- Pass 6: gates 28 to 35 for the five revise lines; gate:30 (T3-043's gloss) moved 4 of 30, escalated to all 183 T3-043 placements, 23 moved; the others moved 0 or 1 of 30. The pair test computed (`c1_pair_test.py`): 78 pairs on ten lines or more; corpus arguable rate 0.613, multi-theme lines 0.961, 76 pairs at 0.713 or more; the rate marks a contested item's history, not the pair. Guard: 24 moves, 4 adding a theme neither reader nor my B1 placed.

**Pass 7 (C1a-07).** The 76 pairs read as declared at C1a-06 (883 item readings), by a test fixed at pair 1 (worded in `notes-C1.md`). 75 joints; 1 unresolved (T3-010 | T3-149); 0 lumps; no merge, split or move (`c1_pair_calls-*.json`, checked by `c1_pair_calls_check.py`). 20 placements stand against a written field (`c1_pair_carried.json`: calls to defend under T3-002 in seven rooms, further marks under T3-033 in five, eight single slips); none moved, since no gate was amended. Guard: 0 moves.

## J's rulings on how a ruling is made (13 October; carry them)

- **QB4-001 (J, 06:43 Berlin):** "Ask it to stop. The point is to try to adjudicate. I imagine that the additions are really just the analyst trying to be nice. And not go back on what others said".
- **J's rulings (06:45 and 06:47 Berlin):** (1) A ruling chooses among the placements (reading A, reading B, my B1) and adds no theme beyond them. (2) It takes the union only when it names, for each theme it keeps, the separate concept that carries it. (3) Re-rule packets 1 to 4's rulings that held a theme no placement held. Done at B4a-05.
- **also_present (J, 09:09 Berlin) and QB4-002 (09:20):** `also_present` lists only themes a reader placed, a reader listed under its own `also_present`, or my B1 named.
- **QB4-003 (J, 11:29 Berlin):** "count them. Themes a reader listed under its own also_present count in the bag test."
- **Lone B1 themes (J, 12:28 Berlin):** "Whatever the agent feels more comfortable with." I chose: in class 4 a theme only my B1 placed stands against the two agreeing readers only with three concepts or more of its own. Since C1a-04 the floor applies only where the readers' theme takes concepts.

**Rule 0 inside the placements.** A concept counts toward a placed theme when that theme's `must_show` takes it and no field sends it to another placed theme. Order by concept count, ties by placements; at most three; a tie at the top places all tied themes. A second or third theme needs three concepts of its own. **The bag test:** four themes with three concepts each make a bag.

## Stage B4, in short

3,288 contested items ruled, 185 unresolved (`adjudication_report.md`); `assign_final.jsonl` is stage B's settled line, unchanged. The blind sample (`transmission-after-revision-B4.md`, two arms): fresh against settled, mean Jaccard uniform 0.657 and 0.622, adjudicated 0.544 and 0.554; G14 among the three worst families. These figures bound whether the written instrument decides, not whether it is right.

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

Agreement is Jaccard on placement sets (alpha on 1 − Jaccard); primary exact agreement beside, never in place. Gold: 40 items in `gold_items.jsonl`, never shown to a reader.

## The scheme

`scheme_final.jsonl`: 197 themes (183 main, 14 rare) in 21 families, frozen. `scheme_v2.jsonl` mirrors it field for field; tier changes go to `tier_history.jsonl`, gates through `mem.py gate` with their rechecks.

## Open, carried

- **From B1.** The ruling on testing G13, G14 and G15 as one index page. Seven pairs of lines telling one event; the cfb and finland records; the 76 themes holding both T3-005 and T3-021 acts. The second-order theme the scheme handles worst: argentina t06.
- **The bag count.** J counts 841 B1 bags; an older head said 846. Not reconciled.
- **My doubts.** Where words carry no speaker's sub I read them as the room's own. T3-084 and T3-011 hold both sides of a request or of help, so C2 cannot read direction from them alone. The named-words test splits a truce told only in pixels into T3-010. I reversed hearthstone t08's unanimous line under my own gate:1. I drew the T3-043 line by person; B4's readers had often drawn it by time. The pair test's rate cannot separate pairs, and my test finds a lump only where a sample has no pure concept, so 0 lumps is weak evidence; I called the 76 alone, on concept labels.

## Ledgers at this close

- B1 to B4, unchanged since B4's close: `confusions.md` (19 pairs), `scheme_final.jsonl` (197), `multiplacement_log.jsonl` (3,171), `b3_classes.jsonl` (7,844), `coder_conflicts.jsonl` (72), `disagreements.jsonl` (3,288), `assign_final.jsonl` (7,844), `reassign.jsonl` (999), `reassign-openai-astra.jsonl` (1,000), with the stage notes, transmission files and `handback-B4.md`.
- C1, unchanged since pass 6's close: `assignments_final.jsonl` (7,844, 2,101 revised, 167 empty), `assign_revisions_only.jsonl` (2,101), `assignments_final.count.txt`; `scheme_v2.jsonl` (197, 15 rare); `gate_history.jsonl` (35); `rechecks-C1.jsonl` (1,297); `tier_history.jsonl` (393) with `c1_tier_ops.jsonl`; `gate_checks.jsonl` (737).
- C1, added at pass 7: `c1_pair_calls-*.json` (76 calls), `c1_pair_packs/`, `c1_pair_carried.json` (20), `c1_guard_C1a-07.json`, with their scripts. Also `notes-C1.md`, the other `out/_analysis/c1_*` files, `c1_unapplied.jsonl` (5) and `c1_pair_test.json`. `validate.py C1`: 0 errors, 0 warnings.
- Asks QB2-001 to QB2-014, QB3-001 to QB3-005, QB4-001 to QB4-003 and QC1-001 to QC1-003 are answered.

## Rules kept

- Never type an id, an order or a name from memory; check with a script. Never log a write before the tool answers. Count a ledger's lines after appending.
- There is no `--kind close` and no `--kind episode`; log those as notes.
- A question to J is `mem.py ask "<question>" --assume "<meanwhile>"`. Read an answer with `mem.py asks <id>`.
- Never put a placeholder or a no-op in a command or a log line. Never put an Edit or Write and the read, dry run or validator run that checks it in one turn. Count the head's words before the closing line.
- Never write an id-like token the run does not define in the head, such as a D or a P followed by digits: `done.sh` reads it as an unresolved link.
- The permission check refuses: shell variables set and expanded in a command; shell loops and words beginning "for_"; shell functions, brace groups and heredocs (an empty one included); awk with system() or `$` fields; env-var prefixes; cat or jq on `out/diary/`; `cut -c` after `mem.py` or a helper (use `--width`); `head -n -N`. Write a script file in `out/_analysis/` instead. `.git` is read-denied, and so are reads outside the run folder.
- `mem.py` pages long output (`--offset`). A Bash output over about 30 KB cannot be read; page it. Set `timeout` up to 600000 for long writes.
- After a compaction the guard requires the head and stage file read again and the exact line "compacted; head reconciled" through `mem.py log --kind note`, in a call of its own, before any other step.
- In C1: amend one discriminator with `c1_gate_disc.py`; other fields with `mem.py gate`. Then `c1_scheme_v2_sync.py --write`; review owed rechecks with `c1_owed_review.py` (a packet, then a focus file of the counted concepts, then each candidate's full concept list); decisions through `c1_decisions_common.py` (with `c1_special_by_change.py`; `--name` for an escalation) and `c1_recheck_apply.py`, dry run first; moves through `c1_reassign_from_rechecks.py`; then `c1_pairs_dump.py`, read, `c1_confirm_pairs.py`. Reviewed lists through `c1_reassign_list.py` (`mem.py reassign` prints "moved"; it cannot empty a line or write `also_present`, and `unplace` is B1's). Every move of a theme is logged `--kind move` and snapped. A theme's gate fields: `c1_theme_fields.py T3-NNN --vs T3-MMM`.

## The next comparison

Pass 8 (C1a-08) first reads the views after pass 7's close. Then the empties and the arguables (section 6): the 167 `third_order: []` lines grouped into kinds, with when each kind first appeared (saturation by kind); the arguable lines checked against B1's prediction in `confusions.md`; the 20 placements of `c1_pair_carried.json` read by their written fields; T3-052's four unresolved items, B4 packet 7's unresolved single failures, harrypotter t11 and tampabaylightning t08. A gate amended there declares its rechecks.

Then the form pass, the fourth-order themes, `scheme_v2.md` (its gate block holding the reading rules above), the handback and the interview.
