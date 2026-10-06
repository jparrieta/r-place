# The yard, file by file

The coding yard is where the coder instrument runs over the census: one folder per community, and around them the files of the agent that runs the yard, the **scheduler** (in this study, a coordinator in Codex). This repository ships the yard as it stands before a run: the scheduler's protocol, its tools, and the case lead's instrument, with the fourteen coded rooms of the Armenia and Dutch example and twelve of their case leads' saved sessions. It does not ship what a running yard writes about itself: the queues, the logs, the progress reports. Everything below links to [`coder/`](../../../coder/README.md).

## Read first, if you are the yard's handler

1. [CONTRACT-scheduler.md](../../../coder/handler/CONTRACT-scheduler.md): the scheduler's contract. What it launches, in what order, what it checks, what it may never do, and what is the PI's to decide ([page](contract-scheduler.md)).
2. [README.md](../../../coder/README.md): the yard itself, and how to run a room from any agent runner.
3. [CODING-SCHEDULER.md](../../../coder/handler/CODING-SCHEDULER.md): the coding queue's rules: smallest first by the 97-hour item count, 500 to 50,000 items, how many rooms at once and why, which model and effort.
4. [BRIEF-COORDINATOR.md](../../../coder/handler/BRIEF-COORDINATOR.md): the brief queue's runbook, step by step, with [the brief writer's prompt](../../../coder/handler/BRIEF-WRITER-PROMPT.md).
5. [CASE-LEAD-PROMPT.md](../../../coder/handler/CASE-LEAD-PROMPT.md): the message added for each case lead ([page](case-lead-prompt.md)).
6. [REPAIR-QUEUE-RESTART-RULES.md](../../../coder/handler/REPAIR-QUEUE-RESTART-RULES.md): how to restart the repair queue, beginning by rebuilding "reality from the filesystem, not from stale memory".
7. [CHECKPOINTS.md](../../../coder/handler/CHECKPOINTS.md) and [VERIFIED-RUN-ARCHIVES.md](../../../coder/handler/VERIFIED-RUN-ARCHIVES.md): saving, resuming and forking a case lead ([page](checkpoints.md)), and packing and restoring a verified room.

## What ships

| Part | What it is |
|---|---|
| `_instrument/v32/` | the case lead's instrument: the contracts for the coder, the case lead, the fleet coder and the brief writer, and the tools every room copies; `rationale/` says why v31 and v32 were made |
| `_tools/` | the scheduler's scripts; [the coder's files](README.md) has a page for each |
| `rooms/<sub>/` | fourteen rooms as the yard left them once verified: `ROOM.md`, `STATE.json`, `run.tar.zst`, `materials.tar.zst`, `validation/` ([ROOM.md](room-md.md), [STATE.json](state-json.md)): armenia, PlaceNL, thenetherlands, cirkeltrek, Goodboye, greece, sweden, norge, norway, czech, blackmirror, indonesia, mindcrack, placehearts |
| `_lead_sessions/` | the saved case lead of twelve of them (not Goodboye, not norway), one `.tar.zst` each, split into parts over 95 MB; restore and talk to one as [the case lead's memory page](../../memory/coder-lead.md) describes |

## How to fill it

1. Get the raw record of a community: its raw24 file (see [data and collection](../../data-and-collection.md)).
2. Build its room, from your own copy of `coder/`: `python3 _tools/build_room.py --sub <sub> --raw <raw24 folder>/<sub>.jsonl --out rooms/<sub> --instrument _instrument/v32` (add `--brief` to bring an existing brief). It writes `rooms/<sub>/` with `ROOM.md`, the record cut to the window, the week before, and `STATE.json`.
3. Run it: by hand, with the commands in the room's `ROOM.md`; or through the queues, as the scheduler's contract describes.

## What a running yard adds

| Part | Written by |
|---|---|
| `rooms/<sub>/run/`, `brief/`, `snapshots/`, `forks/`, then `run.tar.zst`, `materials.tar.zst`, `validation/` | the agents, `room.py`, the archive tools |
| `STATUS.tsv`, `PRIOR-RUNS.tsv` | `status.py`, the scheduler |
| `_coding_queue/` (state, events, logs), `CODING-PROGRESS.md` and `.json` | `coding_queue.py`, `update_coding_progress.py` |
| `BRIEF-QUEUE.json` and `.tsv`, `BRIEF-RUN-LOG.jsonl`, `BRIEF-PROGRESS.md` | `brief_queue.py` |
| `_repair_queue/` | `repair_queue.py` |
| `_lead_sessions/` | `codex_lead.py`, `lead_archive.py` |
| a handover, a change log, a log of what has been shown to work | the handler |

## How the scheduler remembers, and saves sessions

The scheduler keeps nothing in its conversation it cannot rebuild. Its state is in the queue files, with every event logged beside them, and a restart begins by rebuilding the state from the files on disk (the repair rules). Each room's state is in its `STATE.json`, rewritten from the room's files; `STATUS.tsv` is rebuilt from all of them. Only the case lead keeps a saved conversation: `codex_lead.py` checkpoints it after every reply, and `lead_archive.py` packs it when the room is done ([how the case lead remembers](../../memory/coder-lead.md)).

## Running a yard elsewhere

The yard runs from any machine with `python3`, `zstd` and Codex. Three scripts name folders on the author's machine and must be pointed at yours before use:

- `_tools/coding_queue.py`, line 16, `LEGACY_TOOLS`: the earlier coder tools;
- `_tools/sync_briefs_to_source.py`, lines 15 and 16, `STAGE` and `SOURCE`: where finished briefs are copied;
- `_tools/update_coding_progress.py`, line 42, `outputs`: where the progress report is also written.
