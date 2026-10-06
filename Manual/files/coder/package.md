# The run's package

What one room hands on: the six outputs named for the aggregator, and the files under `run/package/`.

**What it holds**

The six outputs this manual groups as the hand-over: `brief.md` (the pre-week description), `case.md` (the within-case account), `codes.jsonl`, `themes.jsonl`, `threads.jsonl` and `pointers.jsonl`. The coder contract's own "six outputs" are different: `case.md`, `notes.md` and the four JSONL files. The aggregator takes the first set: each room's folder in the run's package holds exactly those six files ([package/armenia/](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/armenia/)). `notes.md` stays with the room's run and is not handed on.

`run/package/` holds `codes.jsonl`, `threads.jsonl`, `pointers.jsonl` (the fleet's pooled rows, each with its batch), `codes_by_thread.md`, `forest.jsonl` and `tree_index.json`. The lead's `out/` holds `case.md`, `notes.md` and the four files `emit.close()` writes, `themes.jsonl` among them.

**Who writes it, and when**

`fleet.py consolidate` pools; `tree_builder.py` writes the forest files; `emit.close()` writes the JSONL files; the lead writes `case.md` and `notes.md`.

**Why it exists**

Outputs go "to a reader that builds the account across three hundred communities and has not seen your corpus".

**Where**

`run/package/` and `run/out/` inside each room's `run.tar.zst`.

Checked against: CONTRACT.v32.md §8 and §9, CONTRACT-case-lead.v32.md §7, tools/fleet.py, yard/README.md, TOOLS-SPEC.md
