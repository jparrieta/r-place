# The corpus files

What a coder reads and cites, and the counts it is told.

**What it holds**

- `coder_corpus.jsonl`: the record, one item per line. `cite` and `emit` resolve against it. The agent "never opens it".
- `corpus.txt`: the rendered corpus with its header of counts and the triage windows, served by `read.py`.
- `coder_corpus.queries.jsonl`: every `find` call, with pattern, matches, limit and whether the scan was cut short.
- `corpus_manifest.json`: the counts the gate is decided on, `items_in_window` and `chars_by_people`.
- `openings.md`: in the lead's run only.

In a fleet batch, `coder_corpus.jsonl` and `corpus.txt` hold the slice plus the openings of earlier threads still running, marked as context.

**Who writes it, and when**

`newrun.py` for the lead, `newrun.build_fleet()` through `fleet.py dispatch` for each batch, `cite.py` for the query log.

**Why it exists**

The JSONL is authoritative and the text is its rendering, so bodies are "byte-identical in both files" and "the citation contract is untouched". The query log means "your query log is produced for you and you never write one" (Rule 4).

**Where**

At the top of `run/` and each `run/fleet/batch_NN/` in a room's `run.tar.zst`.

Checked against: newrun.py, render_corpus_v32.py, cite.py, CONTRACT.v32.md, TOOLS-SPEC.md
