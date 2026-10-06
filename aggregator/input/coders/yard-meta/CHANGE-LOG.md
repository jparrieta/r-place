# Change log

## 2026-09-07 — authorized scope and execution

- Queue contains only the 395 communities with missing briefs and no earlier recorded run. The 30 previously coded communities are excluded.
- Queue uses `items_in_window` from the 97-hour event window, ascending; equal counts use the subreddit name as a stable tie break. Pre-week size does not set the order.
- First room: `britishcolumbia`, 300 event-window items. `the_donald` is rank 394; `place` is rank 395.
- Requested GPT-5.6 is implemented as `gpt-5.6-sol`, explicitly selected for correction agents and brief writers. Full platform transcripts are available; their model field is checked when collecting writer output.
- The 395 briefs consist of 370 writer assignments and 25 empty-record harness outputs.
- Work runs in this writable staging yard. Source data were copied from `/Users/arrieta/Documents/Codex/rplace/atlas_yard`; final write-back is a separate logged filesystem operation.

## 2026-09-07 — supplementary brief revision v30-brief-r1

- Replaced the oversized compulsory header with a compact archive summary, seven actual calendar-day counts, moderation/removal counts, top 40 authors, and a summary of remaining authors. The thread index is available through sampled or paginated titles.
- Bounded each reading response at 18,000 characters and enforced the 75,000-estimated-token ceiling before output. Long items and threads have explicit continuation positions.
- Changed sampling from unbounded whole-thread output to bounded item excerpts across least-read active days and rotating thread-size quantiles. Writers must read surrounding thread context before describing interactions. This is an explicit change in the brief reading procedure.
- Coverage now records the exact Unicode body spans served. Repeated reads are deduplicated; partial items and complete items are distinguished; comments count on their own actual dates, even in older threads. Empty days and unread active days are distinguished across all seven days.
- Added the tool-generated `out/evidence.json` receipt. The validator reconstructs its coverage from the source record and read log.
- Removed the blanket 300-word floor; retained substantive required sections and evidence support. Sparse records may produce short, qualified briefs.
- Added strict item-linked quote validation against the spans actually served. Wrong-item matches no longer fall back to another item elsewhere in the corpus; fabricated quotations receive no tolerance.
- Header-only reading and unexplained omission of active days now fail validation. A recorded hard-ceiling exception must name the omitted days.
- Empty briefs now describe zero items in the supplied archive without claiming independent historical completeness. Their raw count and output hashes are checked; no fake agent transcript is created.
- Corrected the empty-record self-test to skip the simulated writer. Self-tests use disposable copies with the revised canonical brief tools.
- A new brief is marked verified only after a passing, current validation receipt. Changes to checked files invalidate the receipt, and downstream event coding cannot start from an unvalidated new brief.
- Added a durable queue, per-room execution events, validation outputs, progress table, and model/transcript provenance.

Original versions, hashes, and the final patch are retained under `_changes/`. Corrections apply to the brief stage; event-coding contracts are not part of this task.

## Validation and first dispatch

All 32 regression tests and empty, sparse, and nonempty end-to-end self-tests passed. The macOS `/var` and `/private/var` aliases are treated as the same evidence path. Pilot dispatch began in queue order on 7 September 2026; afip was generated and verified automatically. Writer assignments and outcomes are recorded in `BRIEF-RUN-LOG.jsonl`.

## Pilot editorial corrections and lifecycle safeguards

- Independent pilot review identified frequency, abbreviation-support, and reply-relationship wording corrections. Writer prompts now explicitly guard against generalizing from one author or thread.
- Actual restart testing exposed a model switch from Sol to Astra. The transcript model gate rejected all three resumed revisions; rejected versions and their mixed-model transcripts were preserved for audit, and original Sol drafts restored for fresh Sol edits.
- Coordinator fork and completed-history recall succeeded. Restarting a worker as coordinator did not grant spawn capability; delegation stays with this coordinator.
- Production acceptance continues to require an explicit GPT-5.6 Sol model check; close/resume is not used for production writers.

- All three pilot edits were accepted after fresh Sol-only revision and mechanical revalidation. Their original and revision transcripts are retained together.
- Buffalo's concurrent item reads generated duplicate sequence numbers. Preserved the pre-repair log and repair manifest, restored the original Sol reading history, retained both fresh Sol reading events in append order, and normalized only their sequence field. No content, spans, item IDs, timestamps, or coverage claims were fabricated. Sequential reads are now explicit in writer prompts; reader serialization is under test.

## Read-log concurrency fix

- Added POSIX file locking around log replay, budget checks, sequence assignment, append/flush, shared state, and evidence generation. This prevents simultaneous reader commands from reusing a sequence or racing the shared reading limit.
- Added real 24-process concurrency and two-live-reader receipt regressions. Full suite now passes 34 tests (10 reader, 13 brief-validator, 11 other existing checks).
- Existing prepared briefs keep their manifest-hashed reader; new preparations receive the fixed reader. Legacy sequence issues are audited and corrected without changing source spans.
- Added a read-only first-N milestone checker for source presence, current validation hashes, no prior runs, and Sol-only full writer transcript models.

- Wales's legacy reader also had concurrent sequence collisions. Preserved all 37 actual read records with timestamps, bodies/spans and character counts unchanged, normalized sequence numbers to append order, and saved before/after hashes and changed-number mapping. Its full Sol transcript and repaired log passed validation.

## First ten editorial acceptance

- Corrected Wales's timing inference by separating the early transport item from late-window local activity.
- Stargate now records SGU without an unestablished expansion and treats two Indeed replies as repeated wording rather than assumed allusions.
- Both original writers applied these changes without closing/resuming; all their transcript turns remained GPT-5.6 Sol. All first-ten briefs passed validation in staging.
