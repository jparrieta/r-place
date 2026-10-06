# The aggregator's files

One page per file the aggregator's run holds or uses: what the file holds, who writes it and when, why the design has it, and a link to the real file. Per-room files are described once, with r/armenia as the example. The levels below follow [the aggregator page](../../5-the-aggregator.md), from what governs the analyst down to the harness that runs it; [how it was built](../../3-how-it-was-built.md) tells why each level came to exist.

## 1. What governs

The analyst is given a few documents that hold at every stage, and one stage file at a time. Several documents instead of one, because each kind of rule changes at a different pace: the brief rarely, the stage files often.

### The documents that hold at every stage

| file | what it is |
|---|---|
| [`CONTRACT-aggregator.md`](contract-aggregator.md) | The brief: what is true at every stage of the run. |
| [`STANDING-INSTRUCTIONS.md`](standing-instructions.md) | What the analyst holds, the tools, its memory, and the shape of a leg. |
| [`METHOD.md`](method.md) | What the method says, and which shelf of literature arrives when. |
| [`AGENT.md`](agent-md.md) | The analyst's first page: who it is, what the folder holds, and what one session may do. |
| [`CLAUDE.md`](claude-md.md) | The rules Claude Code loads into every analyst session, binding on every turn. |

### Stages, steps and legs

The run is cut into stages so the analyst cannot read a later stage while answering an earlier one, and into legs so no session runs long enough to compact unseen.

| file | what it is |
|---|---|
| [`stages/`](stages-folder.md) | The stage files, handed to the analyst one stage at a time. |
| [`tools/steps.tsv`](tool-steps-tsv.md) | Every stage and step of the run, one per line. |
| [`tools/steps.py`](tool-steps-py.md) | Parses stage and leg ids against `steps.tsv`. |
| [`shelves/`](shelves-folder.md) | The literature, arriving with the stages that read it. |

### Documents for particular stages

| file | what it is |
|---|---|
| [`PRIOR-template.md`](prior-template.md) | The template for `out/prior.md`, the analyst's expectations written before it can see results. |
| [`FLEET.md`](fleet.md) | The fan-out to readers, the figures, and the return. |
| [`SCHEMA-adaptations.md`](schema-adaptations.md) | The types of the return: elements, operations, the ledger line, adjudication. |
| [`handoff/` (RETURN-D.md, TASK-template.md, HANDLER.md)](handoff-templates.md) | The templates stage D1 turns into the labelers' folder. |

## 2. What it holds at the start

Everything here is built by script before stage A1, so the analyst starts by reading and never assembles its own material.

### The coders' package

The coders' sealed work, one folder per room, kept as the coders wrote it.

| file | what it is |
|---|---|
| [`package/<room>/brief.md`](room-brief-md.md) | The coder's account of the room's pre-event week. |
| [`package/<room>/case.md`](room-case-md.md) | The coder's within-case account of the room's week. |
| [`package/<room>/codes.jsonl`](room-codes-jsonl.md) | The coder's first-order concepts for one room, as written. |
| [`package/<room>/themes.jsonl`](room-themes-jsonl.md) | The coder's second-order themes for one room. |
| [`package/<room>/threads.jsonl`](room-threads-jsonl.md) | The coder's disposition of every thread it looked at. |
| [`package/<room>/pointers.jsonl`](room-pointers-jsonl.md) | Every mention of another place that the coder recorded in the room. |
| [`package/FRAME.md`](package-frame-md.md) | The frame: which rooms the run holds, dated and hashed. |

### The joined store

The same material joined across rooms in `package/store/`, so a question across seven hundred rooms is one query and not seven hundred reads.

| file | what it is |
|---|---|
| [`package/store/README-store.md`](store-readme.md) | The store's dictionary: what each file is, and what none of them is. |
| [`package/store/_README-neighbours.md`](store-readme-neighbours.md) | The neighbours file's own dictionary entry, with its counts. |
| [`package/store/_README-relations.md`](store-readme-relations.md) | The mention graph's dictionary entry, with its counts. |
| [`package/store/_README-transitions.md`](store-readme-transitions.md) | The transitions ledger's dictionary entry, with its counts. |
| [`package/store/_build.json`](store-build-json.md) | The build record: what went into the store and what came out. |
| [`package/store/_retracted.jsonl`](store-retracted.md) | Every concept its coder withdrew, listed and kept out of the store. |
| [`package/store/_unjoined.jsonl`](store-unjoined.md) | Concepts whose item the forest does not hold. |
| [`package/store/codes.jsonl`](store-codes.md) | Every first-order concept of every room, joined. |
| [`package/store/themes.jsonl`](store-themes.md) | Every second-order theme of every room, with its concepts. |
| [`package/store/items.jsonl`](store-items.md) | Every item of every coded thread, without its text. |
| [`package/store/threads.jsonl`](store-threads.md) | Every coded thread, its shape and the coder's disposition in one line. |
| [`package/store/rooms.jsonl`](store-rooms.md) | One line per room of the frame: the census. |
| [`package/store/pointers.jsonl`](store-pointers.md) | Every pointer every coder wrote, in one file. |
| [`package/store/relations.jsonl`](store-relations.md) | The mention graph: every room another room's coder recorded. |
| [`package/store/transitions.jsonl`](store-transitions.md) | The transitions ledger: every coded turn that answers a coded turn. |
| [`tools/build_store.py` (build script)](tool-build-store-py.md) | Stage 00: the joined store from the coders' documents. |
| [`tools/relations.py`](tool-relations-py.md) | Stage 00's builder of the mention graph. |
| [`tools/transitions.py`](tool-transitions-py.md) | Stage 00's builder of the transitions ledger. |

