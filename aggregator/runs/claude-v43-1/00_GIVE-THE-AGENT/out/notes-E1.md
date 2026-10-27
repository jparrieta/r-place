# Notes, stage E1: the audit

## E1a: the scripts

**The close-check report of D6a-18** (`_closes/D6-D6a-18-20261027T153104Z.validate.txt`): 0 errors, 0 warnings.

**What this leg did.** It wrote the scripts of stage E1 section 1, as the stage file declares them, and ran each once. Every script is in `audit-E1/`, with its rule in its docstring, declared before it ran, and its output beside it under the same stem. A stranger reruns one with `python3 out/audit-E1/<script>.py > out/audit-E1/<output>`. Where a first run had a fault, the output was kept under a `.superseded-N` name and the fault is named in the script's docstring or in the diary. The readings by hand that the scripts call for are left to the audit sections.

| script | output | what it computes | result |
|---|---|---|---|
| `quotes_resolve.py` | `.json` | every quote in every output, resolved against the store's participant words, labels, case accounts, the instrument's texts and the instructions | 3,230 cited concept quotes; 3,218 resolve to the concept they cite; 12 do not (2 to nothing, 2 to another concept, 1 to a label, 7 return lines quoted beside an evidence citation); 2,042 uncited spans of five words or more resolve to nothing; five spot-checks drawn by seed |
| `links_check.py` | `.txt` | `links.py` and `validate.py --links` | both exit 0; 3 files checked, all ids resolve |
| `quote_check_raw.py` | `.json` | the handler's `quote-check-E1.json` (seed 13, 80 rooms) | code_quote_found_share 1.0; case_quote_found_share 0.6573; 389 missing strings listed against 548 by the file's count; 227 of the 389 are in the room's coded passages once case and end punctuation are set aside |
| `store_figures.py` | `.tsv` | README-store.md, A1's recomputation and now, three columns | all 16 figures agree; the 158,227 item lines hold 137,732 distinct ids, 21,011 in the unnamed state `collapsed` (A1's defect) |
| `coverage.py` | `.json` | room, forest and case records in the read logs, by log | 705 rooms read by `room`, 705 by `forest` (704 whole), 705 case accounts; no room unread; the fleets apart |
| `canvas_uses.py` | `.json` | rule 7's uses, by log | `mem.py room` with the canvas shown: A1 715, B1 1,874, C2 22, C5 218, D3 4, D5 5; canvas files named in commands at C2a-03, D3b, D5a-40, D5b, D6b |
| `orderings.py` | `.json` | the orderings by snap, and every key file's hash history | the scheme before B3, prior.md before B1's first theme, the D1 seal before the return, and the branch cuts before the projection all held; 82 D4 snaps after the projection (the room forms) |
| `moves.py` | `.json` | both history ledgers by stage and move; the move snaps against the diary's move lines | diary move lines equal move snaps by count from C2 to D6; 'sequencing' (C2) and 'stabilizing' (D3) are not among the eight |
| `probes_score.py` | `.json` | the recall probe, as filed and re-read | 283 of 300 answer files are in bold markdown, which probe.py does not parse; goal right 17 as filed, 298 re-read |
| `element_reach.py` | `.json` | prior.md section 3's element-reach half | 4,759 of 5,380 themes with a coordinating turn (88.46 per cent) reached by a standing element; 297 of 696 rooms in full |
| `unplaced.py` | `.json` | the unplaced at each tier | 151 second-order themes unplaced (407 concepts); T3-017 and T3-133 in no fourth-order theme; every fourth-order theme in a dimension |
| `manifest.py` | `.json` | `run_manifest.json`, whole | 19 entries with model, seed and decoding; the D3 re-check return has none |
| `counts_rule.py` | `.json` | the census twice, D4 section 4's four counts, the ledgers against the head, the handbacks' count phrases | 705 and 705; 476 + 0 + 229 + 0 = 705; tier history 1,026 against the head's 1,020; 361 count phrases to check |
| `clocks.py` | `.json` | the coder's time against the item's; datings in written order | equal in all 115,350 joined concepts; 237 of 598 case chronologies step back; 14 of 21 arrows name such a room |
| `claims.py` | `.json` | propositions and branches by kind, evidence, rival and validation | 9 propositions (pattern 7, both 2), each with a rival; 35 branches (33 groupings, 2 forms) |
| `diary_transcript.py` | `.json` | the diary against the transcript, one leg per stage by seed | 17 legs; 392 of 905 diary lines found word for word; the rest are tool-written lines, to be read |
| `fleet_figures.py` | `.json` | the fleet figures beside FLEET.md section 2 | the verdict fleet's readers differ in 163 of 705 rooms (0.2312) |

