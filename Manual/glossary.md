# Glossary

*Kind of page: reference.*

Terms a newcomer meets here, in alphabetical order, defined as the sources define them.

**Aggregate dimension.** The top tier: what the fourth-order themes are about, named as a construct and declared borrowed, adapted or coined. The analyst builds as many as composition needs; none or one is reported as a failure state.

**Analysed set.** The frame less the rooms stage A1 drops. "N of M communities" says what M holds.

**Arm.** The models that serve a stage, declared in `CONTROL/arm.json`: the analyst's model and effort, and the readers' route and model. In v37 the "cheap arm" was the low-cost reader fleet.

**Branch A, branch B.** How a coder room is read. Branch A: the case lead reads the whole room itself (500 items or fewer in the window). Branch B: the lead cuts the room into slices and a serial fleet of coders reads them, one after another.

**Bridge.** In a forest, an uncoded turn kept because a coded reply hangs below it, so the distance between two coded turns stays visible (`tree_builder.py`).

**Brief.** Two senses. On the coder side, `brief.md` is a room's account of the seven days before the canvas opened, written by a brief writer. On the aggregator side, a brief is what the analyst writes at an interview point, under 800 words.

**Case.** One community read as one case. Its within-case account, written by the case lead, is `case.md`.

**Case lead.** The coder agent in charge of one room: it decides the branch, reads the room itself (branch A) or runs a fleet over it (branch B), and writes the case. The only coder agent with a saved conversation.

**Checkpoint.** A saved state that can be restored. Coder side: `codex_lead.py` commits one after each completed lead reply. Aggregator side: `close.sh` publishes one per leg under `CONTROL/snapshots/`, with `COMMITTED` written last.

**Code / first-order concept.** The first tier: a participant's words, coded, with the quote.

**Compaction.** When a long session's context is summarised to make room. The analyst cannot see it happen; the hook `after_compact.sh` has it re-read its head and stage file and reconcile them with the diary.

**Contract.** The written instrument an agent works under: `CONTRACT-aggregator.md` for the analyst, `CONTRACT.v32.md` and its role contracts for the coders, `CONTRACT-scheduler.md` for the yard's handler.

**Cut.** Two senses. On the aggregator side, a leg closed at a named checkpoint, snapped and resumable (`done.sh <stage> --cut <name>`, as in `done.sh B1 --cut interview`). `packets-out` closes the build leg of a fleet stage; `interview` closes an interview point. On the coder side, the window a room's record is cut to: the 97-hour cut.

**Dispatch.** Sending work to readers. Coder side: `fleet.py dispatch` builds the batch folder for one slice, and the yard's `codex_coder.py` runs the fleet coder in it. Aggregator side: `dispatch.sh` runs `fleet.py` over the analyst's packets, outside the analyst's session.

**Drop.** Three senses. A room stage A1 drops from the frame, with its reason (`dropped.jsonl`). An item a forest does not show, being neither coded nor above a code. And `DROPS/`, the handler's folder of files delivered to the analyst at each stage's first leg.

**During window.** The 73 hours the canvas was open, 2017-03-31 16:00 to 2017-04-03 17:00 UTC. The coders' window is 97 hours: the during window plus one day.

**Fleet.** Readers under a written instrument. The coder fleet reads a large room in slices, one coder per slice. The aggregator's reader fleets place themes, test the scheme or give verdicts, through the OpenRouter gateway.

**Forest.** A room's coded threads as reply trees, coded turns hung on them, gaps kept (`trees/<sub>.md`). A reply shows order, never cause.

**Fork.** A new, independent session started from a saved one. Coder side: `codex_lead.py fork`. Aggregator side: every leg forks the last close's session; an interview (`interview.sh` or `legs.py interview`) forks a closed leg in a copy of its folder; `step.sh --from-cut` opens a leg from a cut; `legs.py branch` makes a whole new run from one close.

**Fourth-order theme.** A named group of third-order themes, named as a construct and declared.

**Frame.** A dated, hashed copy of every room whose coding had finished when the copy was taken (`package/FRAME.md`). It held 696 rooms on 28 September 2026, 700 on 2 October and 705 on 4 October 2026 ([the numbers](numbers.md)). The frame is not the population: the census and the contract count the population as 706 rooms, and rooms coded after the copy are not in the frame.

**Handler.** The Claude session that runs the aggregator's harness, drives the legs through the leg handler and answers the analyst in files; on the coder side, the scheduler that runs the yard. See [the handlers](6-the-handlers.md).

