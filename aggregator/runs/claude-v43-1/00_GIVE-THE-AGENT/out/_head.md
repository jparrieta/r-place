# Head, claude-v43-1

Under 3,000 words, rewritten whole at every close. Last written at B4a-06, 2026-10-13 (UTC). Stage B4 is open: packets 1 to 6 of 7 of the adjudication are ruled. The next leg is B4a-07: packet 7.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1 is closed. Stage B1 (the third-order scheme, 197 themes in 21 families), B2 (the pilot) and B3 (the fleet) are done. Stage B4: the adjudication runs one packet a leg; packets 1 to 6 are ruled (2,808 of 3,288 contested items; 480 remain, the rest of G20 and G21).

## J's rulings on how a ruling is made (13 October; carry them)

- **QB4-001, answered (J, 06:43 Berlin):** "Ask it to stop. The point is to try to adjudicate. I imagine that the additions are really just the analyst trying to be nice. And not go back on what others said".
- **J's rulings (06:45 and 06:47 Berlin):** (1) A ruling chooses among the placements (reading A, reading B, my B1) and adds no theme beyond them. (2) It takes the union only when it names, for each theme it keeps, the separate concept that carries it; otherwise it chooses. (3) Re-rule packets 1 to 4's rulings that held a theme no placement held. Done at B4a-05.
- **also_present (J, 09:09 Berlin) and QB4-002 (09:20):** `also_present` lists only themes a reader placed, a reader listed under its own `also_present`, or my B1 named.
- **QB4-003, answered (J, 11:29 Berlin):** "count them. Themes a reader listed under its own also_present count in the bag test. Apply it to packet 6 and to the 43 rulings in packets 1 to 5 that out/_analysis/b4_bag_named_check.py lists, keeping the superseded ledger." Done at B4a-06.
- **Lone B1 themes (J, 12:28 Berlin, through the PI):** "Whatever the agent feels more comfortable with. They can also adapt the code definition if needed". I chose: in class 4 a theme only my B1 placed stands against the two agreeing readers only with three concepts or more of its own; with fewer it is left out and named in the why; the readers' list stands where its test takes concepts, and where it takes none the item is unresolved. Class 3 unchanged. Applied to packets 1 to 6 at B4a-06.

**How I apply them (rule 0 inside the placements).** A concept counts toward a placed theme when that theme's `must_show` takes it and no field sends it to another placed theme; a `must_not_show` pointing to an unplaced theme does not stop it; otherwise it is left out and named in the why. Order by concept count, ties by placements; at most three. A one- or two-concept theme is kept only when it leads its level on placements; a tie at a level with equal placements keeps none and ends the order; a tie at the very top places all tied themes; a theme alone at its level is kept. **The bag test:** the placed themes and the readers' own `also_present` themes are counted, each with the concepts its `must_show` takes that no placed theme in the ruling holds, read against the test; four themes with three concepts make a bag, which places the largest act a placement holds and lists every other counted theme with three or more under `also_present`; a placed theme with three concepts is never cut by the limit of three. Unresolved where no placement's test takes the material.

## Stage B4 (B4a-01 to B4a-06)

