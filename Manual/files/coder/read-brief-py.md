# read_brief.py

The brief writer's reading tool, revision `v32-brief-r1`.

**What it holds**

Verbs `header`, `titles [n] [--day d] [--offset N]`, `sample [n]`, `thread ID [--offset] [--limit]`, `item ID [--offset] [--limit]`, `state` and `evidence`. Bodies come from the adjacent `brief_corpus.jsonl`. Every response is bounded (at most 18,000 characters) and every served span is logged in character offsets. `sample` draws item excerpts from the least-read active days first. `evidence` writes `out/evidence.json`, the coverage receipt. There is a reference budget and a hard ceiling at three times it.

**Who writes it, and when**

The instrument's author. `newbrief.py` copies it into `brief/`; the brief writer calls it.

**Why it exists**

"The writer must never open either corpus directly." The brief writer asks "what is ordinary here", so its verbs sample for breadth across the week, where the coder's `read.py` serves triage windows. The receipt lets a reader "calibrate a description" whose coverage it can see.

**Where**

[read_brief.py](../../../coder/instrument/v32/read_brief.py).

Checked against: read_brief.py, CONTRACT-brief-writer.v32.md, TOOLS-SPEC.md
