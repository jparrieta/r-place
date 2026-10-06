# emit.py

The recording tool: every code, theme, disposition and pointer is a call, appended to a journal.

**What it holds**

The `Emit` class: `stage`, `code`, `pointer`, `thread`, `threads_bulk`, `theme`, `theme_add`, `retract`, `reading` and `close`. Each call appends one line to `out/_journal.jsonl`. `close()` writes `codes.jsonl`, `themes.jsonl`, `threads.jsonl`, `pointers.jsonl` and `_run.json` from the journal. It checks each quote against the record, refuses a code on an item `read.py` never served or on a context opening, and in v32 refuses a large read exclusion without a cited line.

**Who writes it, and when**

The instrument's author. Coders and the lead call it while working; only the case lead calls `close()`.

**Why it exists**

"If a step's output is a file, the agent is never the thing that formats it." The stage stamp makes `discovered_at` "a measurement instead of a claim". Append-only means "nothing is revised", and "if the journal and the final outputs ever disagree, the journal is right."

**Where**

[emit.py](../../../coder/instrument/v32/emit.py).

Checked against: emit.py, CONTRACT.v32.md §9, CHANGELOG-v32.md
