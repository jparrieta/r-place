# `.claude/settings.json`

The permissions, hooks and sandbox each analyst leg runs under.

## What it holds

Rendered from `settings.template.json`: default mode auto; reads of `CONTROL/`, `DROPS/` and `~/.claude/` denied, as are web fetch and search, MCP tools, messaging, scheduling and Skill; Write and Edit denied in `tools/`, `stages/`, `package/`, `trees/` and `shelves/`. Hooks: SessionStart with matcher `compact` runs `after_compact.sh`; PreToolUse on Bash, Write, Edit, MultiEdit, NotebookEdit, Read, Grep and Glob runs `pretool_guard.py`; PostToolUse on Write, Edit and MultiEdit runs it with `--post`. Sandbox on, no network domains, reads of `CONTROL`, `DROPS`, `STAGE CARDS` and `READ-ME-FIRST.md` denied. `cleanupPeriodDays` 36500. `protocol_guard.py` adds denies for the folders beside the run, `INPUT/`, any `.git` around it and some home folders, and, before E1, for `out/_probe` and `out/_transcripts`.

## Who writes it, and when

`protocol_guard.py settings`, run by `step.sh` and again at launch, writes it into `00_GIVE-THE-AGENT/.claude/` for each leg's stage.

## Why it exists

`pretool_guard.py` calls its own string checks "a tripwire, never a wall: the sandbox's denyWrite is the wall". `protocol_guard.py`'s v38 note says the E1 wall is held by the permission rules and the sandbox, "not only by the stage file".

## Where

[.claude/settings.json](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/.claude/settings.json); template [harness/settings.template.json](../../../aggregator/handler/claude/settings.template.json).

Checked against: harness/settings.template.json, harness/protocol_guard.py, harness/pretool_guard.py, harness/step.sh.

## In a clone

The file in the repository carries the author's paths, and Claude Code loads it when anyone opens a leg with the talk command. The command does not rely on it: it removes the tools that run commands or write (`--disallowedTools`), so the hooks have nothing to guard, and the deny rules that name the author's folders match nothing. [Talking with a leg](../../9-resuming.md) explains the whole command.
