# The coder

*Kind of page: explanation.*

The coder reads one community's week of talk about r/place and codes it. It writes codes in the participants' words, themes that group them by what these people were doing (Gioia's first-order concepts, though the files call them `second_order`; see [for reviewers](10-for-reviewers.md)), and a within-case account, and it sees no other community while it works. This page describes the coder instrument (v32) from the top down: what governs it, what one room holds, the tools, the fleet and the case lead, and the yard that runs every room. [How it was built](3-how-it-was-built.md) tells why each level exists; the [file index](files/coder/README.md) lists every page.

## What governs: the contracts

One contract holds the method, and every role reads it first: [the coder contract](files/coder/contract.md), with the Gioia two-level coding, the setting, the rules, the five steps and the outputs. The other contracts exist because the roles differ. A room too big for one reader needs [a case lead](files/coder/contract-case-lead.md) to own the account and [fleet coders](files/coder/contract-fleet-coder.md) to read its slices; the week before the canvas needs [a brief writer](files/coder/contract-brief-writer.md); and the whole yard needs [a scheduler](files/coder/contract-scheduler.md) to run the agents. Each role file says only what differs from the main contract and wins on that. [AGENT.md](files/coder/agent-md.md) is the short page of operating notes that sits beside them, [the case-lead prompt](files/coder/case-lead-prompt.md) adds a calibration block to the lead's first message, and [the changelog](files/coder/changelog.md) records what moved between versions and why.

The source files are in [the v32 instrument folder](../coder/instrument/v32/README.md).

## One room

Everything needed to code a community sits in its own folder, so a room runs on any machine with Python and can be rebuilt or forked on its own. [ROOM.md](files/coder/room-md.md) is its front page: the numbers and the commands in order. [STATE.json](files/coder/state-json.md) is its memory, rewritten from the files and extended by the scheduler. [The record files](files/coder/record-files.md) are the 97-hour cut (the 73 hours the canvas was open, plus the day after) and the seven days before, counted before any agent arrives. [The brief's folder](files/coder/brief-outputs.md) holds the brief writer's work, and the run folder holds the coder's. What a coder reads and cites is described under [the corpus files](files/coder/corpus-files.md); what it hands on is [the package](files/coder/package.md): the codes, themes, thread dispositions and pointers, the case and the notes. Once a room is verified, its inputs are packed into [materials.tar.zst](files/coder/materials-archive.md), its whole run into [run.tar.zst](files/coder/run-archive.md), and the receipts of how it was prompted and checked into [validation/](files/coder/validation.md).

## The tools

Tools exist because handing an agent the material and asking for codes did not work: it spent its turns writing parsers and serialisers, and its account of its own reading could not be checked. Each tool takes one job away from the agent and leaves a record.

- **Reading.** [read.py](files/coder/read-py.md) serves the rendered corpus in order and logs every service. The brief writer has its own reader, [read_brief.py](files/coder/read-brief-py.md).
- **Citing.** [cite.py](files/coder/cite-py.md) resolves a quote to the record's exact words and offsets, or refuses.
- **Emitting.** [emit.py](files/coder/emit-py.md) records every code, theme, disposition and pointer as an appended call, and refuses some defects at the moment of writing.
- **Closing.** [close_run.py](files/coder/close-run-py.md) is the end gate, twelve checks that pass or fail. The agent runs it as a preflight before its final message, and the scheduler runs it again after.

Around them sit the builders: [newrun.py](files/coder/newrun-py.md) and [newbrief.py](files/coder/newbrief-py.md) lay out a directory, [render_corpus_v32.py](files/coder/render-corpus.md) and [cut_window_v32.py](files/coder/cut-window.md) turn the raw record into what a coder reads. [TOOLS-SPEC.md](files/coder/tools-spec.md) says what these tools share with the brief writer's and the aggregator's.

## The serial fleet and the case lead

A room of more than 500 items does not fit one reader. The case lead reads [the openings file](files/coder/render-openings.md) to see the week's shape, decides the branch once, and in branch B cuts the room into slices of whole threads. [tools/fleet.py](files/coder/fleet-py.md) builds one batch folder per slice, in order, and the yard's [codex_coder.py](../coder/handler/tools/codex_coder.py) runs one coder in each; each coder works in [a fleet batch](files/coder/fleet-batch.md) and passes a timeline and a lexicon to the next. When the last batch is collected, the lead builds the forest with [tools/tree_builder.py](files/coder/tree-builder-py.md), passes the gate in [tools/audit_fleet.py](files/coder/audit-fleet-py.md), groups every first-order code into the room's second-order themes, and writes the account. How the lead and its coders remember across calls is told in [the coder lead's memory page](memory/coder-lead.md).

## The yard and its scheduler

The yard is one folder per census room plus a scheduler that runs them, smallest first. The scheduler follows [its contract](files/coder/contract-scheduler.md): launch an agent, check what it wrote, record the result, and ask J, the principal investigator, only what is his. [room.py](files/coder/room-py.md) drives one room from outside without calling a model, and [coding_queue.py](files/coder/coding-queue-py.md) launches rooms in order, a set number at once. The case lead is the one agent saved whole: [start_yard_lead.py](files/coder/start-yard-lead-py.md) runs its first turn, [codex_lead.py](files/coder/codex-lead-py.md) checkpoints it after every reply as [CHECKPOINTS.md](files/coder/checkpoints.md) describes, and [lead_archive.py](files/coder/lead-archive-py.md) packs the finished store into [the lead session archive](files/coder/lead-session-archive.md). The yard's own README is at [../coder/README.md](../coder/README.md).

## If you read only five files

1. [The coder contract](files/coder/contract.md): the method and the five steps.
2. [The case lead's contract](files/coder/contract-case-lead.md): what changes when a room is too big for one reader.
3. [emit.py](files/coder/emit-py.md): how a reading becomes a record.
4. [close_run.py](files/coder/close-run-py.md): what counts as a finished room.
5. [The scheduler's contract](files/coder/contract-scheduler.md): how the yard runs.
