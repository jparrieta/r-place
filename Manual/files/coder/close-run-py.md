# close_run.py

The end-of-run gate: twelve checks that pass or fail.

**What it holds**

`python3 close_run.py RUNDIR [--record CORPUS.jsonl] [--role lead|fleet] [--preflight]`. Checks C1 (six outputs exist), C2 (a transcript), C3 (code text matches the record), C4 (every code in one theme), C5 (large read exclusions carry a cited line), C6 (declared reading matches served reading), C7 (instrument files unchanged since dispatch), C8 (pointer and exclusion text match the record), C9 (codes and pointers sit on served items), C10 (nothing recorded after the last `close()`), C11 (every `coded` thread has a live code), C12 (branch-B notes repeat the gate). `--preflight` skips C2 and C10. It exits non-zero on any failure.

**Who writes it, and when**

The instrument's author. Agents run `--preflight` before their final message; the scheduler runs the full check after the agent exits (check E2).

**Why it exists**

"A run is not finished when the coder stops talking." An earlier session reported transcripts saved when only the journal was; "the fix is not a reminder. It is a check that fails."

**Where**

[close_run.py](../../../coder/instrument/v32/close_run.py).

Checked against: close_run.py, CONTRACT-scheduler.md, CHANGELOG-v32.md
