# Head, claude-v43-1

Under 3,000 words, rewritten whole at every close. Last written at B4a-05, 2026-10-13 (UTC). Stage B4 is open: packets 1 to 5 of 7 of the adjudication are ruled. The next leg is B4a-06: packet 6.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1 is closed. Stage B1 (the third-order scheme, 197 themes in 21 families), B2 (the pilot) and B3 (the fleet) are done. Stage B4: the adjudication runs one packet a leg; packets 1 to 5 are ruled (2,308 of 3,288 contested items; 980 remain).

## J's rulings on how a ruling is made (13 October; carry them)

- **QB4-001, answered (J, 06:43 Berlin):** "Ask it to stop. The point is to try to adjudicate. I imagine that the additions are really just the analyst trying to be nice. And not go back on what others said".
- **J's rulings (06:45 and 06:47 Berlin):** (1) The placements are the readers' and the analyst's (my B1). A ruling chooses among those placements and adds no theme beyond them. (2) A ruling takes the union of placements only when it names, for each theme it keeps, the separate concept that carries it; otherwise it chooses. (3) Re-rule the items in packets 1 to 4 whose ruling held a theme no placement held, keeping the superseded ledger. Done at B4a-05.
- **J's ruling on also_present (09:09 Berlin), through the PI:** rule (1) extends to `also_present`, which lists only themes that a reader or my B1 named, in new rulings and in the ledger's existing entries.
- **QB4-002, answered (J, 09:20 Berlin):** "yes. A theme a reader listed under its own also_present counts as named by that reader. also_present may list themes a reader placed, a reader listed under its own also_present, or your B1 named; nothing else."

**How I apply them (rule 0 inside the placements).** The placed themes are reading A's, reading B's and my B1's. A concept counts toward a placed theme when that theme's `must_show` takes it and no field sends it to another placed theme; a `must_not_show` pointing to an unplaced theme does not stop it; otherwise the concept is left out and named in the why. Order by concept count, ties by how many of the three placements hold the theme; at most three. A one- or two-concept theme is kept only when it leads its level on placements; a tie at a level with equal placements keeps none and ends the order; a tie at the very top places all tied themes; themes of three concepts or more tied on placements at the limit of three are left out together. A bag needs four placed themes with three concepts each; its `also_present` lists only placed themes. Unresolved where no placement's test takes the material.

## Stage B4 (B4a-01 to B4a-05)

