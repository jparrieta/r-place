# `out/_probe/`

The recall probe's questions, answers and scores, one set per leg.

## What it holds

`NN-L.questions.md` (five questions, "Answer from memory, without opening any file"), `NN-L.answers.md` (the reply verbatim) with `NN-L.answers.md.session` (the fork's id), `NN-L.json` (answers, what was expected, misses, score out of 1), and `notes.jsonl`, one line per leg with a miss.

## Who writes it, and when

`close.sh`, after the leg closes: `probe.py --ask`, then `protocol_guard.py probe` runs one headless turn in a fork of the leg's session with Bash, Read, Edit, Write, Glob, Grep, NotebookEdit, Agent and Task disallowed, then `probe.py --score`. The leg's own transcript is untouched.

## Why it exists

STANDING §2: the probe "measures whether the goal survived the leg"; a miss the head or the diary answers is a note, and a miss neither answers is a defect. It is closed to the analyst until E1, by the permission rules and the sandbox, so it cannot learn the questions. E1 writes `probes-E1.md` from it.

## Where

[out/_probe/](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/_probe/).

Checked against: tools/probe.py, harness/close.sh, harness/protocol_guard.py, STANDING-INSTRUCTIONS.md §2, stages/STAGE-E1-formalizing-audit.md.
