# r/place: the Manual

This repository holds a study of how communities organized on Reddit's r/place in 2017: the data, the instrument that coded each community (the coder), the instrument that builds a model across all of them (the aggregator), and the run of the aggregator, instrument v43, whose record grows here stage by stage. The stage table below says how far it has got; until a stage is finished, this repository offers a method and its evidence trail, not findings. Read in this order:

1. [Introduction](1-introduction.md): what the project aims to do, and how this Manual is laid out. Reviewing the method? Start with 10.
2. [r/place and the data](2-rplace.md): the event, what we hold, what the data let us see, and a worked example (Armenia and the Dutch), down to one thread and its codes.
3. [How it was built](3-how-it-was-built.md): why each kind of file came to exist.
4. [The coder](4-the-coder.md) and 5. [the aggregator](5-the-aggregator.md): each instrument top down.
6. [The handlers](6-the-handlers.md): who runs the agents, their files, their memory, how sessions are saved.
7. [Tool usage](7-tool-usage.md): which tools the agents use, and which almost never.
8. [The v37 run](8-the-v37-run.md): the previous aggregator run.
9. [Talking with a leg, and continuing a run](9-resuming.md): what the talk command does, piece by piece, and what it can touch on your machine.
10. [For reviewers](10-for-reviewers.md): the tiers against Gioia's, which model did each step, the departures the method names, and how to check one room yourself.

Reference: [every kind of file](files/README.md), [how the aggregator remembers](memory/aggregator.md), [how the coder lead remembers](memory/coder-lead.md), the [glossary](glossary.md), [requirements and data](requirements-and-data.md) and [data and collection](data-and-collection.md).

The population and the evidence: [the census](census.md), from 1,473 artworks to the communities the study counts; [trace one claim](trace-a-claim.md), from a case account down to the Reddit comment; and [the numbers](numbers.md), every count that moves, regenerated from the files at every close.

Each page's first line names its kind: a tutorial to learn by doing, a how-to for a task, reference to look up, or explanation of why.

The run below is generated from its records at every close (`CONTROL/harness/gen_manual.py`); do not edit this page by hand.

## The run

| stage | name | status |
|---|---|---|
| [A1](stages/A1.md) | Reading: room notes | finished |
| [B1](stages/B1.md) | Coding: third-order scheme | finished |
| [B2](stages/B2.md) | Coding: pilot | finished |
| [B3](stages/B3.md) | Coding: fleet | not started |
| [B4](stages/B4.md) | Coding: adjudication and freeze | not started |
| [C1](stages/C1.md) | Model: structuring | not started |
| [C2](stages/C2.md) | Model: the loop | not started |
| [C3](stages/C3.md) | Model: literature | not started |
| [C4](stages/C4.md) | Model: the field | not started |
| [C5](stages/C5.md) | Model: account | not started |
| [D1](stages/D1.md) | Adaptation: return build | not started |
| [D2](stages/D2.md) | Adaptation: labelers and verdicts | not started |
| [D3](stages/D3.md) | Adaptation: adjudication | not started |
| [D4](stages/D4.md) | Forming: the tree | not started |
| [D5](stages/D5.md) | Forming: branch accounts | not started |
| [D6](stages/D6.md) | Forming: the retelling | not started |
| [E1](stages/E1.md) | Formalizing: audit | not started |
| [E2](stages/E2.md) | Formalizing: feedback | not started |

## The repository

Two layers are the instrument: [`aggregator/`](../aggregator/handler/HANDLER.md) holds everything to run the aggregator (the analyst's instrument in `instrument/`, the handler in `handler/` with the Claude harness in `claude/` and the Codex runtime in `codex/`, the shared input in `input/`, and one folder per run in `runs/`), and [`coder/`](../coder/README.md) everything to code communities (the case lead's instrument in `instrument/v32/`, the scheduler's contract, runbooks and tools in `handler/`, the census, and the example rooms). [`data/`](../data/README.md) holds how to get every piece of data, one folder per store, and [`archive/`](../archive) earlier versions of the instruments.

## What every file is, and why

- [Every kind of file](files/README.md): the aggregator's and the coder's, each with what it holds, who writes it and when, why it exists, and a link to a real one.
- How each side remembers: [the aggregator](memory/aggregator.md), [the coder lead](memory/coder-lead.md).
- [The handler's protocol and scripts](files/handler/README.md): what whoever runs the study must do around the analyst, and the tools to do it.
- The coding yard, ready to fill, with the case lead's instrument v32 and the fourteen coded rooms of the Armenia and Dutch example (twelve with their case lead's saved session), is in [`coder`](../coder/README.md).

## Talk with the analyst at any leg

Each closed leg on a stage page carries a command. Copy it into a terminal (macOS, Linux or WSL) inside a clone of this repository. It opens the leg's own conversation as a read-only fork: the analyst remembers everything it did up to that close and can open files to answer you; it cannot run commands or write. The fork is a new session on your own account and your own usage; nothing in the repository changes. No command appears until a leg has closed.

You need Claude Code installed and logged in (`claude` once). The fork does not need the run's harness or python. Downloaded as a zip rather than cloned: replace `$(git rev-parse --show-toplevel)` with the folder you unzipped to. [Talking with a leg](9-resuming.md) explains every part of the command, the files it opens, what it cannot do on your machine, and how to check it before you run it.

## Start a run of your own

The analyst's instrument is in [`aggregator/instrument`](../aggregator/instrument/CONTRACT-aggregator.md), the harness that runs it in [`aggregator/handler/claude`](../aggregator/handler/claude/READ-ME-FIRST.md), and the handler's protocol in [HANDLER.md](../aggregator/handler/HANDLER.md).

Build it outside your clone. Built inside, its first close would regenerate this Manual over the published one and commit and push to your clone's remote (`publish.sh` commits whatever repository the run sits in).

```bash
REPO="$(git rev-parse --show-toplevel)"; mkdir -p ~/runs/MYRUN
cp -R "$REPO/aggregator/input" ~/runs/input         # the coders' files and the canvas, joined at build
bash "$REPO/aggregator/handler/claude/build.sh" ~/runs/MYRUN --input-root ~/runs/input --input ~/runs/input/coders
cd ~/runs/MYRUN && CLAUDE_CONFIG_DIR="$PWD/CONTROL/.cc" claude   # log the run's own Claude in once, then /exit
bash CONTROL/harness/acceptance.sh          # must end ALL CLEAR
```

Then follow `STAGE CARDS/`, one card per stage, in order. What you need first (Python, packages, keys, what the readers cost and where their packets go) is on [requirements and data](requirements-and-data.md); what each script does when it runs is on [talking with a leg, and continuing a run](9-resuming.md).

## What is where

- [`aggregator/runs/claude-v43-1/READ-ME-FIRST.md`](../aggregator/runs/claude-v43-1/READ-ME-FIRST.md): the handler's guide to the run
- [`aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT`](../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT): the analyst's folder, with everything it wrote in `out/`
- [`aggregator/runs/claude-v43-1/CONTROL`](../aggregator/runs/claude-v43-1/CONTROL): the harness, the checkpoints and the records
- [`aggregator/handler`](../aggregator/handler/HANDLER.md): the handler's protocol, its scripts, the harness and the Codex runtime
- [`coder`](../coder/README.md): the coder layer: the case lead's instrument, the scheduler's handler, the census and the rooms
- [`archive`](../archive): every earlier version of the instruments, in one archive