**Carried for this stage, and where each goes.**
- **prior.md section 3's measure, the element-reach half.** It is computed here, at E1a (`audit-E1/element_reach.py`). It will be reported in the audit section on composition (section 3). The other half, a validated adaptation or a theme listed as unresolved with its reason, is not computed, so local validation stays not established.
- **Defects 100 and 101** (the survival paragraph rests on work_remained; four timings the canvas contradicts) are reported open in the ledgers section, not rewritten.
- **PR-D6-10** stays an unvalidated proposal. It is checked against the D3a-55 ruling in the moves and provenance section. The script shows that all eleven proposals are 'unvalidated' on the base model 46384686…, the D3 freeze, and that `amendments-D6.jsonl` holds no line.
- **The D6 extra legs, D6a-09 to D6a-18**, are audited as part of the run. One of them, D6a-17, is in the diary draw. Their moves, snaps and outputs are read in the moves and provenance section.

**QE1-001, asked of J at this leg.** Stage E1's close-check counts each D4 snap that lists the projection as an error. There are 82 such snaps, which give 246 lines. They are the D4a-03 interview cut, the closes of D4a-04 to D4a-08, and the move snaps 238 to 313: the room forms, made after the projection at J's instruction. The branch cuts, moves 200 to 237, were all snapped before it. Rule 18 bars changing the snaps, and the snaps belong to the harness. So every E1 leg would fail its close-check on these lines until the check was changed or J ruled. My assumption, logged with the question: the check is changed to print these snaps as the audit's finding. The first done.sh of this leg failed on these 246 lines alone (`_closes/E1-E1a-20261027T172649Z.validate.txt`).

**QE1-001, answered** (J, 27 October 18:45 Berlin, through the PI): "Yes. I would not change the structure of the journey for bookkeeping." The handler amended `check_orderings`. A D4 snap now counts as a branch cut only where it changed `branches.jsonl` from the previous snap. A snap that lists the projection with `branches.jsonl` unchanged is printed as a finding, and the error stays for any snap that changed the branches after the projection. My assumption held as the answer states it, so nothing that rested on it changes. I checked the answer against the snaps by script: 82 D4 snaps list the projection, and none of them changed `branches.jsonl` from the previous snap. `validate.py E1` now gives 0 errors, 246 findings on those 82 snaps, and 1 warning for the stage's later outputs (`_analysis/e1a_validate_E1-2.txt`). The audit reports the 82 snaps, in the orderings section (E1b-02), as the finding they are: the room forms were made after the projection, by J's ruling, and they are not a recut of the branches.

**The audit sections I plan: eight, E1b-01 to E1b-08.** Each leg writes its section to its own file, `audit-E1/section-NN.md`. The reason: the close-check reads `audit-E1.md` whole as soon as it exists, and it requires the composition line and the methods paragraph, which can only be written last. `audit-E1.md` is assembled from the eight files at the check leg, E1d. That leg adds stage section 5, the methods paragraph and the `composition_status` line, all of which need the reconstruction's fidelity.
1. **E1b-01, the quotes and the clocks** (section 1): the 12 cited-quote defects and the 2,042 unresolved spans, read; the five spot-checks by hand; the 389 missing case-account strings, read, and the 548 against 389; links; the store's figures in three columns; the clocks, with relations.jsonl by hand.
2. **E1b-02, the orderings, the counts, coverage and the canvas** (section 1): each ordering held or broken; the 361 count phrases of the handbacks against their files; coverage by stage; every canvas use named, declared or not, with the places the canvas may have shaped unseen; QE1-001's answer.
3. **E1b-03, the moves and provenance** (section 1): the moves by stage and by the eight, including 'sequencing' and 'stabilizing'; the recuts after C5; the D6 proposals against their evidence, with PR-D6-10 against D3a-55; D6a-09 to D6a-18; the manifest; the figures restated with FLEET.md section 2's definitions.
4. **E1b-04, claims against their evidence** (section 1): `claims-E1.md`, every proposition and branch by kind and validation; prior.md section 3's declaration against what each level rests on; the switch records of `literature-C3.md`.
5. **E1b-05, the diary, the probes and the unplaced** (section 1): the 17 drawn legs read against their transcripts; `probes-E1.md`, per stage and per question, as filed and re-read, with notes apart from defects and n/a apart from recall; the 151 unplaced themes, T3-017 and T3-133, read.
6. **E1b-06, the ledgers, the stories and what a reader was given** (section 2): findings by status, warrant and refuted_by; every ledger's lines; new kinds per hundred themes; the stories and the account's passes; the five things a reader was given; the departures with their costs; the defects, the material's apart from the instrument's, 100 and 101 open; the forks (none arrived); rule 9.
7. **E1b-07, composition and expectations** (section 3): the diagnostics recomputed against prior.md section 3, with the element reach; local validation and unresolved evidence apart; clusters and distinct global changes; prior.md section 2's expectations; `expectations-E1.md` with the field's entries; the onset contrast.
8. **E1b-08, what bore the load and what the study cannot say** (sections 6 and 7): stage by stage, the replay of `tools/chunk_compare.py`, the data-structure view at C2's last snap against `data_structure-C5.md`, the tiers' work; the absences, the ungrounded, the coder conflicts, the standing departures; the critique shelf; the one thing to say plainly.

