# Talking with a leg, and continuing a run

*Kind of page: how-to: the commands, each explained piece by piece.*

Every stage page ends each closed leg with a command. This page says what that command does, piece by piece, what it opens on your machine, what it can and cannot touch, and how to check all of it before you run it. The second half says how the run's owner continues a run, and what a clone can and cannot resume. No leg of the run has closed yet, so the stage pages carry no commands until one does.

## The command, piece by piece

A stage page prints, for a leg such as `B1b-03`:

```bash
cd "$(git rev-parse --show-toplevel)/aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT" && claude --resume "$PWD/out/_transcripts/leg-B1.B1b-03-<id>.jsonl" --fork-session --permission-mode plan --model claude-opus-5-5 --effort xhigh --strict-mcp-config --disallowedTools Bash Write Edit MultiEdit NotebookEdit
```

| Piece | What it does |
|---|---|
| `git rev-parse --show-toplevel` | prints the root of your clone, so the command works wherever you cloned. Downloaded as a zip, with no git: replace `$(git rev-parse --show-toplevel)` with the folder you unzipped to. |
| `cd .../00_GIVE-THE-AGENT` | moves into the analyst's folder, the one it worked in, so the files it names by relative path (`out/_head.md`, `package/armenia/codes.jsonl`) resolve. |
| `claude` | starts Claude Code, installed and logged in on your account. |
| `--resume "<file>.jsonl"` | loads that transcript: the leg's whole conversation, every message, tool call and tool result, as the run recorded it. Claude Code accepts a transcript path here as well as a session id ([sessions](https://code.claude.com/docs/en/sessions)). |
| `--fork-session` | starts a new session from a copy of that conversation. The file in the repository is read, never written; your questions go into the new session only. |
| `--permission-mode plan` | plan mode: the analyst may read and propose, not edit. The flag overrides the `dontAsk` mode the analyst's folder sets for the run (v43; `auto` before) ([permission modes](https://code.claude.com/docs/en/permission-modes)). |
| `--model`, `--effort` | the model and effort the leg ran at, read from `CONTROL/arm.json` with the leg's own override applied, as the launch read them. Your account must have access to the model; if not, pass another and say so when you cite what it tells you. |
| `--strict-mcp-config` | loads no MCP servers, not even yours, as in the run's own launches. |
| `--disallowedTools Bash Write Edit MultiEdit NotebookEdit` | removes the tools that run commands or write. What is left is reading: `Read`, `Grep`, `Glob`. This is what makes the fork read-only on any machine; plan mode alone can be left from inside the session. |

## The transcript file

`out/_transcripts/leg-<LABEL>-<session id>.jsonl` is a plain text file, one JSON object per line: each user message, each assistant reply, each tool call and its result, with timestamps. [close.sh](files/aggregator/harness-close-sh.md) copies it there at every close, from the run's session store (`CONTROL/.cc/projects/run/`; the folder is kept out of git, and each checkpoint's `agent.tar.gz` holds that `projects/run/` and nothing else of it), after checking its session id is the one the leg was launched with. You can read it without Claude, in any text editor, or as a list:

```bash
python3 -c "import json,sys; [print(r.get('type'), str(r.get('message',{}).get('content',''))[:200]) for r in map(json.loads, open(sys.argv[1]))]" out/_transcripts/leg-<LABEL>-<id>.jsonl
```

