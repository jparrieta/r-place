# Read me first: running the aggregator

Target length: under 1,250 words. Instrument v43, Claude platform, as of 6 October 2026.

This folder is one run of the aggregator. Three parties: **the analyst**, a Claude session that lives in `00_GIVE-THE-AGENT/` and sees nothing else; **the handler**, a Claude session of its own (Claude Code on your Mac, or Cowork), which builds the run, checks each close and answers in files (`aggregator/handler/HANDLER.md`); **you**, who own the study and decide.

## The run's shape

Five sections: **A** reading, **B** coding, **C** model, **D** adaptation and forming, **E** formalizing. Each holds stages (A1, B1 ... E2), and each stage a sequence of lettered steps. A leg is named by its step: `B1c` for a step taken once, `B1b-03` for the third leg of a step that repeats, `B2a-r1` for a pilot round, `B1c-p2` for a leg resumed after a pause. `00_GIVE-THE-AGENT/tools/steps.tsv` lists every step; each stage's card in `STAGE CARDS/` lists its legs and dispatches in order. A leg id that does not name a step of its stage is refused, with the stage's steps listed.

## How a leg works

- **Every leg continues the last one.** A leg forks the conversation of the last committed close, in the same folder; the head file and diary orient it and do not replace it. The run's first leg is fresh; `step.sh LEG --fresh` opens a fresh one on purpose and logs it as a departure.
- **Nothing asks.** A leg runs in `dontAsk`: what the settings allow runs, anything else is refused and the analyst sees the refusal. No permission question or trust dialog reaches you; a refusal the analyst needed is recorded, and the orchestrator widens the rule with your approval.
- **The analyst can ask you.** `mem.py ask` puts a question in `out/asks.jsonl`, with what the analyst does meanwhile; `close.sh` lists every open one. Your answer is `out/_answers/<id>.md` (ids like `QA1-001`), which the analyst never writes; the first message of the next leg opened after it names it; `legs.py answer` writes it and gives it to a running leg beside its next tool result, or to an open leg with its next turn.
- **Helpers** read, summarise or test, on the analyst's own model, logged; never a fleet's work, never evidence.
- **Readers never run inside the analyst.** Where a stage uses readers (B2, B3, B4, C2, C5, D2, D3, E1), the analyst builds the packets and closes at `packets-out`; you run `dispatch.sh`; the check leg reads what came back.
- **The close.** `close.sh` asks the analyst five recall questions in a last turn and scores them, runs the trusted check, audits that the model that served is the one `CONTROL/arm.json` names (for a forked leg, counting its own messages only), takes the snap and the checkpoint in `CONTROL/snapshots/<label>/`, and runs `publish.sh`. A paused or forced close records the audit but is not stopped by it, and does not advance the run (the Manual, a commit, tags, a push when a remote is set).

## Once, before stage A1

```
bash CONTROL/harness/acceptance.sh
bash CONTROL/harness/acceptance_v41.sh
```

Both need the analyst's own login: the first time, run `CLAUDE_CONFIG_DIR="$PWD/CONTROL/.cc" claude` once in this folder, log in, and quit. Both must end ALL CLEAR. Then the repository's first commit and push, so that A1a's close commits only A1a. The leg handler has its own live check, outside this run, from the repository folder: `python3 aggregator/handler/claude-adapter/probe_lifecycle.py --model claude-sonnet-5-5 --effort low`.

## Every leg

**Through the leg handler** (`aggregator/handler/claude-adapter/LEGS.md`). From the repository folder, once, in a Terminal you leave open:

```
python3 aggregator/handler/claude-adapter/legs.py serve
```

In a second Terminal, the window where you talk to every agent of the run:

```
python3 aggregator/handler/claude-adapter/legs.py chat claude-v43-1
```

The handler (or you) then runs `legs.py run claude-v43-1 A1`, `open`, `close`, `status` and `wait`. Each turn is one headless Claude process in this folder; `step.sh` prepares the leg and `close.sh` closes it, as by hand. A list stops at a refusal, a failed or interrupted turn, a pause, a dispatch, an interview point or a forced close, and says why.

**By hand.**

```
bash CONTROL/harness/step.sh B1b-03
bash CONTROL/harness/close.sh B1b-03
```

The first opens Claude with the leg's first message sent; the analyst works, ends with `done.sh` and stops; you type `/exit`, then the second line. A leg opened by hand may be closed with `legs.py close`. While `legs.py` drives the run, do not run `step.sh` or `close.sh` on it by hand: `close.sh` and `dispatch.sh` name the next leg in `legs.py`'s form first.

## A dispatch

```
bash CONTROL/harness/dispatch.sh NN
```

In your own Terminal, where your Keychain holds the OpenRouter key. Stage B2 takes `--round k`, and its check leg is `B2b-rk`. Stage D2 also prints what to give the adaptation handler in Codex. `dispatch.sh` prints the check leg to open next.

## Pausing

`bash CONTROL/harness/pause.sh`, or `legs.py pause claude-v43-1`: the analyst stops at its next safe stop, logs where to pick up, and closes with `done.sh NN --pause`. The close prints "paused" and the leg to resume with, the same id with `-p2`. To stop at once: `legs.py stop claude-v43-1 --now`, then `legs.py close claude-v43-1 <leg> --force` (by hand: quit Claude, then `close.sh <leg> --force`); the diary keeps what was logged.

## Interviews

An interview is you opening a closed leg to talk to it. Twelve steps end at an interview point, from `A1c` (the reading done) to `E2b` (the feedback); the stage cards mark them. Each interview is a fork of the leg in a copy of the analyst's folder as it stood at the close (`interview-workspaces/`): talk freely, add material there if you like; nothing enters the run. Two ways:

```
bash CONTROL/harness/interview.sh
bash CONTROL/harness/interview.sh --list
bash CONTROL/harness/interview.sh C5d
```

The last interview point, the list, or one by its leg; the transcript is copied to `interviews/`. Or, in the chat, `?C5d text` (and `?C5d+ text` for a new one), or `legs.py interview claude-v43-1 C5d TEXT`: later words continue that interview, whose transcript stays in the run's Claude folder (`CONTROL/.cc/projects/iv-<fork>/`, on disk, not committed) until E2a. Both record the fork in `CONTROL/interviews.tsv`, and at E2a every listed interview reaches the analyst's `handling/interviews/`. A transcript is committed only if you decide so, interview by interview; the handler gives you the commands. The analyst's brief is in `00_GIVE-THE-AGENT/out/interview/`, named by leg, stage, step and minute. To answer the analyst after an interview, write the reply file `interview.sh` names, or say it to the next leg.

## Stage E2

Before E2, put the study's proposal as it stands then in `DROPS/E2/handling/proposal.md`. The design note is there already; replace it if the design changed.

## Talking to the analyst

Only you speak to the analyst, in your own words: through `legs.py` (the chat or `say`), which delivers a line beside the analyst's next tool result, or as a new turn, and records it with its delivery in `CONTROL/messages-to-legs.jsonl`, committed at every close; an answer to a question is the file `out/_answers/<id>.md`. The handler never speaks to the analyst in its own words: it passes yours, verbatim, only when you ask it to. If the analyst asks something, it writes it down, and the answer reaches it in a file or in your words. In a leg opened by hand, say nothing beyond what the harness sends. Interviews are forks, never legs: talk freely.
