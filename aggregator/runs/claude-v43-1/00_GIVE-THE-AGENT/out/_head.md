# Head, claude-v43-1

Under 3,000 words, rewritten whole at every close. Last written at the close of B2a-r1, 2026-10-11 (UTC): the pilot's round 1 built, closed at `done.sh B2 --cut packets-out`. The dispatch runs next, without me; the next leg of mine is the check leg B2b-r1.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1 is closed; all 705 rooms have a note. Stage B1, the third-order scheme, is done (B1a to B1e). Stage B2, the pilot, is open: its round 1 is built.

**B2a-r1, built.**
- **Hard set** (`author_items.jsonl`, 40 items, seed `b2a-r1:hard`): 19 confusion-pair items, 8 rule 0 bags and 13 random items. The list is `out/_analysis/b2_hardset_r1.tsv`. The 19 pairs are `confusions.md`'s 17 plus two sibling pairs added at this leg (T3-014/T3-152 and T3-015/T3-063); ten of the 19 sit inside one family.
- **Gold set** (`gold_items.jsonl`, 40 items, seed `b2a-r1:gold`), drawn by the same rule with no item shared. It is shown to no reader and kept out of the packets folder.
- **My placements** were written before any packet. Hard set: 5 clear, 35 arguable, 24 on more than one kind. Gold set: 4 clear, 36 arguable, 17 multi. My primary is among the B1 working kinds in 39 of 40 hard items and all 40 gold items. Where my placement differs, it mostly drops a kind.
- **Declarations** in `notes-B2.md`:
  - the stopping threshold, mean pairwise agreement 0.70 on the hard set;
  - agreement by Jaccard on placement sets (`["T3-004"]` against `["T3-004","T3-011"]` scores 0.5);
  - alpha with distance 1 − Jaccard and chance correction over sets;
  - gold seeded at 1 per 20 items in B3, at most two per batch;
  - the batch cap, to be set at B2b-r1 from the position curves.
- **`RETURN-B2.md`** holds rule 0 in the contract's words. Rule 0's log line rides on the return line as `multiplacement_log`, with `END-OF-RETURN` and the confirm line.
- **Packets**, flat in `out/_packets-B2/`: `index.md`, `G01.md` to `G21.md`, and the round-1 item packet named for round 1 (40 items, 49,720 bytes, seed 20261011; its name is in `MANIFEST.json`). They serve `scheme.jsonl` as shipped at B1e, with no exemplars. The nested first build was moved to `out/_analysis/b2_packets_round1_nested/`.
- **`run_manifest.json`** has a B2 round-1 entry: `@preset/cheap` times 3 through the gateway.
- `validate.py B2`: 0 errors, 0 warnings.

**Departure, with QB2-001 open.** `packets.py B2` serves one packet per round under the 50 KB ceiling. The ten biggest second-order themes of the B1 notes cannot be served: leagueoflegends t02 alone renders 86,762 bytes. So the items were capped by rendered size: nominated items at 2,500 bytes, pool picks at 1,600 and random picks at 1,500, near the median of 1,470. Rule 0 bags stand in for the ten biggest. Five nominated pair items were replaced by seeded pool picks: pairs 7, 8, 11, 12 and 19. The random items are likely easier than the corpus.

**QB2-002 open.** Which packet path `fleet.py` reads. I built flat, as HOW-TO-RUN.md and the validator expect.

**B1 in one paragraph.** 197 third-order themes (183 main, 14 rare) in 21 families, with gates, discriminators, floors and 578 exemplars. Every room was walked (705 of 705). New kinds per hundred second-order themes ran 60 in the first hundred, 0 in the last. The saturation test found 0 new kinds; the second pass, 108 rooms in seven stretches, found none either. The claim F-001: half the 7,786 placed second-order themes (51.1%) sit on one kind, and themes about dealing with other rooms need the most kinds (36.0% single against 54.1%). The share rises with the theme's grain. The hardest confusion pair is T3-005/T3-021, estimated at 15 to 20% disagreement. `handback-B1.md` and `out/interview/B1e.md` hold the rest.

**J's words for B1 (7 October 2026):** "national elements are very important here"; "we need to get as much variance on organizing behavior early on so that later we have enough to create the model". National, political and conflict content is study material, named as plainly as any other. **The handler's rule:** a choice to leave out or soften content for any reason other than the study's goes to J first with `mem.py ask`, and the content stays meanwhile.

