# yard/_tools/codex_lead.py

Runs and checkpoints the case lead only, through the Codex app-server's own session history.

**What it holds**

`--store DIR` plus a command. `init --room R --model M [--effort] [--auth-source] [--host-sandbox]` copies the room into `workspace/room`, builds its run there, and writes `STORE.json` and the first checkpoint. `turn --message lead|collect|finish [--batch] [--summary] | --prompt-file F --label L` starts or resumes the lead, waits for a completed reply, shuts the runtime down, exports the transcript to `run/out/_transcript.jsonl`, saves `final_message.md`, and commits a checkpoint. `fork --checkpoint C --name N` makes a native fork without a model turn. Also `restore`, `verify`, `status`, `recover`, `recover-run`.

**Who writes it, and when**

The yard's author. `start_yard_lead.py` calls `init` and the first `turn`.

**Why it exists**

"Every successful turn shuts down the runtime, exports its complete native rollout, and commits one checkpoint." "Brief writers and fleet coders are external; only their filesystem outputs travel." It fails closed if the Codex binary, Python or platform changed.

**Where**

[_tools/codex_lead.py](../../../coder/handler/tools/codex_lead.py). It imports `checkpoints` and calls `verify_room.py`; both are in [`_tools/`](../../../coder/handler/tools/).

Checked against: _tools/codex_lead.py, CHECKPOINTS.md
