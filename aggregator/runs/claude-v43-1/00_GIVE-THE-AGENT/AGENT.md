# This run

You are the analyst. Your contract is `CONTRACT-aggregator.md`, in this folder, with
`METHOD.md` and `STANDING-INSTRUCTIONS.md`; `FLEET.md` comes with the fleet stages and
`SCHEMA-adaptations.md` from the return (D1). Read the contract once, whole, at stage A1, and by
section afterwards (`mem.py contract --section <n>`). Then the stage file you were told to read.

## What is here

    CONTRACT-aggregator.md      the questions, the tiers, the rules, the stages, the frame
    METHOD.md                   what the method says, and the shelves
    STANDING-INSTRUCTIONS.md    what you hold, the tools, your memory and the leg
    PLATFORM-claude.md  PLATFORM-codex.md   your platform's models, routes and legs; read yours once
    WRITING.md                  how to write, in your own words (the last line below)
    FLEET.md  SCHEMA-adaptations.md   when their stages come
    stages/STAGE-NN-*.md        the stages handed to you so far, in order
    package/  trees/            the evidence and the store. Read-only. The canvas is in
                                package/ from the start (rule 7)
    tools/                      cite.py, mem.py, validate.py, gen_views.py, packets.py,
                                counts.py, handoff.py, ingest.py, rebuild.py, done.sh;
                                HOW-TO-RUN.md says how
    out/                        yours; its tree is STANDING-INSTRUCTIONS §2. `_probe/`
                                and `_transcripts/` are the harness's

There is nothing outside this directory.

## State

Stages completed: the stage files in `stages/` and the corresponding files in `out/`. Every
ordinary leg continues the preceding completed checkpoint, with its conversation and
filesystem. Read the startup packet for orientation: the head, current stage file, last five
diary entries and `validate.py --open NN`. These notes do not replace the retained history.
Only delivered stages are available. Do not infer or begin a later stage.

## This session

One leg of the stage you were told to read, and then `done.sh`. Do not begin the next leg or
the next stage, and do not summarise what you would do in it. When the harness relaunches you
for a check leg it tells you so in one line.

How to write what you write, in your own words: `WRITING.md`, read once at stage A1 and again before C5, D5, D6 and E1.
