# How it was built

*Kind of page: explanation: why each kind of file came to exist.*

Nobody sat down and designed the files in this repository. Each kind of file is here because some earlier version lacked it and paid for the lack. This page tells that story in order: first the data, then the coder, then the aggregator, then the handlers that run both. At each step it names the files the step left behind and links their pages. The history is simplified; where the sources do not settle a point, the page says so.

## First, the data

The problem was structured in three parts: collect the data, build a solid foundation for each community, and only then aggregate.

Collection came first. For each community in the census the project fetched its Reddit record and cut it to a fixed window. The window was ten days at first. It became 97 hours, from the canvas opening on 2017-03-31 at 16:00 UTC to one day after placement stopped, when several codings of r/liverpoolfc found every code inside it and nothing codeable beyond. The cut had a second benefit: a large room's corpus now fit in one agent's context. The seven days before the canvas opened were kept apart, as a separate record for a separate reader.

That part of the work left [the record files](files/coder/record-files.md) in each room, cut by [cut_window_v32.py](files/coder/cut-window.md), rendered into readable text by [render_corpus_v32.py](files/coder/render-corpus.md) and served to the coder as [the corpus files](files/coder/corpus-files.md). The raw collection itself is not in this repository.

## A foundation for each community: the coder contract

The coder contract started from one question: what would Gioia, Corley and Hamilton, and Eisenhardt, need from a case? The criterion was written down early, in J's words: "Gioia and Eisenhardt, done by a single agent that sees one forum and no other case. Everything else is negotiable." Gioia needs first-order concepts in the informants' words and themes grouped from them. Eisenhardt needs a within-case account written before any comparison.

So the coder writes both, as separate files. The codes and themes go to one set of files, the account to another, so that aggregators of different kinds could use the output: one working from the codes up, another reading the cases as accounts. That is why [the package](files/coder/package.md) a room hands on holds `codes.jsonl` and `themes.jsonl` beside `case.md`, and why the aggregator's side has pages for [the room's codes](files/aggregator/room-codes-jsonl.md), [its themes](files/aggregator/room-themes-jsonl.md) and [its case](files/aggregator/room-case-md.md) as distinct files.

The contract went through some thirty versions before the one in this repository, [v32](files/coder/contract.md). There were many rounds of pilots before coding went wide. Each round found something: a rule the coder misread, an output nobody downstream used, a field that let the coder describe its own work instead of recording it. [The changelog](files/coder/changelog.md) keeps the recent reasons; the older ones are in the project's notes.

The coder is also given a brief: an account of the community's ordinary week before the canvas, written by a different agent, so the coder can tell the room's own habits from what the event brought. That produced [the brief writer's contract](files/coder/contract-brief-writer.md), its builder [newbrief.py](files/coder/newbrief-py.md), its reader [read_brief.py](files/coder/read-brief-py.md), and [the brief's outputs](files/coder/brief-outputs.md).

Each coder is free to read and choose as it sees fit. Every coder of a given version runs the same contract on the same kind of material, and a new reading can be run whenever one is needed, so replications were run only where a question called for them: r/liverpoolfc, read several times under different versions and models, and r/dorset, read by seven independent coders (30 to 43 codes, 6 to 16 themes, every item cited by all seven). The evidence is small; [for reviewers](10-for-reviewers.md) gives it with its limits.

## Why tools were built

In contrast to the aggregator, the coder is meant to work in context. Most rooms hold fewer than 500 items, and the whole record fits in the window. The first idea was simple: hand the agent the material and ask for the codes.

It did not work out that way. Coders spent their turns writing code instead of coding. In one pilot, 18 of the 32 scratch scripts the coders left behind did nothing but write their own output files as JSONL. Others parsed and counted the corpus. And a coder's account of what it had read could not be checked against anything. So tools were built, to spare the agent the plumbing and to turn its self-reports into records:

- [read.py](files/coder/read-py.md) serves the corpus in order and logs every service, so "I read this thread" becomes something the log shows.
- [cite.py](files/coder/cite-py.md) turns a quote the agent believes is in the record into the record's exact words and offsets, or refuses. It closed the door on invented quotes.
- [emit.py](files/coder/emit-py.md) records every code, theme, disposition and pointer as a call, appended to a journal. The agent never writes JSONL, and the tool stamps the order in which codes were minted, so nobody has to take the coder's word for it.
- [close_run.py](files/coder/close-run-py.md) is the gate at the end: a set of checks that pass or fail, now twelve. One of them exists because a handover once claimed transcripts were saved when they were not.

