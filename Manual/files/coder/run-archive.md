# run.tar.zst

The case lead's whole run directory, as it stood when the room was verified.

**What it holds**

`run/`, as found on disk: the lead's instrument copy (`AGENT.md`, `CONTRACT.md`, `CONTRACT-case-lead.md`, `cite.py`, `read.py`, `emit.py`, `close_run.py`, `tools/`); the inputs (`corpus.txt`, `coder_corpus.jsonl`, `coder_corpus.queries.jsonl`, `corpus_manifest.json`, `openings.md`, `brief.md`, `_manifest.json`); `out/` (the lead's outputs, journal, gate, ledger, notes, transcript); `staging/` (each batch's codes, dispositions, pointers and read log); `package/` (the pool and the forest files); `trees/` (the rendered forest); and `fleet/batch_NN/` for each coder.

**Who writes it, and when**

`newrun.py` builds `run/`; the lead, `fleet.py`, `tree_builder.py` and `emit` fill it. The armenia `STATE.json` records `run_archive`, its sha256, 1,083,960 bytes, archived 2026-09-25. Which script packs it is not stated in the sources.

**Why it exists**

CASE-LEAD-PROMPT.md: the canonical reading is published under `rooms/<community>/run/`, and "the byte-identical run copy retains its original instrument paths and hash baselines; it is a review copy, not a relocated native conversation."

**Where**

`run.tar.zst` in each sample room, for example [armenia](../../../coder/rooms/armenia/). Parts: [corpus files](corpus-files.md), [package](package.md), [fleet batch](fleet-batch.md).

Checked against: newrun.py, CONTRACT-case-lead.v32.md §7, CASE-LEAD-PROMPT.md, rooms/armenia/STATE.json