**Licences exercised at E1a.**
- probe.py's `--score` was not rerun. It writes into `_probe/`, which belongs to the harness, and it scores the open distinctions against the question files as they stand now. I read the filed scores and re-read the answers by its rules against the expected values the harness stored at each close.
- The scripts read `package/<sub>/case.md` and the store's files directly, as stage A1's checks did under the departure in `departures.jsonl` line 1. They print only counts and the strings the stage asks to be read.
- The coordinating rule is A1's own code (`_analysis/a1_ends.py`), imported, not rewritten. It reproduces `organizing_end-A1.jsonl` in all 705 rooms.

**Slips at E1a.**
- A survey command piped a helper through `cut -c` and was refused; it was re-run without it. A shell loop was refused too; I used the peek script instead.
- Two Edits to `moves.py` went in one turn. They touched separate lines and both applied.
- Five scripts needed a second run, and the first output of each is kept: `quotes_resolve` (twice: the pairing of quotes, and a citation taken from the next quote), `store_figures` (distinct ids counted as lines), `canvas_uses` ('placements' matched theme placements), `moves` (twice: 'move N' in lower case only, and the eighth move bucketed as dropping) and `probes_score` (one leading mark stripped).

## E1b-01: the quotes and the clocks

**The close-check report of E1a** (`_closes/E1-E1a-20261027T174924Z.validate.txt`): 0 errors, 1 warning (the stage's later outputs not yet written), and 246 findings on the 82 D4 snaps after the projection (QE1-001). **QE1-001** was read again at this leg's start, as the leg message asked. The answer had been reconciled at E1a, and nothing else rested on my assumption, so no work changed.

**What this leg did.** It wrote `audit-E1/section-01.md`, part 1 of the audit's section 1, on four items: the quotes and ids against the logs, the quotes against the raw record, the store's figures, and the clocks. It wrote seven scripts, each with its rule in its docstring, declared before the run, and its output beside it:
- `unresolved_read.py`: what the 2,042 spans resolved to nothing are;
- `unresolved_hand.py`: where the 84 left over first appear in the transcripts;
- `quote_sources_check.py`: quotes of a named source, beside the source;
- `labels_read.py`: the 3,641 spans that resolve to a label;
- `case_missing_read.py`: the handler's 389 missing case-account strings;
- `relations_clock.py`: two rooms' records of one encounter;
- `links_views.py`: `links.py`'s resolver over the views.

The readings by hand are logged one by one in the diary.

**What it found.**
- **Cited quotes.** 3,218 of 3,230 cited concept quotes resolve to the concept cited. Of the 12 that do not, 2 are faults of form and 10 are faults of the script.
- **Invented quotes.** I found no invented quote in my files.
- **Defects of mine.** Two D6 quotes give the coder's wording as members' words, carried from the case accounts. Two small misquotes of the instrument's own text. Three examples of my own wording in quotation marks.
- **The handler's file.** It gives code_quote_found_share 1.0 and case_quote_found_share 0.6573. Its 389 listed strings are mostly participant words missed on punctuation and markup, the coder's own labels and phrases, and translations. 33 come from uncoded items, beyond my reach.
- **The store's figures.** All 16 agree with README-store.md and with A1.
- **Ids.** No id of the model, the scheme or the store fails to resolve in the head, the questions or the views.
- **The clocks.** The coder's time equals the item's in all 115,350 joined concepts. The store's builder is absent, so this may hold by construction. No pair of two rooms' records dates one encounter at two times.
- **Defects ledger.** Eight lines were appended to `defects.jsonl`: 5 the instrument's, 1 provenance, 2 the material's.

**Licences exercised at E1b-01.**
- I read `_transcripts/`, open at this stage, by script for where a span first appears.
- The handler's `quote-check-E1.json` is read from the folder root, where it arrived.
- I count the readers' room models, which the E1a rule did not leave out, as outputs. Their quotes are reported apart from mine.

**Slips at E1b-01.**
- The first `unresolved_read.py` run kept the earlier class and so moved nothing. Its output is kept as `.superseded-1`.
- Two `unresolved_hand.py` runs with `grep` were too slow and were stopped. Their empty outputs are kept as `.superseded-1` and `-2`.
- A survey command piped `tail` into `cut` and was refused; it was re-run without the cut.
- Two diary lines needed correcting lines after them: the count of the instrument's defects lines (5, not 6), and the r/argentina and r/uruguay pair, which I first read as one encounter.
