# Head, claude-v43-1

Under 3,000 words, rewritten whole at every close. Last written at B4a-01, 2026-10-12 (UTC). Stage B4 is open: packet 1 of 7 of the adjudication is ruled. The next leg is B4a-02, packet 2.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1 is closed. Stage B1 (the third-order scheme, 197 themes in 21 families) is done. Stage B2, the pilot, is done (`pilot_report.md`, `stability-B2.md`, `handback-B2.md`). Stage B3, the fleet, is done (`handback-B3.md`). Stage B4: the adjudication runs one packet a leg; packet 1 is ruled.

## Stage B4 (from B4a-01)

**The selection (the PI at 21:19Z, J's amended stage file).** `tools/assemble.py` wrote `b3_classes.jsonl` with J's five classes. Class 1 (readers agree, equal to B1) 2,566 and class 2 (readers agree, a proper subset of B1; B1 kept, tagged `b1_grouping_kept`) 1,990 stand. Class 3 (readers differ) 2,393, class 4 (readers agree outside B1) 837 and class 5 (no B1 grouping) 58 are contested: 3,288 items. For the blind sample at B4b, J agreed the two readers stay DeepSeek V4.1 Flash, and a third reader per item from an OpenAI model is a separate arm, reported apart, never pooled, with no Claude reader. The handler sets that arm in `arm.json` before B4b.

**Before the first ruling.**
- **Gold drop:** 755 seeded gold placements and 1,210 duplicate copies dropped; `assign_final.jsonl` reads corpus copies only and holds 7,844 lines, equal to `assignment_items_expected`.
- **Transmission** (`transmission-B4.md`, over 90 gold and pilot items):
  - gold 21, 1, 6, 12 across the four rows;
  - pilot 30, 0, 12, 8;
  - of the 20 fourth-row items, 11 are "I was wrong" and 9 "unintended";
  - rule 0's "under rule 0" pairing did not transmit.
- **Conflicts pass:** eight lines for packet 1 in `coder_conflicts.jsonl`, CC-001 to CC-008 (among them a members' flood, makers' jokes called "the room's own", testing claims, moderators applying rules on the joke day, upvote-threshold promises).
- **Policy and blindness:** declared in `notes-B4.md`.
  - Confidence counts for nothing.
  - My B1 grouping is shown as a third placement.
  - Class 4 is author-error when the readers' list is taken and author-disagrees when a B1 theme is kept.
  - Readings are blinded as A and B in seeded order.

**The packets.** Seven, built by `out/_analysis/b4_adjudication_packets.py` into `out/_adjudication-B4/`, in chunks of 25:
- packet 1: 491 (gloss-only, G01, G02);
- packet 2: 447 (G03 to G06);
- packet 3: 500;
- packet 4: 461;
- packet 5: 409;
- packet 6: 500;
- packet 7: 480.

Drafts go through `out/_analysis/b4_rule_append.py`: a dry run first, then `--write`. It now also has `--replace`, which corrects a ruled line in place and keeps the old file under a superseded name. `out/_analysis/b4_scheme.py` prints a theme's tests. `out/_analysis/b4_assign_final.py` rewrites `assign_final.jsonl` after each packet. `out/_analysis/b4_packet_summary.py` writes a packet's figures.

**Packet 1, ruled.** 491 rulings: genuine-joint 137, scheme-ambiguous 123, author-error 97, reader-error 77, author-disagrees 37, item-is-a-bag 20.
- **Counts:** unresolved 52; named_neither 84.
- **Fields that failed:** must_show 78, discriminators 39, decide_when_both 4, must_not_show 2.
- **Themes that failed most:** T3-017 29, T3-023 27, T3-001 24.
- **Agreement:** before 0.486 mean Jaccard; after 0.633, which is not a reliability figure.
- **Predicted pairs:** of B2's, only T3-001|T3-023 (20), T3-001|T3-095 (11), T3-015|T3-063 (7) and T3-015|T3-075 (4) could appear. Unpredicted, T3-017|T3-031 (17), T3-001|T3-048 (13) and T3-023|T3-095 (11) split as much.
- **Two rulings corrected in place,** formula1 t05 and elitedangerous t01: T3-063 takes canvas posts only.
- **Files:** `adjudication_report.md`, the interim report after packet 1; `out/_adjudication-B4/boundaries.md`, the boundary paragraphs.

**What packet 1 ruled, to carry into the next packets.**
- **The joke's stage** (T3-001|T3-023). A change to the sub made by moderators, or by members flooding it "as a sub acting together", is T3-023. Members' fakes in an unchanged sub are T3-001.
- **The canvas condition** (T3-017|T3-031). T3-031 needs the canvas. An in-joke with no canvas is T3-017, scheme-ambiguous on T3-017's discriminator.
- **Whose joke** (T3-001|T3-048). The source in the words decides; unresolved where it is not shown. A member relaying an outside joke is T3-048 (CC-002).
- **Who staged the claim** (T3-001|T3-095). A test of a member's own fake stays T3-001.
- **Open or known** (T3-048|T3-095). The larger share decides.
- **The jokes or the look** (T3-032|T3-097). Complaints about the sub's own joke look or rule, and requests to end it, go to T3-097.
- **Applied or made** (T3-063|T3-185). A day's exception, or a kind of post banned, is a rule made.
- **Upvote bargains** (T3-023|T3-051). They are T3-051 unless the change was made (CC-007).
- **T3-023's own rule.** It adds T3-095 or T3-032 at three concepts, and T3-097 or T3-100 on one. Four themes needed means a bag.
- **Three gaps,** each unresolved:
  - April Fools play not posted as true (T3-001 `must_show`);
  - another sub's change (T3-023 `must_show`);
  - moderators applying standing rules to non-canvas posts (T3-063 `must_show`, CC-004).

## Stage B3, in short

J's rulings QB3-001 and QB3-002 set B2's packet shape: at most 15 items and 180,000 bytes, self-contained, fleet ids only. The fleet ran 1,212 batches, one reader each, R = 2; B0192 and B0927 were rebuilt in fleet-id halves under QB3-003. The gold check after group 1 passed (fidelity 0.637 against 0.625). The assembly of record: `assign_raw.jsonl` 17,653 lines and `b3_classes.jsonl`. The figures:
- gold fidelity 0.645 against B2's 0.631;
- agreement Jaccard 0.786 and alpha 0.782, at the stability floor;
- G18 the family that agreed least; the multi rate 0.158.

Waivers: QB3-004 (32 returns without a prediction line) and QB3-005 (22 record slips), in `return_waivers.jsonl`. Failed replies: 87, of which 72 cited a neighbouring item's concepts.

## Stage B2, in short

Rounds 1 to 3 and gold: fidelity 0.594, 0.639, 0.682, 0.624; pairwise 0.733, 0.718, 0.728, 0.818. Stability 0.807 is the floor every later figure is read against. Readers from round 2: deepseek/deepseek-v4.1-flash, direct, medium effort. Primary match on gold 0.800. Four gold wording defects go to C1: uofmn t01, cuboulder t04, mariokart t04, ireland t12. The frozen scheme: `scheme_final.jsonl` (197 themes; 183 main, 14 rare), `families.jsonl` (21), `gate_checks.jsonl` (496 pairs). The freeze gave T3-002, T3-033 and T3-038 one counting rule (the act with most concepts leads), the sentence I am least sure a stranger reads as I meant.

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

`scheme_final.jsonl` holds 197 themes (183 main, 14 rare) in 21 families. Rare: T3-007, T3-025, T3-067, T3-077, T3-093, T3-106, T3-128, T3-133, T3-144, T3-161, T3-166, T3-186, T3-191 and T3-197. It is frozen: stage B4 logs defects and never edits it.

## Open, carried

- **From B1.** The ruling on testing G13, G14 and G15 as one index page. The B1d leftovers: 106 (line, kind) pairs over 81 episode lines whose kinds none of their rooms holds; seven pairs of lines telling one event; E989; the cfb and finland records; shared-member counts that may include AutoModerator; the 76 themes holding both T3-005 and T3-021 acts; T3-149 and T3-150 members that may hold T3-195; kinds left out of bags. The second-order theme the scheme handles worst: argentina t06.
- **Distinctions** (none filed in `_questions/`): who started the work; wars told twice; rivals who turn partners (E1076, E1122, E1142, E1318); whose flag a shared flag is (E1118); records that disagree on who attacked, on promises, truces, bots and design changes; who drove a bot and why it left a work (E1025); a room's own scripts barring it from sparing a neighbour (E843), or wrecking a protectorate it then rebuilt (E1209); one member on both sides of a quarrel (E820, E947); objections to altering the final image (T3-054 or T3-105).
- **The bag count.** J counts 841 B1 bags; an older head said 846. Not reconciled.
- **From B4a-01.** Single-concept second themes were not added perfectly evenly in packet 1 (magictcg t09). Chunk 18 held 16 of the packet's 77 reader-errors, on single-concept G02 items.

## Ledgers at this close

- B1: `scheme_current.jsonl`, `families.jsonl` (21), `confusions.md` (19 pairs), `findings.jsonl` (2), `episodes-B1.jsonl` (1,341).
- B2: `notes-B2.md`, `pilot_report.md`, `stability-B2.md`, `handback-B2.md`, `author_items.jsonl` (50), `gold_items.jsonl` (40), `scheme_final.jsonl` (197), `scheme_edits.jsonl` (306), `gate_checks.jsonl` (519 lines).
- B3: `notes-B3.md`, `RETURN-B3.md`, `batches-B3.jsonl` (1,212), `_packets-B3/`, `assign_raw.jsonl` and `assign_pass2.jsonl` (17,653 each), `multiplacement_log.jsonl` (3,171), `predicted_confusion-B3.jsonl` (1,180), `b3_classes.jsonl` (7,844), `defects.jsonl` (63), `return_waivers.jsonl` (74), `handback-B3.md`.
- B4: `notes-B4.md`; `transmission-B4.md`; `coder_conflicts.jsonl` (8); `disagreements.jsonl` (491; the old file kept as `disagreements.superseded-20261012T221214Z.jsonl`); `assign_final.jsonl` (7,844: class 1 2,566, class 2 1,990, ruled 491, pending 2,797; older versions kept as `assign_final.superseded-*.jsonl`); `adjudication_report.md` (interim); `out/_adjudication-B4/` (seven packets, `boundaries.md`, packet 1's drafts and `summary.md`).
- Asks QB2-001 to QB2-014 and QB3-001 to QB3-005 are answered; none is open.

## Rules kept

- Never type an id, an order or a name from memory; check with `jq` or a script. Never log a write before the tool answers. Count a ledger's lines after appending.
- There is no `--kind close` and no `--kind episode`; log those as notes.
- A question to J is `mem.py ask "<question>" --assume "<meanwhile>"`; `mem.py log --kind ask` writes only a diary line and gives no id.
- Never put a placeholder or a no-op in a command. Never put an Edit and the read that checks it in one turn. Count the head's words before the closing line, not after.
- Never write an id-like token the run does not define in the head, such as a D or a P followed by digits: `done.sh` reads it as an unresolved link. Name later stages and packet files in words.
- The permission check refuses: "=w="; shell for and while loops, and words beginning "for_"; shell functions, brace groups and heredocs; awk with system() or `$` fields; a variable set from `$(...)`, and some `python3 -c` scripts; jq with a `test()` regex, and env-var prefixes; cat or jq on `out/diary/`; `cut -c`, `cut -b` and `colrm` after `mem.py`, `cite.py` or a helper (use `--width`). Split those, or write a script file in `out/_analysis/`.
- `mem.py` pages long output; fetch the rest with `--offset` before trusting a count. A Bash output over about 30 KB is saved where I cannot read it; page it.
- After a compaction the guard requires the head and stage file read again and the exact line "compacted; head reconciled" through `mem.py log --kind note`, in a call of its own, before any other write.
- In B4: a ruling never cites a room note; reader-error never where both readers made the same placement; T3-063 takes canvas posts only; a correction goes through `b4_rule_append.py --replace`, never a hand edit.

## The next comparison

Packet 2 (447 items, G03 to G06) is ruled at B4a-02 against the same tests and the boundaries ruled in packet 1. Its conflicts pass runs over its notes first. After packet 7: the full `adjudication_report.md`, then B4b, the blind sample, compared against the stability floor 0.807 and B3's agreement 0.786.
