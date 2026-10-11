# Head, claude-v43-1

Under 3,000 words, rewritten whole at every close. Last written at the close of B2b-r1, 2026-10-11 (UTC): round 1 of the pilot checked and the scheme edited. Round 2 opens; its build leg, B2a-r2, comes next.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1 is closed. Stage B1 (the third-order scheme, 197 themes in 21 families) is done. Stage B2, the pilot, is open: round 1 is built, dispatched and checked.

**Round 1, as scored** (readers r12, r15 and r16 only; the other attempts failed):
- fidelity against `author_items.jsonl` 0.594 (mean Jaccard; primary match 0.742);
- pairwise agreement 0.733 (primary 0.767);
- alpha 0.726;
- 18 of 40 items with two readers differing.

The readers ran on deepseek/deepseek-v4-flash-0731 at high effort on mixed providers. The run cost 0.369 USD, with 747,469 input and 494,282 output tokens. The line is in `pilot_rounds.jsonl`; the per-item table is `out/_analysis/b2_r1_items.tsv`.

**What round 1 showed.** I placed 24 of 40 items on two kinds. The readers placed one kind almost always (3, 6 and 1 multi lines). In 14 items all three agreed on one theme among mine. Those second placements are my author-errors under rule 0, read strictly. Further author-errors: orderofthebluecorner t08 (readers T3-121, me T3-087) and stardustcrusaders t19 (readers T3-043; the gate's default made T3-009 primary). Real splits came on guatemala t02 and catalunya t01 (the homeland's flag), dofus t01, cubers t12, nVade t04 (another room's work defended), WisconsinBadgers t04 and farmcarrots t15. acecombat t05, Goodboye t03 and simonfraser t08 are bags.

**Stopping.** Agreement 0.733 clears the declared 0.70. Under the PI's round-2 rule no round may stop before the ten biggest bags of the B1 notes are read once, and this round made edits, so round 2 opens.

**The edits** (`scheme_edits.jsonl`, 286 lines, round 1):
- 6 sentence changes:
  - T3-005 must_not_show (the contradiction with T3-021 on repair during a raid, fixed);
  - T3-021 must_show;
  - T3-009 and T3-043 decide_when_both (the side with more concepts is primary);
  - T3-065 must_show (announcements and calls for the room's own flag go there);
  - T3-092 decide_when_both.
- 8 discriminators from the round's splits.
- 28 new questions, each in both gates, for `must_not_show` lines with no discriminator.
- 7 questions in the deal cluster, where a decide_when_both named T3-010 with no discriminator (T3-012, T3-035, T3-039, T3-040, T3-084, T3-123, T3-139). `mem.py gates` does not check that shape; read the other clusters for it before the freeze.
- 202 word-for-word mirrors of one-way discriminators (kind gate-check, QB2-003).

`mem.py gates` now finds no defect. 28 pairs are confirmed in `gate_checks.jsonl`; the other 464 are read before the freeze. The drafts `out/_analysis/b1e_draft_G*.jsonl` hold the edits, and `b1e_assemble.py --write` rebuilt `scheme.jsonl`, `families.jsonl` and `scheme.md`. The first, bundled edit record is `out/_analysis/scheme_edits_b2b-r1_bundled.jsonl`; its 36 tier_history lines (253 to 288) are superseded by the per-edit lines after them. `tier_history.jsonl` has 372 lines.

**The rechecks.** The 84 non-mirror edits owed 697 recheck records, all recorded in `out/rechecks-B2.jsonl` by `out/_analysis/b2_rechecks_r1.py`. 22 items move: 18 author-errors and 4 edits doing their work (GreenCorner t03, dofus t01, stardustcrusaders t19, guatemala t02). `author_items.jsonl` stays as written. From round 2, fidelity is reported against it and against the rechecked placements.

**Section 4.** Two of three readers still improve between their first and last ten items. The B3 batch cap is declared at 40 items, the first 10 a warm-up block that is not counted; it is revisited with round 2's curves. The 18 dividing items are in `exemplar_candidates.jsonl`.

**Corrections on the record.** F-001 is superseded: the grain bound does not hold across rooms (Spearman −0.08 over 633 rooms; within rooms, 0.28, positive in 482 of 619). The new line is bounded. "107 episode lines" is 106 (line, kind) pairs over 81 lines. Both corrections are appended to `notes-B1.md` and `handback-B1.md`.

## What round 2's build leg (B2a-r2) must do

- **Where:** build in `out/_packets-B2/round-2/` (`packets.py`'s default; `dispatch.sh` gives `fleet.py` that folder). Leave round 1's packets where they are: flat in `out/_packets-B2/`, with J's copy in `round-1/`.
- **The ten biggest bags of `notes-B1.md`** are served in parts to the same reader (QB2-001). Each part stays under 50 KB with its end marker, and the reader answers once per item after the last part. `packets.py B2` cannot part a round, so the splitter is a helper in `out/_analysis/`, and the parts are recorded in `MANIFEST.json` and `notes-B2.md`. No round may stop before these ten have been read once.
- **Items:** round 2's hard set is still `author_items.jsonl` (stage B2 runs the same hard set across rounds; `pilot_rounds` n_items must equal the set). The ten biggest bags must be placed by me first and added to the hard set before any packet exists. Their size is not a reason to drop them.
- **`RETURN-B2.md`** gains the `also_present` clause (rule 0 as amended). The return line then carries `also_present: {}` unless `item_is_a_bag`.
- **Manifest:** the round-2 entry records the reader settings: one provider (Relace), medium reasoning effort, the same model. A change in agreement is partly the settings.
- **Gates:** the remaining pairs of edited themes (`mem.py gates T3-a`) are read and confirmed before the freeze.

## Standing words from J and the PI (carry into every head)

**J's words for B1 (7 October 2026):** "national elements are very important here"; "we need to get as much variance on organizing behavior early on so that later we have enough to create the model". National, political and conflict content is study material, named as plainly as any other. **The handler's rule:** a choice to leave out or soften content for any reason other than the study's goes to J first with `mem.py ask`, and the content stays meanwhile.

**J on reading (11 October, 16:54 Berlin).** Stop cutting room reads to a line length. Read room lines whole. Page a long read by line ranges or offset, never by truncating lines. Use `--width N` on a `mem.py` read if a clip is ever needed; the guard refuses `cut -c` after `mem.py`.

**J on asking (11 October, 17:01 Berlin).** Ask J with `mem.py ask` whenever a question is needed; asking does not stop the run.

**The PI's clarifications (8 October, approved by J):** the thresholds are the design's heuristic; the rule is unchanged.

**How to work, from J (8 October, 23:45 Berlin, "can you do a hot change for the batching?"; relayed by the handler at 22:03Z; carry this paragraph into every head).** A change in how I work, not in what I read or decide. Fewer turns. When two or more tool calls do not depend on each other's output, make them in one turn. Chain ordered commands in one Bash call with &&, so that a failure stops the rest; for example, the `mem.py log` or note just decided, then the next `mem.py codes`. Never put a write in the same turn as the read it depends on. Never run two writes to the same file as separate parallel calls. Keep one room's material per read, as now. Every tool still writes its own record; nothing about what I read or decide changes.

**Two rules from J at B1b-29 (through the handler, 20:10Z; carry them into every head).** Write rule 0 lines and bags with `b1_multiplace_write4.py` and `b1_bags_from_file2.py`, not the old scripts, which made one `mem.py` call per row of the whole table and grew to 8.5 minutes a write. Never end a turn while a job runs in the background; run every write and check in the foreground.

## The pilot's declarations (from `notes-B2.md`)

- **Threshold:** mean pairwise agreement 0.70 on the hard set.
- **Agreement:** Jaccard on placement sets (`["T3-004"]` against `["T3-004","T3-011"]` scores 0.5). Fidelity is mean Jaccard against my set. Alpha uses distance 1 − Jaccard, chance over the round's pooled sets. Primary exact agreement is reported beside, never in place.
- **Gold:** 40 items in `gold_items.jsonl`, never shown to a reader, seeded in B3 at 1 per 20 items, at most two per batch.
- **Sets:** the hard set and the gold set were drawn by `out/_analysis/b2_select.py` (seeds `b2a-r1:hard`, `b2a-r1:gold`); round 1's items were capped by rendered size (QB2-001 has since ruled against capping).
- **Scoring tools:** `out/_analysis/b2_score.py --round K --readers ...` scores a round (add `--alt` for rechecked placements); `b2_exemplar_candidates.py` appends the dividing items.

## The scheme

`scheme.jsonl` holds 197 themes (183 main, 14 rare) in 21 families. The floor is two rooms unlike each other in size, side or form: 181 main themes on size and two on form (T3-173, T3-189). Rare: T3-007, T3-025, T3-067, T3-077, T3-093, T3-106, T3-133, T3-144, T3-161, T3-166, T3-186, T3-191 and T3-197; T3-128 is rare because its three rooms tell one episode (E1132). F-001, as superseded: half the 7,786 placed second-order themes sit on one kind; themes about dealing with other rooms need the most kinds. Within a room, larger themes need more kinds.

## What B1 handed to B2, still open

- The ruling on testing G13, G14 and G15 as one index page.
- Whether B3 readers see exemplars.
- The B1d leftovers:
  - 106 (line, kind) pairs over 81 episode lines whose kinds none of their rooms holds;
  - seven pairs of lines telling one event;
  - E989;
  - the cfb and finland records;
  - shared-member counts that may include AutoModerator;
  - the 76 themes holding both T3-005 and T3-021 acts;
  - T3-149 and T3-150 members that may hold T3-195;
  - kinds left out of bags.
- The second-order theme the scheme handles worst: argentina t06.

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

- B1: `scheme_current.jsonl` (197 themes, 7,786 placed second-order themes, 13,432 placements); `scheme.jsonl` (197, edited); `families.jsonl` (21); `confusions.md` (19 pairs); `findings.jsonl` (2 lines, F-001 and its superseding line); `multiplacement_log.jsonl` (6,663); `episodes-B1.jsonl` (1,341).
- B2:
  - `notes-B2.md`; `author_items.jsonl` (40); `gold_items.jsonl` (40); `RETURN-B2.md`; `pilot_rounds.jsonl` (1);
  - `scheme_edits.jsonl` (286); `rechecks-B2.jsonl` (697, none owed); `gate_checks.jsonl` (28 pairs confirmed); `exemplar_candidates.jsonl` (18); `tier_history.jsonl` (372); `run_manifest.json` (A1 and B2 round 1).
- Asks QB2-001, QB2-002 and QB2-003 are answered.

## Rules kept

- Never type an id, an order or a name from memory; check with `jq` (allowed now) or a script. Never log a write before the tool answers. Count a ledger's lines after appending.
- There is no `--kind close` and no `--kind episode`; log those as notes.
- Check a notes section against the diary before closing. Never put a placeholder or a no-op in a command. Never put an Edit and the read that checks it in one turn.
- Never write an id-like token the run does not define in the head, such as a D or a P followed by digits: `done.sh` reads it as an unresolved link. Name later stages and packet files in words.
- The permission check refuses:
  - "=w=";
  - shell for and while loops, and words beginning "for_";
  - shell functions, brace groups and heredocs;
  - awk with system();
  - a variable set from `$(...)`, and some `python3 -c` scripts;
  - jq with a `test()` regex, and env-var prefixes;
  - cat or jq on `out/diary/`;
  - `cut -c`, `cut -b` and `colrm` after `mem.py`, `cite.py` or a helper.

  Split those, or write a script file in `out/_analysis/`.
- `mem.py recheck` runs about one record every 2.5 seconds, so 600 rechecks take about 25 minutes. Run them in the foreground in slices under ten minutes; `b2_rechecks_r1.py` skips what is already recorded.
- `mem.py theme` prints the working placements above the concepts; `mem.py blind on` hides them.
- After a compaction the guard requires the head and stage file read again and the exact line "compacted; head reconciled" through `mem.py log --kind note`, in a call of its own, before any other write. After an interrupted turn or a lost connection, check the record before rerunning anything.

## The next comparison

At round 2:
- whether readers on the edited gates still split guatemala-like flag items, dofus-like lone starts and nVade-like defence of another room's work;
- whether T3-004 and T3-021, chosen by no round-1 reader, draw any reader;
- fidelity against my rechecked placements beside the original;
- how readers handle the ten biggest bags served in parts.
