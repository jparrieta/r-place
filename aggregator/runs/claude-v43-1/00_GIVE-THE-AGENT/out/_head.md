# Head, claude-v43-1

Under 3,000 words, rewritten whole at every close. Last written at the close of B2a-r2, 2026-10-11 (UTC): round 2 of the pilot built, the ten biggest bags placed and served in parts. The dispatch runs next, then the check leg B2b-r2.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1 is closed. Stage B1 (the third-order scheme, 197 themes in 21 families) is done. Stage B2, the pilot, is open: round 1 is built, dispatched, checked and edited; round 2 is built.

**Round 1, as scored** (readers r12, r15 and r16 only; the other attempts failed):
- fidelity against `author_items.jsonl` 0.594 (mean Jaccard; primary match 0.742);
- pairwise agreement 0.733 (primary 0.767);
- alpha 0.726;
- 18 of 40 items with two readers differing.

The readers ran on deepseek/deepseek-v4-flash-0731 at high effort on mixed providers. The run cost 0.369 USD. The line is in `pilot_rounds.jsonl`; the per-item table is `out/_analysis/b2_r1_items.tsv`.

**What round 1 showed.** I placed 24 of 40 items on two kinds; the readers placed one kind almost always. Those second placements are my author-errors under rule 0, read strictly. Real splits came on guatemala t02 and catalunya t01 (the homeland's flag), dofus t01, cubers t12, nVade t04 (another room's work defended), WisconsinBadgers t04 and farmcarrots t15. acecombat t05, Goodboye t03 and simonfraser t08 are bags.

**The edits** (`scheme_edits.jsonl`, 286 lines, round 1): 6 sentence changes (T3-005 and T3-021 on repair during a raid, T3-009 and T3-043, T3-065, T3-092); 8 discriminators from the round's splits; 28 new questions for `must_not_show` lines with no discriminator; 7 questions in the deal cluster around T3-010; 202 word-for-word mirrors (kind gate-check, QB2-003). `mem.py gates` finds no defect. 28 pairs are confirmed in `gate_checks.jsonl`; 464 are not, and are read before the freeze. `mem.py gates` does not see a decide_when_both that names a theme with no discriminator; the deal cluster was found by reading, and the other clusters are read for it before the freeze.

**The rechecks.** 754 records in `rechecks-B2.jsonl`, none owed. 697 are round 1's: 22 items moved (18 author-errors, 4 edits doing their work). 57 are the ten new items under 42 edits: all unchanged, each read against the edit's changed sentence (`out/_analysis/b2_rechecks_r2.py`). `author_items.jsonl` stays as written; fidelity is reported against it and against the rechecked placements.

## Round 2, as built (B2a-r2)

**The hard set is 50 items:** round 1's 40, plus the ten biggest bags of `notes-B1.md`, read whole and placed by me before any packet (`out/_analysis/b2_author_r2.py`, source "biggest-bag"). Rule 0 as amended decides the form: no line places more than one theme; a bag places one and names the rest under `also_present`, each with its concepts. All ten are arguable.
- Single placements: leagueoflegends t02 T3-023, theblackvoid t09 T3-006, ainbowroad t11 T3-035, dota2 t05 T3-023.
- Bags: 2007scape t04 T3-038 (five more), theblackvoid t12 T3-174 (four), ainbowroad t04 T3-021 (four), ainbowroad t03 T3-005 (four), ainbowroad t07 T3-041 (four), sweden t01 T3-065 (five).

**`RETURN-B2.md`** gains the `also_present` clause and a paragraph on parts: read every part, reply with the end marker alone on all but the last, answer for every item on the last. The round-1 text is kept as `out/_analysis/RETURN-B2_round1.md`.

**The packet, in parts (QB2-001).** `out/_packets-B2/round-2/` holds `index.md`, 21 family pages from the edited `scheme.jsonl`, and eleven parts of one packet, 513,096 bytes in all, each under 51,200. `out/_analysis/b2_parts_r2.py` built them with `packets.py`'s own renderers, seed 20261012. An item may run on into the next part under a "(continued)" heading; leagueoflegends t02 runs over four parts. The order is in `out/_analysis/b2_order_r2.json`, outside the readers' folder. Round 1's packets stay flat in `out/_packets-B2/`, with J's copy in `round-1/`.

