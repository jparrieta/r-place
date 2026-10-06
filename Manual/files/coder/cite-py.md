# cite.py

The citing tool: it turns a quote the agent believes is there into the exact words of the record and their offsets, or refuses.

**What it holds**

The `Corpus` class with `cite(item_id, quote)` and `find(regex, limit)`, the `FindResult` list with its `truncated` flag, and `CiteError`. `cite` searches the item's body (a post is title plus text) and returns `{item_id, start, end, text}`, cut from the body. It refuses a quote that is absent or occurs twice, and offers the nearest real text. Offsets are Unicode code points. Every `find` call is logged to `<record>.queries.jsonl`.

**Who writes it, and when**

The instrument's author. `newrun.py`, `newbrief.py` and `fleet.py dispatch` copy it into every run, brief and batch. Agents call it; its output goes straight into `emit`.

**Why it exists**

An agent "cannot count characters", and a quote typed from memory makes "an honest citation indistinguishable from a fabricated one". So "what the agent typed is discarded; what comes back is the record's". Quotes must be participants' own words because codes are "informant-centric" (CONTRACT §1), every code "rests on text `cite` can find" (Rule 2), and a cited pointer is "a reference somebody can go back to and check" (§6). The harness still re-checks every line: "the check should catch fabrication, not clumsiness."

**Where**

[cite.py](../../../coder/instrument/v32/cite.py).

Checked against: cite.py, CONTRACT.v32.md, TOOLS-SPEC.md, newrun.py
