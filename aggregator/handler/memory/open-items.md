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