[TOOLS-SPEC.md](files/coder/tools-spec.md) says what these tools do the same way for the brief writer, the coder and the aggregator. [newrun.py](files/coder/newrun-py.md) builds a run directory with all of them in place, and [AGENT.md](files/coder/agent-md.md) is the short page of operating notes each agent reads first.

## From small to large, and the serial fleet

Coding went from small rooms to large ones. The small rooms worked. The bigger ones became a problem, because they would not fit in one context. A room of several thousand items cannot be read whole by one agent, however it is cut. A few methods were tried. The one that stuck is an internal fleet, and it is serial.

The room is cut into slices of whole threads, in time order. The first fleet coder reads the first slice and codes it. It passes on a rolling record of what it learned (a timeline of facts and a lexicon of the room's own words) to the second coder, and the second passes it on to the third, until every thread is read and coded. Then everything goes to the case lead, who takes all the first-order codes and groups them into the room's second-order themes, and writes the account. A room of 500 items or fewer skips the fleet: the lead reads it whole.

This arrived with instrument v29 and brought its own files. [The case lead's contract](files/coder/contract-case-lead.md) and [the fleet coder's contract](files/coder/contract-fleet-coder.md) each say only what differs from the main contract. [tools/fleet.py](files/coder/fleet-py.md) plans the slices and dispatches, collects and consolidates them; each slice becomes [a fleet batch](files/coder/fleet-batch.md). The lead reads [the openings file](files/coder/render-openings.md) first, to see the shape of the week before any coder does. [tools/tree_builder.py](files/coder/tree-builder-py.md) hangs the codes on each thread's reply tree, the forest, and [tools/audit_fleet.py](files/coder/audit-fleet-py.md) is the gate before the lead's step 4. The lead's own memory of the fleet is a ledger on disk, since its conversation will be compacted on a long run ([how the case lead remembers](memory/coder-lead.md)).

## The yard, and the step from v30 to v32

With the fleet working, coding moved into a yard: one folder per census room, each holding everything needed to code it, and a scheduler that runs rooms smallest first. A room carries [ROOM.md](files/coder/room-md.md), its front page, and [STATE.json](files/coder/state-json.md), its memory. [room.py](files/coder/room-py.md) drives one room from outside, and [coding_queue.py](files/coder/coding-queue-py.md) launches them in order.

The case lead became the one agent worth saving whole. Its conversation and the room are checkpointed after every reply, so a lead can be resumed or forked later: [CHECKPOINTS.md](files/coder/checkpoints.md), [codex_lead.py](files/coder/codex-lead-py.md), [start_yard_lead.py](files/coder/start-yard-lead-py.md) with [the case-lead prompt](files/coder/case-lead-prompt.md), and, once a room is done, [the lead session archive](files/coder/lead-session-archive.md) packed by [lead_archive.py](files/coder/lead-archive-py.md). A verified room also keeps [its inputs](files/coder/materials-archive.md), [its whole run](files/coder/run-archive.md) and [its validation receipts](files/coder/validation.md).

The step from v30 to v32 had a plain cause. The OpenAI agent running the yard's repairs noticed that many failed runs failed the same few ways: a value entered wrong, a record left incomplete, so the run did not close cleanly and the defect showed only after the agent had gone. The rationale files count four such classes in 34 of the 60 rooms picked for repair. So the contract now keeps the lead around after the work is done, to run the end checks on its own files (`close_run.py --preflight`) and fix what they find, and only then close. v32 went one step further for the commonest defect and made `emit.py` refuse it at the moment of writing.

## The aggregator, four times

Once enough rooms were coded, the aggregator was tried, and its limits showed quickly. It has had four broad forms. Each failed in a way that shaped the next.

**The first got lost in counting.** It treated the work as tallies, and it read any counterexample as proof that it had made a mistake, so it dropped findings at the first room that did not fit. The fix is in [the contract](files/aggregator/contract-aggregator.md) today: a counterexample bounds a claim; it does not erase it, and the checks exist so the analyst can claim boldly and survive being checked.

**The second, v35, had freedom but did not understand the method well.** It ran in Claude Cowork. By the time it came to build the model, it had forgotten everything that had happened before. The v36 design note records that the v35 analyst still dropped findings at a counterexample, so the counting habit had not fully gone. The response was to give the method its own document, [METHOD.md](files/aggregator/method.md), with the literature arriving on [shelves](files/aggregator/shelves-folder.md) at the stages that read it.

**The third, the v37 run, worked well.** It ran to its last stage. But its dendrograms were weak, and its context compacted often, with no control over what survived. The weak trees are why the taxonomy is now read off the return to the rooms and the old tree is kept only as a comparison. The compaction is why the current version was built the way it was.

**The current one, v38, changes the idea.** It no longer tries to be a smart aggregator that holds the study in its head. It has a huge but limited working memory, and it is built around that limit. Knowledge is stored in writing. Only decisions are made in context. The new part is a kind of virtual memory: the agent pages what it needs in from disk, one page at a time, across the levels of the data structure, and writes back what it decides.

Most of the aggregator's files follow from that idea.

- **Stages, steps and legs.** The work is cut into [stage files](files/aggregator/stages-folder.md), handed over one at a time, so the analyst cannot read a later stage while answering an earlier one. Each stage is a series of steps listed in [steps.tsv](files/aggregator/tool-steps-tsv.md), and each step is one or more legs, a leg being one fresh launch. A long session costs far more per output token and compacts unseen; a short leg that starts from the files does neither. [done.sh](files/aggregator/tool-done-sh.md) is a leg's one exit.
- **What it holds.** The coders' work arrives sealed as [the package](files/aggregator/package-frame-md.md) and is joined by script into [the store](files/aggregator/store-readme.md), with [the forests](files/aggregator/trees-room-md.md) beside it, before the analyst arrives.
- **The verbs.** The analyst reads through [mem.py](files/aggregator/tool-mem-py.md), one page at a time, and quotes only through [cite.py](files/aggregator/tool-cite-py.md). Every call is logged in [the read logs](files/aggregator/out-read-logs.md).
- **Its memory.** [The head](files/aggregator/out-head-md.md), [the diary](files/aggregator/out-diary.md), [the snaps](files/aggregator/out-snap.md) and [the recall probe](files/aggregator/out-probe.md) are where the knowledge lives between legs. [The memory page](memory/aggregator.md) tells how they work together.
- **The fleets and the return.** Work too large or too independent for the analyst goes to readers under a written instrument ([FLEET.md](files/aggregator/fleet.md), [packets.py](files/aggregator/tool-packets-py.md)), and the return to every room goes out through [the handoff templates](files/aggregator/handoff-templates.md) and comes back through [ingest.py](files/aggregator/tool-ingest-py.md), typed by [the adaptation schema](files/aggregator/schema-adaptations.md).

[The v37 to v38 changelog](../aggregator/instrument/CHANGELOG-v37-to-v38.md) and [the v38 design note](../aggregator/handler/DESIGN-NOTE-v38.md) give the detail.

## The handlers

Both instruments run through a handler: an agent that launches the working agents, snaps them, checks their work, gives feedback when a check fails, and brings J only what is his to decide. These agents have grown more complex too, and more skilled at keeping the working agents well cared for.

On the coder side the handler is the yard's scheduler, governed by [its own contract](files/coder/contract-scheduler.md). On the aggregator side it is the run's handler, who works through the harness: [step.sh](files/aggregator/harness-step-sh.md) opens a leg, [launch.sh](files/aggregator/harness-launch-sh.md) starts the session, [close.sh](files/aggregator/harness-close-sh.md) closes it, [dispatch.sh](files/aggregator/harness-dispatch-sh.md) sends a fleet out, [interview.sh](files/aggregator/harness-interview-sh.md) opens a read-only fork to talk with the analyst, and [the guards](files/aggregator/harness-protocol-guard-py.md) hold the rules the analyst might forget. Many of the harness rules came from failures in the v37 run: a fence that denied the analyst its own folder, connectors the analyst inherited from the account, a compaction nobody saw. [The handlers page](6-the-handlers.md) tells that part of the story.
