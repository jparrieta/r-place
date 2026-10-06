# A fleet batch (fleet/batch_NN/)

One fleet coder's directory: its slice, its tools, and what it wrote.

**What it holds**

Inputs: `AGENT.md`, `CONTRACT.md`, `CONTRACT-fleet-coder.md`, `brief.md`, `timeline.md` and `lexicon.md` (as the lead's `out/` held them at dispatch), `corpus.txt` and `coder_corpus.jsonl` (the slice and its context openings), `read.py`, `cite.py`, `emit.py`, `close_run.py`, `_manifest.json`. In `out/`: `case.md` and `notes.md` (the coder's), `codes.jsonl`, `themes.jsonl`, `threads.jsonl`, `pointers.jsonl` (written at `consolidate`), `_run.json`, `_read.jsonl`, `_read_index.json`, `final_message.md` and `_transcript.jsonl` (placed by the scheduler). The journal is `out/_journal.jsonl`.

**Who writes it, and when**

`fleet.py dispatch` builds it; one coder works in it; the scheduler places the transcript and final message and runs `check --batch NN`; `collect` and `consolidate` read from it. A failed batch moves whole to `fleet/_failed/`.

**Why it exists**

Branch B splits a room above 500 items into slices read "one at a time: the fleet is serial because each coder inherits the facts files of the one before" (scheduler's contract). The coder sees no other coder's codes, case or notes.

**Where**

`run/fleet/batch_NN/` inside each room's `run.tar.zst`.

Checked against: tools/fleet.py, newrun.py, CONTRACT-fleet-coder.v32.md, CONTRACT-scheduler.md
