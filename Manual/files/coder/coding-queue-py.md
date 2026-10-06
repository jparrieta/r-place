# yard/_tools/coding_queue.py

The launcher: it starts rooms smallest first, up to a set number at once.

**What it holds**

`python3 _tools/coding_queue.py [--parallel N] [--inspect] [--clear-pause] [--requeue-failed]`. A room is ready when it has 500 to 50,000 in-window items, no failure, no `run/`, no store or archive, no earlier coder run (except `liverpoolfc`), and a brief that passes. It launches `start_yard_lead.py <sub> --complete` for each, or a repair script for a failed room, keeps `_coding_queue/STATE.json`, `EVENTS.jsonl` and a log per launch, pauses on a `DRAIN` file, a usage limit, an unexplained exit or low disk, and stops retrying a room after two failures. A room counts as finished when its `STATE.json` says `verified` and `validation/RUN-RECEIPT.json` exists.

**Who writes it, and when**

The yard's author. Run by the scheduler; the model is fixed at `gpt-5.6-sol`, `medium`.

**Why it exists**

Its docstring: "Owns scheduling, never research decisions."

**Where**

[_tools/coding_queue.py](../../../coder/handler/tools/coding_queue.py). The repair and progress scripts it calls are not among these sources.

Checked against: _tools/coding_queue.py, _tools/start_yard_lead.py
