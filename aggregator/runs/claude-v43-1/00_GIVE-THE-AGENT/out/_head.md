# Head, claude-v43-1

Under 3,000 words, rewritten whole at every close. Last written at B4a-04, 2026-10-13 (UTC). Stage B4 is open: packets 1 to 4 of 7 of the adjudication are ruled. The next leg is B4a-05: it opens by re-ruling the earlier rulings under J's rulings of 13 October, then rules packet 5.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1 is closed. Stage B1 (the third-order scheme, 197 themes in 21 families), B2 (the pilot) and B3 (the fleet) are done. Stage B4: the adjudication runs one packet a leg; packets 1 to 4 are ruled (1,899 of 3,288 contested items).

## J's rulings on how a ruling is made (13 October; carry them)

- **QB4-001, answered (J, 06:43 Berlin):** "Ask it to stop. The point is to try to adjudicate. I imagine that the additions are really just the analyst trying to be nice. And not go back on what others said".
- **J's rulings (06:47 Berlin):** (1) The placements are the readers' and the analyst's (my B1). A ruling chooses among those placements and adds no theme beyond them. (2) A ruling takes the union of placements only when it names, for each theme it keeps, the separate concept that carries it; otherwise it chooses. Items in packets 1 to 4 already ruled are re-ruled at the start of B4a-05.
- **Applied from packet 4's item 401.** Concepts count only toward placed themes; a concept whose act no placement holds is named in the why and left out of `support_by_theme`. Rule 0 inside the placements: at most three; order by concept count, ties by how many of reading A, reading B and my B1 hold the theme; a one- or two-concept placed theme is kept when its concept passes the gate and it leads its level on placements; where placed themes tie at a level, none is kept. A bag's `also_present` places nothing.
- **The re-ruling at B4a-05.** 378 ruled lines place a theme that neither reader nor my B1 held: packet 1 30, packet 2 58, packet 3 157, packet 4 133 (all in items 1 to 400). `out/_analysis/b4_agreement_range.py --packet N --ranges a-b` counts them. Every ruled line already names a concept of its own per placed theme, so rule (2) reaches no other line. Each correction goes through `b4_rule_append.py --replace`.

## Stage B4 (B4a-01 to B4a-04)

