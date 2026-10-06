# tools/tree_builder.py

Builds the forest: each coded thread's reply tree with its codes hung on it.

**What it holds**

`python3 tools/tree_builder.py --sub SUB --record coder_corpus.jsonl --codes-file <codes> --out-dir .`. It writes `trees/<sub>.md` (the forest a reader reads), `package/forest.jsonl` (one line per coded thread) and `package/tree_index.json` (coordinate to item ID and metadata). Coordinates are Dewey: `0` is the post, `1`, `2` its replies, `1.1` below. Node states: coded, bridge, removed, pruned, collapsed. Each coded line shows its chunks in text order, such as `[c0012 na c0015]`. Dropped items are counted.

**Who writes it, and when**

The instrument's author. The case lead runs it after `emit.close()` and before the audit, in both branches.

**Why it exists**

"No agent draws a tree." Dropped items are counted because a forest that hides them "would let a reader mistake what was not coded for what was not said". Its limit: "a reply is a reply"; the tree shows sequence, not cause.

**Where**

[tools/tree_builder.py](../../../coder/instrument/v32/tools/tree_builder.py).

Checked against: tools/tree_builder.py, CONTRACT-case-lead.v32.md §4, CHANGELOG-v32.md
