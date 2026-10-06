# Contract v37 to v38: what changed, and the rename table

Date: 2026-09-24. Source: `_v37-source/CONTRACT-aggregator.md` (662 lines). Target:
`CONTRACT-aggregator.md` (v38). Decisions: `../DESIGN/DECISIONS.tsv`.

## The rename table

Apply in one sweep to the contract, the stage files, `tools/`, the store fields, the return
specifications and the stage-18 scripts. Old names must not survive anywhere in `INSTRUMENT/`
except this table and `_v37-source/`.

| v37 | v38 | where it lived |
|---|---|---|
| first-order codes | first-order concepts | §3, store `codes.jsonl`, `mem.py codes` |
| case themes | second-order themes | §3, store `case_themes.jsonl` → `themes.jsonl`, `mem.py theme`, rule 0, stage 02 to 06 |
| second-order themes (analyst's) | third-order themes | §3, `scheme_*.jsonl`, `mem.py where`, rule 0, rule 11, the construct-name ban |
| third-order chunks, chunks | fourth-order themes | §3, stage 07, 09, 11; `mem.py --chunk` → `--third` for third-order, and a `--fourth` verb |
| aggregate dimensions | aggregate dimensions | unchanged |
| S07 (second-order id) | T3-007 | ids in placements and views |
| C3 (chunk id) | T4-003 | ids; C is now a claim prefix in the model |
| `case_theme` (package field) | `second_order` | the yard already writes `second_order`; the store build maps nothing |
| `rooms_index.md` read at start | `mem.py note` on demand | standing instructions |
| `diary-NN.md` written at close | `diary/NN-k.jsonl` via `mem.py log` | rule 20, §9 |
| `cite_case.py`, `C.cite(...)` | `cite.py` | §2 tools, rule 3 |
| "composes" verdict by the analyst's fleet | verdict by a fresh cheap fleet; room model and ledger by labelers | rule 12, §7 |
| stages 13 to 17, the crossing | removed | §1, §3, §6, §7 |
| stage 18, the audit | stage 13 | §6, rule 17; the v37 stage-18 scripts are ported under 13 |

## Sections changed

- Opening: 696 rooms, one instrument; "think on disk" becomes "never rely on having read".
- §1: the method question above the theory question; composition defined (Machlup 1967: 30;
  Kozlowski and Klein's compilation named); what a form is; the check in both directions;
  prediction secondary; the crossing parked; `prior.md` carries the temporal brackets.
- §2: the package is one instrument's documents; `relations.jsonl` in the store; shelves in two
  tiers; the tools list from 04a §6; the `Read` cap line.
- §3: the five tiers renamed; the model typed (elements, arrows, ids); Grodal, Anteby and Holm
  added to the method paragraph; the adaptation and hierarchy shelves; the methods-section
  paragraph carries the four departures and the replicability sentence (inspection, no rerun
  promise).
- §4: the frame is a dated hashed copy; the instrument's shape (flat second-order tier; the
  concept-reach threshold); retracted concepts dropped; the range-restriction sentence about the
  smallest rooms removed; "other rooms are data, never units".
- §5: rules 3 (mechanical exemplar check), 10 (leg field), 11 (`move` field; a move closes the
  leg), 12 (rewritten for the two fleets and the guard), 14 (append-only), 15 (generated views),
  17 (10a, 10b, 10c), 18 (snaps harness-owned); new rules 19 (counts and amendments) and 20 (the
  diary).
- §6: the stage table with models and 10a to 10c; the crossing parked; the budget paragraph
  replaced by the token record.
- §7: one fan-out instance; what every fleet stage has (from the handler log); alpha; the
  prompt-stability check; the return described.
- §8: the adequacy sentence.
- §9: new; the memory and the leg, from 04a.

## J's review of 2026-09-24, applied

Aggregate dimensions named in full in the construction sentence; the four universal problems of
organizing named in the ban; the remainder sentence rewritten; the dozen-cases sentence added to
"no number"; one dimension defined; a gate defined at first use; the two shelves given a sentence
per read-tier work; minting stamped by the harness (leg, rooms read, themes read, tokens read,
the prompting room and theme) at 02 and 07; the in-sample sentence made precise (the tier the
model was built from); `canvas/artworks.jsonl` in the package under rule 7; the diary declared
per stage in parts and never read whole; "exactly" removed from rule 0; the crossing removed and
the audit renumbered 13; every fleet stage as three legs with the dispatch outside the analyst's
session, `@preset/best` orchestrating `@preset/cheap` readers, the analyst relaunched for the
check and told the readers left their files.

## Not yet done

- The stage files (18 in v37) are not rewritten; `_v37-source/STAGE-*.md` are the sources.
- `RETURN-10.md`, the labeler task template, the handler brief.
- `STANDING-INSTRUCTIONS.md` and `AGENT.md` for v38.
- The tools named in §2 that do not exist in v37 (`cite.py` as the successor to `cite_case.py`,
  `gen_views.py`, `probe.py`, `done.sh --cut`, `handoff.py`, `ingest.py`, `rebuild.py`, the new
  `mem.py` verbs, `validate.py --links`).

## Audit of the contract's order and size, 2026-09-24, and what was done

Sizes: v37 662 lines, 8,337 words in one file. v38 first draft 792 lines, 9,694 words (16 per
cent more, from §9 and the typed model). After the split: the contract 553 lines, 7,000 words;
`METHOD.md` 1,400 words; `STANDING-INSTRUCTIONS.md` 1,800 words. Each file carries a generated
index of sections with line ranges and word counts (`index_md.py`, run at every edit), and
`mem.py contract --section <n>` serves one section.

Problems found in the first draft's order, and the repair:

1. The tools sat between the questions and the tiers, so an analyst reading for the argument met
   a command reference at line 180. Moved to the standing instructions.
2. §3 carried four things: the tiers, the typed model, the method paragraphs and the shape of the
   run. The method paragraphs and the shape are now `METHOD.md`; the contract's §2 is the tiers
   and the model only.
3. The frame (which rooms, the canvas, the coded layer) came before the rules and after the
   method, so the reader met "what the material lets you see" before "what you may do". Now:
   questions, tiers, rules, stages, frame, fleets, saturation.
4. The memory section (§9) governed every leg but sat last. It is now the standing instructions'
   §2, given with every stage, and the contract's preamble points at it.
5. The fan-out section mixed the figures, the fleet mechanics and the return. Kept as one section
   with three headed parts, since they share the vocabulary; the return points at the schema.
6. Rule 17's "§3's method licences" pointed into the method paragraphs; it now points at
   `METHOD.md`.

The goals paragraph (Felin and Zenger 2009) went into §1's standing claim.

## The two audits of 2026-09-24 (AUDIT-A.md, AUDIT-B.md), and what was applied

Applied: the three failure shares pre-registered in `prior.md` (15 per cent, 50 per cent, ten)
and reported at 13; `organizing_end_hour` and the aftermath share under a coordinating-turn rule
in `prior.md`, reported per branch at 12; the waterfall expectation moved to `prior.md`;
"reliability" renamed "transmission after revision" with a stability row and the Jaccard metric
for set-valued placements; the Gioia mapping corrected (the third tier is their first-order
concepts consolidated across cases; the fourth is their second-order themes); three sentences for
what a form is, in the order they bind; the stage 08 test as a written mapping per fourth-order
theme; compilation as failure at the population level and description at the form level; the
sparse-ledger sentence and the unadapted group; rule 12 with sameness defined and two rooms as
the trigger; rule 16 scoped to findings at 07 to 09; stage 11 a judgement stage; the hostile
reader before the final two passes; the story file `model/story-NN.md`; the onset contrast
reported at 13; the verdict criterion in FLEET §3; the scheme served in packets; a glossary and
the "you spans models" sentence in the contract's preamble; the schema stripped of its draft
front matter and outside references, `origin` for provenance, the lift through
`assignments_final.jsonl` at the model version, `instantiate` carrying a source, `revised`
under the portability check, `pending` before `particular`, the distance written as a formula
with the mass normalisation, the reconstruction scored against `case.md`, the operations mapped
once to Fisher and Aguinis; the standing instructions' tree extended to every named file,
`scheme_current.jsonl` as a paged startup read at 02 and 06, compaction owned by the harness;
`PRIOR-template.md` added. Not applied: nothing the audits raised was left; the two findings
marked uncertain by the auditors (cladistic vocabulary with cross-links; rule 19 against rule 9
in FLEET's preamble) were read and judged not to need a change beyond the glossary's
"similarity hierarchy, no descent" sentence already in METHOD.

## The stage files, 2026-09-24 late

Written in `stages/`: 01, 02, 03, 04, 05, 06, 07, 08, 09, 10a, 10b, 10c, 11, 12, 13, each with
model, legs, startup packet, reads allowed and forbidden, outputs, the operation, moments to log,
the final message and the close; the v37 sources are `_v37-source/STAGE-*.md`, and 04, 05, 06, 08
and 09 were written from the v37 pattern without re-reading their sources line by line, so the
operator checks their figures against the sources before the kit ships. `handoff/`:
`RETURN-10.md`, `TASK-template.md`, `HANDLER.md`. Not yet written: `AGENT.md`, `CLAUDE.md` for the
analyst, `HOW-TO-RUN.md` for v38, and every tool named in the standing instructions that v37 did
not have.

## Versioning, from 2026-09-24 late

Every document in `INSTRUMENT/` is versioned by `tools/version_log.py`: `VERSIONS.tsv` holds one
row per version (UTC stamp, path, sha256, words, note), and `_versions/` holds a copy of every
version under `<path>.<stamp>.<ext>`. Run it after every edit; an unchanged file adds nothing. To
backtrack, diff the current file against its copy in `_versions/` or check out the copy.

## 2026-09-25: the dispatch without an orchestrator model

J, 2026-09-24: run the fleet without an orchestrator. `tools/fleet.py` is the dispatch leg: a script sends the packets to fresh readers through the gateway, records the served model, validates, reissues, and analyses nothing. Every line that said `@preset/best` orchestrating `@preset/cheap` now names `fleet.py`. The stage 07 reviewer and the stage 09 readers run on Opus (J); every other fleet on `@preset/cheap`.

## 2026-09-27: the return to the field

J, 2026-09-27: r/place, the subreddit the event was named after, is the field, not a room. It leaves the population (census rule, `validations.jsonl`) and is coded and modelled apart by a sealed analyst under its own contract. Stage C3 gains a fourth step, `C3d` the field: after the literature and before the account, the analyst receives the field model and its evidence in `field/` (never r/place's corpus), and writes `field-C3.md` in three lists: where the two agree, what only the field sees, where they disagree. What only the field sees may enter the model as a hypothesis marked `from-field`; stage D1 returns it to every room blind, and D3 and E1 report the field's entries apart. The C3 interview point moves from `C3c` to `C3d`. Placed before D so that the rooms test what the field adds, and so that a change the field forces does not require the return to run twice.

## 2026-09-27, later: the field as its own stage

J, 2026-09-27 10:04: the field is its own stage, C4, not a step of C3. Stage C3 is again the literature alone (interview at `C3c`). Stage C4, the field, is one leg (`C4a`, interview there) with its own stage file, check and arm entry; it writes `field-C4.md` and, where it changes the model, `model-C4.md`, `structure-C4.md`, `concept-C4.md` and `manifest-C4.txt`, which the account reads first. The account moves from C4 to C5 in every file, script and check (`STAGE-C5-model-account.md`, `checks/stage_C5.py`, `C5a` to `C5d`, `-C5` file names); the run has 19 stages.

## 2026-09-28: the frame is final at 696

J: the run reads 696 rooms; the twelve largest by text are not coded in it. Contract §5 now gives the census's narrowing (777 communities, 708 the population, r/place the field) and names the twelve; stages C5 and E1 and `build_store.py`'s FRAME.md say 708 and 696 in place of 696 as the population. J: the single-thread slices the coders returned uncoded are not recoded; §5 names the rooms whose canvas talk is under-read.

## 2026-09-28: the koi

J: r/OrderOfTheKoi's canvas region is the koi, drawn from the pixel record (541 pixels, `INPUT/canvas/derived_regions.json`), not the Flag of Italy. `tools/build_neighbours.py` reads derived regions beside the atlas, so the koi borders and overlaps r/italy in `neighbours.jsonl`.

## 2026-09-28: what the v37 reader and scheme-maker said (changes A to K)

J approved eleven changes after interviewing v37's stage 01 and stage 02 checkpoints in read-only forks.

- A1. The note gains `coder unsure:` (what the coder said she could not place, with thread ids). Section 3 writes `order-A1.txt`; `mem.py next` names the next unread room from it, and `harness/after_compact.sh` prints it after every compaction, so the order lives on disk, not in the summary. A room skipped in the order is refused at the block's close (`order:gap`). The concepts are read before the note (`mem.py codes --sub` or `cite.py --room` logged before the `note` line). Ties seen and not checked go to `leads-A1.jsonl`.
- A2. Ties are ranked: named both ways, named one way, shared artwork, overlap, border (`mem.py neighbours` sorts so). A one-way naming is a claim of the naming room. Every room has its top five ties read; every lead of A1 is resolved in `leads-A2.jsonl` (confirmed, one-sided, not found). Clusters come from the rooms' own words only (mention, theme); the canvas ties are shown in `canvas`, marked as outcome, and a cluster tied by the canvas alone is refused (rule 7). Each cluster has a `kind`. The reading list interleaves the clusters: no two rooms of one cluster in a row while another has rooms left. This replaces the contiguous-run rule.
- B1. Legs are stretches of the interleaved list. The floor is two rooms from clusters of two different kinds. Two rooms that tell one episode (the same thread, or the same artwork in the same hours) are recorded in `episodes-B1.jsonl`, count as one room for the floor, and stand as corroborated. `prior.md` carries an `exemplar rule:` line; exemplars name their `rivals`. The second pass stops after two stretches in a row, each of at least twenty rooms, add no theme.

## 2026-09-28, later: hooks where rules were not kept, and the audit's fixes

J: enforce with hooks what the v37 analysts were asked and did not do. After a compaction, `after_compact.sh` writes `CONTROL/.compact-gate.json` and `pretool_guard.py` refuses every call until `out/_head.md` and the stage file are read and `mem.py diary` run; the gate lifts at the next `mem.py log`, opens after five refusals (logged in `guard.log`), and `step.sh` sets a gate left by an earlier leg aside. At A1, a room note is refused until its concepts were read, and `pretool_guard.py --post` (PostToolUse) runs the note's form check, now `note_problems()` in `checks/stage_A1.py`, the moment a note is written; it warns on quotes outside `struck by:`. From the code audit: `mem.py next` no longer reports every room skipped before the first note; placeholder notes do not count as noted; the order file is the only declared order; `mem.py` logs room names in the frame's spelling; the checks fold `r/` and case (`vlib.canon`); a dropped room in the order and a lead naming one room twice are refused; the note line that dates a room's note is the one naming that room alone.

## 2026-09-29: when to stop (the PI's rule)

J: a stopping rule for the stages that read rooms one at a time, built in `tools/saturation.py` and replayed from the files at every call. Material is counted in words, in units of the average room. A new kind in the last 10 average rooms: read on. Ten without: a round, whose length is the estimate of how far the next kind is (Chao et al. 2014), never past what is already read; a new kind resets everything. Three empty rounds: marker 1 (where the literature would stop); three more: marker 2; then a random draw from the unread rooms, as many words as the three rounds between the markers: marker 3. The report (`stopping-<ST>.md`) gives rooms read, share of the words, rooms left, words left in average rooms, the markers, every round, when each kind first came and what the draw rules out (Callaghan and Müller-Hansen 2020). Stage B1 follows the rule (`mem.py next --stage B1`), pauses at marker 3, and the PI decides to finish or stop (`saturation.py decide`). Stage A1 reads every room in a seeded random order (`saturation.py order`; the seed is the sha256 of the store's `rooms.jsonl`), counts a kind as an entry of the running file (ids K001 ...; the note's new `kinds:` line), and records the rule without stopping. `mem.py idea` stamps a prospective theme; mints are stamped with words read. The handler's choice, for J to confirm: when no kind has been seen once, a round is as long as the one before, at least 10 average rooms.

## 2026-09-29, later: guards against reading everything by accident

J: no estimate before 50 average rooms and 25 rooms; no round longer than 25 average rooms; a check-in at 60% of the words before marker 3, when B1 reports and pauses and the PI decides to continue, finish or stop (`saturation.py decide` records the point). A dry run on v37's final placements (300 rooms, 94 second-order themes, 10 of them in one room only) found the last new theme at room 239 to 300 of 300 in twenty random orders: the rule never reached marker 1, and the check-in fell at rooms 177 to 187 with 87 to 91 of the 94 themes seen, coverage 0.99, and an estimate of 17 to 40 unseen themes against 3 to 7 in fact (the estimate overstates when many themes stand in one room).

## 2026-09-29, later: stage A2 removed

J: the map and the reading list go; stage A2 with them. The run has 18 stages. B1 reads the analysed set in a seeded random order (the store's sha256, tag B1), drawn at every call by `tools/saturation.py`, under the stopping rule; no list is written. The floor is again two rooms unlike each other, with rooms that tell one episode counted as one (`episodes-B1.jsonl` stays); the floor across cluster kinds, the interleave, the clusters and the resolution of leads by A2 go. `leads-A1.jsonl` stays as a record B1 reads when it meets those rooms. `mem.py neighbours` stays, for any stage. Removed from the instrument: `stages/STAGE-A2-reading-the-map.md`, `tools/checks/stage_A2.py`, A2's rows in `steps.tsv`, `arm.json` and the stage cards, its row in the contract's stage table, its interview point (`A2b`). Both files are kept in `rplace-set-aside-2026-09-26/instrument-before-removing-A2-0929/retired/` and in `_versions/`. The harness test's interview cut now runs at `C4a`.

## 2026-09-29, later: an interview point at A1c

J: with `A2b` gone, the reading gets its own interview point. `A1c` (the lexicon, the analysed set and the handback) now ends with a brief, `out/interview/A1c.md`, and `done.sh A1 --cut interview`. Twelve interview points, `A1c` to `E2b`. Files: `steps.tsv`, `stages/STAGE-A1-reading-room-notes.md` (steps line and close), `STANDING-INSTRUCTIONS.md` (the list of points), the contract's A1 row, `harness/READ-ME-FIRST.md`.

## 2026-09-29, later: the audit's first fixes and three of J's rulings

From `memory/audits/audit-2026-09-29.md`. `mem.py mint` and `idea` crashed at C1 and D3 (the stopping rule's stamp, added that morning, now runs only at A1 and B1; tested). J's rulings: a new kind inside the draw restarts the count, as inside a round (`saturation.py`). At B1 the rule counts kinds as met, from `out/kinds-B1.jsonl`, which `mem.py mint` and `place` append with the room being read; a merge or split logged through `mem.py log` is a new kind; the file is never rewritten, so a regrouping leaves the past as read (`stage_B1.py` errs when a placement is missing from it; new plant). Which rooms keep the work alive is answered from the record, silence included: `organizing_end-A1.jsonl` gains `work_remained` (kept, lost, silent) with the concepts that say it (contract §1, A1 §5, check and plant); D5 reports it per branch (check and plant); C5's implications must answer the clause from the record (check and plant) and its canvas paragraph reads kept and lost from the record; D6's telling reads the record, the canvas only as outcome. `saturation.py` reads its files one line at a time.

## 2026-09-29, later: the field's entries go to every room as tentative (J, option a)

A mechanism only the field sees enters at C4 as an element or arrow with `origin: "from-field"`, `status: "tentative"` and `field_support`; a fourth-order theme never enters from the field (C4 text and check, two plants). C2 and C5 accept a tentative field arrow without room support, since every room tests it at D (check and plant). `handoff.py` sends every tentative entry to every room, marked `tentative` and with no word of its source; the mark stays in `out/sealed/FIELD.jsonl`, never served. The same change projects arrows with `from`, `to` and `mechanism` and matches a room's entries on any tier (audit H8), since a tentative arrow served empty could not be answered. RETURN-D tells the labeler to answer a tentative entry like any other, `absent` when the record says nothing. D3 rules each field entry out of tentative and reports it apart in `notes-D3.md`; E1 sets its take-up beside the other elements' in `expectations-E1.md` (checks and plants).

## 2026-09-29, later: the audit's items fixed and the missing tools built (J: "build whatever needs building")

From `memory/audits/audit-2026-09-29.md`; J's rulings: the C2 and C5 readers run on the analyst's model in sessions of their own, and only the coding and adaptation fleets run on DeepSeek; the D tools are built now. What changed, by kind:

- **Closes that could not close.** Checks are step-aware where a stage has steps (`vlib.current_step`): A1's last leg is A1c, not the leg that writes the coordinating rule; B1a closes on `prior.md` and notes; C5's table, figure and implications are owed at C5d; D3's element-group and re-check legs check only what is ruled so far; C1 may close a pass early. C5c repeats, one leg per pass.
- **A1 and B1.** `organizing_end-A1.jsonl` names `last_coordinating_code` and `aftermath_coordinating_codes`, and the A1 close recomputes the hour, the turns after hour 73 and the share from the store (the claim that the harness recomputes them at B1 had no code). `_head.md` is due at A1a's close. The diary rule needs an `opened` and a `note` line per room. A main theme names its floor, two rooms and how they are unlike (size checked from the store). B1 reads A1's closing files. The B1 card, `vlib`, `mem.py` and `lib.sh` lose the last words of A2; `_next_b1_list` removed. `saturation.py decide` is the PI's: the guard refuses it to the analyst, and the B1 card tells the PI how to run it. Rounds convert Chao's rooms into average rooms. The guard sets aside a malformed gate and never switches off; one bad line in a read log is skipped; the gate opens after five refusals, as documented.
- **B to C.** Form-pass ids are `FP-01`. A recut after C1 is written into `scheme_v2.jsonl` and through a new verb, `mem.py reassign`, which rewrites a second-order theme's line of `assignments_final.jsonl` with the move recorded on it (C1 to D6); after the freeze `mint` stamps the discovery only, and `place` and `unplace` are B1's. B2's gold and stability rounds have steps (`B2c`, `B2d`), packets (`--round gold|stab-1|stab-2`, `--brief`) and a stage-card line. C1 reads the frozen scheme. The contract's B4 row says transmission after revision, never reliability. C4 cannot close with the field unread. Readers of C2 and C5 run through the CLI on the subscription. C3c is "the four problems". The fourth-order themes partition the third-order tier (stated in C1, an error in C1 and C2). Findings are `F-001`, propositions `N01`, branches `F01`. One vocabulary for the four problems (`vlib.PROBLEMS`). The story file is `story-pN.md` everywhere. `gen_views.py` draws the C5 figure (`_views/figure-model.md`, Mermaid, with and without the theorised arrows).
- **The model frozen.** `vlib.model_hash` covers the model and its tiers; `done.sh` records it at C5d, D3c and D6b (`out/_closes/model-<stage>.sha256`) and `prior.md`'s hash at D1; D1 refuses a model that moved after C5; D4 refuses a `prior.md` changed without a departure; the guard keeps `out/_closes/` and `out/sealed/` for the harness.
- **Stage D built.** `tools/dreturn.py`, one rule set for the returns, used by `ingest.py` and the D2 check, and the verdict schema `fleet.py` validates against. `ingest.py` rewritten: it compiles the ledger (with `labeler_run`), the verdicts, the room copies and the D2 counts, marks a rejected room unreturned, compiles the re-check with ids `R-<sub>-NNN`, and re-lifts the ledger (`--relift`), which D3c and D4 require. `step.sh` runs it when D2's check leg and D3b open. The re-check has its own verdict packets (`verdict-D/recheck/`, from `MODEL-D3.md`) and dispatch (`dispatch.sh D3`, `_fleet_raw/D3v/`); a `modify` ruling alone no longer triggers it. `EXPECTATIONS.jsonl` is sealed in `out/sealed/`. The vocabulary serves arrows with their ends and mechanism. D1 is one leg. `prior.md` §7 has a stated form the D1 check parses; `distance.py` says where its weights came from and writes each room's delta, an average-linkage dendrogram and a NEXUS file for SplitsTree's NeighborNet; `tools/projections.py` writes D4's projections. D6 amendments need a history and a diary line, and D6b its retelling. E1 names its sample and return files and reads the handler's quote check (`check_quotes.py`, now on the E1 card). RETURN-D's `link` starts from a theme.
- **Tests.** The self-test also runs each stage's clean fixture, which must raise nothing (18 more checks; it found the D1 check's lower-case "drops/D" bug). `tools/tests/test_stage_d.py` runs D's plumbing end to end: the compile, then the D2 check with no error; a rejected room; the re-check ids; the re-lift. Three new harness tests for the guard.

## 2026-09-29, evening: the second audit's items fixed

A second audit (four readers: the first audit's items re-traced, A1 to C5, D to E, code) found the batch above left new seams. Fixed, by kind:

- **Closes that could not close.** D2: the verdict reader's id is taken from its file (`r1.jsonl`), so two readers are never one; an unreturned or rejected room is exempt from the grade and copy checks; `step.sh` builds the D2 views after the compile. D1: a room in `UNBUILT.tsv` and named in the handback is exempt; the tier forms are C2's (a list, a dimension, an `FP-` id). D3: `tentative` is a status until D3c; a field entry's ruling out of tentative is not a rewrite that forces the re-check; a model moved after the re-check build is a warning with its reason owed in `notes-D3.md`. B1: rooms with no second-order theme are left out of the order, so they are never "read out of turn". C1: `reassign` also writes `assign_revisions_only.jsonl`. `mint` is allowed at C1 to C5, D3 and D6 (a stamp only after B1) and counts `scheme_v2` among the minted ids.
- **Seals and freezes.** `sealed/FIELD.jsonl` is written once, at D1, never by the re-check build. The `prior.md` seal is written at any D1 close that is not a pause, and D4 errs when it is absent. The D3 and D6 model hashes are compared at D4, D5, D6 and E1 (`vlib.model_moved`). D2 re-verifies `handoff-D.sha256`; labelers return to `DROPS/D/<sub>/`, never into the served folder. The stopping rule's seed is frozen in `out/seed.txt`; `kinds-B1.jsonl` and `stopping-*-decision.jsonl` are guarded, and the decide regex catches the flags in any order; the guard's copy rule matches only the destination.
- **What a room is served.** Element pages are rendered by `handoff.py` from the served fields only, never from `_wiki/` (which named other rooms). Tentative entries and entries on a form-pass tier go to every room. `absent` needs no cited concept, since silence has none. The verdict line carries `concepts`; `residue` lists themes or concepts (D1 text, `dreturn.py`), and `fleet.py` checks the enums as well as the keys.
- **D tools.** `distance.py`: `cut()` drops the k-1 highest merges (the chain does not merge in height order: 81 of 600 random cases were wrong); the rooms are the analysed set less the unreturned. `ingest.py`: a non-object line or a broken `run.json` rejects one room, not the compile; `UNRETURNED.tsv` is rewritten without rooms later accepted; a stale verdicts file is set aside; a line with a source and no lift is flagged; the compile runs only when a return is newer than the ledger. D5 reads the `readers` list. `projections.py` percentiles are mid-rank. `rebuild.py` prints every arrow with its ends, its mechanism and the room's lines on it, and rebuilds a re-checked room from its re-check lines. D3 reads `verdicts-recheck-D.jsonl` and checks its version. E1 checks that `audit-E1.md` reports both shares of `quote-check-E1.json`, and resolves `F-001` and `N01` ids.
- **Views and verbs.** The figure without theorised arrows filters on each arrow's own grounding. `snap.py` keeps a copy of the elements, the arrows and `scheme_v2` beside each snap, so `mem.py diff-model` and `diff-scheme` run, and `diff-model` covers the arrows. `saturation.py order --stage B1` prints B1's order for the second pass. `dispatch.sh` names B2d after the gold and stability rounds and D3b after the re-check, and no longer exits 1 at D3. `stopping-B1.md` must match the record's rooms read. The B1 floor pair is compared case-blind. The C4 history check matches the id, not a substring.
- **Text.** C1's broken sentence on borrowed themes; `notes-B3.md` in C1's reads; `FP-` kept apart from `F-001` (`vlib.FORM_PASS`); C1's startup read is `scheme_final` in STANDING and `validate.py`; C2 `model/story-p2.md`; C3, C5, D3 and D6 list `scheme_v2.jsonl` and `assignments_final.jsonl` among their outputs for a recut, and D3 says to write `scheme_v2` and `reassign`; C4 says a field entry sits under a theme C3 already mapped; C5's steps `C5c-01`, the table and figure at C5d, the model moving after C5 only through D3 and D6; D1 one leg; D2's steps line once; B3's full stop; the contract's B2 row and status list (`tentative`); FLEET says the C2 and C5 readers run through the CLI; `F-031` in both HOW-TO-RUN files; `reassign` documented; the D1 and D3 docstrings; the Manual's handoff page.
- **Tests.** 137 self-test checks, the verb tests and the stage D test pass; the harness test passes 50 of 50.

Left for J (method): whether a room with few turns after hour 73 is `silent` or `unrecorded`; whether a B1 kind is credited to the room being read or to the room that holds it; whether A1 needs a verb that serves the running file's kinds against a room.

## 2026-09-29, night: A1 is reading only (J)

J: "Remove kinds from A1"; "A1 should be just about reading". A1 is back to how it was before the stopping rule: the note has no `kinds:` line (ten fixed lines), `running-A1.md` has no ids, there is no `stopping-A1.md`, and the analyst declares the blocks and the order in `notes-A1.md` and `order-A1.txt`, as before; the close-check no longer demands a seeded order. Kept from later rulings: the A1c interview, `organizing_end-A1.jsonl` with `work_remained` and its recomputation, the leads, the head at A1a. `saturation.py` is B1's alone: `order --stage B1` prints B1's order, the seed is frozen in `out/seed.txt` at B1's first draw, and `mem.py`'s words-read stamp runs at B1 only. Two self-test plants retired (a kind the running file lacks; an order not seeded): 135 checks.

## 2026-09-29, night: B1's estimates follow Chao (J)

J: "Follow chao if it does not affect other things." `saturation.py` now counts a kind, for the estimates, in the room that holds it (`sub` in `kinds-B1.jsonl`), as Chao et al. 2014 assume of incidence data; a theme placed into an earlier room counts in that room from the moment of placement. When a kind is new, and so the resets, the markers' triggers and the draw, is still read from `at`, the room being read. On a simulated walk (120 rooms, 20 kinds, each placed into four earlier rooms) the new-kind events were identical under both creditings; coverage was 0.99 against 0.00 and the rounds 3 against 6. `silent` stays as it is (J). Also: lint, seven unused imports removed; FOR-AGENTS.md records the problem of A1's kinds outliving A2.

## 2026-09-29, night: ChatGPT's review of d9fffd000eec2ea1 (J: "do as you discussed"; point 4 as J set it)

- **One stage file.** `build.sh` moves aside any stage file the instrument no longer holds (to `DROPS/_superseded/`); the renamed C4 file had stayed in `DROPS/C4/` beside the current one, and the compaction hook and `validate.py` took it by name order. `step.sh` writes `.stagefile` from `DROPS/ORDER.tsv`; `validate.py` and `after_compact.sh` read it, and `validate.py` refuses two candidates rather than choosing one.
- **The recall probe.** Each question is right, wrong, missing or not applicable; the score is the right answers over the questions that could be checked, or none. `next` is scored against the leg's last `next:` in the diary. The record says what each check looks at: `changed` checks the id, not the reason.
- **The compaction gate.** A read with `offset` or `limit` no longer counts as reading the head or the stage file, and the stage file is the one `.stagefile` names. The release after five refusals stays (J, 2026-09-28), is logged with the leg, and the close reports it as an exception, not a recovery.
- **Interviews in their own folder (J).** `interview.sh` restores the leg's checkpoint, the analyst's folder and its sessions, into `run/interview-workspaces/<label>__<fork>/` and a Claude project of its own, and runs there, not in plan mode: the PI may add material and the analyst may write, and nothing reaches the live run. The copy's settings shut the live folder and every other copy and carry no hooks. `step.sh --from-cut` refuses a cut that is not the last close.
- Harness test 57 of 57 (seven new: the stale stage file, the partial read, the interview restore).

## 2026-09-29, late: the six must-fix items of audit c (J)

- The trusted validator (`CONTROL/harness/validation_tools/`) now holds every module its checks import (`saturation`, `dreturn`, `handoff`, `ingest`, `distance`, `counts`); every B1 close and the D2 to D4 closes would have failed. A harness test checks the imports.
- `HOW-TO-RUN.md`, emptied by an edit on 29 September, restored from its 27 September version with the later verb changes and three lines for `next`, `idea` and `saturation.py`; `tools/HOW-TO-RUN.md` holds the same text, and A1 and STANDING name the shipped file.
- Checkpoints (`run/CONTROL/snapshots/`) and the harness test's `tests/bin/` are gitignored: the checkpoints stay on disk, one full copy per leg, and git keeps every leg's files through the close commits.
- CONTRACT §6 and METHOD describe B1's stopping rule, not a census to the last room.
- The interview is described as a fork in a copy of the folder, not read-only, in STANDING, ten stage files, the stage cards and READ-ME-FIRST.
- E2's first leg no longer stops under bash 5 when an interview left no transcript; `interview.sh` records a fork only after its folder is restored.


## 2026-10-02: v40, the research changes of the OpenAI copy

J: ChatGPT built a copy of the aggregator that runs on OpenAI's platform (Jail 2, v40) and changed the method on the way; port what applies so that both instruments do the same work. Ported, with Claude's models and routes kept (contract §6, FLEET.md, arm.json unchanged):

- Contract rules 12 and 16, METHOD, the prior template, the adaptations schema, FLEET, the three handoff files and fifteen stage files: counterexamples may warrant a local adaptation, a scope change, a revision or a withdrawal; repetition prompts a substantive comparison, never an automatic revision; the fixed global verdict, the adapted local account and the shared branch are judged apart; silence is unknown, never absence (`observation`: observed-absent, not-needed, unobserved, not-testable); zero or one dimension is a finding; dated within-room and inter-room loops in `model/loops.jsonl`; D3's `recheck-scope.json`; D6's new ideas go to `proposals-D6.jsonl`, unvalidated; E1 audits composition by level and version.
- Tools: `adaptation_ledger.py`, `adaptation_tree.py`, `chunk_compare.py` (new; needs scipy); `dreturn`, `ingest`, `rebuild`, `handoff`, `packets`, `distance`, `gen_views`, `vlib`, `done.sh` and the checks C2, C5, D2 to E1, with three new test files. The trusted validator copies the new tools.
- Continuity: every ordinary leg now forks the last committed close's session, in the same folder (`step.sh`; `--fresh` overrides and is logged). The head and diary orient the leg and do not replace its history.
- The labelers at D2 resume each room's original case lead in Codex (the yard's `_lead_sessions`), where they had been fresh Codex sessions.

Not ported: the OpenAI runtime (`rplace/runtime/`, `run.py`, the control panel, the Codex adapter), the retired hooks, `AGENTS.md` and `OPENAI-RUNTIME.md`, `fleet.py`'s removal of dispatch, the GPT-6 models in `arm.json`.


## 2026-10-02: v41, one instrument on two platforms

J: one version both can run; Codex uses its settings, Claude its own. Built in a new folder, `Jail/Jail 3/rplace`, from Jail 1 (v40, Claude) and the runtime of Jail 2 (v40, OpenAI); both stay as they were.

- The shared files name no model: the stage headers, the contract's stage table, FLEET.md and STANDING-INSTRUCTIONS.md say "as `arm.json` sets", "the routine readers on the platform's reader route", "the reviewer model". HOW-TO-RUN.md's harness section became "Your platform".
- Two schedules, `harness/arm.claude.json` (Claude's v40 arm.json) and `harness/arm.codex.json` (Jail 2's). `harness/gen_platform.py` writes `PLATFORM-claude.md` and `PLATFORM-codex.md` from them; `build.sh` refuses when they are stale and hands the analyst the Claude file; the Codex runtime hands the Codex one (`runtime/study.py`).
- The switch is the reader: Claude Code reads `CLAUDE.md`, Codex reads `AGENTS.md`; each now points to its platform file.
- Runtime from Jail 2: `runtime/`, `run.py`, `OPENAI.md`, `FLEET-ARMS.md`, `harness/fleet-arms.json`, `harness/handling/`, `AGENTS.md`, `OPENAI-RUNTIME.md`. Changed: it reads `arm.codex.json`; it delivers `PLATFORM-codex.md`; "Jail 2" in its messages became the workspace or Jail 3.
- `build.sh` loops over the stage files by glob, so a path with a space (Jail 3) works.

## 2026-10-02: the repository restructured (v41 unchanged in method)

J approved the layout on 2026-10-02. `aggregator-handler/aggregator/` is `aggregator/instrument/`; the harness is `aggregator/handler/claude/`; the Codex controller is `aggregator/handler/codex/`; the input every run reads is `aggregator/input/`; the run is `aggregator/runs/claude-v41-1/`, beside `aggregator/runs/openai-v41-1/`. `yard-handler/` is `coder/`. The Orchestrator is `orchestrator/`. In the instrument only the two platform files changed: the paths they name. The harness changed in four ways: paths; the guard shuts siblings three levels above the run, so the shared input, the other runs, `coder/`, `data/` and `orchestrator/` stay closed to the analyst; stage D4's activity table comes from `input/canvas/D4/`; tags carry the run's folder name (`claude-v41-1/A1`). The fingerprint changes at the next build.

## 2026-10-03: v42, legs five times larger

J ruled (2026-10-03, 09:10 Berlin) after the first two reading legs of claude-v41-1: a leg carries about five times more work, in stage A1 and in the stages after it. A reading block in A1 is about 3 MB (was 0.6) and compacts several times; a stretch in B1b is about 3 MB of second-order material, stated where it had been "as many rooms as a leg holds"; a B4 packet is at most five hundred contested items per leg (was one hundred); `mem.py progress --plan` defaults to 3 MB. `mem.py compare` no longer crashes on a pointer whose `normalised` is null (claude-v41-1, A1a defect 1). The handler's `step.sh --reopen` guard, added on 2026-10-03, refuses a leg the analyst has closed. Method and checks unchanged. The run restarts from A1a as claude-v42-1; claude-v41-1 stops after A1b-02 and stays as the record.

## 2026-10-04: v43, the frame of 705, questions for the principal investigator, nothing asks

Built in a new folder, `r-place`, copied from `rplace` (J, 2026-10-04: "start a new instrument folder ... copy everything else exactly and start updating the instrument with what we discussed"). claude-v42-1 stays in `rplace` as the run of v42.

- **The frame.** Seven rooms finished in the yard on 3 and 4 October joined (r/anime, r/DestinyTheGame, r/hearthstone, r/masseffect, r/pcmasterrace, r/rickandmorty, r/wow; v32, gpt-5.6-sol at medium). r/lehigh and r/upvote left: the census counts a room only if it wrote about the event while the canvas was open (J: "we need only communities in which there was some writing"); r/lehigh's writing about it begins at hour 78.98, and r/upvote's one thread names no canvas, drawing or placement. The frame is 705 of a population of 706; r/the_donald is not coded. Contract §5, stages C5 and E1 and `build_store.py`'s FRAME.md text say so. Contract §5 also says its list of uncoded single-thread slices was made on the frame of 696 and not checked on the eleven rooms added since.
- **Questions for the principal investigator** (J, 2026-10-03: "the agent needs flexibility and to know there is someone on their side"). `mem.py ask "<question>" --assume "<what you do meanwhile>"` writes `out/asks.jsonl` and a diary line of kind ask; `mem.py asks` shows the questions and the answers in `out/_answers/<id>.md`. STANDING-INSTRUCTIONS §2 says when to ask and that the work goes on meanwhile; the tree names both files, and **P**, the principal investigator, as a writer. The wording waits for J's approval.
- **The A1 checks get a verb.** `mem.py audit [frame|rooms|retracted|build]` serves the raw fields the package checks need (claude-v42-1, A1b-03, asked for a saved script). Stage A1 names it, and a saved script with hashed inputs for anything it does not serve. The screen also reads any room first coded after hour 73.
- **The harness (Claude): nothing asks.** A leg runs in `dontAsk` (settings and the launch flag): reads in the working folders, read-only commands, sandboxed Bash and the allow rules run; anything else is refused, never asked. Allow rules: writes in `out/` and in the CLI's scratchpad for this folder, which is now a working directory (from claude-v42-1 after A1b-03), and `Agent`. Before every launch the run's own login marks the repository, the run and the folder trusted (a `git init` above the run had made every leg ask). Interviews run the same way. `step.sh` names answers waiting; `close.sh` lists the open questions. `acceptance.sh` runs its probes in `dontAsk`, one command per Bash call (the batching flake). Harness test 74 of 74.

## 2026-10-04 (later the same day): v43, what a move is for, and the audits

J read Günther, Joshi and Constantinides (2026, *MIS Quarterly* 50(3), 851 to 878: trustworthiness over transparency as an end; what a claim owes depends on whose vocabulary comes first and on whether the words of texts or the shape of the corpus carry it) and asked for the changes the instrument needs, kept inside v43 since no research has run on it, with the audits that a large change deserves. OpenAI's stage-by-stage proposal of 12:18Z was read and mostly declined: most of it the fleet stages already do (readers of one model bound whether the instrument decides, never whether it is right; a split the analyst was unsure about is never revised away; stability under two rewordings is measured in the pilot), and a record field at every stage is the box-ticking the paper argues against. What changed:

- **METHOD.md.** "Rigor is transparency about the moves" is gone: rigor is in the moves, and a move is shown rigorous by its fit to the claim it serves. A paragraph on the paper with its page numbers: the two choices, the two kinds of claim and the validation each owes, the record of a consequential move, the switch record, what same-model agreement shows. The paper is on the A1 shelf, on request (CC BY 4.0; `shelves/_src/gunther-joshi-constantinides-2026.pdf`, `BIB.json`, `_meta`). Felin and Zenger (2016) is held (the SSRN version), as the C3 read shelf had it since; METHOD said not held, and a stale on-request stub listed it twice (set aside in `_to_delete/`).
- **Contract §1, two kinds of claim.** A claim about what rooms did or meant rests on the words of the record and is validated by exemplars and the return; a claim about a pattern across rooms rests on the shape of the corpus and is validated by counts with denominators, the documented events of the 73 hours and D4's alternatives; never one with the other's evidence. `prior.md` §3 declares before B1 which kind each level's verdict will rest on. Rule 11 names the move record.
- **Stage B1 §6, the move record.** A `split`, `merged`, `retired`, `rescoped` or `moved_to_rare` line of `tier_history.jsonl` carries `prompted_by`, and `why` says what the tier after the move carries that it did not; the B1 and C2 checks refuse one without it (planted defect added). `model/history.jsonl` already carries the harness's stamp with the room and theme that prompted each change.
- **Stage A1 §2.** A drop's `why` says what the analysed set loses with the room; a room kept against a doubt is noted.
- **Stage C3 §1, the switch record.** When a work changes what a claim rests on, one paragraph in `literature-C3.md`: the cue, what moved, what is redone, what differs, why the new state serves the claim, the superseding finding. The planned reading is never a switch.
- **Stage C5 §6.** A proposition says what carries it (`carried_by`: words, pattern, both with one primary) and names its strongest rival (`rival`); the C5 check requires both (planted defect added); the D5 fixture follows.
- **Stage D5.** §2 says what a branch's claim rests on (the keys, a pattern; what the rooms did with them, their words); §4 reads a dated change against the bracket of `prior.md` §4 and the members' placements by hour: timing the canvas corroborates is said to be, a mechanism never is.
- **Stage E1 §1, claims against their evidence.** For every proposition and branch, the kind declared, the evidence named, the rival, and whether the validation received is of its kind; `prior.md` §3's declaration against what each level rests on; every switch record against the findings it superseded; written to `claims-E1.md`, which the E1 check now expects `audit-E1.md` to name.
- **Audits.** Stale version strings (the repository and handler READMEs, HOW-TO-RUN, the Manual's front pages said v41 or v38 for the current instrument); `gen_manual.py` reads the version from the run and leaves the Codex pages to the Codex generator; pyflakes clean on the aggregator's Python (unused imports); shellcheck on the harness (a `cd` that could fail silently in `publish.sh`, `verify.sh` and the harness test; `ls`-driven loops in the acceptance scripts; an unused array); the verbs, tools, files and shelves named in the stage files resolve; the Manual's links resolve; `build_shelves.py --only` keeps the report's other rows; `make_meta.py` reads an abstract from the PDF's Subject field when the journal prints no heading. Self-test 0 failures (119 planted defects fire, two new).

## 2026-10-04 (evening): WRITING.md, how the analyst writes

J asked for a style guide the analyst always has (2026-10-04: "generate a writing style guide for the agent that follows Orwell's 6 rules and [Wikipedia's Signs of AI writing] ... a link to the file at the end of claude.md or agent.md but not many links in either nor something at the top"). `WRITING.md` (under 750 words), shipped with the standing documents: Orwell's six rules and what they mean here; the signs of machine writing from the Wikipedia page as read that day (inflated significance, the trailing clause of analysis, vague attribution, editorial asides, negative parallelism, the rule of three, copulas avoided, hollow closers, chat remnants, stacked hedges), each with its watch words; shape and marks (sentence case, bold only for a defined term, no em or en dash, straight quotes, no contractions); the record's own rules restated. It governs the analyst's own words, never a quote, an id or a count. `tools/prose_check.py` lists the watch words in a file and decides nothing; the close-check does not read prose. One line at the end of `AGENT.md` names the file (read at A1, again before C5, D5, D6, E1); the after-compaction reading list is unchanged. `build.sh` ships and fingerprints it; `validate.py` knows the two files. OpenAI asked to add `WRITING.md` to the Codex build's list of standing documents.

## 2026-10-06 (morning): v43.2, a fork's first close counts its own work

J approved the fix ("Fix", 2026-10-06). Every leg after a run's first continues the last close's conversation as a fork (v40). At that fork's first close, `close.sh` skipped the parent transcript's raw line count before it summed the leg's tokens and collected the models for the model audit. A fork in claude 2.1.289 copies only the parent's messages, with their ids, and leaves the parent's other lines behind (seen on J's Mac, 2026-10-05: 56 parent lines, 51 in the fork), so the skip ran into the leg's own rows. On that fork the old count found no turn and no model, and the audit passed with nothing to audit; the new count finds the turn and its model. The cost now runs in `protocol_guard.py cost`: a fork's first session skips its parent's messages by their ids (`rows_skipped_as_inherited` in `cost.json`), and a later boundary of the same session still skips the lines already counted. The harness test adds the case. `claude-v43-1` was rebuilt before its first leg: fingerprint 2cea36a3b16d5aa8 to 343c0f03e9156ecc; the acceptance test is to run again on the Mac. Earlier files: `_to_delete/2026-10-06-claude-harness-before-fork-cost`.

## 2026-10-06 (morning, later): v43.2, the documents as they stand

J, before the first research leg: "update everything", each document "as they are today (noy just changes) imagine thjis is the only version people wil read". No behaviour changed. The harness's `READ-ME-FIRST.md` is rewritten for the principal investigator: how a leg works, the two acceptance tests and the leg handler's live check, every leg through `legs.py` or by hand, both kinds of interview, and who talks to the analyst (only the principal investigator, through `legs.py`, each message and its delivery recorded in `CONTROL/messages-to-legs.jsonl`). Outside the instrument: `HANDLER.md`, the adapter's `LEGS.md` and `README.md`, the Manual's handler pages, glossary and six file pages, the repository's entry pages and the orchestrators' notes. `claude-v43-1` was rebuilt before its first leg: fingerprint 343c0f03e9156ecc to 7690434af40d8f78 (3b57d04d8738fe59 before an independent review's fixes: who speaks to the analyst, the first commit before A1a, the stop-and-close line, D3 among the fleet stages); the acceptance tests are to run again on the Mac. Earlier files: `_to_delete/2026-10-06-docs-before-final-round`.

## 2026-10-06 (morning, last): v43.2, the open fixes and a pristine start

J: "fix the unchanged problems"; then "I want in git that we have at the start a pristine environment", and "the orchestrator is not part of the instrument". Harness (`aggregator/handler/claude/`): `publish.sh` reports a failed `git add` instead of hiding it as "nothing new"; `close.sh` names the next leg in the leg handler's form first (an interview point, a pause), and D1's packets go out with `dispatch.sh D2`; `dispatch.sh` names the check leg in the same form; `step.sh` names each answer to the analyst's questions in the first message of the first leg opened after it, once (`CONTROL/answers-named.tsv`), where an answer written before a leg's `done.sh` was never named. Leg handler (`claude-adapter/legs.py`): an answer to an open leg whose turn has ended is queued for its next turn; every answer, and who sent each line (`source`: the chat or `say`), is in `CONTROL/messages-to-legs.jsonl`; `wait` shows every notice not yet shown; a leg opened by hand is no longer called a leg to "talk to there". Tests: harness 80 (five new), leg handler 15 (one new). The repository's first commit is pristine: the orchestrators' live record (heads, diaries, decisions, messages, change log, the v41 notes) moved outside, to `Jail/Orchestrator/`; the handler's memory starts with its headings only (the v42 run's memory stays in rplace). `claude-v43-1` was rebuilt before its first leg: fingerprint 9b498d8aa840fd18. Earlier files: `_to_delete/2026-10-06-code-before-open-fixes`, `-docs-before-pristine-start`, `-pristine-start`, `-docs-before-fix-descriptions`.

## 2026-10-06 (morning, after the acceptance): v43.2, interviews by J's decision, one repository

J, after `acceptance.sh` 22 of 22 and `acceptance_v41.sh` 23 of 23 on 9b498d8aa840fd18: "interviews can be committed but that is decided on a interview by interview basis", and "r-place should have everything". `.gitignore` keeps out the run's `interviews/` and the analyst's `handling/interviews/`; `CONTROL/interviews.tsv`, the list, stays committed. `HANDLER.md` gives the commands for an interview J decides to commit (`git add -f`); `READ-ME-FIRST.md`, `LEGS.md`, the Manual's handler pages and the comment in `interview.sh` say the same. No step changed: `interview.sh` still copies its transcript beside the run, and at E2a `step.sh` still copies every listed interview into `handling/interviews/`. `orchestrator/Claude/` no longer names `rplace`, which J keeps but nothing relies on; the v42 run's handler memory is also in `Jail/_to_delete/2026-10-06-pristine-start/`. Tests: the harness's test repository runs without background gc (`gc.auto 0`); the leg handler's test checks the new ignore rules. `claude-v43-1` was rebuilt before its first leg: fingerprint 32b4db114bbf4825; its `CONTROL/harness/` differs from the accepted build in one comment line of `interview.sh`, and the acceptance tests are to run again on the Mac. Earlier files: `_to_delete/2026-10-06-before-interview-policy`.

## 2026-10-06 (morning, later): v43.2, nothing set aside stays in the repository

J: "as a rule abything to delete goes to. jail/to_delete with the folder structure fromwhre ut was", and "i dont want extra files in the r-place at tyhe start"; also "I will not delete git rplace but i do not want you to rely on it". `Jail/_to_delete/` now takes everything set aside, under the path it had in `Jail/` (a taken path gets the UTC time before its extension), with one line per move or backup in `Jail/_to_delete/WHY.tsv` and a README there. Harness: `lib.sh` gains `set_aside_dir`; `acceptance.sh` and `acceptance_v41.sh` keep what they make in `Jail/_to_delete/<repository>/aggregator/runs/<run>/acceptance-<time>/` instead of the run's `_to_delete/`, with the compaction gate `acceptance.sh` makes (before, renamed in `CONTROL/`, where it would have been committed) and the guard log the tests' sessions write when there was none before (before, left in `out/_closes/` for J to move). A run outside a repository, as in the harness test, keeps them in its own `_to_delete/`. Tests: harness 84 (four new). The rules (`HANDLER.md` rule 1, `orchestrator/`), the `.gitignore` comment, the Manual's acceptance page and two input READMEs (the frame-before-705 folder is in `Jail/_to_delete/2026-10-04-set-aside/`) say the same. Moved out of r-place: the run's `_to_delete/` (five acceptance folders, two guard logs), five compaction gates from `CONTROL/`, and an empty `_to_delete/` at the top. `claude-v43-1` was rebuilt before its first leg: fingerprint 74db41ef9490edae; the acceptance tests are to run again on the Mac. Backups: `Jail/_to_delete/r-place/...` with the time 20261006T085307Z.
