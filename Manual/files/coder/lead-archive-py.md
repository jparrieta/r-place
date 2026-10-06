# yard/_tools/lead_archive.py

Compresses a finished case-lead store into one archive, and restores it.

**What it holds**

`python3 _tools/lead_archive.py archive <sub>`, `restore <sub>` and `archive-all`. Stores live at `_lead_sessions/<sub>-gpt56-calibration-v1`. `archive` refuses while `RUNNING.json` exists, writes an `ARCHIVE.json` marker, packs the store with `bsdtar` and `zstd -6`, test-extracts it and compares every file, writes the archive's sha256 and size into the room's `STATE.json`, then deletes the live store. `restore` checks the archive's sha256 against `STATE.json`, extracts it, rewrites the paths in `STORE.json` and `state/runtime.json` to the new location, records `lead_store` in `STATE.json`, and deletes the archive. Both require `STORE.json`, `HEAD.json` and `state/lead.json` inside the archive.

**Who writes it, and when**

The yard's author. The sources do not say who runs it; the armenia `STATE.json` notes a compression on 2026-09-09 "after work ended".

**Why it exists**

Its docstring: "Archive and restore complete case-lead stores one at a time." The archive keeps the store forkable ("Archive is missing fork state" is its refusal).

**Where**

[_tools/lead_archive.py](../../../coder/handler/tools/lead_archive.py). It imports `checkpoints`, which is not among these sources.

Checked against: _tools/lead_archive.py, rooms/armenia/STATE.json
