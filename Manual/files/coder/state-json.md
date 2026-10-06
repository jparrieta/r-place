# STATE.json

A room's memory: what the files say, plus what only the scheduler knows.

**What it holds**

Counts from the build (`items_in_window`, `threads`, `preweek_items`, expected branch), the stage, the brief's model and validation receipt, the instrument and fingerprint, the branch, slices, verdict, codes and themes, `agents` (role, model, start and end), dated `notes`, `log`, `snapshots`, `forks`, `carried`, and for the native lead: `lead_model`, `lead_prompt_version`, `coding_status`, `lead_store` or `lead_archive` with its sha256 and size, and the `run_archive` and `materials_archive` paths, hashes and sizes. Paths are absolute paths on the machine that ran the room.

**Who writes it, and when**

`room.py` rewrites it from the files on every `status` and after each command; the scheduler adds fields and notes (§6 of its contract); `start_yard_lead.py` records the lead start; `lead_archive.py` records the archive or the restored store. Which script writes the `run_archive` and `materials_archive` fields is not stated in the sources.

**Why it exists**

"STATE.json is the room's memory." `lead_archive.py restore` refuses unless the archive's sha256 matches `lead_archive_sha256` here.

**Where**

[rooms/armenia/STATE.json](../../../coder/rooms/armenia/STATE.json).

Checked against: rooms/armenia/STATE.json, _tools/room.py, _tools/lead_archive.py, _tools/start_yard_lead.py, CONTRACT-scheduler.md
