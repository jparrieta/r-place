# render_corpus_v32.py

The renderer: it turns a room's JSONL record into the text corpus a coder reads, with every number precomputed.

**What it holds**

Functions that write `corpus.txt`: a header of `#` lines (counts, the day histogram, every author, the thread index with text share, deleted counts, accounts that look automatic), then every thread in time order, each long thread with its triage window. Timestamps become forms like `d3 12:28`. `windows=False` leaves out the triage windows, for the brief corpus. It rebuilds correct permalinks on demand.

**Who writes it, and when**

The instrument's author. `newrun.py`, `build_fleet()` and `newbrief.py` call it when they build a directory.

**Why it exists**

Pilot coders spent "~38% of their turns writing python", parsing and counting. The rule behind it: "If a step's output is a number, the agent is never the thing that computes it." The JSONL stays authoritative, so `cite` still resolves against it.

**Where**

[render_corpus_v32.py](../../../coder/instrument/v32/render_corpus_v32.py). Its docstring still carries "VERSION 26".

Checked against: render_corpus_v32.py, newrun.py, newbrief.py
