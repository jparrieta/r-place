# `harness/after_compact.sh`

The hook that runs after a compaction of the analyst's context.

## What it holds

It prints a short instruction naming the stage and leg (from `.stage` and `.leg`): read `out/_head.md` in full; read the stage file in full; run `mem.py diary --last 5`; reconcile the head with the diary and log it (`mem.py log "compacted; head reconciled" --kind note`); then continue where the diary says the leg stopped. At stage A1 it also prints the next room from `mem.py next`. It writes `CONTROL/.compact-gate.json`, and [pretool_guard.py](harness-pretool-guard-py.md) refuses every other call until the head, the stage file and the diary are read; `step.sh` sets a gate left by an earlier leg aside.

## Who writes it, and when

Claude Code's SessionStart hook with matcher `compact`, as `settings.json` names it. It lives in `CONTROL/harness/`, where the analyst cannot edit it.

## Why it exists

STANDING §2: a long reading leg "will compact, more than once, and you cannot see it happen"; "what is on disk survives it." Its header: hook output over about 10,000 characters is cut to a preview, so it names the files to read and never pastes them. `acceptance.sh` checks it prints under 9,000 characters.

## Where

[harness/after_compact.sh](../../../aggregator/runs/claude-v43-1/CONTROL/harness/after_compact.sh).

Checked against: harness/after_compact.sh, harness/settings.template.json, harness/acceptance.sh, STANDING-INSTRUCTIONS.md §2.