**J on reading (11 October, 16:54 Berlin; carry into every head).** Stop cutting room reads to a line length (`cut -c` or any other cut). Read room lines whole. When a read is too long, page it by line ranges or by offset, never by truncating lines. Recorded in `notes-B2.md`.

**J on asking (11 October, 17:01 Berlin).** Ask J a question whenever one is needed, with `mem.py ask`. Do not hold a question back to avoid interrupting; asking does not stop the run.

**The PI's clarifications (8 October, approved by J):** the thresholds are the design's heuristic; the rule is unchanged.

**How to work, from J (8 October, 23:45 Berlin, "can you do a hot change for the batching?"; relayed by the handler at 22:03Z; carry this paragraph into every head).** A change in how I work, not in what I read or decide. Fewer turns. When two or more tool calls do not depend on each other's output, make them in one turn. Chain ordered commands in one Bash call with &&, so that a failure stops the rest; for example, the `mem.py log` or note just decided, then the next `mem.py codes`. Never put a write in the same turn as the read it depends on. Never run two writes to the same file as separate parallel calls. Keep one room's material per read, as now. Every tool still writes its own record; nothing about what I read or decide changes.

**Two rules from J at B1b-29 (through the handler, 20:10Z; carry them into every head).** Write rule 0 lines and bags with `b1_multiplace_write4.py` and `b1_bags_from_file2.py`, not the old scripts, which made one `mem.py` call per row of the whole table and grew to 8.5 minutes a write. Never end a turn while a job runs in the background; run every write and check in the foreground.

## What the check leg B2b-r1 does (the stage file's section 3, kept here for after a compaction)

- The harness says the readers left their files in `_fleet_raw/B2/round-1/`. Validate them first; then score in this order:
  - fidelity against `author_items.jsonl`, the primary figure;
  - pairwise agreement among the three readers, with alpha;
  - (after the last round only) my own consistency, by re-placing ten of the hard set blind.
- Write one line in `pilot_rounds.jsonl`. Copy `fleet.py`'s counts (readers, reissues, durations) into `notes-B2.md`.
- Every item where any two disagree is a finding. Each edit goes in `scheme_edits.jsonl` with its kind (scheme-ambiguous, item-is-a-bag, reader-error, author-error, genuine-joint), `caused_by`, was, now and why, plus a `tier_history.jsonl` line (relabelled or rescoped; move asking questions or splitting). Never tighten a theme by narrowing it until it becomes rare. Watch every theme's base rate.
- Section 4: compare each reader's first ten items against its last ten; set the B3 batch cap; export the items that divided readers to `exemplar_candidates.jsonl`.
- Stop when a round makes no edit, when agreement reaches 0.70, or after four rounds. Then freeze (`scheme_final.md` and `.jsonl`), and `B2c` builds the gold round and two stability rounds.
- The readers' rule 0 lines arrive on their return lines (`multiplacement_log`). They go into the pilot's own record, not the B1 log.
- Read `mem.py asks QB2-001` and `QB2-002` at the start of the leg.

## The scheme, as shipped

`scheme.jsonl` holds 197 themes. `scheme.md` holds the index and every family in full. The drafts `out/_analysis/b1e_draft_G01.jsonl` to `G21.jsonl` are its source: to change a gate, edit the drafts and rerun `b1e_assemble.py --write`, which rewrites `scheme.jsonl`, `families.jsonl` and `scheme.md`. Then rebuild the packets with `--scheme scheme.jsonl --to out/_packets-B2`.

The floor is two rooms unlike each other: in size, in side of the contrast, or in form. 181 main themes rest on size and two on form (T3-173, T3-189). Rare: T3-007, T3-025, T3-067, T3-077, T3-093, T3-106, T3-133, T3-144, T3-161, T3-166, T3-186, T3-191 and T3-197, each seen in one room; T3-128, in three rooms that tell one episode (E1132).

## What B1 handed to B2

- Asks from the B1 handback:
  - a verb that serves a theme's concepts without its placements;
  - a ruling on testing G13, G14 and G15 as one index page;
  - whether B3 readers see exemplars;
  - the B1d leftovers.