### The forests

Each room's coded threads as reply trees, so a claim about who answered whom can be shown on the page.

| file | what it is |
|---|---|
| [`trees/<room>.md`](trees-room-md.md) | The rendered forest of one room: its coded threads as reply trees. |
| [`package/forest.jsonl`](package-forest-jsonl.md) | Every coded thread of every room as a reply tree, in one file. |
| [`package/tree_index.json`](package-tree-index-json.md) | Coordinate to item for every room, with the forest's header counts. |

### The canvas and the neighbours

What each room did on the canvas and whom it touched, kept beside the text and never mixed into it.

| file | what it is |
|---|---|
| [`package/case_facts_outcome.jsonl`](package-case-facts-outcome.md) | The canvas outcome per room: the six canvas fields. |
| [`package/pixels.csv`](package-pixels-csv.md) | Placements in each room's region, hour by hour. |
| [`package/DATA-manifest-canvas.md`](package-data-manifest-canvas.md) | The manifest of the canvas files, with the caveat the tools print. |
| [`package/canvas/artworks.jsonl`](package-canvas-artworks.md) | Every atlas artwork, with its pixels, placers and placements by hour. |
| [`package/store/neighbours.jsonl`](store-neighbours.md) | Every pair of rooms that touch on the canvas or name each other. |
| [`tools/build_neighbours.py` (build script)](tool-build-neighbours-py.md) | Stage 00: who neighbours whom, on the canvas and in the coders' record. |

## 3. The verbs

The analyst reads and writes through tools, and every call is logged, so what it says it read can be checked.

### Reading, quoting and recording

| file | what it is |
|---|---|
| [`tools/mem.py`](tool-mem-py.md) | The store and the analyst's own files, one page at a time, and the only writer to the diary. |
| [`tools/cite.py`](tool-cite-py.md) | The only way a quote enters an output. Every call is logged. |
| [`tools/counts.py`](tool-counts-py.md) | The denominators, from the canonical files. |
| [`tools/gen_views.py`](tool-gen-views-py.md) | Regenerates `out/_views/` and `out/_wiki/` from the canonical files. |
| [`tools/saturation.py`](tool-saturation-py.md) | The stopping rule: A1's random order, when B1 may stop reading, and the report the PI decides on. |
| [`tools/snap.py`](tool-snap-py.md) | The record of what existed when: a hash of every file in `out/` under a name. |
| [`HOW-TO-RUN.md`](how-to-run.md) | The command reference for the analyst's tools. |
| [`tools/NEW-VERBS.md`](tool-new-verbs-md.md) | The verbs and options added or changed in the v38 tools pass. |
| [`tools/TOOLS_VERSION`](tool-tools-version.md) | One line naming the version of the tools. |

### Opening and closing a leg

| file | what it is |
|---|---|
| [`tools/validate.py`](tool-validate-py.md) | The close-check of every leg and the open-check of every launch. |
| [`tools/vlib.py`](tool-vlib-py.md) | The shared library of the close-checks. |
| [`tools/checks/`](tool-checks.md) | One close-check per stage, and the self-test that proves each one fires. |
| [`tools/links.py`](tool-links-py.md) | Checks that every id named in the head and the questions exists. |
| [`tools/probe.py`](tool-probe-py.md) | The recall probe: five questions at every close, and their score. |
| [`tools/done.sh`](tool-done-sh.md) | The leg's one exit. |

### The fleets and the return

| file | what it is |
|---|---|
| [`tools/packets.py`](tool-packets-py.md) | What a fleet reader is served, assembled by script. |
| [`tools/handoff.py`](tool-handoff-py.md) | Stage D1's builder of the labelers' folder and the verdict packets. |
| [`tools/ingest.py`](tool-ingest-py.md) | Validates the labelers' returns, compiles the ledger, the verdicts, the room copies and the D2 counts, and re-lifts the ledger after D3. |
| [`tools/dreturn.py`](tool-dreturn-py.md) | The one rule set for stage D's returns, shared by ingest, the D2 check and the verdict schema. |
| [`tools/rebuild.py`](tool-rebuild-py.md) | A room's model rebuilt from the global model plus its accepted adaptations. |
| [`tools/distance.py`](tool-distance-py.md) | The stage D4 distance between rooms, from the adaptation ledger; the per-room delta, the dendrogram and the NEXUS file for SplitsTree. |
| [`tools/projections.py`](tool-projections-py.md) | Stage D4's projections: the verdicts and the canvas per branch and per cluster, against a permutation null. |

