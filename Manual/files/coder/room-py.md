# yard/_tools/room.py

One room of the yard, driven from outside. It calls no model.

**What it holds**

Commands, run in `rooms/<sub>/` or with `--room DIR`: `status` (reads the files, rewrites `STATE.json`, says what is next), `brief --model ID` (builds `brief/`), `run --model ID` (builds `run/` with `newrun.py`, only once the brief has a current passing receipt), `message brief|lead|coder|collect|finish|fork` (prints the exact opening message for an agent), `check [--batch NN | --brief | --fork NAME]` (runs `verify_room.py`; for a brief it writes `brief/out/_validation.json`), `snapshot NAME`, `fork NAME [--from after-fleet]`, `note "text"`, and `final --batch NN "message"`.

**Who writes it, and when**

The yard's author. The scheduler, a person or an agent, runs it between agent launches. `codex_lead.py` and `start_yard_lead.py` call it too.

**Why it exists**

"STATE.json is the room's memory. room.py rewrites it from what the files say; the scheduler adds the things files cannot say." The messages are printed by it "so the text every agent receives is the same on every platform" (scheduler's contract). `snapshot` and `fork` are the older filesystem-only, fresh-lead comparison.

**Where**

[_tools/room.py](../../../coder/handler/tools/room.py). It calls [`verify_room.py`](../../../coder/handler/tools/verify_room.py), in the same folder.

Checked against: _tools/room.py, CONTRACT-scheduler.md, CHECKPOINTS.md