- B1d leftovers not taken up:
  - 107 episode lines whose kinds none of their rooms holds;
  - seven pairs of lines telling one event;
  - E989;
  - the cfb and finland records;
  - shared-member counts that may include AutoModerator;
  - the 76 themes holding both T3-005 and T3-021 acts;
  - T3-149 and T3-150 members that may hold T3-195;
  - kinds left out of bags.
- The second-order theme the scheme handles worst: argentina t06, on T3-150 with a bag naming seven more kinds.

## Stage A1, what B1 inherited

- J's rulings of 7 October: hour 0 is the canvas opening; the onset is the first coded turn at hour 0 or later; the organizing end is reported with and without calls after hour 73 (QA1-002).
- `coordinating-rule-A1.md`, copied into `prior.md` §5. 44,116 of 115,388 concepts coordinate. Census 705 rooms; second-order themes 7,844.
- The onset contrast is in `contrast.md` and `prior.md` §6.

## Open distinctions, carried past B1

None is filed in `_questions/`. These remain open:
- who started the work;
- wars told twice;
- rivals who turn partners (E1076, E1122, E1142, E1318);
- whose flag a shared flag is (E1118);
- records that disagree on who attacked, on promises, truces, bots and design changes;
- who drove a bot and why it left a work (E1025);
- a room's own scripts barring it from sparing a neighbour (E843), or wrecking a protectorate it then rebuilt (E1209);
- one member on both sides of a quarrel (E820, E947);
- objections to altering the final image (T3-054 or T3-105).

## Ledgers at this close

- A1: `lexicon-A1.md` 1,289 lines; `running-A1.md` 773; `leads-A1.jsonl` 2,478; `departures.jsonl` 9; `defects.jsonl` 8.
- B1: `scheme_current.jsonl` (197 themes, 7,786 placed second-order themes, 13,432 placements); `scheme.jsonl` (197); `families.jsonl` (21); `confusions.md` (19 pairs now); `findings.jsonl` (1); `tier_history.jsonl` (252); `multiplacement_log.jsonl` (6,663); `episodes-B1.jsonl` (1,341); `notes-B1.md`; `handback-B1.md`.
- B2: `notes-B2.md`; `author_items.jsonl` (40); `gold_items.jsonl` (40); `RETURN-B2.md`; `out/_packets-B2/`; `run_manifest.json` (A1 and B2 round-1 entries). The scripts are `out/_analysis/b2_item_sizes.py`, `b2_select.py`, `b2_author.py` and `b2_author_vs_working.py`. Asks: QB2-001 and QB2-002.

## Rules kept

- Never type an id, an order or a name from memory; check with `jq` or a script. Never log a write before the tool answers. Count a ledger's lines after appending.
- There is no `--kind close` and no `--kind episode`; log those as notes.
- Check a notes section against the diary before closing. Never put a placeholder or a no-op in a command. Never put an Edit and the read that checks it in one turn.
- Never write an id-like token the run does not define in the head, such as a D or a P followed by digits: `done.sh` reads it as an unresolved link. Name later stages and packet files in words.
- The permission check refuses:
  - "=w=";
  - shell for and while loops, and words beginning "for_";
  - shell functions, brace groups and heredocs;
  - awk;
  - a variable set from `$(...)`, and some `python3 -c` scripts;
  - jq with a `test()` regex, some jq filters with chained `or` selects or jq variables or array subtraction, and env-var prefixes;
  - cat or jq on `out/diary/`.

  Split those, or write a script file in `out/_analysis/`.
- In zsh a word beginning with "=" fails. The guard refuses any text holding the name of the PI's decision command.
- A file over 256 KB is read with `offset` and `limit`. The shell shows at most 30 KB per call. The Read tool cannot open files under `$TMPDIR`. BSD grep has no `-P`.
- `mem.py theme` prints the working placements above the concepts; `mem.py codes --sub S --second tNN` does not, but it lacks the theme note.
- The diary is in part B2-1 at this close. After a compaction the guard requires the head and stage file read again and the exact line "compacted; head reconciled" through `mem.py log --kind note`, in a call of its own, before any other write. After an interrupted turn or a lost connection, check the record before rerunning anything.

## The next comparison

At B2b-r1:
- whether readers split GreenCorner t03 between T3-005 and T3-021, as `confusions.md` predicts;
- whether anarcho_capitalism t12, acecombat t05 and parabola t02 land under T3-010 when the gate says truce, bartering or alliance;
- whether readers holding one family's page miss the neighbour themes in another;
- fidelity against my placements for the first time.
