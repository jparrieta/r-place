# The coder's files

One page per kind of file in the coder instrument (v32) and the run yard. Each page says what the file holds, who writes it and when, why it exists, and where it is. The levels below follow [the coder page](../../4-the-coder.md), from the contracts that govern every agent down to the yard that runs every room; [how it was built](../../3-how-it-was-built.md) tells why each level came to exist.

## 1. What governs: the contracts and notes

One contract holds the method. The others exist because the roles differ: a large room needs a case lead and fleet coders, the week before the canvas needs a brief writer, and the yard needs a scheduler. Each role file says only what differs from the main contract.

- [The coder contract](contract.md): method, rules, five steps, outputs; every role reads it first.
- [The case lead's contract](contract-case-lead.md): openings, gate, fleet, forest, steps 4 and 5.
- [The fleet coder's contract](contract-fleet-coder.md): one slice, steps 1 to 3, tagged edges.
- [The brief writer's contract](contract-brief-writer.md): the seven days before the canvas.
- [The scheduler's contract](contract-scheduler.md): launching, checking and recording between agents.
- [AGENT.md](agent-md.md): the operating notes each agent reads first.
- [The case-lead prompt](case-lead-prompt.md): the calibration block added to the lead's opening message.
- [The changelog](changelog.md): what moved in v29 to v32, and why.

## 2. One room

Everything needed to code a community sits in its own folder, so a room can be run, rebuilt or forked on its own.

- [ROOM.md](room-md.md): the room's numbers and commands.
- [STATE.json](state-json.md): the room's memory.
- [The record files](record-files.md): the cut, the pre-week, counts, openings.
- [The brief and its outputs](brief-outputs.md): the brief writer's directory.
- [The corpus files](corpus-files.md): what a coder reads and cites.
- [The package](package.md): the six outputs and `run/package/`.
- [validation/](validation.md): prompting and check receipts.
- [materials.tar.zst](materials-archive.md): record, brief and instrument, packed.
- [run.tar.zst](run-archive.md): the case lead's whole run directory.

## 3. The tools

Handing an agent the material and asking for codes did not work: it spent its turns writing parsers and serialisers, and its account of its own reading could not be checked. Each tool takes one job away from the agent and leaves a record.

### Reading, citing, emitting, closing

- [read.py](read-py.md): the coder's logged reader.
- [read_brief.py](read-brief-py.md): the brief writer's logged reader.
- [cite.py](cite-py.md): quotes resolved to the record's exact words.
- [emit.py](emit-py.md): the append-only recorder.
- [close_run.py](close-run-py.md): the end-of-run gate, C1 to C12.
- [TOOLS-SPEC.md](tools-spec.md): what the tools share across tiers.

### Building a directory and its corpus

- [newrun.py](newrun-py.md): builds a run directory and fleet batches.
- [newbrief.py](newbrief-py.md): builds a brief writer's directory.
- [cut_window_v32.py](cut-window.md): the 97-hour cut.
- [render_corpus_v32.py](render-corpus.md): the renderer.

## 4. The serial fleet and the case lead

A room of more than 500 items does not fit one reader. It is cut into slices, read by one coder after another, and handed to a case lead who writes the account.

- [render_openings_v32.py](render-openings.md): the openings file.
- [tools/fleet.py](fleet-py.md): plan, dispatch, collect, consolidate.
- [A fleet batch](fleet-batch.md): one coder's slice and outputs.
- [tools/tree_builder.py](tree-builder-py.md): the forest.
- [tools/audit_fleet.py](audit-fleet-py.md): the gate before step 4.
- [How the case lead remembers](../../memory/coder-lead.md): state, checkpoints, resuming and forking.

## 5. The yard and its scheduler

**[The yard, file by file](yard-structure.md)**: every part of the yard the scheduler built, what it is, who writes it, what a new yard handler reads first, and what to change to run a yard elsewhere.

The yard runs every room, smallest first, under a scheduler. The case lead is the one agent saved whole, so a room can be resumed or forked later.

- [room.py](room-py.md): one room, driven from outside.
- [coding_queue.py](coding-queue-py.md): the smallest-first launcher.
- [start_yard_lead.py](start-yard-lead-py.md): the first calibrated lead turn.
- [codex_lead.py](codex-lead-py.md): run and checkpoint the case lead.
- [CHECKPOINTS.md](checkpoints.md): saving, resuming and forking the case lead.
- [lead_archive.py](lead-archive-py.md): pack and restore a lead store.
- [The lead session archive](lead-session-archive.md): the compressed checkpoint store.

## Other yard tools, without a page of their own

Each line is the script's own first line.

- [`codex_coder.py`](../../../coder/handler/tools/codex_coder.py): runs one fleet coder in a temporary, validation-bounded Codex session.
- [`coder_preflight.py`](../../../coder/handler/tools/coder_preflight.py): read-only checks for one fleet coder's batch before consolidation; copied into each batch as `_scheduler_preflight.py`.
- [`build_room.py`](../../../coder/handler/tools/build_room.py): makes one room of the yard from a raw24 collection. The entry point for coding another community.
- [`verify_room.py`](../../../coder/handler/tools/verify_room.py): the scheduler's mechanical checks on one room.
- [`status.py`](../../../coder/handler/tools/status.py): rebuilds `STATUS.tsv` from every room's `STATE.json`.
- [`checkpoints.py`](../../../coder/handler/tools/checkpoints.py): immutable, content-addressed checkpoints for a managed room.
- [`continue_yard_room.py`](../../../coder/handler/tools/continue_yard_room.py): runs the serial fleet cycle, verifies and publishes one reading.
- [`compare_forks.py`](../../../coder/handler/tools/compare_forks.py): sets a room's run and its forks side by side.
- [`archive_verified_run.py`](../../../coder/handler/tools/archive_verified_run.py) and [`archive_verified_materials.py`](../../../coder/handler/tools/archive_verified_materials.py): archive or restore a verified room's run, and its record, brief and instrument.
- [`repair_queue.py`](../../../coder/handler/tools/repair_queue.py) and [`brief_queue.py`](../../../coder/handler/tools/brief_queue.py): the queues for repairing blocked rooms and for writing briefs.
