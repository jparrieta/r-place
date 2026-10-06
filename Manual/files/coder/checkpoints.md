# Case-lead checkpoints (CHECKPOINTS.md)

How the case lead's conversation and the whole room are saved after every completed lead reply, and how to resume or fork from a save.

**What it holds**

How to start a room with `codex_lead.py init` and `turn`. What one turn saves: the native lead ID, turn ID, final reply and rollout; every file under `workspace/`; the isolated native Codex home; runner state and settings. Branch B with a persistent lead, and the `after-fleet` label on the last collect. Resume, fork and restore. Recovery (`RUNNING.json`, `recover-run`, `recover`) and portability. The older filesystem-only `room.py snapshot` and `fork`. Tests.

**Who writes it, and when**

Not stated in the sources. The scheduler's contract dates native continuation to 2026-09-07.

**Why it exists**

"Only the case lead has a persisted native agent session." A checkpoint "is evidence of a restorable conversation boundary, not certification that the reading passed its checks." Restore works only at "the same absolute paths", and a changed runtime fails closed.

**Where**

[CHECKPOINTS.md](../../../coder/handler/CHECKPOINTS.md). It names [`_tools/checkpoints.py`](../../../coder/handler/tools/checkpoints.py) and [`_tools/test_checkpoints.py`](../../../coder/handler/tools/test_checkpoints.py), both in the repository.

Checked against: CHECKPOINTS.md, CONTRACT-scheduler.md, _tools/codex_lead.py
