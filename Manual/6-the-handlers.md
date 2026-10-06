# The handlers

*Kind of page: explanation.*

Two instruments, two handlers. The yard's handler runs the coder side: it launches the agents that code each room, checks what they leave, repairs what fails and keeps the queue moving. The aggregator's handler builds a run, closes each leg, sends the readers their packets and answers the analyst in files. Neither handler reads for the study. Both keep their memory on disk, and part of it lives outside this repository.

## The yard's handler (coder side)

### What it does

The [scheduler's contract](../coder/handler/CONTRACT-scheduler.md) ([page](files/coder/contract-scheduler.md)) states the job: "you take a room from `rooms/`, launch the agents its `ROOM.md` names in the order the instrument fixes, check each agent's work with the checks below the moment it ends, keep `STATUS.tsv` true, set aside what failed, take the snapshot the forks are made from, and tell J what only J can decide." It is "not a reader". It never judges a coding, never rewrites an agent's line, and passes nothing between agents except the files the instrument says travel.

The contract asks for no particular model or program. In this study the coordinator ran in Codex, latterly on GPT-5.6 Terra, while brief writers, case leads and fleet coders ran on GPT-5.6 Sol.

Its work, as the yard's documents lay it out:

- **Launching.** [room.py](../coder/handler/tools/room.py) ([page](files/coder/room-py.md)) prints the opening message for each agent. [start_yard_lead.py](../coder/handler/tools/start_yard_lead.py) ([page](files/coder/start-yard-lead-py.md)) prepares a room and runs its first lead turn. [coding_queue.py](../coder/handler/tools/coding_queue.py) ([page](files/coder/coding-queue-py.md)) picks the smallest ready room and keeps up to six running; when one ends, it checks that room, archives it and fills the slot ([CODING-SCHEDULER.md](../coder/handler/CODING-SCHEDULER.md)). Briefs have their own queue and runbook ([BRIEF-COORDINATOR.md](../coder/handler/BRIEF-COORDINATOR.md)).
- **Feedback.** A failed batch check goes back to the same coder for up to two correction turns; a failed room check goes back to the same case lead, also twice at most.
- **Repairs.** After two failed runs in a row a room stops, with `repair-stopped-after-two-failures` recorded. The [repair rules](../coder/handler/REPAIR-QUEUE-RESTART-RULES.md) say how to restart the queue, and that a restart begins by rebuilding "reality from the filesystem, not from stale memory". A model service at capacity is recorded as a service interruption and does not count against the room.
- **Changing the instrument.** When a defect repeats, the handler writes down why the instrument must move, and the instrument's [changelog](files/coder/changelog.md) records the change. A dispatched run keeps the instrument it started with.

### How it remembers

The yard's handler has no single head file. The yard ships empty, so none of what follows is in this repository: each file is written by the handler or its tools once a yard runs.

| file | what it holds | written by |
|---|---|---|
| `rooms/<sub>/STATE.json` | each room's memory ([page](files/coder/state-json.md)) | `room.py status`, the scheduler |
| `STATUS.tsv` | one line per room, rebuilt, never edited | `status.py` |
| `_coding_queue/STATE.json`, `EVENTS.jsonl`, `REPORT-STATE.json`; `CODING-PROGRESS.md` | the queue's state, its event history, what has been reported; the progress report | `coding_queue.py`, `update_coding_progress.py` |
| `BRIEF-QUEUE.json`, `BRIEF-RUN-LOG.jsonl`, `BRIEF-PROGRESS.md` | the brief queue, its completion history, its report | `brief_queue.py` |
| `_repair_queue/` | the repair queue's state and events, and its state before each intervention | `repair_queue.py` |
| a handover, a change log, a log of what has been shown to work | the handler's own notes between sessions | the handler |

The repair rules add one plain instruction: record model, effort, start, end, tokens and archive hash "so future reports do not depend on chat memory". [The yard, file by file](files/coder/yard-structure.md) shows what ships and what a running yard adds.

### How it snaps and saves sessions

Only the case lead keeps a saved conversation. [codex_lead.py](../coder/handler/tools/codex_lead.py) ([page](files/coder/codex-lead-py.md)) runs the lead in Codex and, after each completed reply, commits a checkpoint through [checkpoints.py](../coder/handler/tools/checkpoints.py): the managed room, the lead's native Codex home, and the runner's state, content-addressed under `_lead_sessions/<sub>-gpt56-calibration-v1/`. The last collect of branch B is saved as `after-fleet`, the fork point. [CHECKPOINTS.md](../coder/handler/CHECKPOINTS.md) ([page](files/coder/checkpoints.md)) covers resume, fork, restore and recovery.

When a room ends, three tools pack it:

- [lead_archive.py](../coder/handler/tools/lead_archive.py) ([page](files/coder/lead-archive-py.md)) packs the lead's store into one `.tar.zst` ([page](files/coder/lead-session-archive.md)) and writes its hash and size into `STATE.json`.
- [archive_verified_run.py](../coder/handler/tools/archive_verified_run.py) packs `run/` into `run.tar.zst` ([page](files/coder/run-archive.md)).
- [archive_verified_materials.py](../coder/handler/tools/archive_verified_materials.py) packs `record/`, `brief/` and `instrument/` into `materials.tar.zst` ([page](files/coder/materials-archive.md)).

Each archive is test-extracted against the source hashes before the source is removed. [VERIFIED-RUN-ARCHIVES.md](../coder/handler/VERIFIED-RUN-ARCHIVES.md) gives the restore commands. How the lead remembers inside a room (ledger, notes, journals) is on [its memory page](memory/coder-lead.md).

Fleet coders and brief writers keep no session. Their outputs and transcripts travel; the temporary coder session is deleted once its batch passes.

## The aggregator's handler

### What it does

The [harness's read-me](../aggregator/handler/claude/READ-ME-FIRST.md) ([page](files/aggregator/harness-read-me-first.md)) names three parties: the analyst, "a Claude session that lives in `00_GIVE-THE-AGENT/` and sees nothing else"; the handler, a Claude session of its own (Claude Code on J's Mac, or Cowork), which builds the run, checks each close and answers in files; and J, who owns the study and decides.

The harness, in `aggregator/handler/claude/`, with a copy in each run's `CONTROL/harness/`:

- [build.sh](../aggregator/handler/claude/build.sh) lays out a run and writes its fingerprint into `CONTROL/RUN.json` ([page](files/aggregator/harness-build-sh.md)); [acceptance.sh](../aggregator/handler/claude/acceptance.sh) tests it before A1 ([page](files/aggregator/harness-acceptance-sh.md)).
- [step.sh](../aggregator/handler/claude/step.sh) opens a leg, continuing the last close's conversation ([page](files/aggregator/harness-step-sh.md)); [close.sh](../aggregator/handler/claude/close.sh) closes it: the recall probe, the trusted close-check, the model audit against `CONTROL/arm.json` (a forked leg counts only its own messages), and the checkpoint ([page](files/aggregator/harness-close-sh.md)).
- [dispatch.sh](../aggregator/handler/claude/dispatch.sh) sends the analyst's packets to the readers ([page](files/aggregator/harness-dispatch-sh.md)); [pause.sh](../aggregator/handler/claude/pause.sh) asks the analyst to stop at its next safe stop ([page](files/aggregator/harness-pause-sh.md)); [interview.sh](../aggregator/handler/claude/interview.sh) opens an interview ([page](files/aggregator/harness-interview-sh.md)).
- [stage_cards.py](../aggregator/handler/claude/stage_cards.py) writes one card per stage for J ([page](files/aggregator/harness-stage-cards-py.md)).

The leg handler, in `aggregator/handler/claude-adapter/` ([LEGS.md](../aggregator/handler/claude-adapter/LEGS.md)), runs those same scripts without a terminal per leg (J, 5 October 2026: "a handler i can access via claude code/cowork that opens and close the sessions plus the ability to talk to EACH AGGREGATOR STAGE.LEG"):

- `legs.py serve`, one process on the Mac, owns the analyst's sessions. Every other command is a client, the same from Terminal, Claude Code (also through Remote Control from the phone) and Cowork.
- `open`, `close` and `run` take a leg or a list of legs. Each turn is one headless Claude process ([actor.py](../aggregator/handler/claude-adapter/actor.py)); `step.sh` prepares the leg and `close.sh` closes it, as by hand. A list stops at a refusal, a failed turn, a pause, a dispatch, an interview point, a stage's end or a forced close, and says why.
- `chat RUN` is one window where J talks to every agent of the run and sees each one's words and tool calls live. A line reaches a running analyst beside its next tool result, with a receipt, or starts a new turn. `answer` delivers J's answer to a question the analyst asked; `interview` opens a closed leg.
- `branch` and its companions make an analysis branch: a new run from one verified close, with a new stage card or data, committed to its own Git branch and never to main.
- [probe.py](../aggregator/handler/claude-adapter/probe.py) and [probe_lifecycle.py](../aggregator/handler/claude-adapter/probe_lifecycle.py) check the live CLI and the actor in a synthetic run, never a research run.

Who speaks to the analyst: only J, in his own words, through the leg handler, and each message and its delivery are recorded in `CONTROL/messages-to-legs.jsonl`, committed at every close. The handler never does. A question from the analyst (`mem.py ask`) is written down and answered in a file. At stage D2 a second handler, the adaptation handler, runs the labelers in Codex; the contract calls that role the handler too.

The v37 handover described the same seat in more detail: seven kinds of message to J (READY, CLOSED, READING, QUESTION, RULING, PROBLEM, FORK), one kind per message. See [the v37 run](8-the-v37-run.md).

### How it remembers

The handler keeps its memory in [`aggregator/handler/memory/`](../aggregator/handler/memory/README.md): a diary with one dated line per action, a decisions table (date, decision, by whom, source), the principal investigator's open items, and handovers between sessions. [HANDLER.md](../aggregator/handler/HANDLER.md) says what goes in each and what to read first. Beside them: [the design note](../aggregator/handler/DESIGN-NOTE-v38.md), the instrument's [change log from v37](../aggregator/instrument/CHANGELOG-v37-to-v38.md), and git, which keeps every version of every file. Inside a run, the harness keeps `CONTROL/sessions.json`, `CONTROL/handover-events.log`, `CONTROL/interviews.tsv` and `CONTROL/snapshots/INDEX.tsv`; the leg handler keeps its streams, requests and results in `CONTROL/legs/` (on disk, not committed) and J's words to legs in `CONTROL/messages-to-legs.jsonl` (committed).

The analyst's own memory (its head, diary and read logs in `out/`) is a different thing, on [its own page](memory/aggregator.md).

### How it snaps and saves sessions

Each close publishes a checkpoint under `CONTROL/snapshots/<label>/`: the analyst's folder, the run's own sessions (`agent.tar.gz`: `projects/run/` of the run's Claude folder and nothing else), the transcript verified by id, the cost and the ancestry, built in a temporary folder under a lock and written `COMMITTED` last. `close.sh` also copies the leg's transcript into `out/_transcripts/` ([page](files/aggregator/out-transcripts.md)).

[snap.py](../aggregator/instrument/tools/snap.py) ([page](files/aggregator/tool-snap-py.md)) writes a hash of every file in `out/` under a name, once, into `out/_snap/` ([page](files/aggregator/out-snap.md)). The harness takes one at every close; the analyst takes one at each move and wherever an order matters.

An interview is a fork of a closed leg in a copy of the analyst's folder restored from its checkpoint (`interview-workspaces/`, not committed); nothing said there reaches the run. [interview.sh](../aggregator/handler/claude/interview.sh) opens one in a terminal, logs it in `CONTROL/interviews.tsv` and copies its transcript to `RUN/interviews/`; `legs.py interview` opens one from the chat, logs it the same way and leaves its transcript in the run's Claude folder (`CONTROL/.cc/projects/iv-<fork>/`). At stage E2a, `step.sh` copies every listed interview into the analyst's `handling/interviews/`. A transcript reaches git only if J decides so, interview by interview. [publish.sh](../aggregator/handler/claude/publish.sh) ([page](files/aggregator/harness-publish-sh.md)) runs after each close and interview: it regenerates the Manual's run pages, commits everything to git, tags interview points and finished stages, and pushes when a remote exists. The run's Claude folder, `CONTROL/.cc`, is kept out by `.gitignore`: it holds the login's account record, the account's synced skills and plugins, and caches. A checkpoint keeps only the run's own sessions from it (`projects/run/`), so no account data reaches git. On macOS the login token is held by the Keychain, not in that folder.

## The orchestrators

Two coordinating agents keep what the handlers run: Claude (the instrument, the Claude harness, the leg handler, the repository's layout and git) and OpenAI (the Codex runtime, its controller and phone panel). Neither runs the study, and the orchestrator is not part of the instrument. [`orchestrator/`](../orchestrator/README.md) describes what they do and holds what they use: `PROTOCOLS.md` (the checks both run) and each one's role, rules, processes and scripts. It changes only with a new version of the instrument. What they write as they work (where things stand, decisions, diaries, messages to each other and to the handler) is kept outside the repository, beside it; a problem found in a run reaches the repository as the next version of the instrument. [OWNERSHIP.tsv](../OWNERSHIP.tsv) says which files are shared, Claude's or Codex's. A change to the instrument or the harness needs J's approval, is recorded in the instrument's change log and `VERSIONS.tsv`, and reaches the handler as a message.

## The protocol, and the handler's own scripts

Whoever handles a run next starts from [HANDLER.md](../aggregator/handler/HANDLER.md), at the top of the handler's folder. It sets out:
- who decides what, and the rules that do not bend (nothing deleted, never writing in the yard, the handler never speaking to the analyst inside a leg);
- how the handler remembers across sessions: the diary, the decisions table, the version log, the PI's open items, handovers;
- its duties before the run (import the rooms, build the canvas, the shelves, build and accept, check the leg handler) and during it (each leg, by hand or through `legs.py`; after each close; at fleet stages; interviews; before E1 and E2);
- how the instrument is changed and recorded, and how the repository is kept.

The scripts those duties name are beside it, in [the handler's folder](files/handler/README.md), with every outside path set once in `aggregator/handler/paths.json`.

## What is not in this repository

Much of the handlers' memory lives in the Claude project "r/place" on claude.ai: its documents (handovers, states of play, design notes, close-outs such as `claude/handover-2026-09-22.md` and `claude/handler-log-v37-close-out.md`) and the project's memory. None of these are mirrored here. Nor are the logs either handler's agents wrote while coding the census and building v38: both handler folders ship as they stand before a run. The coded rooms themselves reach the aggregator as its input, in `aggregator/input/`; see [requirements and data](requirements-and-data.md).
