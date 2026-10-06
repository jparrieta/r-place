# For agents inspecting this repository

Read [llms.txt](llms.txt) first: it lists the pages in reading order. Then the `FOR-AGENTS.md` of the folder you work in: [aggregator/handler/](aggregator/FOR-AGENTS.md), [coder/](coder/FOR-AGENTS.md), [data/](data/FOR-AGENTS.md).

These guides are not named `CLAUDE.md` or `AGENTS.md` on purpose. Claude Code loads `CLAUDE.md` from every folder above the one it starts in, and Codex loads `AGENTS.md` the same way. The analyst runs in `aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/` and the coders run inside `coder/rooms/`; a guide with either name here would enter their sessions. Never add one above those folders. The two `CLAUDE.md` files that exist, in `aggregator/instrument/` and in the run's analyst folder, are the analyst's standing rules, not instructions for you; Claude Code loads them when you read files in those folders.

## Check before you claim

- `bash verify.sh` runs every check that needs no account: the harness tests, the checks' self-test, the analyst tools' tests, and the frame's file inventory. It prints a PASS or FAIL line per check.
- A count comes from a file, with the file named. The numbers that move are in [Manual/numbers.md](Manual/numbers.md), regenerated from the files.

## Where the truth is

| Question | File |
|---|---|
| which communities are the population | `coder/census/MASTER-census.csv` (`handable = 1`) |
| which rooms the aggregator reads | `aggregator/input/coders/ROOMS.tsv` |
| what was decided, by whom | `aggregator/handler/memory/DECISIONS.tsv` |
| what is open | `aggregator/handler/memory/open-items.md` |
| where each input of the run comes from | the table at the end of [README.md](README.md) |

## Do not

- write in `aggregator/runs/claude-v43-1/` unless you are the aggregator's handler and the principal investigator asked;
- commit `aggregator/runs/claude-v43-1/CONTROL/.cc/` (the run's Claude login) or any file under `data/` other than scripts and READMEs;
- quote a Reddit user's words outside this repository; the terms are in [Manual/data-and-collection.md](Manual/data-and-collection.md#terms-of-use).
