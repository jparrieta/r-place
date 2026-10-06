# The record files (record/)

The room's source material, cut and counted before any agent arrives.

**What it holds**

- `coder_corpus.jsonl.gz`: the 97-hour cut, one item per line, threads whole, items outside the window marked as context. `room.py run` unpacks it and `newrun.py` builds `run/` from it.
- `preweek.jsonl.gz`: the seven days before the canvas opened, what the brief writer reads.
- `cut_stats.json`: the counts computed at build. The scheduler checks the gate against it.
- `openings.md`: every thread's metadata, counts, title and opening text, for the case lead; `room.py run` copies it into `run/` (large rooms also get titles-only and digest files).

**Who writes it, and when**

When the room is built. The yard README names `build_room.py` and `add_openings.py`, which are not among these sources; the openings format is `render_openings_v32.py`'s and the window is `cut_window_v32.py`'s.

**Why it exists**

"If a step's output is a number, the agent is never the thing that computes it." The record stays authoritative for `cite`. The scheduler reads it "only to settle a mechanical question, never to form a view of the room".

**Where**

`record/` inside each room's `materials.tar.zst`, for example [armenia](../../../coder/rooms/armenia/).

Checked against: yard/README.md, CONTRACT-scheduler.md, cut_window_v32.py, render_openings_v32.py
