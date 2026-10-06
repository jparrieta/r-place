# The brief and its outputs (brief/)

The brief writer's directory: what it read, how it read, and the brief it wrote.

**What it holds**

Inputs from `newbrief.py`: `brief_corpus.jsonl` (the pre-week record), `brief_corpus.txt` (rendered, no triage windows), `CONTRACT.md`, `read_brief.py`, `cite.py`, `_manifest.json` (hashes of what was dispatched). Logs: `brief_corpus.queries.jsonl` (every `find`). In `out/`: `brief.md` (the brief), `_read.jsonl` (every service), `evidence.json` (the coverage receipt), `_transcript.jsonl` and `final_message.md` (the session), `_validation.json` (the check receipt), `validation.txt`.

**Who writes it, and when**

`room.py brief` builds the directory; the brief writer writes `brief.md` and calls `evidence()`; the scheduler places the transcript and runs `room.py check --brief`, which writes `_validation.json` with a digest over the checked files. Who writes `validation.txt` is not stated in the sources.

**Why it exists**

The brief is the coder's step 1: a description of the ordinary week "for orientation", "never evidence". The receipt makes the brief's coverage visible. `room.py run` refuses to build until the receipt is current and passing.

**Where**

`brief/` inside each room's materials archive; the brief is also copied to `run/brief.md`.

Checked against: newbrief.py, read_brief.py, _tools/room.py, CONTRACT-brief-writer.v32.md, CONTRACT.v32.md §4
