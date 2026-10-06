# yard/_tools/start_yard_lead.py

Prepares one room and runs its first calibrated case-lead turn.

**What it holds**

`python3 _tools/start_yard_lead.py <sub> [--complete]`. It refuses a room that already has `run/`, a store or an archive; a room outside 500 to 50,000 in-window items; a room coded before (except `liverpoolfc`); and a brief without a current passing receipt. Then it runs `codex_lead.py init` with `gpt-5.6-sol` at `medium`, builds the opening message from `room.py message lead` plus the block in `CASE-LEAD-PROMPT.md`, saves it as `state/lead-opening.txt` and a receipt as `state/prompting.json`, notes the start in `STATE.json`, and runs the first `turn` with label `lead-first`. With `--complete` it hands on to `continue_yard_room.py`.

**Who writes it, and when**

The yard's author. `coding_queue.py` launches it for each ready room.

**Why it exists**

Its docstring: "Prepare one authorised room and run its first calibrated native lead turn." The receipt records the prompt version, model, effort and hashes so the calibration is "an explicit condition of new runs" (CASE-LEAD-PROMPT.md).

**Where**

[_tools/start_yard_lead.py](../../../coder/handler/tools/start_yard_lead.py). `continue_yard_room.py` is not among these sources.

Checked against: _tools/start_yard_lead.py, CASE-LEAD-PROMPT.md, _tools/coding_queue.py
