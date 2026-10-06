# newbrief.py

Builds a brief writer's directory from the seven days before the canvas opened.

**What it holds**

`python3 newbrief.py BRIEFDIR SUB RAW24.jsonl MODEL`. It cuts the pre-week out of a raw file into `brief_corpus.jsonl`, renders `brief_corpus.txt` without triage windows, copies in `read_brief.py` and `cite.py`, fills the brief writer's contract, and writes `_manifest.json` with the hashes of what it dispatched.

**Who writes it, and when**

The instrument's author. `room.py brief` builds `brief/` when a room's brief is still to write.

**Why it exists**

It fixes two faults its docstring names. Brief corpora "were rendered with the coder's triage windows in them", an instruction that is "meaningless in the seven days before the event existed". And "the brief writer had no reading tool", so it "was the only agent in the pipeline whose behaviour was entirely unobserved".

**Where**

[newbrief.py](../../../coder/instrument/v32/newbrief.py). Its output is the `brief/` part of each room's materials archive.

Checked against: newbrief.py, yard/_tools/room.py
