# `harness/pretool_guard.py`

The analyst's PreToolUse and PostToolUse hook: standing rules enforced as a tool runs.

## What it holds

It reads the tool call as JSON and blocks it (exit 2, the reason sent back to the analyst) when: a Write, Edit, MultiEdit or NotebookEdit targets `tools/`, `stages/`, `package/`, `trees/`, `shelves/` or `.claude/`, or `out/diary/`; a Bash command runs `rm`, `rmdir`, `unlink`, `shutil.rmtree` or `os.remove`; a Bash command redirects, tees, moves, copies or edits into those folders or into `out/diary/`. Two more since 2026-09-28: after a compaction every call is refused until `out/_head.md` and the stage file are read and `mem.py diary` run (the gate lifts at the next `mem.py log`, or opens after five refusals, logged); and at A1 a room note is refused until that room's concepts were read. With `--post`, after a room note is written, it runs the note's form check and returns what is wrong at once. Every block goes to `out/_closes/guard.log`.

## Who writes it, and when

Claude Code, as the hook `settings.json` names, on every Bash, Write, Edit, MultiEdit, NotebookEdit, Read, Grep and Glob call, and after every Write, Edit and MultiEdit. It lives in `CONTROL/harness/`, out of the analyst's reach.

## Why it exists

The rules are "never delete a file", the instrument's folders are read only, and "the diary is written only through mem.py". It calls itself "a tripwire, never a wall"; the sandbox is the wall.

## Where

[harness/pretool_guard.py](../../../aggregator/runs/claude-v43-1/CONTROL/harness/pretool_guard.py).

Checked against: harness/pretool_guard.py, harness/settings.template.json, CONTRACT-aggregator.md rules 18 and 20.
