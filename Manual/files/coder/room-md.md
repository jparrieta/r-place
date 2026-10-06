# ROOM.md

A room's front page: its numbers and the commands to run it, in order.

**What it holds**

A table: items in the 97-hour window, threads with an in-window item, characters of people's text, items in the seven days before, the brief's state, and the expected branch and slice count at threshold 500. A list of what the room holds. The `room.py` commands in order, from `status` through `brief`, `run`, `message lead`, the coder loop, `snapshot after-fleet`, `finish` or `fork`, to `check`.

**Who writes it, and when**

When the room is built. The yard README names `build_room.py` as "how a room was made from raw24"; that script is not among these sources. It is not rewritten as the room moves on: the armenia copy still says "brief: to write" and "instrument/ (v30, whole)" though its `STATE.json` records a brief and v32.

**Why it exists**

So a person or agent standing in the room knows what to run. It points to `CONTRACT-scheduler.md` for what to look for between the commands.

**Where**

[rooms/armenia/ROOM.md](../../../coder/rooms/armenia/ROOM.md); each sample room has one.

Checked against: rooms/armenia/ROOM.md, rooms/armenia/STATE.json, yard/README.md
