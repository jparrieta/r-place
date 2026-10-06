# materials.tar.zst

A verified room's inputs, packed into one archive: the record, the brief stage and the room's instrument.

**What it holds**

Three folders, as found on disk:

- `record/`: the cut the coders read, the pre-week, the counts and the openings file. See [the record files](record-files.md).
- `brief/`: the brief writer's directory, with its corpus, tools, contract, manifest and outputs. See [the brief and its outputs](brief-outputs.md).
- `instrument/`: the room's own copy of the coder instrument, from which `room.py run` built `run/`.

**Who writes it, and when**

After the room is verified. The armenia `STATE.json` records `materials_archive`, its sha256, its size (940,395 bytes) and `materials_archived_utc` 2026-09-25. Which script packs it is not stated in the sources.

**Why it exists**

Not stated in the sources in so many words. `room.py` shows the effect: when a room is verified, has a `materials_archive` file, and no longer has `record/`, `brief/` or `instrument/` folders, `status` keeps the saved stage "until its materials are restored".

**Where**

`materials.tar.zst` in each sample room, for example [armenia](../../../coder/rooms/armenia/). To read it: `zstd -dc materials.tar.zst | tar -xf -`.

Checked against: rooms/armenia/STATE.json, _tools/room.py
