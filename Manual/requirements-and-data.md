# Requirements and data

*Kind of page: reference.*

What you need to use this repository, what data it holds, and what it leaves out.

## What you need

To read the Manual and check a room: a browser, and `zstd` to open a room's archives. To talk with a leg: Claude Code. To run the instruments, the list below.

- **bash on macOS, Linux or WSL2.** The harness is written for macOS bash 3.2 ([lib.sh](../aggregator/handler/claude/lib.sh)). `build.sh` and `acceptance.sh` call `shasum`, which macOS has; on Linux, install it (it ships with Perl) or alias it.
- **Python 3.11 with numpy, scipy and pandas.** That is what the repository's test workflow pins ([instrument-tests.yml](../.github/workflows/instrument-tests.yml)), and `acceptance.sh` refuses a run without the three packages, which stage D4's tree comparison and [build_neighbours.py](../aggregator/instrument/tools/build_neighbours.py) use. The other tools use the standard library. A saved case lead refuses to resume if the Python version or path differs from the one recorded in its store.
- **Claude Code, logged in.** The analyst runs in the Claude Code CLI with its own config folder. Before stage A1, run `CLAUDE_CONFIG_DIR="$PWD/CONTROL/.cc" claude` once in the run folder, log in, quit, then run [acceptance.sh](files/aggregator/harness-acceptance-sh.md) until it ends with ALL CLEAR ([the harness read-me](files/aggregator/harness-read-me-first.md)). The analyst's settings require Claude Code's sandbox, which macOS has built in and Linux needs `bubblewrap` for; native Windows has none.
- **An OpenRouter key** for the reader fleets. [fleet.py](files/aggregator/tool-fleet-py.md) reads it from the macOS Keychain (service `openrouter`) or from `$OPENROUTER_KEY`, never from a file in the run. `dispatch.sh` is run in your own Terminal for that reason. The readers' model, `@preset/cheap`, is a preset in the author's OpenRouter account, not a fixed model: define your own and record what it resolves to.
- **Codex**, for the coder side's sessions and the labelers at D2. [codex_lead.py](files/coder/codex-lead-py.md) runs `codex app-server` and needs a Codex login at `~/.codex/auth.json` or `--auth-source`. To resume a saved lead it also needs the same Codex build, the same Python and the original store path; see [the case lead's memory](memory/coder-lead.md).
- **zstd**, to open the coder archives (`run.tar.zst`, `materials.tar.zst`, the lead session archives). Lead archives over 95 MB are split into parts; join them with `cat` first.
- **git**, if you want [publish.sh](files/aggregator/harness-publish-sh.md) to commit each close. Build a run outside your clone; see [the front page](README.md#start-a-run-of-your-own).

## Where the text goes when you run it

- The analyst's legs go to Anthropic through Claude Code, on the account logged in to the run's config folder.
- The reader fleets' packets, each holding Reddit text, go to OpenRouter and on to whichever providers the preset routes to.
- The coders, the case leads and the D2 labelers go to OpenAI through Codex.

## Cost and time

No figures for a whole run are recorded here yet. Each closed leg's stage page gives its tokens in and out; the stage table in [the contract](../aggregator/instrument/CONTRACT-aggregator.md), section 4, gives each stage's model and effort, and [FLEET.md](files/aggregator/fleet.md) the readers per packet.

## What data is here

- The coding yard as it stands before a run, in `coder/`: the scheduler's contract and runbooks, its tools, the case lead's instrument v32, the fourteen rooms of the Armenia and Dutch example (twelve coded in the yard; Goodboye and norway coded earlier, their yard rooms not run) with their archives, and twelve of their case leads' saved sessions (about 1.2 GB, split into parts where over 95 MB). No queue state, logs or progress reports.
- The aggregator, in `aggregator/handler/`: the handler's protocol and scripts, the harness, the analyst's instrument (v43) in `aggregator/instrument/`, the design note, and the run in `aggregator/runs/claude-v43-1/`, built and waiting for stage A1, with its input in `aggregator/input/` (the coders' files and the canvas).
- The run folder's package: the coders' documents for each room (`brief.md`, `case.md`, `codes.jsonl`, `themes.jsonl`, `threads.jsonl`, `pointers.jsonl`), the joined store, the forests, and the canvas files ([the aggregator's files](files/aggregator/README.md)).
- Earlier instrument versions, one archive in [`archive/`](../archive/). The code that collects and builds the data is in `data/`, with each store's folder; see [data and collection](data-and-collection.md).

## What is not here

- **The data stores** (the pixel record, the atlas, the placer accounts, the venues, raw24, the pixels per artwork and per hour): `data/` holds the scripts that download or build each one in place, described in [data and collection](data-and-collection.md). The census that picks the rooms is here, in `coder/census/` ([the census](census.md)). Rooms were built from raw24 with [`build_room.py`](../coder/handler/tools/build_room.py), which is here.
- **The rest of the coding yard**: the other rooms' runs, the saved case lead sessions (44 GB), the queues and the logs. The coded result of every room is here, as the aggregator's input.
- **Earlier aggregator runs**, v37 among them: one run per repository, and this one carries v38's; see [the v37 run](8-the-v37-run.md).
- **The handlers' memory in the Claude project** on claude.ai, its documents and memory; see [the handlers](6-the-handlers.md).

## A note on the data

The repository holds Reddit users' public words under their real names. The coder contract is plain about it: "Authors are real accounts, nothing is pseudonymised, and this is public data." Item bodies are "byte-identical to the collected record. Real usernames and ids." Removed and deleted content stays as the record shows it and is never reconstructed.

The canvas data can be linked back to usernames through a hash. The study's own join hashes each username as `base64(sha1(username))`; anyone holding a list of usernames can compute the same hash and match placements to accounts.

How the text was collected, and on what terms it is shared: [data and collection](data-and-collection.md). Coders were told to "flag, never fetch": nothing was retrieved during coding.

The terms of use and the licences are on [data and collection](data-and-collection.md). This page gives no legal advice.