**The selection (the PI at 21:19Z on 12 October, J's amended stage file).** `b3_classes.jsonl` holds J's five classes. Class 1 (readers agree, equal to B1) 2,566 and class 2 (a proper subset of B1; B1 kept) 1,990 stand. Class 3 (readers differ) 2,393, class 4 (readers agree outside B1) 837 and class 5 (no B1 grouping) 58 are contested: 3,288 items. For B4b, the two readers stay DeepSeek V4.1 Flash; a third reader per item from an OpenAI model is a separate arm, reported apart, never pooled, with no Claude reader. The handler sets that arm in `arm.json` before B4b.

**Policy** (`notes-B4.md`): confidence counts for nothing; my B1 grouping is a third placement; readings are blinded as A and B in seeded order. The transmission rows are in `transmission-B4.md`.

**The packets,** in `out/_adjudication-B4/`, chunks of 25: packet 1 491 (gloss-only, G01, G02); packet 2 447 (G03 to G06); packet 3 500 (G07, part of G08); packet 4 461 (G08's end, G09 to G11); packet 5 409 (G12 to G14); packet 6 500 (G15 to G19, part of G20); packet 7 480 (the rest of G20, G21). Each packet's conflicts pass runs over its notes first; `coder_conflicts.jsonl` holds CC-001 to CC-062.

**The tools,** in `out/_analysis/`: `b4_rule_append.py` (dry run, then `--write`; `--replace` corrects a ruled line, keeping the old ledger); `b4_own_support_check.py --leg <leg>` after every chunk; `b4_scheme.py <ids, space-separated> --fields=...`; `b4_packet_pairs.py`; after each packet `b4_assign_final.py --write`, `b4_packet_summary.py --packet N --write`, `b4_cumulative.py`, `b4_named_neither_split.py`, `b4_packet_detail.py`, `b4_agreement_range.py --ranges`; checks `b4_bag_named_check.py` and `b4_lone_b1_check.py`; `b4_bag_view.py --brief`; re-rule builders `b4_bag_draft.py` and `b4_lone_b1_draft.py`. A draft line: `{"n", "r", "t", "c", "q", "f", "th", "br", "sup", "ap", "u", "w"}`.

**Corrections at B4a-06.** QB4-003's revisit read 64 lines: 45 became bags, 19 were kept; four slips outside the list became bags (utaustin t05, japan t05, loliconsunite t02, lebanon t02); chibears t10 gained reader A's T3-050 after packet 6. The lone-B1 rule changed 130 class 4 lines (author-error 83, author-disagrees 40, scheme-ambiguous 7; unresolved 30).

**Packet 6.** 500 rulings: genuine-joint 256, author-error 83, scheme-ambiguous 71, author-disagrees 51, item-is-a-bag 20, reader-error 19; unresolved 49; named_neither 145, all from my B1. Agreement before 0.454, after 0.600. Class 4: the readers' list 87, a B1 theme kept 32, unresolved 15. The sentences that failed most: T3-017's discriminator against T3-031 (24) and T3-001's (8), the canvas condition.

**The six packets together** (`adjudication_report.md`, interim): 2,808 rulings; genuine-joint 1,348, author-error 482, scheme-ambiguous 421, item-is-a-bag 238, author-disagrees 186, reader-error 133; unresolved 161; named_neither 649; agreement before 0.489, after 0.642, not a reliability figure. Fields: must_show 227, discriminators 110, must_not_show 56, decide_when_both 28. Worst themes: T3-017 54, T3-033 34, T3-001 32, T3-023 26, T3-004 26. Class 4 (719): the readers' list 493, a B1 theme kept 144 (each with three concepts or more), unresolved 69.

**Boundaries ruled, to carry** (`out/_adjudication-B4/boundaries.md`; each sends a concept to its theme only where a placement holds it).
- **Packets 1 to 5.** T3-023 is a change to the sub, T3-001 members' fakes. Calls and answers count toward T3-002, placing toward T3-038, a new mark toward T3-033, a further piece toward T3-041, directions toward T3-070. An attack answered as a fight is T3-005, watching or fixing T3-021. A fight, threat, peace or truce in the words is T3-149; lines and space with none T3-010. Destroying is T3-006, taking space T3-061. Help sent with nothing asked is T3-011; help for help or room T3-151 when the return is named.
- **Packet 6.** A joke with the canvas in the words is T3-031; with none T3-017, scheme-ambiguous on T3-017's discriminator. Playing inside the sub's April Fools change stays T3-023. A taunt at a rival community is T3-050 even as a joke. A figure worked out with a reason is T3-018; a bare name for a neighbour's figure T3-052; a mock reading kept up as a joke T3-031. An alliance or promise to defend is T3-150.
- **Readings:** T3-086 the community's own quarrel; T3-130 national politics; T3-080 a political symbol argued over; T3-081 a fight in a nation's real war history, not fandom war talk (T3-135); T3-154 victory claimed, T3-050 mockery with none; T3-142 jokes about a people; T3-016 the event, its rules, the heat map; a glitch explained T3-016, coped with T3-074, used T3-088; T3-105 records, T3-057 remakes; a bare title naming r/place shows no act.
- **Gaps carried, each unresolved:** April Fools play not posted as true (T3-001); another sub's change (T3-023); moderators applying standing rules to non-canvas posts (T3-063, CC-004); a bot claim with no fairness in question (T3-027).

## Stage B3 and B2, in short

B3: fleet ids only (QB3-001, QB3-002); 1,212 batches, R = 2; `assign_raw.jsonl` 17,653 lines and `b3_classes.jsonl`. Gold fidelity 0.645; agreement Jaccard 0.786, alpha 0.782; G18 agreed least. B2: gold fidelity 0.624 and pairwise 0.818; stability 0.807 is the floor every later figure is read against.

## J's rulings that bind (carry them)

- **Bags.** No one cuts the bags (J, 12:24 Berlin). A bag stays one item: one theme placed, its others under `also_present`, each with three concepts of its own and named by a reader or my B1. `out/recut/WITHDRAWN.json` keeps the withdrawn split out of every view.
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

- **From B1.** The ruling on testing G13, G14 and G15 as one index page. The B1d leftovers: 106 (line, kind) pairs over 81 episode lines; seven pairs of lines telling one event; E989; the cfb and finland records; shared-member counts that may include AutoModerator; the 76 themes holding both T3-005 and T3-021 acts; T3-149 and T3-150 members that may hold T3-195. The second-order theme the scheme handles worst: argentina t06.
- **Distinctions** (none filed in `_questions/`): who started the work; wars told twice; rivals who turn partners (E1076, E1122, E1142, E1318); whose flag a shared flag is (E1118); who drove a bot (E1025); a room's own scripts barring it from sparing a neighbour (E843) or wrecking a protectorate (E1209); one member on both sides (E820, E947).
- **The bag count.** J counts 841 B1 bags; an older head said 846. Not reconciled. 26 older bags in packets 1 to 5 could list more named themes (QB4-003 named 43); the packet 4 item 197 `also_present` note.
- **Defects for stage C1.** T3-017's and T3-001's discriminators put the room's jokes "on the day" in T3-031, against T3-031's canvas condition. T3-018's "whose character a figure is" reaches bare naming (T3-052). T3-052 presumes the room has a mark. T3-086's "rivalry from the community's own life" against T3-050's "internal quarrel". T3-023 does not say whether another sub's change counts. Earlier: T3-092's example (bangtan t10); T3-021's `must_not_show` and the homeland flag; T3-089 against T3-168; T3-088's `decide_when_both`; T3-010 against T3-012 (japan t10); T3-150 or T3-067 (ice_poseidon t15).
- **My doubts.** The three-concept floor of the lone-B1 rule is my choice, and class 3 still keeps one-concept themes of mine (most of packet 6's named_neither). The level rule keeps a theme alone at a lower level after a larger one was dropped above it (cmu t05). The canvas condition read from the words or from the thread (bakchodi t19). In serbia t04 I named the 1999 war where the words give the date and the burning refinery.

## Ledgers at this close

- B1 to B3: `scheme_current.jsonl`, `families.jsonl` (21), `confusions.md` (19 pairs), `episodes-B1.jsonl` (1,341); `notes-B2.md`, `pilot_report.md`, `stability-B2.md`, `gold_items.jsonl` (40), `author_items.jsonl` (50), `scheme_final.jsonl` (197); `notes-B3.md`, `assign_raw.jsonl` (17,653), `multiplacement_log.jsonl` (3,171), `b3_classes.jsonl` (7,844), `defects.jsonl` (63), `return_waivers.jsonl` (74).
- B4: `notes-B4.md`; `transmission-B4.md`; `coder_conflicts.jsonl` (62); `disagreements.jsonl` (2,808; older versions kept as `disagreements.superseded-*.jsonl`, the last 20261013T111959Z); `assign_final.jsonl` (7,844: class 1 2,566, class 2 1,990, ruled 2,808, pending 480); `adjudication_report.md` (interim, packets 1 to 6); `out/_adjudication-B4/` (seven packets, `boundaries.md`, each ruled packet's drafts and `summary.md`; the re-rule folders of B4a-05 and B4a-06).
- Asks QB2-001 to QB2-014, QB3-001 to QB3-005, QB4-001 to QB4-003 are answered.

## Rules kept

- Never type an id, an order or a name from memory; check with `jq` or a script. Never log a write before the tool answers. Count a ledger's lines after appending.
- There is no `--kind close` and no `--kind episode`; log those as notes.
- A question to J is `mem.py ask "<question>" --assume "<meanwhile>"`. Read an answer with `mem.py asks <id>`.
- Never put a placeholder or a no-op in a command. Never put an Edit or Write and the read, dry run or validator run that checks it in one turn. Count the head's words before the closing line.
- Never write an id-like token the run does not define in the head, such as a D or a P followed by digits: `done.sh` reads it as an unresolved link.
- The permission check refuses: "=w="; shell for and while loops, and words beginning "for_"; shell functions, brace groups and heredocs; awk with system() or `$` fields; a variable set from `$(...)`, and some `python3 -c` scripts; jq with a `test()` regex, and env-var prefixes; cat or jq on `out/diary/`; `cut -c`, `cut -b` and `colrm` after `mem.py`, `cite.py` or a helper (use `--width`). Write a script file in `out/_analysis/` instead. `.git` is read-denied.
- `mem.py` pages long output; fetch the rest with `--offset`. A Bash output over about 30 KB is saved where I cannot read it; page it. A `Read` of a chunk file over 25,000 tokens is cut; read it by offset and limit.
- After a compaction the guard requires the head and stage file read again and the exact line "compacted; head reconciled" through `mem.py log --kind note`, in a call of its own, before any other step.
- In B4: a ruling never cites a room note; reader-error never where both readers made the same placement; T3-063 takes canvas posts only; a correction goes through `--replace`, never a hand edit. An author-disagrees, author-error or reader-error quote is a concept id; a scheme-ambiguous quote is the failing sentence of the named field. Class 4: the readers' list taken is author-error, a B1 theme kept author-disagrees; class 3 with several themes, or one chosen on a tie, is genuine-joint; class 5 with a bare title is unresolved, author-disagrees. `adjudication_report.md` names both themes of every `boundary_ruling` pair, or `validate.py` fails.

## The next comparison

B4a-07 rules packet 7 (480 items, the rest of G20 and G21) under J's rulings, rule 0 inside the placements, the bag test after QB4-003 and the class 4 lone-B1 rule: its conflicts pass first, then `b4_packet_pairs.py --packet 7` and a boundary paragraph for each pair that splits five items or more, then the chunks. Watch whether B2's pairs 9 (T3-009|T3-073) and 14 (T3-009|T3-043) split readers, and whether G20's canvas condition keeps failing. After packet 7: the full `adjudication_report.md`, then B4b, the blind sample, compared against the stability floor 0.807 and B3's agreement 0.786.
