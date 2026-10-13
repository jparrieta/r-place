# Head, claude-v43-1

Under 3,000 words, rewritten whole at every close. Last written at B4a-03, 2026-10-13 (UTC). Stage B4 is open: packets 1 to 3 of 7 of the adjudication are ruled. The next leg is B4a-04, packet 4.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1 is closed. Stage B1 (the third-order scheme, 197 themes in 21 families) is done. Stage B2, the pilot, is done (`pilot_report.md`, `stability-B2.md`, `handback-B2.md`). Stage B3, the fleet, is done (`handback-B3.md`). Stage B4: the adjudication runs one packet a leg; packets 1 to 3 are ruled (1,438 of 3,288 contested items).

## Stage B4 (from B4a-01 to B4a-03)

**The selection (the PI at 21:19Z on 12 October, J's amended stage file).** `tools/assemble.py` wrote `b3_classes.jsonl` with J's five classes. Class 1 (readers agree, equal to B1) 2,566 and class 2 (readers agree, a proper subset of B1; B1 kept, tagged `b1_grouping_kept`) 1,990 stand. Class 3 (readers differ) 2,393, class 4 (readers agree outside B1) 837 and class 5 (no B1 grouping) 58 are contested: 3,288 items. For the blind sample at B4b, J agreed the two readers stay DeepSeek V4.1 Flash, and a third reader per item from an OpenAI model is a separate arm, reported apart, never pooled, with no Claude reader. The handler sets that arm in `arm.json` before B4b.

**Before the first ruling (B4a-01).** The gold drop left `assign_final.jsonl` at 7,844 lines, equal to `assignment_items_expected`. The transmission rows are in `transmission-B4.md`. Policy in `notes-B4.md`: confidence counts for nothing; my B1 grouping is a third placement; class 4 is author-error when the readers' list is taken and author-disagrees when a B1 theme is kept; readings are blinded as A and B in seeded order.

**The packets,** in `out/_adjudication-B4/`, chunks of 25: packet 1 491 (gloss-only, G01, G02); packet 2 447 (G03 to G06); packet 3 500 (G07, the first 254 of G08); packet 4 461 (the last 6 of G08, G09 to G11); packet 5 409 (G12 to G14); packet 6 500 (G15 to G19, part of G20); packet 7 480 (the rest of G20, G21). Each packet's conflicts pass runs over its notes first; `coder_conflicts.jsonl` holds CC-001 to CC-025.

**The tools,** in `out/_analysis/`. `b4_rule_append.py`: a dry run, then `--write`; `--replace` corrects a ruled line in place and keeps the old ledger. It refuses a placed theme only when its concept list equals another's, so run `b4_own_support_check.py --leg <leg>` after every chunk. `b4_scheme.py` prints a theme's tests; `b4_packet_pairs.py` a packet's splitting pairs. After each packet: `b4_assign_final.py --write`, `b4_packet_summary.py --packet N --write`, `b4_cumulative.py`, `b4_named_neither_split.py`, `b4_packet_detail.py`. `b4_br_tag_draft.py` adds a boundary tag with the ruling unchanged.

**Packets 1 and 2** (B4a-01, B4a-02). Packet 1: 491 rulings; scheme-ambiguous 123, reader-error 77; named_neither 84; agreement before 0.486, after 0.633. Packet 2: 447; genuine-joint 215, author-disagrees 65; named_neither 155; before 0.537, after 0.603. Class 4, readers' list taken against a B1 theme kept: 89 and 29, then 53 and 63.

**Packet 3, ruled at B4a-03.** 500 rulings: genuine-joint 231, scheme-ambiguous 106, item-is-a-bag 76, author-error 45, author-disagrees 39, reader-error 3. Class 4: 40 and 37.
- **Counts:** unresolved 7; named_neither 280 (56.0%). 123 add only themes from my B1 grouping; 157 add a theme no placement held (T3-041 27, T3-065 14, T3-002 13).
- **Fields:** must_show 54, must_not_show 26, discriminators 23, decide_when_both 3. 24 of the `must_not_show` failures are the homeland flag or its emblems, which no sibling's `must_not_show` sends to T3-065. **Worst themes:** T3-004 25, T3-033 25 (no "first" in its `must_show`), T3-038 11.
- **Agreement:** before 0.475 mean Jaccard, 0.598 primary match; after 0.473 and 0.535, below before for the first time. In 76 items both readers put T3-038 first, and my rulings kept it first in 27. 201 of 500 rulings place three themes (packet 2: 117 of 447), often with a one- or two-concept theme no placement held. **QB4-001** asks J whether to keep adding those; meanwhile packets 4 to 7 are ruled as packets 1 to 3.
- **Corrections** (`--replace`): catalonia t07, sadboys t03, bisexual t04, kpop t05, seven support fixes, 11 boundary tags.

**The three packets together** (`adjudication_report.md`, interim): 1,438 rulings; genuine-joint 583, scheme-ambiguous 291, author-error 200, author-disagrees 141, item-is-a-bag 140, reader-error 83; unresolved 69; named_neither 519; agreement before 0.498, after 0.566, not a reliability figure.

**Boundaries ruled, to carry into the next packets** (each a paragraph in `out/_adjudication-B4/boundaries.md`).
- **Packet 1 (G01, G02).** T3-001|T3-023: a change to the sub made by moderators, or by members flooding it, is T3-023; members' fakes in an unchanged sub are T3-001. T3-031 needs the canvas. The other G01 pairs stand as written there.
- **The counting rule** (T3-002, T3-033, T3-038). Calls, volunteers and answers ("I'm in", "on it") count toward T3-002. Placing and reports of the work's state, with coordinates of the work in progress, count toward T3-038. A new mark named counts toward T3-033 even when it asks for help. Ties: T3-038 when the work was placed; else T3-002 when the mark was chosen, T3-033 when not. Tag such items with the pair.
- **Packet 2.** T3-002|T3-070: mostly coordinates, templates, order or how-to count as directions. T3-002|T3-005: the attack must be in the words. T3-004|T3-070: corrections to match the design go to T3-004, the template to T3-070. T3-070|T3-091: following the current plan, a stale copy and an official design thread are T3-091. T3-014|T3-153: another room must be in the chat. Teaching how to place a pixel is T3-016.
- **Packet 3.** A further piece once a mark stands is T3-041, its proposal, placing and reports included (T3-033|T3-041, T3-038|T3-041). Lettering beside, objects around and a standing mark made bigger are T3-041; colours, outline, a detail inside, the planned size and corrections are T3-004. A subject offered counts toward T3-033 until one is chosen. Where the work stands is T3-038, templates T3-070, a link to finished work T3-026. The sub's name, its letters included, is T3-169. A known mark located is T3-026; a mark the room did not know of is T3-082.
- **Readings applied:**
  - the homeland flag: its build, size, spot, repair and calls for hands are T3-065, emblems in or beside it T3-113; a reader's T3-004, T3-020 or T3-041 on it is scheme-ambiguous on that theme's `must_not_show`;
  - a design cut down: a smaller or simpler version of the same mark is T3-004; T3-069 only when a piece is dropped for another; T3-042 when growth is set aside; doubt about the hands T3-136. This replaces packet 2's "scaling down to T3-069";
  - finished and celebrated is T3-009 at any time; up, still there or "for now" is T3-026;
  - T3-169 for the sub's name written (T3-044 when bringing visitors is the stated point); T3-084 for requests received; T3-062 for calls posted to communities; T3-035 for permission asked of a host; T3-099 for relying on a bigger room;
  - T3-074 needs a placing trouble while building; a border with no protection stated is T3-004; "defend" with no attacker named is T3-002;
  - T3-137 for an outside plan followed; T3-068 for another's mark converted; T3-061 for a neighbour's space taken; T3-170 for friendly fire and members' own misclicks; T3-171 for a colour faction spreading; T3-196 for former fans; T3-130 for national politics.
- **Gaps carried, each unresolved:** April Fools play not posted as true (T3-001 `must_show`); another sub's change (T3-023 `must_show`); moderators applying standing rules to non-canvas posts (T3-063 `must_show`, CC-004); naming a feature of a faction's ground; a pointer to another sub's thread on the room's work.

## Stage B3, in short

J's rulings QB3-001 and QB3-002 set B2's packet shape: at most 15 items and 180,000 bytes, self-contained, fleet ids only. The fleet ran 1,212 batches, one reader each, R = 2; B0192 and B0927 were rebuilt in fleet-id halves under QB3-003. The gold check after group 1 passed (fidelity 0.637 against 0.625). The assembly of record: `assign_raw.jsonl` 17,653 lines and `b3_classes.jsonl`. Figures: gold fidelity 0.645 against B2's 0.631; agreement Jaccard 0.786 and alpha 0.782, at the stability floor; G18 the family that agreed least; the multi rate 0.158. Waivers QB3-004 and QB3-005 are in `return_waivers.jsonl`.

## Stage B2, in short

Rounds 1 to 3 and gold: fidelity 0.594, 0.639, 0.682, 0.624; pairwise 0.733, 0.718, 0.728, 0.818. Stability 0.807 is the floor every later figure is read against. Readers from round 2: deepseek/deepseek-v4.1-flash, direct, medium effort. Primary match on gold 0.800. Four gold wording defects go to C1: uofmn t01, cuboulder t04, mariokart t04, ireland t12. The frozen scheme: `scheme_final.jsonl` (197 themes; 183 main, 14 rare), `families.jsonl` (21), `gate_checks.jsonl` (496 pairs). The freeze gave T3-002, T3-033 and T3-038 one counting rule (the act with most concepts leads), the sentence I am least sure a stranger reads as I meant; packets 2 and 3 split on it more than on any other.

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
- **From B4a-01 and B4a-02.** Single-concept second themes were not added perfectly evenly (magictcg t09). Class 4's yield fell; the blind sample's adjudicated stratum is the test.
- **From B4a-03.** QB4-001, open. Agreement after fell below before. T3-092's own example "I added a little something for my bias" contradicts its discriminator against T3-060 (bangtan t10). Pairs split that B2 did not predict lead packet 3: T3-004|T3-041 12, T3-033|T3-041 11.

## Ledgers at this close

- B1: `scheme_current.jsonl`, `families.jsonl` (21), `confusions.md` (19 pairs), `findings.jsonl` (2), `episodes-B1.jsonl` (1,341).
- B2: `notes-B2.md`, `pilot_report.md`, `stability-B2.md`, `handback-B2.md`, `author_items.jsonl` (50), `gold_items.jsonl` (40), `scheme_final.jsonl` (197), `scheme_edits.jsonl` (306), `gate_checks.jsonl` (519 lines).
- B3: `notes-B3.md`, `RETURN-B3.md`, `batches-B3.jsonl` (1,212), `_packets-B3/`, `assign_raw.jsonl` and `assign_pass2.jsonl` (17,653 each), `multiplacement_log.jsonl` (3,171), `predicted_confusion-B3.jsonl` (1,180), `b3_classes.jsonl` (7,844), `defects.jsonl` (63), `return_waivers.jsonl` (74), `handback-B3.md`.
- B4: `notes-B4.md`; `transmission-B4.md`; `coder_conflicts.jsonl` (25); `disagreements.jsonl` (1,438; older versions kept as `disagreements.superseded-*.jsonl`); `assign_final.jsonl` (7,844: class 1 2,566, class 2 1,990, ruled 1,438, pending 1,850; older versions kept as `assign_final.superseded-*.jsonl`); `adjudication_report.md` (interim, packets 1 to 3); `out/_adjudication-B4/` (seven packets, `boundaries.md`, each ruled packet's drafts, revisions and `summary.md`).
- Asks QB2-001 to QB2-014 and QB3-001 to QB3-005 are answered. QB4-001 is open.

## Rules kept

- Never type an id, an order or a name from memory; check with `jq` or a script. Never log a write before the tool answers. Count a ledger's lines after appending.
- There is no `--kind close` and no `--kind episode`; log those as notes.
- A question to J is `mem.py ask "<question>" --assume "<meanwhile>"`; `mem.py log --kind ask` writes only a diary line and gives no id. Read an answer with `mem.py asks <id>`.
- Never put a placeholder or a no-op in a command. Never put an Edit and the read or dry run that checks it in one turn. Count the head's words before the closing line, not after.
- Never write an id-like token the run does not define in the head, such as a D or a P followed by digits: `done.sh` reads it as an unresolved link. Name later stages and packet files in words.
- The permission check refuses: "=w="; shell for and while loops, and words beginning "for_"; shell functions, brace groups and heredocs; awk with system() or `$` fields; a variable set from `$(...)`, and some `python3 -c` scripts; jq with a `test()` regex, and env-var prefixes; cat or jq on `out/diary/`; `cut -c`, `cut -b` and `colrm` after `mem.py`, `cite.py` or a helper (use `--width`). Split those, or write a script file in `out/_analysis/`.
- `mem.py` pages long output; fetch the rest with `--offset` before trusting a count. A Bash output over about 30 KB is saved where I cannot read it; page it.
- After a compaction the guard requires the head and stage file read again and the exact line "compacted; head reconciled" through `mem.py log --kind note`, in a call of its own, before any other write.
- In B4: a ruling never cites a room note; reader-error never where both readers made the same placement; T3-063 takes canvas posts only; a correction goes through `b4_rule_append.py --replace`, never a hand edit. An author-disagrees quote is a concept id, not a scheme sentence. Reading A and reading B are seeded per item, so a ruling never refers to "reader A" of another item.

## The next comparison

Packet 4 (461 items: the last 6 of G08, then G09 to G11) is ruled at B4a-04 against the same tests and the boundaries ruled in packets 1 to 3. Read QB4-001's answer first if it has come. Its conflicts pass runs over its notes before the first ruling. G09 holds T3-005 and T3-021, B2's first predicted pair, and CC-017 (making and keeping the mark named as one practice) meets them there. After packet 7: the full `adjudication_report.md`, then B4b, the blind sample, compared against the stability floor 0.807 and B3's agreement 0.786.