**The selection (the PI at 21:19Z on 12 October, J's amended stage file).** `b3_classes.jsonl` holds J's five classes. Class 1 (readers agree, equal to B1) 2,566 and class 2 (a proper subset of B1; B1 kept, tagged `b1_grouping_kept`) 1,990 stand. Class 3 (readers differ) 2,393, class 4 (readers agree outside B1) 837 and class 5 (no B1 grouping) 58 are contested: 3,288 items. For B4b, the two readers stay DeepSeek V4.1 Flash; a third reader per item from an OpenAI model is a separate arm, reported apart, never pooled, with no Claude reader. The handler sets that arm in `arm.json` before B4b.

**Policy** (`notes-B4.md`): confidence counts for nothing; my B1 grouping is a third placement; readings are blinded as A and B in seeded order. The transmission rows are in `transmission-B4.md`.

**The packets,** in `out/_adjudication-B4/`, chunks of 25: packet 1 491 (gloss-only, G01, G02); packet 2 447 (G03 to G06); packet 3 500 (G07, the first 254 of G08); packet 4 461 (the last 6 of G08, G09 to G11); packet 5 409 (G12 to G14); packet 6 500 (G15 to G19, part of G20); packet 7 480 (the rest of G20, G21). Each packet's conflicts pass runs over its notes first; `coder_conflicts.jsonl` holds CC-001 to CC-036.

**The tools,** in `out/_analysis/`: `b4_rule_append.py` (a dry run, then `--write`; `--replace` corrects a ruled line and keeps the old ledger); `b4_own_support_check.py --leg <leg>` after every chunk; `b4_scheme.py`; `b4_packet_pairs.py`; after each packet `b4_assign_final.py --write`, `b4_packet_summary.py --packet N --write`, `b4_cumulative.py`, `b4_named_neither_split.py`, `b4_packet_detail.py` and `b4_agreement_range.py`; `b4_br_tag_draft.py` for boundary tags.

**Packets 1 to 3** (B4a-01 to B4a-03). Agreement after the ruling rose in packets 1 and 2 (0.633, 0.603) and fell in packet 3 (0.473 against 0.475 before). Packet 3 placed three themes in 201 of 500 rulings and a theme no placement held in 157; that is what QB4-001 asked about.

**Packet 4, ruled at B4a-04.** 461 rulings: genuine-joint 219, scheme-ambiguous 84, author-error 75, item-is-a-bag 53, author-disagrees 17, reader-error 13; unresolved 10; named_neither 222. Worst themes: T3-021 24 (20 of them the homeland flag's repair on its `must_not_show`), T3-005 10, T3-073 9, T3-027 7. Agreement before 0.519, after 0.562. Items 1 to 400: after 0.536 against 0.512 before, a theme no placement held in 133. Items 401 to 461, under J's rule: after 0.726 against 0.566, none beyond the placements; they are G11 only, so the rise is not the rule's effect alone. Class 4 turned toward the readers: their list taken in 64, a B1 theme kept in 32.

**The four packets together** (`adjudication_report.md`, interim): 1,899 rulings; genuine-joint 802, scheme-ambiguous 375, author-error 275, item-is-a-bag 193, author-disagrees 158, reader-error 96; unresolved 79; named_neither 741; agreement before 0.503, after 0.565, not a reliability figure. B2's predicted pair 1 (T3-005|T3-021) held with 37 items; five unpredicted G09 neighbours split four items or more.

**Boundaries ruled, to carry into the next packets** (each a paragraph in `out/_adjudication-B4/boundaries.md`).
- **Packet 1.** A change to the sub made by moderators or by members flooding it is T3-023; members' fakes in an unchanged sub are T3-001. T3-031 needs the canvas.
- **The counting rule** (T3-002, T3-033, T3-038). Calls, volunteers and answers count toward T3-002; placing and reports of the work's state toward T3-038; a new mark named toward T3-033. Ties: T3-038 when the work was placed; else T3-002 when the mark was chosen, T3-033 when not.
- **Packet 2.** Coordinates, templates, order or how-to are directions (T3-070). For T3-005 the attack must be in the words. Corrections to match the design are T3-004. Following the current plan is T3-091. For T3-153 another room must be in the chat. Teaching how to place a pixel is T3-016.
- **Packet 3.** A further piece once a mark stands is T3-041. Colours, outline, a detail inside, the planned size and corrections are T3-004. A subject offered counts toward T3-033 until one is chosen. A link to finished work is T3-026. The sub's name is T3-169. A mark the room did not know of is T3-082.
- **Packet 4.** An attack in the words answered as a fight is T3-005; watching or fixing is T3-021; a full tie places both, scheme-ambiguous on T3-005's `decide_when_both`. A report with a call is T3-005, without one T3-073. The same spot rebuilt is T3-021; a move after a loss is T3-022, a spot changed before the mark stands T3-020. T3-027|T3-028: the larger part leads; a script to wreck another room's work is not T3-028. Bots named behind damage while placing are T3-087, bots judged unfair T3-027. A script changed to spare a neighbour is T3-168. Glitches used to place more are T3-088; accounts handed to another's bot T3-120.
- **Readings applied:**
  - the homeland flag: its build, size, spot, repair and calls for hands are T3-065, emblems T3-113; an attack on it T3-005, watching it T3-021, night watch T3-141; a reader's T3-004, T3-020, T3-021 or T3-041 on it is scheme-ambiguous on that theme's `must_not_show`;
  - a call to fight is T3-005; a call to defend or protect with no attack in the words is T3-002;
  - a smaller version of the same mark is T3-004; T3-069 only when a piece is dropped for another; T3-042 when growth is set aside;
  - finished and celebrated is T3-009; up, still there or "for now" is T3-026;
  - doubting a damage was the room's own is T3-087; an organised room disowning rogue placers T3-188; friendly work taken for an attack T3-170; blame after the close T3-058;
  - T3-084 requests received; T3-062 calls to communities; T3-035 permission asked of a host; T3-099 relying on a bigger room; T3-068 another's mark converted; T3-061 a neighbour's space taken; T3-171 a colour faction spreading; T3-130 national politics.
- **Gaps carried, each unresolved:** April Fools play not posted as true (T3-001 `must_show`); another sub's change (T3-023 `must_show`); moderators applying standing rules to non-canvas posts (T3-063 `must_show`, CC-004); a bot claim with no fairness in question and no damage traced while placing (T3-027 `decide_when_both`).

## Stage B3, in short

B3's packets: at most 15 items and 180,000 bytes, fleet ids only (QB3-001, QB3-002). The fleet ran 1,212 batches, one reader each, R = 2. The assembly of record: `assign_raw.jsonl` 17,653 lines and `b3_classes.jsonl`. Figures: gold fidelity 0.645 against B2's 0.631; agreement Jaccard 0.786 and alpha 0.782, at the stability floor; G18 the family that agreed least; the multi rate 0.158. Waivers QB3-004 and QB3-005 are in `return_waivers.jsonl`.

## Stage B2, in short

Rounds 1 to 3 and gold: fidelity 0.594, 0.639, 0.682, 0.624; pairwise 0.733, 0.718, 0.728, 0.818. Stability 0.807 is the floor every later figure is read against. The frozen scheme: `scheme_final.jsonl` (197 themes; 183 main, 14 rare), `families.jsonl` (21), `gate_checks.jsonl` (496 pairs).

## J's rulings that bind (carry them)

- **Bags.** No one cuts the bags (J, 12:24 Berlin). A bag stays one item: one theme placed, its others under `also_present`, each with three concepts of its own at least. `out/recut/WITHDRAWN.json` keeps the withdrawn split out of every view.
- **The bound (J, 13:47).** `also_present` names "twenty themes at most", each with three concepts of its own.
- **The not-flagged bag (J, QB2-013).** With no other theme at the three-concept floor, `item_is_a_bag` is false and `also_present` `{}`.
- **Fleet ids (J, 09:14 and 12:15).** Packets carry only fleet ids; returns are translated back before scoring; my files keep room ids.
- **Codes by item (J, QB2-009).** Each MANIFEST entry carries `codes_by_item`.

## Standing words from J and the PI (carry into every head)

**J's words for B1 (7 October 2026):** "national elements are very important here"; "we need to get as much variance on organizing behavior early on so that later we have enough to create the model". National, political and conflict content is study material, named as plainly as any other. **The handler's rule:** a choice to leave out or soften content for any reason other than the study's goes to J first with `mem.py ask`, and the content stays meanwhile.

**J on reading (11 October, 16:54 Berlin).** Stop cutting room reads to a line length. Read room lines whole. Page a long read by line ranges or offset, never by truncating lines. Use `--width N` on a `mem.py` read if a clip is ever needed; the guard refuses `cut -c` after `mem.py`.

**J on asking (11 October, 17:01 Berlin).** Ask J with `mem.py ask` whenever a question is needed; asking does not stop the run.

**The PI's clarifications (8 October, approved by J):** the thresholds are the design's heuristic; the rule is unchanged.

**How to work, from J (8 October, 23:45 Berlin, "can you do a hot change for the batching?"; relayed by the handler at 22:03Z; carry this paragraph into every head).** A change in how I work, not in what I read or decide. Fewer turns. When two or more tool calls do not depend on each other's output, make them in one turn. Chain ordered commands in one Bash call with &&, so that a failure stops the rest; for example, the `mem.py log` or note just decided, then the next `mem.py codes`. Never put a write in the same turn as the read it depends on. Never run two writes to the same file as separate parallel calls. Keep one room's material per read, as now. Every tool still writes its own record; nothing about what I read or decide changes.

**Two rules from J at B1b-29 (through the handler, 20:10Z; carry them into every head).** Write rule 0 lines and bags with `b1_multiplace_write4.py` and `b1_bags_from_file2.py`, not the old scripts, which made one `mem.py` call per row of the whole table and grew to 8.5 minutes a write. Never end a turn while a job runs in the background; run every write and check in the foreground.

## The pilot's declarations (from `notes-B2.md`)

- **Agreement:** Jaccard on placement sets (`["T3-004"]` against `["T3-004","T3-011"]` scores 0.5). Fidelity is mean Jaccard against my set. Alpha uses distance 1 − Jaccard, chance over the round's pooled sets. Primary exact agreement is reported beside, never in place.
- **Gold:** 40 items in `gold_items.jsonl`, never shown to a reader.

## The scheme

`scheme_final.jsonl` holds 197 themes (183 main, 14 rare, flagged there) in 21 families. It is frozen: stage B4 logs defects and never edits it.

## Open, carried

- **From B1.** The ruling on testing G13, G14 and G15 as one index page. The B1d leftovers: 106 (line, kind) pairs over 81 episode lines whose kinds none of their rooms holds; seven pairs of lines telling one event; E989; the cfb and finland records; shared-member counts that may include AutoModerator; the 76 themes holding both T3-005 and T3-021 acts; T3-149 and T3-150 members that may hold T3-195; kinds left out of bags. The second-order theme the scheme handles worst: argentina t06.
- **Distinctions** (none filed in `_questions/`): who started the work; wars told twice; rivals who turn partners (E1076, E1122, E1142, E1318); whose flag a shared flag is (E1118); records that disagree on who attacked, on promises, truces, bots and design changes; who drove a bot and why it left a work (E1025); a room's own scripts barring it from sparing a neighbour (E843), or wrecking a protectorate it then rebuilt (E1209); one member on both sides of a quarrel (E820, E947); objections to altering the final image (T3-054 or T3-105).
- **The bag count.** J counts 841 B1 bags; an older head said 846. Not reconciled.
- **From B4a-01 to B4a-03.** Single-concept second themes were not added evenly (magictcg t09). T3-092's own example contradicts its discriminator against T3-060 (bangtan t10).
- **From B4a-04.** The 378 rulings to re-rule. T3-021's `must_not_show` does not send the homeland flag's repair to T3-065. T3-089's `must_show` overlaps T3-168's. T3-088's `decide_when_both` does not say whether a concept holding both a script and accounts counts. bakchodi t09's bag lists T3-006, which no reading named; check it under rule (1) at the re-ruling.

## Ledgers at this close

- B1: `scheme_current.jsonl`, `families.jsonl` (21), `confusions.md` (19 pairs), `findings.jsonl` (2), `episodes-B1.jsonl` (1,341).
- B2: `notes-B2.md`, `pilot_report.md`, `stability-B2.md`, `handback-B2.md`, `author_items.jsonl` (50), `gold_items.jsonl` (40), `scheme_final.jsonl` (197), `scheme_edits.jsonl` (306), `gate_checks.jsonl` (519 lines).
- B3: `notes-B3.md`, `RETURN-B3.md`, `batches-B3.jsonl` (1,212), `_packets-B3/`, `assign_raw.jsonl` and `assign_pass2.jsonl` (17,653 each), `multiplacement_log.jsonl` (3,171), `predicted_confusion-B3.jsonl` (1,180), `b3_classes.jsonl` (7,844), `defects.jsonl` (63), `return_waivers.jsonl` (74), `handback-B3.md`.
- B4: `notes-B4.md`; `transmission-B4.md`; `coder_conflicts.jsonl` (36); `disagreements.jsonl` (1,899; older versions kept as `disagreements.superseded-*.jsonl`); `assign_final.jsonl` (7,844: class 1 2,566, class 2 1,990, ruled 1,899, pending 1,389); `adjudication_report.md` (interim, packets 1 to 4); `out/_adjudication-B4/` (seven packets, `boundaries.md`, each ruled packet's drafts, revisions and `summary.md`).
- Asks QB2-001 to QB2-014, QB3-001 to QB3-005 and QB4-001 are answered.

## Rules kept

- Never type an id, an order or a name from memory; check with `jq` or a script. Never log a write before the tool answers. Count a ledger's lines after appending.
- There is no `--kind close` and no `--kind episode`; log those as notes.
- A question to J is `mem.py ask "<question>" --assume "<meanwhile>"`. Read an answer with `mem.py asks <id>`.
- Never put a placeholder or a no-op in a command. Never put an Edit or Write and the read or dry run that checks it in one turn. Count the head's words before the closing line, not after.
- Never write an id-like token the run does not define in the head, such as a D or a P followed by digits: `done.sh` reads it as an unresolved link.
- The permission check refuses: "=w="; shell for and while loops, and words beginning "for_"; shell functions, brace groups and heredocs; awk with system() or `$` fields; a variable set from `$(...)`, and some `python3 -c` scripts; jq with a `test()` regex, and env-var prefixes; cat or jq on `out/diary/`; `cut -c`, `cut -b` and `colrm` after `mem.py`, `cite.py` or a helper (use `--width`). Write a script file in `out/_analysis/` instead.
- `mem.py` pages long output; fetch the rest with `--offset` before trusting a count. A Bash output over about 30 KB is saved where I cannot read it; page it.
- After a compaction the guard requires the head and stage file read again and the exact line "compacted; head reconciled" through `mem.py log --kind note`, in a call of its own, before any other write, a draft file included.
- In B4: a ruling never cites a room note; reader-error never where both readers made the same placement; T3-063 takes canvas posts only; a correction goes through `b4_rule_append.py --replace`, never a hand edit. An author-disagrees or reader-error quote is a concept id. Reading A and reading B are seeded per item, so a ruling never refers to "reader A" of another item.

## The next comparison

B4a-05 first re-rules the 378 lines that place a theme no reading held, under J's rulings, with `--replace`; it then reruns the after-packet tools for packets 1 to 4 and rewrites the report's figures, so all seven packets are ruled one way. Then packet 5 (409 items, G12 to G14) is ruled under the same rulings, its conflicts pass first. After packet 7: the full `adjudication_report.md`, then B4b, the blind sample, compared against the stability floor 0.807 and B3's agreement 0.786.
