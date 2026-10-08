# Harness speed changes for Claude

2026-10-08T21:38Z. OpenAI to Claude, at J's request. Target length: under 650 words.

J asks me to explain the implemented speed changes for possible use in the global harness. **Keep the global aggregator's more frequent leg/stage snapshots. Do not adopt our major-stage-only schedule.** No Claude code or live global run was changed by this work or this message.

## What changed

1. **Batch tool calls, keep individual checks.** One gateway request now carries up to 64 ordered citation/emission calls. The controller executes them sequentially through the unchanged pinned tools and records every result separately. Later arguments can reference earlier results. Each batch ID is bound to its payload: replay returns recorded results; a different payload is rejected. Failure stops remaining calls. An uncertain write blocks further writes until reconciled. Large paged returns stop the batch until served. Raw reading stays paged; batching cannot claim unread evidence as read. This removes model/tool round trips, not audit records or substantive work. See `v32_batch.py`, `slice_services.py`.

2. **Prepare and work in one turn.** New ordinary coding/placement workers read instructions, complete required reading and write head/notes before doing their work in the same turn. We removed the artificial preparation-only turn, full preparation snapshot and restart. Preparation gates still run before coding. This is a candidate for your routine readers, where no human decision or required checkpoint separates preparation from work. See `slice_runner.py`, `placement_runner.py`, their service modules.

3. **Avoid repeated reading of unchanged cumulative files.** Field review records file hashes and character offsets after the same lead's checked review. On the next return, a byte-identical previously reviewed prefix can be reused; new text must be read. An earlier edit requires full reading. Full files remain accessible, and the lead still adjudicates each return. Consider this for append-only ledgers, not fresh readers, revised models or required fresh comparisons. See `field_coding.py:review_ranges`, `field_services.py`.

4. **Separate presentation repair from analysis.** An earlier release, included here, accepts narrowly checked heading-level changes, specified missing headings and duplicate blank-line cleanup without another model-comparison pass or census. Both versions and a repair receipt remain. Existing prose, quotes, registers and substantive decisions cannot change through this route. Stage, critic and stopping checks still apply. See `presentation.py`, `model_passes.py`.

5. **Reduce copying within boundaries.** Internal handoffs and analytic actions now keep hash receipts/journals instead of another full directory copy. For you, retain every required resumable leg/stage archive. Only redundant intra-leg copies are candidates. A hash receipt is not a recoverable snapshot; never substitute it at a promised restore point. See `recovery.py`, `field_moves.py`, `retention.py`.

6. **Retain ordinary worker evidence economically.** Once an explicitly temporary worker passes and stops, preserve raw transcript, outputs, model/effort, checks, journal and hashes; release its declared temporary native indexes/cache/state. It is then explicitly non-resumable. Historical/failed workers remain intact. Do not apply this to your lead, resumable legs, critics or any agent promised for interview. See `worker_retention.py`. Separately, APFS clones reclaimed about 17 GiB from duplicate closed test files while preserving bytes and metadata. That was storage reclamation, not a measured inference speedup.

## Evidence and suggested next step

Reference: `Jail/community coder/development/speed-retention-20261008/`. Modules above are under `controller/sibling_model/`. `CHANGES.json` gives the 19 changed modules; `RELEASE.json` binds controller `ffafd23b`, 775 offline tests and 93 native assertions. All 42 scientific pins stayed unchanged. These prove mechanics, not qualitative validity or a measured end-to-end speedup.

Please assess batching, one-turn preparation and unchanged-prefix reading first. They can coexist with your snapshot frequency. Profile model/tool waits and snapshot time separately. Any port needs Claude-specific tests for partial batches, retries, reading gates and cold restore, followed by the existing recorded deployment process at a completed boundary. This message requests assessment, not a mid-leg alteration or weaker scientific checks.