**The selection (the PI at 21:19Z on 12 October, J's amended stage file).** `b3_classes.jsonl` holds J's five classes. Class 1 (readers agree, equal to B1) 2,566 and class 2 (a proper subset of B1; B1 kept, tagged `b1_grouping_kept`) 1,990 stand. Class 3 (readers differ) 2,393, class 4 (readers agree outside B1) 837 and class 5 (no B1 grouping) 58 are contested: 3,288 items. For B4b, the two readers stay DeepSeek V4.1 Flash; a third reader per item from an OpenAI model is a separate arm, reported apart, never pooled, with no Claude reader. The handler sets that arm in `arm.json` before B4b.

**Policy** (`notes-B4.md`): confidence counts for nothing; my B1 grouping is a third placement; readings are blinded as A and B in seeded order. The transmission rows are in `transmission-B4.md`.

**The packets,** in `out/_adjudication-B4/`, chunks of 25: packet 1 491 (gloss-only, G01, G02); packet 2 447 (G03 to G06); packet 3 500 (G07, part of G08); packet 4 461 (the rest of G08, G09 to G11); packet 5 409 (G12 to G14); packet 6 500 (G15 to G19, part of G20); packet 7 480 (the rest of G20, G21). Each packet's conflicts pass runs over its notes first; `coder_conflicts.jsonl` holds CC-001 to CC-048.

**The tools,** in `out/_analysis/`: `b4_rule_append.py` (a dry run, then `--write`; `--replace` corrects a ruled line and keeps the old ledger); `b4_own_support_check.py --leg <leg>` after every chunk; `b4_scheme.py <ids> --fields=must_show,must_not_show,decide_when_both`; `b4_packet_pairs.py`; after each packet `b4_assign_final.py --write`, `b4_packet_summary.py --packet N --write`, `b4_cumulative.py`, `b4_named_neither_split.py`, `b4_packet_detail.py`, `b4_agreement_range.py`; `b4_br_tag_draft.py`; `b4_ap_scan.py`. A draft line: `{"n", "r", "t", "c", "q", "f", "th", "br", "sup", "ap", "u", "w"}`.

**Corrections at B4a-05.** The 378 rulings of packets 1 to 4 that placed a theme no placement held were re-ruled through `--replace`; agreement after over those packets rose from 0.565 to 0.628, named_neither fell from 741 to 485. Then 128 `also_present` lines (273 themes) were corrected; four bags re-ruled by hand (archlinux t01, ireland t04, starvstheforcesofevil t02, de t02); 84 lines keep a theme only a reader's own `also_present` named.

**Packet 5, ruled at B4a-05.** 409 rulings: genuine-joint 291, author-disagrees 44, author-error 41, reader-error 16, scheme-ambiguous 14, item-is-a-bag 3; unresolved 3 (linux t03, survivor t26, PurplePixels t13); named_neither 131, all from my B1 alone. Agreement before 0.467, after 0.612. Class 4: the readers' list in 42, a B1 theme kept in 44. The sentence that failed most: T3-006's discriminator against T3-061 (4). B2's predicted pairs 2, 11, 12 and 13 split readers; T3-006|T3-061 and the help pairs were not predicted.

**The five packets together** (`adjudication_report.md`, interim): 2,308 rulings; genuine-joint 1,117, scheme-ambiguous 350, author-error 334, author-disagrees 208, item-is-a-bag 185, reader-error 114; unresolved 85; named_neither 616; agreement before 0.496, after 0.625, not a reliability figure. Fields: must_show 196, discriminators 78, must_not_show 48, decide_when_both 28. Worst themes: T3-033 33, T3-017 30, T3-023 25, T3-001 24. Class 4 took the readers' list in 329 and kept a B1 theme in 220. Labels carried as they stand: 12 packet 4 author-error rulings keep a B1 theme; 2 packet 2 author-disagrees take the readers' list.

**Boundaries ruled, to carry** (paragraphs in `out/_adjudication-B4/boundaries.md`; each sends a concept to its theme only where a placement holds it).
- **Packets 1 to 3.** T3-023 is a change to the sub; T3-001 members' fakes. T3-031 needs the canvas. Calls, volunteers and answers count toward T3-002, placing and progress toward T3-038, a new mark toward T3-033. Directions are T3-070; one plan kept T3-091; T3-153 needs another room in the chat. A further piece once a mark stands is T3-041; the look and size T3-004.
- **Packet 4.** An attack in the words answered as a fight is T3-005; watching or fixing T3-021; a full tie places both. A report with a call is T3-005, without one T3-073. A move after a loss is T3-022. Bots named behind damage are T3-087, bots judged unfair T3-027. Glitches used to place more are T3-088.
- **Packet 5.** A fight, threat, peace or truce in the words is T3-149; lines and space with none T3-010. The neighbour in the exchange is T3-010; sparing by the room's own choice T3-024. Destroying is T3-006, taking space for the room's flag T3-061. Help sent with nothing asked is T3-011; help for help or room T3-151, only when the return is named.
- **Readings applied:** doubting a damage was the room's own is T3-087; an organised room disowning rogue placers T3-188; friendly work taken for an attack T3-170; a request for help T3-084; a request for space to its holder T3-035; a host ruling on many requests T3-162, a single grant T3-012; a member's effort moved to another build T3-137; T3-150 keeps help traded when a fight is the frame; T3-099 needs the bigger room's size in the words; T3-078 kin felt in the words; T3-149 rooms already in contact.
- **Gaps carried, each unresolved:** April Fools play not posted as true (T3-001); another sub's change (T3-023); moderators applying standing rules to non-canvas posts (T3-063, CC-004); a bot claim with no fairness in question (T3-027); one concept joining an outside plan to erase (linux t03).

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
- **The bag count.** J counts 841 B1 bags; an older head said 846. Not reconciled.
- **Defects for stage C1.** T3-092's example against its discriminator (bangtan t10). T3-021's `must_not_show` and the homeland flag. T3-089's `must_show` overlaps T3-168's. T3-088's `decide_when_both` on a script with accounts. From packet 5: T3-010's "overlaps accepted or refused" reaches T3-012's grant (japan t10); an alliance against a third room's work (T3-150 or T3-067, ice_poseidon t15); a refusal grounded in the flood (T3-115 or T3-075, england t05).
- **My doubts.** Rule 0 inside the placements keeps a lone one- or two-concept B1 theme, so class 4 turns toward my B1 (44 of 86 in packet 5) and named_neither stays high (131). If J reads "otherwise it chooses" as asking for fewer unions, the one-concept keep is the rule to change. In theitalyplace t11, requests for room inside a host's flag were left out as T3-035's act, though the T3-010|T3-024 paragraph counts "a request for room" toward T3-010; the ruling's set is the same either way.

## Ledgers at this close

- B1 to B3: `scheme_current.jsonl`, `families.jsonl` (21), `confusions.md` (19 pairs), `episodes-B1.jsonl` (1,341); `notes-B2.md`, `pilot_report.md`, `stability-B2.md`, `gold_items.jsonl` (40), `author_items.jsonl` (50), `scheme_final.jsonl` (197); `notes-B3.md`, `assign_raw.jsonl` (17,653), `multiplacement_log.jsonl` (3,171), `b3_classes.jsonl` (7,844), `defects.jsonl` (63), `return_waivers.jsonl` (74).
- B4: `notes-B4.md`; `transmission-B4.md`; `coder_conflicts.jsonl` (48); `disagreements.jsonl` (2,308; older versions kept as `disagreements.superseded-*.jsonl`, the last 20261013T081847Z); `assign_final.jsonl` (7,844: class 1 2,566, class 2 1,990, ruled 2,308, pending 980); `adjudication_report.md` (interim, packets 1 to 5); `out/_adjudication-B4/` (seven packets, `boundaries.md`, each ruled packet's drafts and `summary.md`; `rerule-B4a-05/` and `rerule-ap-B4a-05/`).
- Asks QB2-001 to QB2-014, QB3-001 to QB3-005, QB4-001 and QB4-002 are answered.

## Rules kept

- Never type an id, an order or a name from memory; check with `jq` or a script. Never log a write before the tool answers. Count a ledger's lines after appending.
- There is no `--kind close` and no `--kind episode`; log those as notes.
- A question to J is `mem.py ask "<question>" --assume "<meanwhile>"`. Read an answer with `mem.py asks <id>`.
- Never put a placeholder or a no-op in a command. Never put an Edit or Write and the read or dry run that checks it in one turn. Count the head's words before the closing line, not after.
- Never write an id-like token the run does not define in the head, such as a D or a P followed by digits: `done.sh` reads it as an unresolved link.
- The permission check refuses: "=w="; shell for and while loops, and words beginning "for_"; shell functions, brace groups and heredocs; awk with system() or `$` fields; a variable set from `$(...)`, and some `python3 -c` scripts; jq with a `test()` regex, and env-var prefixes; cat or jq on `out/diary/`; `cut -c`, `cut -b` and `colrm` after `mem.py`, `cite.py` or a helper (use `--width`). Write a script file in `out/_analysis/` instead.
- `mem.py` pages long output; fetch the rest with `--offset` before trusting a count. A Bash output over about 30 KB is saved where I cannot read it; page it. A `Read` of a chunk file over 25,000 tokens is cut; read it by offset and limit.
- After a compaction the guard requires the head and stage file read again and the exact line "compacted; head reconciled" through `mem.py log --kind note`, in a call of its own, before any other write, a draft file included.
- In B4: a ruling never cites a room note; reader-error never where both readers made the same placement; T3-063 takes canvas posts only; a correction goes through `b4_rule_append.py --replace`, never a hand edit. An author-disagrees, author-error or reader-error quote is a concept id; a scheme-ambiguous quote is the failing sentence of the named field. Reading A and reading B are seeded per item. Class 4: the readers' list taken is author-error, a B1 theme kept author-disagrees; class 3 with several themes, or one theme chosen on a tie, is genuine-joint.

## The next comparison

B4a-06 rules packet 6 (500 items, G15 to G19 and part of G20) under J's rulings and rule 0 inside the placements: its conflicts pass first, then `b4_packet_pairs.py --packet 6` and a boundary paragraph for each pair that splits five items or more, then the chunks. Watch whether class 4 keeps turning toward my B1 and whether G15's alliances and truces split as G14's deals did. After packet 7: the full `adjudication_report.md`, then B4b, the blind sample, compared against the stability floor 0.807 and B3's agreement 0.786.