**Head.** `_head.md`, the narrative of the argument, at most 3,000 words, read first at every leg and rewritten at every close.

**Interview point.** One of twelve steps, `A1c` to `E2b`, that end with a brief and a cut, so the principal investigator can talk to the analyst in an interview: a fork of the leg in a copy of its folder, from which nothing reaches the run.

**J.** Jose Arrieta, the principal investigator: the person who owns the study, answers the handlers' questions and makes the author's judgements.

**Kind.** What stage B1 calls a third-order theme while it is being found: a kind of second-order theme that recurs across rooms.

**Labeler.** At stage D2, one fresh GPT session in Codex per room, which reads the model and the room and proposes the adaptations the model would need to explain that room.

**Leg.** One launch of the analyst. Since v40 a leg continues the last close's conversation, forked from its checkpoint, in the same folder; only the run's first leg is fresh. A stage is one or more legs.

**Leg handler.** `legs.py`, in `aggregator/handler/claude-adapter/`: one process on the Mac that opens, runs and closes the analyst's legs headless through the harness, and the one chat window where the principal investigator talks to every leg. See [the handlers](6-the-handlers.md).

**Lexicon.** On the coder side, `out/lexicon.md`: the room's own words, each with the item of its first use. Stage A1 of the aggregator also writes one.

**Orchestrator.** Either of the two coordinating agents, Claude and OpenAI, that keep the instrument, the harness and the Codex runtime. `orchestrator/` holds their roles, rules, checks and scripts; their working record is kept outside the repository. Neither runs the study. See [the handlers](6-the-handlers.md#the-orchestrators).

**Package.** The coders' work, sealed: one folder per room with the same six files (`brief.md`, `case.md`, `codes.jsonl`, `themes.jsonl`, `threads.jsonl`, `pointers.jsonl`), plus the canvas data.

**Pause.** A clean stop: `pause.sh` writes `.pause`, and at its next safe stop the analyst logs where to pick up and closes with `done.sh <stage> --pause`.

**Pointer.** A coder's record of another venue a passage names (a subreddit, a Discord, a poll), made with `emit.pointer` and kept in `pointers.jsonl`.

**Probe.** The recall probe: five questions asked at every close in a fork of the leg, scored against the head, the diary and the read log.

**Return.** Stages D1 to D3: the model is returned to every room, each room's labeler proposes adaptations, readers give verdicts, and the analyst rules on each. The forms of organizing are read off what the rooms required.

**Room.** One community's folder: in the yard, `rooms/<sub>/` with its record, brief and run; in the aggregator, a subreddit in the package.

**Second-order theme.** The coders' within-case grouping of a room's concepts, gerund-led and bound to its case. The yard's files call its label field `second_order`. In Gioia's terms these are first-order concepts, consolidated within a case; see [for reviewers](10-for-reviewers.md).

**Shelf.** The literature, arriving with the stages that read it (`shelves/<stage>/`). A shelf that has arrived stays.

**Slice.** In branch B, a run of whole threads in time order, read by one fleet coder.

**Snap.** A hash of every file in `out/` under a name, written once by `snap.py`, so a reviewer can see what existed when.

**Stage and step (A1 to E2).** The aggregator's work in five sections: A reading, B coding, C model, D adaptation and forming, E formalizing. Each stage is a sequence of lettered steps; `tools/steps.tsv` lists them. A leg is named by its step, as in `B1b-03`. The v37 run used stages 01 to 18.

**Store.** The package joined by script before stage A1 (`package/store/`): codes, themes, items, threads, rooms, transitions, relations and neighbours.

**Third-order theme.** A cross-case kind of second-order theme, the analyst's first tier: two to five words plus a gloss, near the material, never a construct's name.

**Thread.** A Reddit post and its replies.

**Transition.** A coded turn that answers a coded turn, with the interval between them; the store keeps them in `transitions.jsonl`.

**Verb.** A subcommand of `mem.py`, the analyst's way to read the store and its own files one page at a time, every call logged. Loosely, the analyst's other tools too: `cite.py` to quote, `validate.py` to check.

**Verdict.** At stage D2, a reader's judgement of whether a room's proposed adaptation holds, given the model and nothing of the room's coder.

**Yard.** The run yard: one folder per community with everything a case lead and its fleet need, and the handler's tools in `_tools/`.