What the fork remembers is exactly this file. It holds the Reddit text the analyst read, with real usernames; treat it as you treat the data (see [the terms](data-and-collection.md#terms-of-use)).

## What else loads when Claude Code starts in that folder

- **`CLAUDE.md`**, the analyst's standing rules ([page](files/aggregator/claude-md.md)). The fork reads them as the analyst did. They tell it to use the verbs (`mem.py`, `cite.py`); in the fork it cannot run them, and will say so. Ask it to open the files instead.
- **`.claude/settings.json`**, the analyst's fence ([page](files/aggregator/claude-settings-json.md)). [protocol_guard.py](files/aggregator/harness-protocol-guard-py.md) writes it at every launch from `CONTROL/settings.template.json`. Hooks and sandbox settings in it apply as soon as Claude Code starts ([settings](https://code.claude.com/docs/en/settings)). On your machine:
  - Deny rules naming the author's folders match nothing. Those that name no path still apply: no web fetch or search, no MCP, no Skill, and no reading of your own `~/.claude/`.
  - The `PreToolUse` hook runs `python3 /Users/.../pretool_guard.py`, a file you do not have; it fires only on the tools the command has already removed, so it has nothing to do. The `SessionStart` hook fires only after a compaction and fails harmlessly.
  - The sandbox, set as required, governs commands; the fork runs none.
  - The file names the author's folders: it tells you how the author's disk is laid out, and nothing else.
- **The files the fork reads** are those in your clone, which hold the run's latest state. A fork of an early leg may open files written after that leg closed. Its memory is of the leg; its reads are of today. Paths the transcript records are the author's (`/Users/...`); the fork should use relative ones, and you may need to tell it to.
- **Your own settings** (`~/.claude/settings.json`, your `CLAUDE.md`) load too, below the project's. The run's launches also turn off auto memory; for a fork as bare as the run was, put `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` before `claude`.
- **The trust prompt.** The first time Claude Code starts in a folder it asks whether you trust it. Read the two files above first; they are everything the folder adds.

| Your machine | What happens |
|---|---|
| macOS, Linux, WSL2 | as described |
| Windows, PowerShell or cmd | the `cd "$(...)"` line is bash; run it from WSL2 or Git Bash, or `cd` by hand and run the `claude ...` part |

## What it costs and what it changes

- **Cost.** Your first message sends the transcript as context. The stage page's `tokens in` is summed over every turn of the leg, so it is far larger than what the fork reloads; the fork's cost is closer to the length of the transcript file (a rough guide: 4 characters to a token). It runs on your account and your usage.
- **Your machine.** Claude Code writes its usual records: the fork's transcript under `~/.claude/projects/<your path, encoded>/`, the trust decision, your prompt history. It writes nothing in the clone.
- **The repository.** Unchanged. `git status` after the talk shows nothing new; if it does, `git checkout -- .` restores it.

## Checking before you run it

1. Open the transcript and read the last few lines: that is where the fork starts.
2. Open `00_GIVE-THE-AGENT/.claude/settings.json` and `CLAUDE.md`.
3. Run `claude --help` and check the flags above exist in your version.
4. Run the command. Ask first what the analyst was doing when the leg closed; the answer should match the last lines you read.

Good first questions, at any leg: what did you read in this leg, and what did you decide; which room surprised you, and why; what would you do differently. At an interview point, the analyst's brief (linked on the stage page) ends with the three questions it would most like to be asked.

## Interviews, which are the run owner's

[interview.sh](files/aggregator/harness-interview-sh.md) makes a fork for the run's owner, on the run's own login (`CLAUDE_CONFIG_DIR=CONTROL/.cc`), at an interview point. It is not read-only: it runs in a copy of the analyst's folder restored from the leg's checkpoint (`interview-workspaces/<LABEL>__<fork>/`), with the leg's sessions in a project of its own, so the analyst sees its files as they stood at the close, you may add material, and nothing reaches the live run. It records the fork in `CONTROL/interviews.tsv`, copies its transcript to `RUN/interviews/<LABEL>__<fork>.jsonl`, and runs `publish.sh`. A transcript is committed only if the owner decides so, interview by interview; one that is committed gets its own talk command on the stage page. The owner's reply to the analyst is a file, `out/interview/<brief>-reply.md`, which the next leg's startup message names. From the leg handler's chat, `?<leg> text` (or `legs.py interview`) opens the same kind of fork; its transcript stays in the run's Claude folder (`CONTROL/.cc/projects/iv-<fork>/`), on disk and not committed. Both kinds reach the analyst at stage E2a: `step.sh` copies every interview listed in `CONTROL/interviews.tsv` into its `handling/interviews/`.

## Continuing the run: how a leg starts and ends

The run owner's loop. Each step is one script with its own page.

1. **`step.sh <leg>`** ([page](files/aggregator/harness-step-sh.md)):
   - checks the leg id against `tools/steps.tsv`;
   - refuses if an API key or gateway is set in the shell (the analyst runs on the subscription);
   - delivers the stage's files from `DROPS/` on its first leg;
   - writes the startup message to `CONTROL/next_prompt.txt`;
   - records a new session id in `CONTROL/pending_launch.json`.
2. **`launch.sh`** ([page](files/aggregator/harness-launch-sh.md)) hands over to `protocol_guard.py launch`, under a lock so two launches cannot overlap. It:
   - rewrites `.claude/settings.json` for this run's paths;
   - starts `claude` in `00_GIVE-THE-AGENT/` with the run's own login, the session id, the leg's model and effort, no MCP servers, no auto memory, and the startup message;
   - records the exit in `CONTROL/last_launch_exit.json`.
3. **The analyst works**, and ends the leg with `tools/done.sh` ([page](files/aggregator/tool-done-sh.md)), which checks its own outputs and writes `out/_closes/<stage>-<leg>.closed`.
4. **`close.sh <leg>`** ([page](files/aggregator/harness-close-sh.md)):
   - runs the handler's check, takes the snap and runs the recall probe;
   - copies the transcript into `out/_transcripts/`;
   - builds the checkpoint in `CONTROL/snapshots/<LABEL>/`, marked `COMMITTED` last;
   - prints the next step;
   - calls [publish.sh](files/aggregator/harness-publish-sh.md), which regenerates this Manual, commits, tags interview points and finished stages, and pushes.

The [leg handler](../aggregator/handler/claude-adapter/LEGS.md) (`legs.py`) runs the same loop without a terminal per leg: `step.sh <leg> --prepare` in place of the interactive launch, one headless Claude turn per message (`claude -p`, stream-json, the leg's session forked or resumed as `step.sh` prepared it), then `close.sh`. Words the owner sends during a turn reach the analyst beside its next tool result, with a receipt, and are recorded with their delivery in `CONTROL/messages-to-legs.jsonl`.

A paused leg continues as `<leg>-p2`; `close.sh` prints the id. Every leg already continues the last close's conversation. `step.sh <leg> --from-cut <LABEL>` names that cut explicitly, and only the last close is accepted; an older state is talked to through an interview, in a copy of its own.

## What a clone can resume, and what it cannot

- **Talk with any closed leg or interview:** yes, with the command above.
- **Start a run of your own from the instrument:** yes; see [the Manual's front page](README.md#start-a-run-of-your-own). Build it outside the clone.
- **Continue this run from a cut, on your machine:** not ready.
  - `step.sh --from-cut` looks for the parent session in the run's live store (`CONTROL/.cc/projects/run/<id>.jsonl`), which git does not carry. You would put the transcript there first, from `out/_transcripts/` or the cut's `agent.tar.gz`, log in the run's Claude, and run `acceptance.sh`.
  - The analyst's files in the clone are the run's latest state, not the cut's. Restoring a checkpoint's folder was a v37 script, `restore_stage.sh`, [not ported to v38](../aggregator/instrument/tools/TOOLS-STATUS.md).
  - Nobody has tried this path. Treat it as a design, not a procedure.
