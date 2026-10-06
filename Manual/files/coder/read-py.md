# read.py

The coder's reading tool: it serves the rendered corpus in order and logs every service.

**What it holds**

Verbs `header`, `windows [n]`, `thread ID`, `item ID`, `state` and `audit`. `windows` serves the next threads as triage windows (or whole when short), in batches of about 20,000 characters. A cursor advances on serving. Every service goes to `out/_read.jsonl`, and the index to `out/_read_index.json`. `audit` compares what was served with what `emit.thread(read=...)` declared. In v32 it refuses a branch-B lead's raw read until `step5_counter` is recorded.

**Who writes it, and when**

The instrument's author. Copied into every run and batch. The coder calls it from the first step; the lead calls it in step 5.

**Why it exists**

Its docstring gives three properties: everything it returns is "a verbatim slice of corpus.txt"; `read` "becomes derived instead of declared", so what the coder was shown "is a fact about the run rather than a claim in it"; and "it resumes", because state lives in the log.

**Where**

[read.py](../../../coder/instrument/v32/read.py).

Checked against: read.py, AGENT.v32.md, TOOLS-SPEC.md
