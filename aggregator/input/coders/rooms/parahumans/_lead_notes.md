# Case-lead running notes

## Before fleet dispatch

- Fresh run: `read.py state` reported cursor 0.
- Read `brief.md` and all of `openings.md` before the gate, as required.
- Gate: branch B; threshold 500; items_in_window 1829; chars_by_people 394650; four slices.
- Openings orientation only: ordinary power and serial discussion gives way to a concentrated r/place episode around making and defending “Read Worm” and the bug, negotiating with neighbouring communities, moving place talk to `r/ParahumansPlace`, welcoming newcomers, and then returning to ordinary discussion after placement ends. This is not coded evidence and will not support relations.
- Batch 01 spans `6243z0` through `62rj2g`, h +0.07 through h +16.41.

## Batch 01 collect

- Collected 25 codes from 25 disposed threads; 5 threads coded; 6 pointers.
- Reviewed all batch additions to `out/timeline.md` and `out/lexicon.md`. Struck none: the timeline lines are edit facts with times and item IDs, and the lexicon lines are participant terms with first-use IDs and no gloss.
- Carry forward: `62ocqw` moves coordination to a replacement thread; later slices must resolve what persisted. Preserve uncertainty around deleted/image-only material, keep the room's own April Fools game separate from canvas conduct, and do not treat an off-platform Discord report as access to the deliberation itself.

## Batch 02 collect

- Collected 70 codes from 27 disposed threads; 16 threads coded; 14 pointers.
- Reviewed all batch additions to `out/timeline.md` and `out/lexicon.md`. Struck none: timeline additions state item-level actions or visible edits with times and IDs, while lexicon additions are participant terms with first-use IDs and no gloss.
- Batch 01's unresolved move is resolved by the replacement coordination thread `62s8mo`. It records containment around Wildbow's request, explicit reply-linked border settlement and repair, newcomer reception, and creation of `r/ParahumansPlace`.
- Carry forward: determine from later slices whether the complete ad and reciprocal defense persisted, whether the dedicated planning subreddit took up coordination, and whether visitor arrival developed into more than immediate welcome. Keep the d3 event-close reply inside batch 02 distinct from batch 02's earlier last-opening edge.

## Batch 03 collect

- Collected 45 codes from 35 disposed threads; 22 threads coded; no pointers.
- Reviewed all batch additions to `out/timeline.md` and `out/lexicon.md`. Struck none: all eleven timeline facts describe edited item content with times and IDs, and all four lexicon lines are participant phrases with first-use IDs and no gloss.
- The inherited project becomes restitution, restraint, reciprocal defense, newcomer welcome, and event-recruited ordinary practices. Direct statements support immediate starting or resuming of Worm after seeing the art, but not sustained readership.
- Carry forward: use batch 04 to settle the Beast and Portuguese help requests, the long Worm/MLP exchange, any continuation in `r/ParahumansPlace`, the fate of newcomer reception, and what the room returned to after placement ended.

## Batch 04 collect

- Collected 48 codes from 31 disposed threads; 12 threads coded; 13 pointers. All four planned slices are now collected.
- Reviewed all batch additions to `out/timeline.md` and `out/lexicon.md`. Struck none: all eleven substantive timeline additions report edited or removed item content with times and IDs, and all eight lexicon additions are participant phrases with first-use IDs and no gloss.
- Earlier allied defense requests receive retrospective evidence in the final-banner and She Beast thanks; redirects to `r/ParahumansPlace` continue. The Steve Irwin complaint directly elicits apology, a boundary promise, repair, and an offer of help.
- Carry to step 5: the strongest contrary item is the comment that the influx made the subreddit “go to shit,” set against direct newcomer defenses. Treat this as an unresolved dispute, not evidence that the community changed its mind. Contrast the final post's “back to normal” claim with the comment-layer dispute. Immediate promises to read and recommendations are supported; sustained retention is not.
- Stop checkpoint: batch 04 collected and reviewed; do not consolidate, pool, theme, or start steps 4–5 until the scheduler continues the run.

## Before step 5 counter-reading

- Step 4 was completed incrementally in slice order. Provisional reading: r/parahumans turned a promotional sign into shared building, negotiated repair and reciprocal neighbour help, then used its visibility to welcome readers while moving disruptive coordination aside.
- Consequential competing account stated before search: the sign was unwanted advertising that encouraged expansion, damaged neighbours, cluttered the subreddit, and produced an unwelcome influx. If the provisional reading is wrong, the record should contain participants abandoning the ad, endorsing attacks or unchecked expansion, refusing repair, or broadly rejecting newcomers.
- Strongest contrary item already in the slice accounts: `dft0tqr`, where a participant says the influx made the subreddit “go to shit.” Also test the earlier “scummy” advertising objection and expansion/attack vocabulary rather than treating later cooperation as unanimous.

## Completion

- Consolidated all four slices, called the required first `emit.close()`, built the forest, and passed `audit_fleet.py` before themes.
- Consolidated themes incrementally by slice. The counter-search added eight grounded codes, including distinct themes for outward-taking proposals and tactical abandonment.
- Counter-search result: cooperation and welcome survive as the main practice account, qualified by real expansion calls, an advertising objection, tactical retreat, and an unresolved newcomer dispute. A refusal-to-repair/help/protect query returned zero items in the searchable record; the scope does not include missing bodies or unseen off-venue talk.
- Wrote the complete case and notes, repaired batch-specific placement of lead remarks in `ledger.md`, reread `_gate.json`, and retained the exact branch-B gate line in `notes.md`.
- Final `emit.close(verdict="full")` recorded two close calls total and integrity `ok: true`. `close_run.py . --role lead --preflight` passed all 10 checks.
