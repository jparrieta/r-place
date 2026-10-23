
### Close-check, D3b (first batch)

`validate.py D3` reports 77,062 of 77,062 ledger lines ruled. It gives 233 errors and 12 warnings.
- **The 233 errors** each name a room with no checked local account for the revised model. They are exactly the 233 rooms pending, second batch (223 not started, 10 reissued). Under J's terms of QD3-009 these rooms stay affected and pending until the second batch, so the errors are the expected state, not a defect in this leg's work.
- **The warnings.** Ten say that `verdicts-recheck-D.jsonl` has no line for a reissued room, and say why here. The reason is above: ingest rejected these ten rooms (nine cut off mid-room, one end marker to be repaired), so the verdict fleet had no return to judge. The other two are the old warnings on the move name 'stabilizing' (history lines 137 and 138, corrected at D3a-06 by an appended line).
- **Written:** 34,819 re-check rulings (`adjudications.jsonl`, now 77,868 lines); the rulings files in `_analysis/d3_rulings/`; this section, the per-room table and the appendix.
- **Unchanged:** verdicts (868), history (170), elements (45), arrows (21), findings (37), tier history (561) and every scope file. No move was made, and the model hash stays 46384686….
- **Questions.** If `done.sh` refuses the close on the 233 pending rooms, the conflict between the close-check and J's term to close D3b at the first batch goes to J as a question.