## 4. Its memory in out/

The analyst holds nothing between legs except what is on disk. Knowledge is stored in writing; the analyst pages in what a decision needs. [How the aggregator remembers](../../memory/aggregator.md) tells how these files work together.

| file | what it is |
|---|---|
| [`out/`](out-folder.md) | The analyst's working folder: the only place it writes, and its memory on disk. |
| [`out/_head.md`](out-head-md.md) | The head: the narrative of the argument, read first at every leg. |
| [`out/diary/`](out-diary.md) | The running log of the run, written as the analyst works. |
| [`out/rooms/` (room notes)](out-rooms-notes.md) | One note per room: the analyst's prior, dated. |
| [`out/_mem_reads-NN.jsonl` and out/_cite_reads-NN.jsonl](out-read-logs.md) | The read logs: one line for every call to `mem.py` and `cite.py`. |
| [`out/_views/`](out-views.md) | Generated tables over the analyst's files, rebuilt at every close. |
| [`out/_wiki/`](out-wiki.md) | Generated pages, one per room and one per model element. |
| [`out/_snap/`](out-snap.md) | Hashes of `out/` under a name: what existed when. |
| [`out/_probe/`](out-probe.md) | The recall probe's questions, answers and scores, one set per leg. |
| [`out/_transcripts/`](out-transcripts.md) | A copy of every leg's session transcript, filed at its close. |

## 5. The harness around it

The analyst does not start, stop or check itself. The handler runs it through these scripts, which also hold the rules an agent might forget.

### Laying out and running a leg

| file | what it is |
|---|---|
| [`READ-ME-FIRST.md` (the run's)](harness-read-me-first.md) | The person running the study's first page: three parties and the lines to type. |
| [`harness/build.sh`](harness-build-sh.md) | Lays out a run from the instrument and the coders' documents, once. |
| [`harness/acceptance.sh`](harness-acceptance-sh.md) | The native-CLI acceptance test, run once before stage A1. |
| [`harness/step.sh`](harness-step-sh.md) | Opens one leg: delivers the stage, writes the first message, launches the analyst continuing the last close's conversation. |
| [`harness/launch.sh`](harness-launch-sh.md) | Starts the analyst's Claude session for a prepared leg. |
| [`.claude/settings.json`](claude-settings-json.md) | The permissions, hooks and sandbox each analyst leg runs under. |
| [`harness/close.sh`](harness-close-sh.md) | Closes a leg after the analyst has run `done.sh` and quit. |
| [`harness/pause.sh`](harness-pause-sh.md) | Asks the analyst to stop at its next safe stop. |
| [`harness/interview.sh`](harness-interview-sh.md) | Talks with the analyst at an interview point, in a read-only fork. |

### Sending work to fleets

| file | what it is |
|---|---|
| [`harness/dispatch.sh`](harness-dispatch-sh.md) | Sends a fleet stage's packets to readers, outside the analyst's session. |
| [`tools/fleet.py` (the handler's)](tool-fleet-py.md) | The dispatch leg of a fleet stage, run outside the analyst's session. |
| [`arm.json`](harness-arm-json.md) | Which model serves each stage, and which readers each fleet uses. |

### Guards and hooks

| file | what it is |
|---|---|
| [`harness/protocol_guard.py`](harness-protocol-guard-py.md) | The handler-side guards: settings, launch, probe, close and checkpoint. |
| [`harness/pretool_guard.py`](harness-pretool-guard-py.md) | The analyst's PreToolUse hook: three standing rules enforced before a tool runs. |
| [`harness/after_compact.sh`](harness-after-compact-sh.md) | The hook that runs after a compaction of the analyst's context. |

### Publishing

| file | what it is |
|---|---|
| [`harness/publish.sh`](harness-publish-sh.md) | Regenerates the Manual and commits the run to git. |
| [`harness/gen_manual.py`](harness-gen-manual-py.md) | Writes the run's Manual, a set of Markdown pages GitHub renders. |
| [`harness/stage_cards.py`](harness-stage-cards-py.md) | Writes `STAGE CARDS/`, one card per stage for the person running it. |

### Also in the harness and its records

| file | what it is |
|---|---|
| [`harness/lib.sh`](../../../aggregator/handler/claude/lib.sh) | Shared functions, sourced by `step.sh`, `close.sh`, `dispatch.sh` and `build.sh`, never run: where the run is, the leg id's parts, the session of a label. |
| `CONTROL/sessions.json` | The session id of every leg, recorded when the leg is prepared; `build.sh` refuses a run that names one. |
| `CONTROL/snapshots/<label>/checkpoint.json`, `cost.json` | A checkpoint's ancestry and validation, and the leg's token counts, summed over every turn. |
| `CONTROL/interviews.tsv` | One line per interview fork: when, the leg, the session forked, the fork's id. |
