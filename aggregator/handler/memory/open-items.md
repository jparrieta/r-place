# Open items

What the principal investigator owes the handler, and what the handler found and left for them. One line each, dated; ticked when done, never deleted.

Seeded 2026-10-06 from Orchestrator/HEAD.md, "Open" (OpenAI's entry of 10:03Z).

- [x] 2026-10-06 J: A1a. Closed 12:30:44Z, checkpoint d556e327327716d9, pushed.
- [ ] 2026-10-06 J: the short-recall rule.
- [ ] 2026-10-06 J: the D1 to D3 and E1 global changes for the siblings (Claude's, per OpenAI's 08:59Z plan).
- [ ] 2026-10-06 J: the "enough" rule for D2 routing.
- [ ] 2026-10-06 OpenAI (not J's; for the record): separate code and test review of Claude's adapter and harness changes through 74db41ef; admission remains disabled.
- [x] 2026-10-06 Handler for J: the run's guard hook firing in a headless turn is not yet seen (LEGS.md, "Before the first real leg", 4); check out/_closes/guard.log after A1a. After A1a: no guard.log anywhere in the run (outside CONTROL/.cc and snapshots); whether the hook fired is still not seen.
- [x] 2026-10-06 J: answer QA1-001 (A1a, concept reach is 1.0 in all 705 rooms; which measure was meant?). Analyst set concept_reach_threshold to 0 meanwhile. Answered 13:17Z with J's approved words: threshold 0, concept level everywhere.
- [ ] 2026-10-06 Handler for J and the orchestrator: A1a refusals. By 12:29Z, 6 of 114 Bash calls refused (mode, dontAsk), every one holding ==, <=, >= or ===, and none that held them passed; 1 Read refused (outside_reads_blocked, the CLI scratchpad root). The run gives Bash no allow rule. The refusal texts ("don't ask mode", "ask the user ... /add-dir") may read to an analyst as "J cannot be asked". Explained in Orchestrator/messages/2026-10-06T12-29Z_from-handler_to-claude_a1a-refusals.md; the fix is the orchestrator's to propose to J.
- [ ] 2026-10-06 J: whether the onset contrast uses the first coded turn at hour 0 or later (r/yogscast -18.58, r/italy -1.14).
- [x] 2026-10-06 Handler for J and the orchestrator: guard false positive at A1b-15 21:21:17Z. pretool_guard.py matched "rm" inside quoted text ("ops rm") in an echo into out/leads-A1.jsonl and refused it as a delete; the analyst reworded the lead to get past it. The guard does fire in headless turns (answers LEGS.md "Before the first real leg", 4). Whether the guard should ignore quoted text is the orchestrator's to propose. Fixed on J's ruling (23:32 Berlin): see changes-for-orchestrator.md, 1.
- [ ] 2026-10-07 J: interview A1c or not (the list stopped at A1c's interview cut); if yes, the commit decision for its transcript.
- [ ] 2026-10-07 J: A1's reading gap. Section 4 asks every room read through forest, coder's account and brief; the read logs show 155, 174 and 98 of 705. The analyst logged it late as a departure and asks whether B1 reads the forest and account for the rooms without them (550 and 531), or only where a comparison needs it.
- [ ] 2026-10-07 J: handback-A1 asks: (1) a verb for package/DATA-manifest-canvas.md, or J's line on placements before hour 0 (defect 7); (2) whether calls after hour 73 to rebuild count as coordinating turns (146 rooms have an organizing end after h73); (3) the B1 reading ruling above; (4) a fix to mem.py diary --last (reads an old diary part once the parts pass 9). Items (1) and (4) are the orchestrator's to build.
- [ ] 2026-10-07 J: B1 starts only on J's word (estimate in stage-estimates.md: 8 to 17 legs, $250 to $600 list).
- [ ] 2026-10-07 J: the catch-up's scope after the A1c interview (accounts and briefs; plus the concepts of the 220 rooms cut at 170; plus forests), its leg size, and the mechanism (extra A1b legs after A1 finished are untested in the harness).
- [ ] 2026-10-07 J: commit the A1c interview transcript or not.
- Catch-up paused by J (2026-10-07 07:55 Berlin) after A1b-33. Resume: move ~/catchup.pause to Jail/_to_delete with a WHY.tsv line, then `legs.py run claude-v43-1 A1b-34..A1b-48` and restart the ticks.
- (closed 2026-10-07 09:23 Berlin, built) B1d stopping rule: orchestrator's proposal (communications/2026-10-07T07-20Z) with J since 07:22Z; open: accept the run-to-marker-1 target, the overflow into seeded order, and whether to set a ceiling.
- Restore of cut notes: J chose (b) at 11:05, prototypes at 11:18; after A1b-48 closes: python3 handler/memory/scripts/build_prototypes.py runs/claude-v43-1; python3 handler/memory/scripts/pretrim_review.py runs/claude-v43-1 49 5; legs.py say claude-v43-1 A1b-48 "$(cat analysis/2026-10-07-msg-restore.txt)", then run A1b-49..A1b-53; catchup.sh restarts 50..53 after audit_restore; audit A1b-53 by hand; then report and wait for J before B1.
- A1b-44's commit is local (push failed 09:45Z, no internet). On return: the next close pushes it, or push by hand on the Mac (not from Cowork). Then lift the pause (move ~/catchup.pause to Jail/_to_delete with a WHY line) and run A1b-45..A1b-48; then the restore (prototypes, message, A1b-49..53).
- A1 restore finished 12:36Z. Before B1: J decides on a short leg to update handback-A1.md (dates from A1c, before the catch-up and the restore). Owed on the Mac: harness test, validator self-test.
- For J: the 9 rooms the restore left minimal on national/political grounds (prototypes exist in pretrim-A1/restored/); whether to put them back, and whether to tell the analyst before B1 that conflict content is study material.
- 2026-10-07 mem.py progress --plan is A1-only; at stage B1 it reports order-A1.txt and 3 MB blocks. Make it stage-aware (B1 order, 1 MB, codes plus themes) or say so in its help.
- 2026-10-08 mem.py codes --grep caps output at 80 lines without saying so loudly; the analyst missed ties because of it (B1b-09). Make the cap visible or add paging.
- 2026-10-08 b1_depth.py: misses room reads done via $TMPDIR files and sed chunks (B1b-13 on), and must add the '[N more characters in the turn's stream.jsonl]' tails; fix before relying on it again.
- 2026-10-08 [future instrument upgrade] analyst-made B1 tools logged in analysis/instrument-upgrade-candidates/2026-10-08/README.md (b1_check_bags.py first; b1_room.py as a mem.py verb; multiplace_write3, split/tier line writers). Review when the instrument is next versioned.
- 2026-10-08 Raise with J at the B1 60% check-in: rule 0 pairs between parents and their own split children (T3-010 with T3-151/150/149; T3-009 with T3-157; T3-014 with T3-152) and T3-001 with T3-095; parents keep absorbing (T3-009 233 placements in 214 rooms). Redraw before B1 closes or leave to C1.
