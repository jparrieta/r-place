# The tools, one way across the tiers (TOOLS-SPEC.md)

What the reading, citing and searching tools do the same way for the brief writer, the coder and the aggregator.

**What it holds**

The shared shell grammar, `python3 <tool>.py <CORPUS> <verb> [arg] [--flag ...]`, and the rule that a refusal prints one line and exits 2. The verbs `read.py` and `read_brief.py` share (`header`, `thread`, `item`, `state`) and the ones they do not (`windows` and `audit` for the coder; `titles` and `sample` for the brief writer). The read log `out/_read.jsonl`. `cite` and `find`, and the query log `<record>.queries.jsonl`. `emit`, coder only. What stays different and why. The aggregator's tools as they stood, with what is to be aligned at v37.

**Who writes it, and when**

The instrument's author, as part of v32. Its author is not named.

**Why it exists**

"So that an agent that has used one is not surprised by another." A refusal "is the tool saying the call was wrong, never the tool breaking; a traceback is a defect."

**Where**

[TOOLS-SPEC.md](../../../coder/instrument/v32/TOOLS-SPEC.md). Not copied into rooms by `newrun.py`.

Checked against: TOOLS-SPEC.md, newrun.py