**MANIFEST.json, on QB2-004's assumption (open).** Each part carries count_key position, group, part k and parts 11; items 0 on parts 1 to 10 and 50 on the last. If J answers otherwise, the next build leg rebuilds with the same helper.

**Manifest.** `run_manifest.json` has a round-2 entry: the same model; J's reader settings, one provider (Relace) and medium reasoning effort; 3 agents, 50 items, every part's bytes and hash. A change in agreement is partly the settings, not only the edits.

**Stopping.** The PI's round-2 rule: no round may stop before the ten biggest bags are read once. Round 2 serves all ten, so its check leg may apply the stopping rules.

## What the check leg B2b-r2 must do

- Copy `fleet.py`'s counts into `notes-B2.md`: readers, reissues, durations, tokens and cost.
- Score round 2 with `out/_analysis/b2_score.py --round 2`: fidelity against `author_items.jsonl` and against the rechecked placements (`--alt`), pairwise agreement, alpha; primary exact agreement beside. Score `also_present` on the six bags separately; it is not in the Jaccard.
- Read how readers handled the parts and the bags: whether every reader answered all 50 on the last part, whether any answered early, and how the four-part item fared.
- The next comparison (below). Edits, rechecks and gate repairs as at B2b-r1; then decide whether round 3 opens.

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
- **Sets:** the hard set and the gold set were drawn by `out/_analysis/b2_select.py` (seeds `b2a-r1:hard`, `b2a-r1:gold`); the ten biggest bags were added at B2a-r2, not drawn.
- **B3 batch cap:** 40 items, the first 10 a warm-up block not counted; revisited with round 2's curves.

## The scheme

`scheme.jsonl` holds 197 themes (183 main, 14 rare) in 21 families. The floor is two rooms unlike each other in size, side or form: 181 main themes on size and two on form (T3-173, T3-189). Rare: T3-007, T3-025, T3-067, T3-077, T3-093, T3-106, T3-133, T3-144, T3-161, T3-166, T3-186, T3-191 and T3-197; T3-128 is rare because its three rooms tell one episode (E1132). F-001, as superseded: half the 7,786 placed second-order themes sit on one kind; themes about dealing with other rooms need the most kinds. Within a room, larger themes need more kinds (Spearman 0.28; across rooms −0.08). "107 episode lines" is corrected to 106 (line, kind) pairs over 81 lines in `notes-B1.md` and `handback-B1.md`.

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
  - `notes-B2.md` (345 lines); `author_items.jsonl` (50); `gold_items.jsonl` (40); `RETURN-B2.md` (with `also_present`); `pilot_rounds.jsonl` (1);
  - `scheme_edits.jsonl` (286); `rechecks-B2.jsonl` (754, none owed); `gate_checks.jsonl` (28 pairs confirmed); `exemplar_candidates.jsonl` (18); `tier_history.jsonl` (372); `run_manifest.json` (A1, B2 round 1, B2 round 2).
- Asks QB2-001 to QB2-003 are answered; QB2-004 is open.

## Rules kept

- Never type an id, an order or a name from memory; check with `jq` or a script. Never log a write before the tool answers. Count a ledger's lines after appending.
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
- `mem.py` pages long output (`[lines 1-80 of N]`); fetch the rest with `--offset` before trusting a count.
- New author items on edited themes owe rechecks under every edit that touches their themes; record them before the close.
- `mem.py recheck` takes about 4.5 seconds a record. Run rechecks in the foreground in slices under ten minutes; the recheck scripts skip what is already recorded.
- `mem.py theme` prints the working placements above the concepts; `mem.py blind on` hides them.
- After a compaction the guard requires the head and stage file read again and the exact line "compacted; head reconciled" through `mem.py log --kind note`, in a call of its own, before any other write. After an interrupted turn or a lost connection, check the record before rerunning anything.

## The next comparison

At round 2:
- fidelity and agreement against round 1's, with the settings change named beside them;
- whether readers on the edited gates still split guatemala-like flag items, dofus-like lone starts and nVade-like defence of another room's work;
- whether T3-004 and T3-021, chosen by no round-1 reader, draw any reader;
- whether readers place the four single bags on one theme as I did, and which themes they name under `also_present` for the six bags;
- whether the theblackvoid t12 split (my T3-174 against the B1 working T3-031) and the ainbowroad t07 split (T3-041 against T3-038) recur among readers.
